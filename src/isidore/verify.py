"""Lane A — typed-claim verifiers, certificate building, `isidore verify`. (ADR-0033, task T-4d3f)

The verifiers decide a Predicate's truth against two oracles (see PCP_SEAMS.md, Rule 1):
- graph.json (nodes/edges) for defines/exports/imports,
- a reparse of the cited file's AST for calls/value/signature (the internal graph has no `calls`),
- a deterministic textual scan for env,
- route stays UNDECIDABLE until a framework extractor exists (honest, never a guess).

Every verifier returns TRUE / FALSE / UNDECIDABLE and records its oracle. UNDECIDABLE never
masquerades as TRUE — fail-closed. Certificates are re-verifiable offline with 0 LLM (`isidore verify`).
"""
from __future__ import annotations

import ast
import re
from pathlib import Path

from .graph import find_graph, load_graph
from .pcp import (
    FALSE,
    GRAY,
    GREEN,
    ORACLE_AST,
    ORACLE_GRAPH,
    ORACLE_GREP,
    TRUE,
    YELLOW,
    Certificate,
    ClaimVerdict,
    Predicate,
    VerifiedMass,
    VerifyContext,
    Verdict,
    prose_hash,
    read_certificate,
    register_verifier,
    undecidable,
)

# ---------------------------------------------------------------- oracle helpers


def _norm(path: str) -> str:
    return path.replace("\\", "/").lstrip("./")


def _symbol_base(label: str) -> str:
    """'authenticate()' -> 'authenticate', 'MyClass' -> 'MyClass'."""
    return label.split("(", 1)[0].strip()


def _symbol_nodes(ctx: VerifyContext, name: str) -> list[dict]:
    """Graph nodes whose symbol label matches `name` (last dotted component tolerated)."""
    want = name.rsplit(".", 1)[-1]
    return [n for n in ctx.nodes if _symbol_base(n.get("label", "")) == want]


def _file_nodes(ctx: VerifyContext, rel: str) -> list[dict]:
    rel = _norm(rel)
    return [n for n in ctx.nodes if _norm(n.get("source_file", "")) == rel]


def _read_source(ctx: VerifyContext, rel: str) -> str | None:
    try:
        return (ctx.repo / rel).read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None


def _ast_of(ctx: VerifyContext, rel: str) -> ast.Module | None:
    if not rel.endswith(".py"):
        return None
    src = _read_source(ctx, rel)
    if src is None:
        return None
    try:
        return ast.parse(src)
    except SyntaxError:
        return None


def _find_funcdef(tree: ast.Module, name: str) -> ast.FunctionDef | ast.AsyncFunctionDef | None:
    want = name.rsplit(".", 1)[-1]
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == want:
            return node
    return None


# ---------------------------------------------------------------- verifiers


def v_calls(pred: Predicate, ctx: VerifyContext) -> Verdict:
    """calls(caller, callee): the caller symbol's body contains a call to callee. Oracle: AST."""
    if len(pred.args) != 2:
        return undecidable("calls expects (caller, callee)")
    caller, callee = pred.args
    nodes = [n for n in _symbol_nodes(ctx, caller) if n.get("source_file", "").endswith(".py")]
    if not nodes:
        return undecidable(f"caller '{caller}' not a Python symbol in the graph")
    callee_last = callee.rsplit(".", 1)[-1]
    for node in nodes:
        tree = _ast_of(ctx, _norm(node["source_file"]))
        fn = _find_funcdef(tree, caller) if tree else None
        if fn is None:
            continue
        for sub in ast.walk(fn):
            if isinstance(sub, ast.Call):
                f = sub.func
                name = (f.attr if isinstance(f, ast.Attribute)
                        else f.id if isinstance(f, ast.Name) else None)
                if name == callee_last:
                    return Verdict(TRUE, ORACLE_AST, f"{caller} calls {callee_last}")
    return Verdict(FALSE, ORACLE_AST, f"{caller} has no call to {callee_last}")


