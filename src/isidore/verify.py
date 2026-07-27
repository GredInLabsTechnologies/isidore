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
from dataclasses import dataclass
from pathlib import Path

from .graph import find_graph, load_graph
from .pcp import (
    CERT_SUFFIX,
    FALSE,
    GRAY,
    GREEN,
    ORACLE_AST,
    ORACLE_GRAPH,
    ORACLE_GREP,
    ORACLE_LANGSPEC,
    TRUE,
    YELLOW,
    Certificate,
    ClaimVerdict,
    Predicate,
    VerifiedMass,
    VerifyContext,
    Verdict,
    parse_stored_predicate,
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
    """defines(file, symbol): the file defines a symbol of that name. Oracles: graph, then AST.

    The graph is consulted first and settles the common case, but its silence is NOT evidence of
    absence: the scanner emits only top-level functions and classes, so a module constant, a method
    or an annotated assignment are real definitions it never models. Judging those FALSE refutes true
    claims — measured on this repo, `defines:claims.py;SEARCH_RADIUS` was refuted while the constant
    sits at claims.py:26. `v_imports` already refuses to conclude absence from a partial oracle for
    exactly this reason; `defines` now does the same, and reaches for the parser instead.

    The asymmetry between languages is deliberate. Python is parsed exactly, so absence there IS
    decidable and FALSE is safe. Every other language goes through the heuristic langspec engine,
    which can miss a declaration it does not recognise, so a miss returns UNDECIDABLE — a verifier
    may fail to prove a claim, it may never invent a refutation.
    """
    if len(pred.args) != 2:
        return undecidable("defines expects (file, symbol)")
    rel, symbol = _norm(pred.args[0]), pred.args[1]
    want = symbol.rsplit(".", 1)[-1]
    fnodes = _file_nodes(ctx, rel)
    if any(_symbol_base(n.get("label", "")) == want for n in fnodes):
        return Verdict(TRUE, ORACLE_GRAPH, f"{rel} defines {want}")

    source = _read_source(ctx, rel)
    if source is None:
        return undecidable(f"cannot read '{rel}' to decide" if fnodes
                           else f"file '{rel}' not in the graph")
    from .surface import extract_surface

    symbols = extract_surface(source, Path(rel).suffix)
    if symbols is None:
        return undecidable(f"'{rel}' is not source this tool can parse")
    if any(s.qualname == symbol or s.name == want for s in symbols):
        return Verdict(TRUE, ORACLE_AST, f"{rel} defines {want}")
    if rel.endswith(".py"):
        return Verdict(FALSE, ORACLE_AST, f"{rel} does not define {want}")
    return undecidable(f"no declaration of {want} found in '{rel}', but its language is scanned "
                       "heuristically, so absence is not decidable")


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


def _langspec_symbols(ctx: VerifyContext, want: str) -> list[tuple[str, str, object]]:
    """[(file, language, SurfaceSymbol)] for every non-Python declaration of `want` in the graph.

    Scoped to files the graph already knows, so a verifier never walks the whole repository, and the
    universe it can decide over stays exactly the code the wiki was built from.
    """
    from .langspec import spec_for
    from .surface import extract_surface

    tail = want.rsplit(".", 1)[-1]
    out: list[tuple[str, str, object]] = []
    seen: set[str] = set()
    for node in ctx.nodes:
        rel = _norm(node.get("source_file", ""))
        if not rel or rel.endswith(".py") or rel in seen:
            continue
        seen.add(rel)
        spec = spec_for(Path(rel).suffix.lower())
        if spec is None or spec.kind != "code":
            continue
        source = _read_source(ctx, rel)
        if source is None:
            continue
        for symbol in extract_surface(source, Path(rel).suffix) or []:
            if symbol.qualname == want or symbol.name == tail:
                out.append((rel, spec.name, symbol))
    return out


def _unquote(text: str) -> str:
    """Strip one layer of matching quotes. Applied to BOTH sides of a literal comparison.

    The Python oracle compares the string's VALUE (`str(node.value)`, no quotes), so a model writing
    `value:PREFIX;'_insight/'` is using the other convention, not stating a different fact. Measured
    on GICS: that quoting difference alone refuted a true claim. Normalising both sides is the fix;
    refuting over punctuation is not a verdict, it is a formatting complaint.
    """
    stripped = (text or "").strip()
    if len(stripped) >= 2 and stripped[0] == stripped[-1] and stripped[0] in "\"'`":
        return stripped[1:-1]
    return stripped


def _decide(matches: list[str], candidates: int, subject: str, kind: str) -> Verdict:
    """TRUE if some declaration satisfies the claim; FALSE only when exactly one could have.

    The rule that matters is the last one. `_langspec_symbols` finds declarations BY NAME, and a name
    is not unique across a repository — `constructor` least of all. Refuting against whichever
    same-named declaration happened to be found first is how a true claim gets called false; measured
    on GICS, that is exactly what happened to `signature:constructor;options`. With more than one
    candidate and no match, the honest answer is that the verifier cannot tell which declaration the
    claim is about.
    """
    if matches:
        return Verdict(TRUE, ORACLE_LANGSPEC, matches[0])
    if candidates == 1:
        return Verdict(FALSE, ORACLE_LANGSPEC, f"{subject}")
    if candidates > 1:
        return undecidable(f"{candidates} declarations named '{kind}' and none matches; cannot tell "
                           "which one the claim is about")
    return undecidable(f"no declaration of '{kind}' this oracle can read")


def _value_via_langspec(name: str, expected: str, ctx: VerifyContext) -> Verdict:
    """`value` decided outside Python, via the declaration the scanner already extracted."""
    from .surface import literal_value

    wanted = _unquote(expected)
    matches: list[str] = []
    seen: list[str] = []
    for rel, _language, symbol in _langspec_symbols(ctx, name):
        literal = literal_value(getattr(symbol, "sig", ""))
        if literal is None:
            continue
        seen.append(literal)
        if _unquote(literal) == wanted:
            matches.append(f"{name} == {expected} in {rel}")
    return _decide(matches, len(seen),
                   f"{name} is bound to {seen[0] if seen else '?'}, not {wanted}", name)


def _signature_via_langspec(fn_name: str, expected: list[str], ctx: VerifyContext) -> Verdict:
    """`signature` decided outside Python — see `surface.parameter_names` for what it refuses.

    FALSE is only returned once the parameter list has actually been READ and only one declaration
    could have been meant. A language whose parameter order is not modelled, a declaration the
    extractor truncated, or an ambiguous name all come back UNDECIDABLE. The generic scanner is a
    heuristic, and a heuristic may fail to confirm a claim — it may not manufacture a refutation out
    of its own blind spots.
    """
    from .surface import parameter_names

    matches: list[str] = []
    readable: list[str] = []
    for rel, language, symbol in _langspec_symbols(ctx, fn_name):
        params = parameter_names(getattr(symbol, "sig", ""), language)
        if params is None:
            continue
        readable.append(", ".join(params))
        if params == expected:
            matches.append(f"{fn_name}({', '.join(params)}) in {rel}")
    return _decide(matches, len(readable),
                   f"{fn_name} params are ({readable[0] if readable else '?'})", fn_name)


def v_value(pred: Predicate, ctx: VerifyContext) -> Verdict:
    """value(name, literal): a module-level assignment `name = literal`. Oracles: AST, then langspec."""
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
    # No comparable Python literal. Before giving up, try the same question in the other languages
    # the scanner reads — the Python-only oracle is why a true claim about a TypeScript constant came
    # back UNDECIDABLE on every non-Python repo.
    return _value_via_langspec(name, expected, ctx)


def v_signature(pred: Predicate, ctx: VerifyContext) -> Verdict:
    """signature(fn, a1, a2, ...): fn's positional parameter names, in order. Oracles: AST, langspec.

    A predicate names a function, not a file, and a name is not unique in a repository: test helpers
    especially repeat (`_make_repo` is defined in five test modules here). Deciding on the FIRST
    candidate refutes a true claim whenever some homonym is visited first — measured on this repo,
    `signature:_make_repo;tmp_path;n_modules` came back FALSE against tests/test_handoff.py because
    tests/test_pipeline.py declares a third parameter. Every candidate is therefore examined, and
    FALSE is only asserted once none of them matches, which is how `v_calls` and `v_value` already
    treat exhaustion. A verifier may fail to prove a claim; it may never invent a refutation.
    """
    if len(pred.args) < 1:
        return undecidable("signature expects (fn, *args)")
    fn_name, expected = pred.args[0], list(pred.args[1:])
    nodes = [n for n in _symbol_nodes(ctx, fn_name) if n.get("source_file", "").endswith(".py")]
    found: list[str] = []
    for node in nodes:
        tree = _ast_of(ctx, _norm(node["source_file"]))
        fn = _find_funcdef(tree, fn_name) if tree else None
        if fn is None:
            continue
        params = [a.arg for a in fn.args.args]
        if params == expected:
            return Verdict(TRUE, ORACLE_AST, f"{fn_name}({', '.join(params)})")
        found.append(f"{_norm(node['source_file'])}: ({', '.join(params)})")
    if found:
        return Verdict(FALSE, ORACLE_AST,
                       f"no {fn_name} has those params — found {'; '.join(sorted(set(found)))}")
    return _signature_via_langspec(fn_name, expected, ctx)


def _env_read_pattern(token: str) -> re.Pattern:
    """The ways a language spells "read this from the environment", for a literal or a name."""
    t = re.escape(token)
    q = r"[\"']?"                       # a constant NAME appears unquoted where a literal is quoted
    return re.compile(
        r"(?:os\.environ\[\s*" + q + t + q + r"\s*\]"
        r"|os\.environ\.get\(\s*" + q + t + q + r"\s*[,)]"
        r"|getenv\(\s*" + q + t + q + r"\s*[,)]"
        r"|process\.env\." + t + r"\b"
        r"|process\.env\[\s*" + q + t + q + r"\s*\])")


def v_env(pred: Predicate, ctx: VerifyContext) -> Verdict:
    """env(NAME): NAME is read from the environment somewhere in the repo. Oracle: grep.

    The read is found through a named constant as well as a literal. Naming the variable once —
    `WIKI_DIR_ENV = "ISIDORE_WIKI_DIR"`, then `os.environ.get(WIKI_DIR_ENV, "")` — is the better
    habit, and a grep for the literal at the call site does not see it. Measured on this repo:
    extracting exactly that constant flipped three TRUE claims to FALSE across two pages while the
    code kept reading the same variable. A verifier that punishes tidier code is manufacturing
    refutations, and a false FALSE is worse than no verdict — it records a true statement as
    contradicted.
    """
    if len(pred.args) != 1:
        return undecidable("env expects (NAME)")
    name = pred.args[0]
    files = {_norm(n["source_file"]) for n in ctx.nodes if n.get("source_file")}
    if not files:
        return undecidable("no source files in the graph to scan for env reads")

    sources = {rel: _read_source(ctx, rel) for rel in sorted(files)}
    direct = _env_read_pattern(name)
    for rel, src in sources.items():
        if src and direct.search(src):
            return Verdict(TRUE, ORACLE_GREP, f"{name} read in {rel}")

    # Second pass: any constant BOUND to that exact string, then read from the environment. The
    # binding and the read may live in different files, so both passes span the repository.
    binding = re.compile(r"^\s*([A-Za-z_][A-Za-z_0-9]*)\s*[:=][^=\n]*?[\"']"
                         + re.escape(name) + r"[\"']", re.MULTILINE)
    aliases = {m.group(1) for src in sources.values() if src for m in binding.finditer(src)}
    for alias in sorted(aliases):
        pat = _env_read_pattern(alias)
        for rel, src in sources.items():
            if src and pat.search(src):
                return Verdict(TRUE, ORACLE_GREP, f"{name} read in {rel} via {alias}")
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


# A certificate stops matching its page for reasons that are NOT interchangeable, and collapsing
# them into one boolean is what left the living doc red with no supported way out (T-e46b): a page
# whose oracles now prove MORE than the recorded run is repaired by re-running them (0 LLM), while a
# page whose published sentence is now refuted needs new prose. `verify` only ever needed the
# boolean; `recertify` and `compile` need the reason, so the reason is what this computes.
CERT_OK = "ok"
CERT_MISSING = "missing"            # no sidecar: the page never went through the claim pipeline
CERT_UNREADABLE = "unreadable"      # sidecar present but not parseable as a certificate
CERT_TAMPERED = "tampered"          # the prose changed since compile — the cert describes other text
CERT_NO_GRAPH = "no-graph"          # nothing to verify against
CERT_DRIFTED = "drifted"            # at least one claim no longer verifies to its recorded verdict


@dataclass(frozen=True)
class CertStatus:
    """Why a page's certificate does or does not still describe the page. 0 LLM."""

    status: str
    cert: Certificate | None = None
    # (claim id, recorded verdict, current verdict) for every claim that moved
    drift: tuple[tuple[str, str, str], ...] = ()
    # child pages whose certificate no longer hashes to what this page recorded (composed integrity)
    children_moved: tuple[str, ...] = ()

    @property
    def ok(self) -> bool:
        return self.status == CERT_OK

    @property
    def refuted(self) -> tuple[tuple[str, str, str], ...]:
        """Drift that re-running the oracles CANNOT repair: the page states it, the code denies it.

        A claim only reaches the published prose when it verified TRUE, so TRUE -> FALSE is the one
        direction where the sentence a reader sees is now wrong. Every other move (a constant an
        older extractor could not see, an oracle that lost sight of a renamed file) is a change in
        what can be PROVED, not a false sentence — re-certifying records it honestly.
        """
        return tuple(d for d in self.drift if d[1] == TRUE and d[2] == FALSE)


def certificate_status(repo: Path, page_path: Path,
                       ctx: VerifyContext | None = None) -> CertStatus:
    """Check a page against its sidecar certificate, offline, 0 LLM (invariant I11).

    Checks, in order: the cert exists and parses; the prose still hashes to `prose_sha256`; every
    typed claim re-verifies to its recorded verdict against the current graph. Pass `ctx` to reuse
    one loaded graph across many pages.
    """
    cert_path = page_path.parent / (page_path.name + CERT_SUFFIX)
    if not cert_path.is_file() or not page_path.is_file():
        return CertStatus(CERT_MISSING)
    try:
        cert = read_certificate(cert_path)
    except ValueError:
        return CertStatus(CERT_UNREADABLE)
    from .claims import parse_claims_block
    clean, _rows = parse_claims_block(page_path.read_text(encoding="utf-8"))
    if prose_hash(clean) != cert.prose_sha256:
        return CertStatus(CERT_TAMPERED, cert)
    ctx = ctx if ctx is not None else _ctx_for(repo)
    if ctx is None:
        return CertStatus(CERT_NO_GRAPH, cert)
    drift: list[tuple[str, str, str]] = []
    for cv in cert.claims:
        # Stored predicates, not model output: a certificate may carry a chain (`wikichain`) that no
        # model is allowed to write, and reading it with the model-facing parser skipped it silently.
        pred = parse_stored_predicate(cv.predicate)
        if pred is None:
            continue                # existence-anchored: staleness is claims --check's job
        current = verify_predicate_ctx(pred, ctx).value
        if current != cv.verdict:
            drift.append((cv.id, cv.verdict, current))
    # A recorded child hash is itself an assertion — "this page rests on exactly that certificate".
    # The pyramid's whole claim is that editing a page below shows up above with no model call; that
    # only holds if someone checks. Cheap: one file hash per child.
    moved = tuple(sorted(page for page, digest in cert.child_cert_hashes.items()
                         if _cert_digest(repo, page) != digest))
    if drift or moved:
        return CertStatus(CERT_DRIFTED, cert, tuple(drift), moved)
    return CertStatus(CERT_OK, cert)


def _cert_digest(repo: Path, page: str) -> str:
    """sha256 of a page's certificate file, "" if it is gone."""
    import hashlib

    from .pipeline import WIKI_DIRNAME
    child = repo / WIKI_DIRNAME / f"{page}{CERT_SUFFIX}"
    return hashlib.sha256(child.read_bytes()).hexdigest() if child.is_file() else ""


def verify_page(repo: Path, page_path: Path,
                ctx: VerifyContext | None = None) -> tuple[bool, Certificate | None]:
    """(ok, cert) for one page. ok is False on any tamper/mismatch/missing-graph."""
    st = certificate_status(repo, page_path, ctx)
    return st.ok, st.cert


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
    shared_ctx = _ctx_for(args.repo)      # one graph load for the whole wiki, not one per page
    for page in pages:
        ok, cert = verify_page(args.repo, page, shared_ctx)
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