def v_defines(pred: Predicate, ctx: VerifyContext) -> Verdict:
    """defines(file, symbol): the file defines a top-level symbol of that name. Oracle: graph."""
    if len(pred.args) != 2:
        return undecidable("defines expects (file, symbol)")
    rel, symbol = _norm(pred.args[0]), pred.args[1]
    fnodes = _file_nodes(ctx, rel)
    if not fnodes:
        return undecidable(f"file '{rel}' not in the graph")
    want = symbol.rsplit(".", 1)[-1]
    if any(_symbol_base(n.get("label", "")) == want for n in fnodes):
        return Verdict(TRUE, ORACLE_GRAPH, f"{rel} defines {want}")
    return Verdict(FALSE, ORACLE_GRAPH, f"{rel} does not define {want}")


def v_exports(pred: Predicate, ctx: VerifyContext) -> Verdict:
    """exports(file, symbol): Python has no explicit exports -> same as defines. Non-Python: undecidable."""
    if len(pred.args) != 2:
        return undecidable("exports expects (file, symbol)")
    if not _norm(pred.args[0]).endswith(".py"):
        return undecidable("exports only decidable for Python (no langspec exporter yet)")
    return v_defines(pred, ctx)


def v_imports(pred: Predicate, ctx: VerifyContext) -> Verdict:
    """imports(file, target): file imports target (module/file). Oracle: graph 'imports' edges."""
    if len(pred.args) != 2:
        return undecidable("imports expects (file, target)")
    src, target = _norm(pred.args[0]), _norm(pred.args[1])
    id_to_file = {n["id"]: _norm(n.get("source_file", "")) for n in ctx.nodes if n.get("id")}
    src_ids = {n["id"] for n in _file_nodes(ctx, src) if n.get("id")}
    if not src_ids:
        return undecidable(f"file '{src}' not in the graph")
    for link in ctx.links:
        if link.get("relation") != "imports" or link.get("source") not in src_ids:
            continue
        tgt_file = id_to_file.get(link.get("target"), "")
        if tgt_file == target or tgt_file.endswith("/" + target) or target.endswith("/" + tgt_file):
            return Verdict(TRUE, ORACLE_GRAPH, f"{src} imports {target}")
    # The graph's import edges are only PARTIALLY resolved (the scanner links intra-repo imports it
    # can resolve; it misses external packages and src-layout/namespace imports). So a missing edge
    # cannot assert absence — fail-closed to UNDECIDABLE, never FALSE (would discredit a real import).
    return undecidable(f"no import edge {src}->{target} in the graph; imports are partially resolved, "
                       "so absence is not decidable")


def _literal_str(node: ast.AST) -> str | None:
    if isinstance(node, ast.Constant):
        return str(node.value)
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub) and isinstance(node.operand, ast.Constant):
        return str(-node.operand.value) if isinstance(node.operand.value, (int, float)) else None
    return None


def v_value(pred: Predicate, ctx: VerifyContext) -> Verdict:
    """value(name, literal): a module-level assignment `name = literal`. Oracle: AST."""
    if len(pred.args) != 2:
        return undecidable("value expects (name, literal)")
    name, expected = pred.args
    nodes = [n for n in _symbol_nodes(ctx, name) if n.get("source_file", "").endswith(".py")]
    files = {_norm(n["source_file"]) for n in nodes} or {
        _norm(n["source_file"]) for n in ctx.nodes if n.get("source_file", "").endswith(".py")}
    saw_literal = False           # only a COMPARABLE literal assignment lets us assert FALSE
    for rel in sorted(files):
        tree = _ast_of(ctx, rel)
        if tree is None:
            continue
        for node in ast.walk(tree):
            targets = (node.targets if isinstance(node, ast.Assign)
                       else [node.target] if isinstance(node, ast.AnnAssign) else [])
            if any(isinstance(t, ast.Name) and t.id == name for t in targets):
                lit = _literal_str(node.value) if node.value else None
                if lit is not None:
                    saw_literal = True
                    if lit == expected:
                        return Verdict(TRUE, ORACLE_AST, f"{name} == {expected}")
    if saw_literal:
        return Verdict(FALSE, ORACLE_AST, f"{name} is assigned a literal, but not {expected}")
    # assigned to a non-literal (Path(...), a call, a name) or not found: cannot compare -> UNDECIDABLE
    return undecidable(f"no comparable literal assignment to {name} found")


def v_signature(pred: Predicate, ctx: VerifyContext) -> Verdict:
    """signature(fn, arg1, arg2, ...): fn's positional parameter names, in order. Oracle: AST."""
    if len(pred.args) < 1:
        return undecidable("signature expects (fn, *args)")
    fn_name, expected = pred.args[0], list(pred.args[1:])
    nodes = [n for n in _symbol_nodes(ctx, fn_name) if n.get("source_file", "").endswith(".py")]
    for node in nodes:
        tree = _ast_of(ctx, _norm(node["source_file"]))
        fn = _find_funcdef(tree, fn_name) if tree else None
        if fn is None:
            continue
        params = [a.arg for a in fn.args.args]
        if params == expected:
            return Verdict(TRUE, ORACLE_AST, f"{fn_name}({', '.join(params)})")
        return Verdict(FALSE, ORACLE_AST, f"{fn_name} params are ({', '.join(params)})")
    return undecidable(f"function '{fn_name}' not found as a Python symbol")


def v_env(pred: Predicate, ctx: VerifyContext) -> Verdict:
    """env(NAME): NAME is read from the environment somewhere in the repo. Oracle: grep."""
    if len(pred.args) != 1:
        return undecidable("env expects (NAME)")
    name = pred.args[0]
    pat = re.compile(
        r"(?:os\.environ\[[\"']" + re.escape(name) + r"[\"']\]"
        r"|os\.environ\.get\(\s*[\"']" + re.escape(name) + r"[\"']"
        r"|getenv\(\s*[\"']" + re.escape(name) + r"[\"']"
        r"|process\.env\." + re.escape(name) + r"\b"
        r"|process\.env\[[\"']" + re.escape(name) + r"[\"']\])")
    files = {_norm(n["source_file"]) for n in ctx.nodes if n.get("source_file")}
    if not files:
        return undecidable("no source files in the graph to scan for env reads")
    for rel in sorted(files):
        src = _read_source(ctx, rel)
        if src and pat.search(src):
            return Verdict(TRUE, ORACLE_GREP, f"{name} read in {rel}")
    return Verdict(FALSE, ORACLE_GREP, f"no environment read of {name} found")


def v_route(pred: Predicate, ctx: VerifyContext) -> Verdict:
    """route(method path, handler): needs a framework extractor. Honest UNDECIDABLE for now."""
    return undecidable("route verification needs a framework extractor (not implemented)")


def register_verifiers() -> None:
    for kind, fn in (("calls", v_calls), ("defines", v_defines), ("exports", v_exports),
                     ("imports", v_imports), ("value", v_value), ("signature", v_signature),
                     ("route", v_route), ("env", v_env)):
        register_verifier(kind, fn)


register_verifiers()


# ---------------------------------------------------------------- symbol grounding

# identifiers in prose worth grounding: backticked tokens, CamelCase, snake_case, dotted paths.
_IDENT_RE = re.compile(r"`([^`]+)`|(?<![\w.])([A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*)+)")
_STOPWORDS = frozenset({"e.g", "i.e", "etc", "self", "cls", "True", "False", "None"})


def _prose_identifiers(prose: str) -> set[str]:
    out: set[str] = set()
    for m in _IDENT_RE.finditer(prose):
        tok = (m.group(1) or m.group(2) or "").strip()
        base = tok.split("(", 1)[0].rsplit(".", 1)[-1]
        if base and base not in _STOPWORDS and re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", base):
            if re.search(r"[A-Z][a-z]|_", base) or "." in tok:   # CamelCase / snake_case / dotted
                out.add(base)
    return out


def ground_symbols(prose: str, ctx: VerifyContext) -> list[str]:
    """Return prose identifiers that DON'T resolve to any graph symbol or file (grounding failures)."""
    known = {_symbol_base(n.get("label", "")) for n in ctx.nodes}
    known |= {Path(_norm(n.get("source_file", ""))).stem for n in ctx.nodes if n.get("source_file")}
    return sorted(i for i in _prose_identifiers(prose) if i not in known)


# ---------------------------------------------------------------- certificate build


def _sentence_split(text: str) -> list[str]:
    # crude but deterministic sentence-ish split for prose mass classification
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+|\n+", text) if s.strip()]


def _claim_symbols(cv: ClaimVerdict) -> set[str]:
    """The code identifiers a claim is about: its predicate args (last dotted component) plus any
    code-shaped tokens (CamelCase/snake_case) in its statement. Lowercased, len>2, non-numeric."""
    from .claims import parse_predicate_field
    syms: set[str] = set()
    pred = parse_predicate_field(cv.predicate)
    if pred:
        syms |= {a.rsplit(".", 1)[-1] for a in pred.args}
    for tok in re.findall(r"[A-Za-z_][A-Za-z0-9_]*", cv.statement):
        if re.search(r"[A-Z][a-z]|_", tok) or tok in syms:
            syms.add(tok)
    return {s.lower() for s in syms if re.fullmatch(r"[a-z_][a-z0-9_]*", s.lower())
            and len(s) > 2 and not s.isdigit()}


def classify_mass(prose: str, claims: list[ClaimVerdict]) -> VerifiedMass:
    """Per-sentence confidence, 0-LLM: green if a sentence mentions a symbol from a claim PROVED
    TRUE, yellow if it mentions a symbol from an anchored (not-proved) claim, gray otherwise.
    Matching on the claim's verified symbols (not a literal statement substring) so paraphrase in
    the prose still counts — a sentence saying 'authenticate ... verify_jwt' is supported by
    calls(authenticate, verify_jwt)=TRUE even if worded differently."""
    green_syms: set[str] = set()
    yellow_syms: set[str] = set()
    for c in claims:
        (green_syms if c.verdict == TRUE else yellow_syms).update(_claim_symbols(c))
    green_syms, yellow_syms = green_syms, yellow_syms - green_syms
    mass = VerifiedMass()
    for sent in _sentence_split(prose):
        toks = set(re.findall(r"[a-z_][a-z0-9_]*", sent.lower()))
        if green_syms & toks:
            mass.green += 1
        elif yellow_syms & toks:
            mass.yellow += 1
        else:
            mass.gray += 1
    return mass


def build_certificate(page: str, markdown: str, anchored_claims: list[dict],
                      ctx: VerifyContext, *, marks=None, violations=None) -> Certificate:
    """Verify each claim's predicate, classify prose mass, hash the prose -> a re-verifiable cert."""
    from .claims import parse_predicate_field   # lane A extends claims.py with the 3-field parser
    verdicts: list[ClaimVerdict] = []
    for c in anchored_claims:
        pred: Predicate | None = parse_predicate_field(c.get("predicate", ""))
        v = verify_predicate_ctx(pred, ctx)
        verdicts.append(ClaimVerdict(
            id=c["id"], statement=c["statement"], evidence=c["evidence"], ehash=c["ehash"],
            predicate=pred.serialize() if pred else "", verdict=v.value, oracle=v.oracle,
            detail=v.detail))
    mass = classify_mass(markdown, verdicts)
    return Certificate(page=page, graph_commit=ctx.commit, prose_sha256=prose_hash(markdown),
                       claims=verdicts, marks=list(marks or []), violations=list(violations or []),
                       mass=mass)


def verify_predicate_ctx(pred: Predicate | None, ctx: VerifyContext) -> Verdict:
    """Dispatch through the registry (kept local so callers don't import pcp directly)."""
    from .pcp import verify_predicate
    return verify_predicate(pred, ctx)


# ---------------------------------------------------------------- offline verify (I11)


def _ctx_for(repo: Path) -> VerifyContext | None:
    graph_path = find_graph(repo)
    if graph_path is None:
        return None
    nodes, links, commit = load_graph(graph_path)
    return VerifyContext(repo=repo, nodes=nodes, links=links, commit=commit)


def verify_page(repo: Path, page_path: Path) -> tuple[bool, Certificate | None]:
    """Re-verify a page against its sidecar certificate, offline, 0 LLM (invariant I11).

    Checks: (1) the cert exists and parses; (2) the prose still hashes to prose_sha256 (tamper);
    (3) every typed claim re-verifies to its recorded verdict against the current graph.
    Returns (ok, cert). ok is False on any tamper/mismatch/missing-graph.
    """
    cert_path = page_path.parent / (page_path.name + ".cert.json")
    if not cert_path.is_file() or not page_path.is_file():
        return False, None
    try:
        cert = read_certificate(cert_path)
    except ValueError:
        return False, None
    from .claims import parse_claims_block, parse_predicate_field
    clean, _rows = parse_claims_block(page_path.read_text(encoding="utf-8"))
    if prose_hash(clean) != cert.prose_sha256:
        return False, cert          # tamper: prose changed since compile
    ctx = _ctx_for(repo)
    if ctx is None:
        return False, cert
    ok = True
    for cv in cert.claims:
        pred = parse_predicate_field(cv.predicate)
        if pred is None:
            continue                # existence-anchored: staleness is claims --check's job
        current = verify_predicate_ctx(pred, ctx).value
        if current != cv.verdict:
            ok = False
    return ok, cert


# ---------------------------------------------------------------- CLI


def register_cli(sub) -> None:
    """Add `isidore verify` (called once from cli.main via the registrar loop — P0 owns that wiring)."""
    p = sub.add_parser("verify", help="re-verify pages against their certificates, offline (0 LLM)")
    p.add_argument("--repo", type=Path, default=Path("."))
    p.add_argument("--contracts", action="store_true",
                   help="also fail if any promoted contract is FALSE against the current graph")
    # opt-in CI gates (default off, so existing users are never broken by a new gate)
    p.add_argument("--min-verified-mass", type=float, default=None, metavar="RATIO",
                   help="fail if the green (proved) share of all sentences is below RATIO (0..1)")
    p.add_argument("--fail-on-marks", action="store_true",
                   help="fail if any page carries an unresolved danger-severity security mark")
    p.set_defaults(func=_cmd_verify)


def _cmd_verify(args) -> int:
    from .pipeline import WIKI_DIRNAME
    wiki = args.repo / WIKI_DIRNAME
    if not wiki.is_dir():
        print(f"[isidore] no wiki at {wiki} — run `isidore compile --execute` first")
        return 2
    pages = sorted(p for p in wiki.glob("*.md"))
    bad = []
    green = yellow = gray = 0
    danger_pages: list[str] = []
    for page in pages:
        ok, cert = verify_page(args.repo, page)
        if cert is None:
            continue
        tag = "OK  " if ok else "FAIL"
        if not ok:
            bad.append(page.name)
        m = cert.mass
        green, yellow, gray = green + m.green, yellow + m.yellow, gray + m.gray
        if any(k.severity == "danger" for k in cert.marks):
            danger_pages.append(page.name)
        print(f"  {tag} {page.name}  ({m.green} proved / {m.yellow} anchored / {m.gray} narrative)")
    rc = 0
    if args.contracts:
        from .contracts import verify_contracts
        from .pcp import CONTRACTS_FILENAME, read_contracts
        ctx = _ctx_for(args.repo)
        contracts = read_contracts(wiki / CONTRACTS_FILENAME)
        for c, v in verify_contracts(contracts, ctx) if ctx else []:
            if v.value == FALSE:
                bad.append(f"contract {c.id}")
                print(f"  BROKEN contract {c.id}: {c.predicate} — {v.detail}")
    # opt-in gates
    total = green + yellow + gray
    if args.min_verified_mass is not None and total:
        ratio = green / total
        print(f"[isidore] verified mass: {ratio:.0%} green (gate >= {args.min_verified_mass:.0%})")
        if ratio < args.min_verified_mass:
            bad.append(f"verified-mass {ratio:.0%} < {args.min_verified_mass:.0%}")
    if args.fail_on_marks and danger_pages:
        bad.append(f"{len(danger_pages)} page(s) with unresolved danger marks: {', '.join(danger_pages)}")
    if bad:
        print(f"[isidore] verify: {len(bad)} failure(s): {'; '.join(bad)}")
        rc = 1
    else:
        print(f"[isidore] verify: {len(pages)} page(s) OK, certificates intact (0 LLM)")
    return rc


# imports used only for mass constants — keep the linters informed they're intentional
_ = (GREEN, YELLOW, GRAY)
