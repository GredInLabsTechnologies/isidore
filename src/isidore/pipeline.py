"""The compiler pipeline: plan -> assemble -> generate -> cache -> lint.

Everything here is deterministic except the single bounded LLM call per dirty page. The
graph already answers WHAT exists and WHERE — so page planning, context assembly, cache
invalidation and citation linting are plain code, and only the prose is delegated.

Hard limits live in code, not in prompts: --max-calls per run (skips are always reported),
a per-prompt character budget (truncation is always reported), one single model
(failure > silent escalation), one timeout per call.
"""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
from collections import Counter, defaultdict, deque
from dataclasses import dataclass, field
from pathlib import Path

from .changeset import affected_modules, changed_lines, changed_symbols
from .journal import append_run, record_page_change
from .claims import (
    CLAIMS_FILENAME,
    CLAIMS_PROMPT_ADDENDUM,
    anchor_claims,
    is_negative_existential,
    parse_claims_block,
    render_claims,
    stale_pages,
)
from .findings import (
    FINDINGS_FILENAME,
    FINDINGS_PROMPT_ADDENDUM,
    filter_findings,
    harvest_todos,
    orphan_file_candidates,
    parse_findings_block,
    render_findings,
    risk_hotspots,
    coverage_gap_candidates,
)
from .graph import CONCEPTS_BUCKET, load_graph, module_of, restrict_to_tracked
from .llm import GenerationError, default_generator
from .render import (
    agents_md_block,
    render_quickstart,
    render_toon_index,
    upsert_agents_block,
)

WIKI_DIRNAME = "wiki"
STATE_FILENAME = ".isidore-state.json"

DEFAULT_MODULE_DEPTH = 2
DEFAULT_TOP_K_PAGES = 24
DEFAULT_MIN_SYMBOLS = 10
DEFAULT_MAX_CALLS = 12
DEFAULT_MAX_PROMPT_CHARS = 28_000
DEFAULT_EXCERPT_RADIUS = 25
DEFAULT_MAX_EXCERPTS = 6
DEFAULT_FLOW_DEPTH = 2

MODULE_PROMPT = """You are writing ONE page of an internal wiki that coding agents read before touching a repository.

Write a Markdown page about the module `{name}` using ONLY the facts below. Every fact was extracted
mechanically (structure graph, exact source excerpts, git log) — treat it as ground truth and do not
invent files, symbols, APIs or behavior that are not evidenced below.

Structure (use these exact section headings):
## Purpose
## Architecture
## Key entry points
## Dependencies
## How to change safely

Rules:
- Cite sources inline as `path:line` using ONLY paths that appear in the facts.
- Explain WHY the module exists and how its pieces relate, not just a file inventory.
- Describe only what IS evidenced. NEVER state that something does not exist, is not used, or is
  not handled — your facts are excerpts, not the whole repo, so absence cannot be proven here.
- Max ~600 words. No preamble, no closing remarks — start directly with the first heading.

FACTS
=====
{facts}
"""

FLOW_PROMPT = """You are writing ONE page of an internal wiki that coding agents read before touching a repository.

Write a Markdown page describing the cross-cutting flow `{name}` — how a request/data travels across
modules — using ONLY the facts below. Every fact was extracted mechanically (structure graph, exact
source excerpts) — treat it as ground truth and do not invent steps that are not evidenced below.

Structure (use these exact section headings):
## What this flow does
## Step by step
## Modules involved
## Where to hook in / change safely

Rules:
- Cite sources inline as `path:line` using ONLY paths that appear in the facts.
- Present the flow as an ordered narrative (A calls B because...), grounded in the graph links given.
- Describe only evidenced steps. NEVER state that a step/handler does not exist or is not handled —
  your facts are excerpts, not the whole repo, so absence cannot be proven here.
- Max ~600 words. No preamble — start directly with the first heading.

FACTS
=====
{facts}
"""

# Appended to a page's prompt for its ONE bounded repair retry when the first draft cited paths that
# do not exist in the repo (the hallucination lint failed). The phantom paths are named back so the
# model can remove or replace them instead of the page shipping with a dead citation inside.
LINT_REPAIR_ADDENDUM = """

CORRECTION REQUIRED. Your previous version cited paths that DO NOT EXIST in this repository:
{paths}
Rewrite the page: remove or replace EACH of those citations with a path that appears VERBATIM in the
FACTS above. Cite only real paths. Keep the rest of the page unchanged.
"""


@dataclass
class PageSpec:
    kind: str                      # "module" | "flow"
    name: str                      # module path or flow name
    files: int = 0
    symbols: int = 0
    doc_files: list[str] = field(default_factory=list)
    hot_symbols: list[tuple[str, str, str, int]] = field(default_factory=list)  # (label,file,loc,deg)
    deps_out: list[tuple[str, int]] = field(default_factory=list)
    deps_in: list[tuple[str, int]] = field(default_factory=list)
    flow_edges: list[tuple[str, str, str]] = field(default_factory=list)        # (src,relation,tgt)
    modules: list[str] = field(default_factory=list)                            # flows: touched modules

    @property
    def filename(self) -> str:
        slug = self.name.replace("/", "-").replace("\\", "-").replace(".", "_").replace(" ", "-")
        return (f"flow-{slug}.md" if self.kind == "flow" else f"{slug}.md")


# ------------------------------------------------------------------ planning

def module_dep_edges(nodes: list[dict], links: list[dict],
                     module_depth: int = DEFAULT_MODULE_DEPTH) -> Counter:
    """Cross-module dependency edges (src_module, dst_module) -> link count. Shared by page planning
    and the impact fingerprint so both see the SAME coupling graph."""
    by_id = {n["id"]: n for n in nodes if "id" in n}
    dep: Counter = Counter()
    for link in links:
        s, t = by_id.get(link.get("source")), by_id.get(link.get("target"))
        if not s or not t:
            continue
        ms = module_of(s.get("source_file"), module_depth)
        mt = module_of(t.get("source_file"), module_depth)
        if ms != mt:
            dep[(ms, mt)] += 1
    return dep

def plan_pages(
    nodes: list[dict],
    links: list[dict],
    *,
    module_depth: int = DEFAULT_MODULE_DEPTH,
    top_k: int | None = DEFAULT_TOP_K_PAGES,
    min_symbols: int = DEFAULT_MIN_SYMBOLS,
) -> list[PageSpec]:
    """Module pages from the graph: top-K modules holding at least min_symbols code symbols.

    top_k=None returns ALL eligible modules — pruning must compare against the full universe
    so a later run with a smaller --top-k never deletes valid pages.
    """
    out_degree: Counter[str] = Counter()
    for link in links:
        src = link.get("source")
        if src is not None:
            out_degree[src] += 1

    files: dict[str, set[str]] = defaultdict(set)
    symbols: dict[str, list[tuple[str, str, str, int]]] = defaultdict(list)
    docs: dict[str, set[str]] = defaultdict(set)
    for n in nodes:
        src_file = n.get("source_file")
        mod = module_of(src_file, module_depth)
        if src_file:
            files[mod].add(src_file)
            if n.get("file_type") == "document":
                docs[mod].add(src_file)
        if n.get("file_type") == "code":
            loc = n.get("source_location") or ""
            symbols[mod].append((n.get("label", n.get("id", "?")), src_file or "", loc,
                                 out_degree.get(n.get("id", ""), 0)))

    dep_out = module_dep_edges(nodes, links, module_depth)

    specs: list[PageSpec] = []
    for mod, syms in symbols.items():
        if mod == CONCEPTS_BUCKET or len(syms) < min_symbols:
            continue
        hot = sorted(syms, key=lambda t: t[3], reverse=True)[:DEFAULT_MAX_EXCERPTS]
        outs = sorted(((t, c) for (f, t), c in dep_out.items() if f == mod), key=lambda x: -x[1])[:8]
        ins = sorted(((f, c) for (f, t), c in dep_out.items() if t == mod), key=lambda x: -x[1])[:8]
        doc_files = sorted(docs.get(mod, ()), key=lambda p: ("readme" not in p.lower(), p))[:2]
        specs.append(PageSpec("module", mod, len(files[mod]), len(syms), doc_files, hot, outs, ins))

    specs.sort(key=lambda s: s.symbols, reverse=True)
    return specs if top_k is None else specs[:top_k]


def _match_seed(node: dict, seed: str) -> bool:
    needle = seed.lower()
    return (needle in str(node.get("id", "")).lower()
            or needle in str(node.get("label", "")).lower()
            or needle in str(node.get("source_file", "")).lower())


def plan_flows(
    nodes: list[dict],
    links: list[dict],
    flows_config: list[dict],
    *,
    module_depth: int = DEFAULT_MODULE_DEPTH,
    depth: int = DEFAULT_FLOW_DEPTH,
) -> list[PageSpec]:
    """Cross-cutting flow pages: BFS over the graph from user-declared seeds.

    Config shape (isidore.json): {"flows": [{"name": "grant-issue", "seeds": ["grants.py", "cmd_grant"]}]}
    """
    by_id = {n["id"]: n for n in nodes if "id" in n}
    adjacency: dict[str, list[tuple[str, str]]] = defaultdict(list)
    for link in links:
        s, t = link.get("source"), link.get("target")
        rel = link.get("relation", "related")
        if isinstance(s, str) and isinstance(t, str) and s in by_id and t in by_id:
            adjacency[s].append((t, rel))
            adjacency[t].append((s, f"~{rel}"))    # reverse edge, marked

    specs: list[PageSpec] = []
    for flow in flows_config:
        name, seeds = flow.get("name"), flow.get("seeds", [])
        if not name or not seeds:
            continue
        seed_ids = [n["id"] for n in nodes if "id" in n and any(_match_seed(n, s) for s in seeds)]
        visited: set[str] = set(seed_ids)
        edges: list[tuple[str, str, str]] = []
        queue = deque((sid, 0) for sid in seed_ids)
        while queue:
            current, dist = queue.popleft()
            if dist >= depth:
                continue
            for neighbor, rel in adjacency.get(current, ()):
                if not rel.startswith("~"):
                    edges.append((current, rel, neighbor))
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, dist + 1))

        touched = sorted({module_of(by_id[v].get("source_file"), module_depth)
                          for v in visited if by_id[v].get("source_file")})
        deg = Counter(v for e in edges for v in (e[0], e[2]))
        hot = []
        for node_id, _count in deg.most_common(DEFAULT_MAX_EXCERPTS):
            n = by_id[node_id]
            if n.get("source_file"):
                hot.append((n.get("label", node_id), n["source_file"],
                            n.get("source_location") or "", deg[node_id]))
        spec = PageSpec("flow", str(name), hot_symbols=hot, modules=touched,
                        flow_edges=[(by_id[a].get("label", a), rel, by_id[b].get("label", b))
                                    for a, rel, b in edges[:60]])
        specs.append(spec)
    return specs


def suggest_flows(nodes: list[dict], links: list[dict], *,
                  module_depth: int = DEFAULT_MODULE_DEPTH, top_n: int = 8) -> list[dict]:
    """Candidate flows: the heaviest cross-module bridges, with their busiest bridge symbol."""
    by_id = {n["id"]: n for n in nodes if "id" in n}
    bridges: dict[tuple[str, str], Counter] = defaultdict(Counter)
    for link in links:
        s, t = by_id.get(link.get("source")), by_id.get(link.get("target"))
        if not s or not t:
            continue
        ms = module_of(s.get("source_file"), module_depth)
        mt = module_of(t.get("source_file"), module_depth)
        if ms != mt and CONCEPTS_BUCKET not in (ms, mt):
            bridges[(ms, mt)][s.get("label", s["id"])] += 1
    ranked = sorted(bridges.items(), key=lambda kv: -sum(kv[1].values()))[:top_n]
    return [
        {"name": f"{a.split('/')[-1]}-to-{b.split('/')[-1]}", "links": sum(c.values()),
         "modules": [a, b], "seeds": [symbol for symbol, _n in c.most_common(2)]}
        for (a, b), c in ranked
    ]


# ------------------------------------------------------------------- context

def read_excerpt(repo: Path, source_file: str, location: str,
                 radius: int = DEFAULT_EXCERPT_RADIUS) -> str:
    """±radius lines around a graph `L<n>` location. Tolerates stale files/locations."""
    match = re.match(r"L(\d+)", location or "")
    path = repo / source_file
    if not match or not path.is_file():
        return ""
    center = int(match.group(1))
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return ""
    lo, hi = max(0, center - 1 - radius), min(len(lines), center - 1 + radius + 1)
    body = "\n".join(f"{i + 1}: {lines[i]}" for i in range(lo, hi))
    return f"--- excerpt {source_file}:{center} ---\n{body}\n"


def git_log_for(repo: Path, pathspec: str, n: int = 8) -> str:
    try:
        out = subprocess.run(["git", "log", "--oneline", f"-{n}", "--", pathspec],
                             cwd=repo, capture_output=True, encoding="utf-8", errors="replace",
                             timeout=30, check=False)
        return out.stdout.strip() if out.returncode == 0 else ""
    except (OSError, subprocess.TimeoutExpired):
        return ""


def assemble_context(repo: Path, spec: PageSpec, *,
                     max_chars: int = DEFAULT_MAX_PROMPT_CHARS) -> tuple[str, list[str]]:
    """Gather one page's facts. Returns (context, truncation-warnings)."""
    if spec.kind == "flow":
        parts = [
            f"flow: {spec.name}",
            "modules involved: " + (", ".join(spec.modules) or "(unknown)"),
            "graph edges (source --relation--> target):\n"
            + ("\n".join(f"  {a} --{rel}--> {b}" for a, rel, b in spec.flow_edges) or "  (none)"),
            "most connected nodes in this flow: "
            + (", ".join(f"{lbl} [{f}:{loc or '?'}] deg={d}"
                         for lbl, f, loc, d in spec.hot_symbols) or "(none)"),
        ]
    else:
        parts = [
            f"module: {spec.name}",
            f"files: {spec.files} · code symbols: {spec.symbols}",
            "depends on (cross-module, link count): "
            + (", ".join(f"{m} ({c})" for m, c in spec.deps_out) or "(none)"),
            "depended on by: " + (", ".join(f"{m} ({c})" for m, c in spec.deps_in) or "(none)"),
            "most connected symbols: "
            + (", ".join(f"{lbl} [{f}:{loc or '?'}] deg={d}"
                         for lbl, f, loc, d in spec.hot_symbols) or "(none)"),
        ]
        log = git_log_for(repo, spec.name)
        if log:
            parts.append(f"recent git history:\n{log}")
        for doc in spec.doc_files:
            path = repo / doc
            if path.is_file():
                head = "\n".join(path.read_text(encoding="utf-8", errors="replace").splitlines()[:150])
                parts.append(f"--- doc {doc} (first lines) ---\n{head}")

    for _lbl, f, loc, _deg in spec.hot_symbols:
        excerpt = read_excerpt(repo, f, loc)
        if excerpt:
            parts.append(excerpt)

    warnings: list[str] = []
    context = "\n\n".join(parts)
    if len(context) > max_chars:
        context = context[:max_chars]
        warnings.append(f"{spec.name}: context truncated to {max_chars} chars (budget)")
    return context, warnings


def prompt_for(spec: PageSpec, context: str) -> str:
    template = FLOW_PROMPT if spec.kind == "flow" else MODULE_PROMPT
    return (template.format(name=spec.name, facts=context)
            + CLAIMS_PROMPT_ADDENDUM + FINDINGS_PROMPT_ADDENDUM)


def context_hash(prompt: str) -> str:
    """Content-addressed page identity: same prompt -> nothing to regenerate."""
    return hashlib.sha256(prompt.encode("utf-8")).hexdigest()


# ---------------------------------------------------------------------- lint

_PATH_TOKEN = re.compile(
    r"\b[\w][\w./\\-]*\.(?:py|ts|tsx|js|jsx|kt|kts|rs|go|java|rb|md|json|ya?ml|toml|sh|ps1|cfg|ini)\b"
)


def lint_cited_paths(markdown: str, repo: Path) -> list[str]:
    """File-looking paths cited in the prose that do NOT exist in the repo."""
    missing: list[str] = []
    for token in sorted({m.group(0) for m in _PATH_TOKEN.finditer(markdown)}):
        rel = token.replace("\\", "/").lstrip("/")
        if "/" not in rel:
            continue  # bare names like config.json are too false-positive-prone
        if not (repo / rel).exists():
            missing.append(rel)
    return missing


def annotate_unverified_paths(markdown: str, missing: set[str]) -> str:
    """Annotate every cited path that does not exist in the repo, inline and visibly — never strip
    the prose. Deterministic and reversible: the next successful regeneration replaces the page."""
    def _mark(match: re.Match) -> str:
        token = match.group(0)
        if token.replace("\\", "/").lstrip("/") in missing:
            return f"{token} [⚠ isidore: path not found]"
        return token
    return _PATH_TOKEN.sub(_mark, markdown)


def _split_negative_existential(items: list[dict], key: str) -> tuple[list[dict], int]:
    """Drop items whose `key` text asserts existential absence (unanchorable). Returns (kept, n)."""
    kept = [it for it in items if not is_negative_existential(it.get(key, ""))]
    return kept, len(items) - len(kept)


# --------------------------------------------------------------------- state

def load_state(wiki_dir: Path) -> dict:
    path = wiki_dir / STATE_FILENAME
    if path.is_file():
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            pass
    return {"pages": {}}


def save_state(wiki_dir: Path, state: dict) -> None:
    (wiki_dir / STATE_FILENAME).write_text(
        json.dumps(state, indent=2, sort_keys=True) + "\n", encoding="utf-8")


# ------------------------------------------------------------------- config

def load_config(repo: Path) -> dict:
    path = repo / "isidore.json"
    if path.is_file():
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            pass
    return {}


# -------------------------------------------------------------------- scope

def _match_only(spec: PageSpec, selectors: list[str]) -> bool:
    """A page matches a selector if the selector equals its filename, or is a prefix of / substring
    of its module path or name. Loose on purpose — the compile reports `scoped: N of M` so the user
    sees the breadth."""
    for sel in selectors:
        sel = sel.strip()
        if not sel:
            continue
        if spec.filename == sel or spec.name == sel:
            return True
        if spec.name.startswith(sel.rstrip("/")) or sel in spec.filename or sel in spec.name:
            return True
    return False


def _resolve_scope(nodes, links, specs, flows, claim_stale, repo, state, *, module_depth,
                   only, changed, since, affected_depth, result) -> "set[str] | None":
    """Compute the eligible page filenames for this run, or None for a full compile."""
    if only:
        pages = {s.filename for s in specs if _match_only(s, only)}
        result.warnings.append(f"scoped by --only to {len(pages)} of {len(specs)} planned page(s)")
        return pages
    if not changed:
        return None
    ref = since or state.get("commit")
    if not ref:
        result.warnings.append("--changed had no baseline commit (never compiled here) — full compile")
        return None
    clines = changed_lines(repo, ref)
    csyms = changed_symbols(nodes, clines)
    amods = affected_modules(nodes, links, csyms, module_depth=module_depth, depth=affected_depth)
    pages = {s.filename for s in specs if s.kind == "module" and s.name in amods}
    pages |= {s.filename for s in flows if set(s.modules) & amods}   # flows touching an affected zone
    pages |= set(claim_stale)                                        # always refresh drifted claims
    result.warnings.append(
        f"scoped by --changed since {ref[:12]}: {len(clines)} file(s), {len(csyms)} symbol(s), "
        f"{len(amods)} affected module(s) -> {len(pages)} page(s)")
    return pages


# ------------------------------------------------------------------ compile

@dataclass
class CompileResult:
    planned: int = 0
    dirty: list[str] = field(default_factory=list)
    generated: list[str] = field(default_factory=list)
    skipped_by_cap: list[str] = field(default_factory=list)
    pruned: list[str] = field(default_factory=list)
    quarantined: list[str] = field(default_factory=list)
    retries: int = 0
    lint_findings: dict[str, list[str]] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)
    findings_kept: int = 0
    findings_dropped: int = 0
    findings_dropped_negative: int = 0
    claims_total: int = 0
    claims_dropped: int = 0
    claims_dropped_negative: int = 0
    claims_repaired: int = 0
    claims_stale_pages: list[str] = field(default_factory=list)


def compile_wiki(
    repo: Path,
    *,
    graph_path: Path | None = None,
    execute: bool = False,
    generator=None,
    module_depth: int = DEFAULT_MODULE_DEPTH,
    top_k: int = DEFAULT_TOP_K_PAGES,
    min_symbols: int = DEFAULT_MIN_SYMBOLS,
    max_calls: int = DEFAULT_MAX_CALLS,
    max_prompt_chars: int = DEFAULT_MAX_PROMPT_CHARS,
    flows_config: list[dict] | None = None,
    only: list[str] | None = None,
    changed: bool = False,
    since: str | None = None,
    affected_depth: int = 1,
) -> CompileResult:
    """Run the pipeline. With execute=False no LLM is called and no page is written.

    Scoping (never deletes — prune is disabled whenever a scope is active):
      only     restrict to pages whose module/filename matches one of these selectors.
      changed  restrict to pages in the blast radius of the git changes since `since` (default: the
               commit recorded at the last compile) — the changed modules plus their dependents
               (fan-in, `affected_depth` hops) plus any claim-stale pages.
    """
    result = CompileResult()
    if graph_path is None or not graph_path.is_file():
        raise FileNotFoundError(
            f"no structure graph found for {repo} — run `isidore scan` (Python repos) "
            "or point --graph at a graph.json (see README for the format)")

    nodes, links, commit = load_graph(graph_path)
    # Exclude gitignored/untracked paths (build artifacts) from ANY producer's graph. A raw
    # filesystem walk (ours or Graphify's) indexes e.g. a Gradle/Chaquopy copy of a source tree
    # as a phantom duplicate module with stale symbols; git is the source of truth for real code.
    nodes, links, dropped_paths = restrict_to_tracked(nodes, links, repo)
    if dropped_paths:
        sample = ", ".join(sorted(dropped_paths)[:3])
        result.warnings.append(
            f"excluded {len(dropped_paths)} gitignored/untracked path(s) from the graph "
            f"(build artifacts / vendored trees, not tracked source): {sample}"
            + (" ..." if len(dropped_paths) > 3 else ""))
    all_modules = plan_pages(nodes, links, module_depth=module_depth, top_k=None,
                             min_symbols=min_symbols)
    flows = plan_flows(nodes, links, flows_config or [], module_depth=module_depth)
    specs = all_modules[:top_k] + flows
    result.planned = len(specs)

    wiki_dir = repo / WIKI_DIRNAME
    state = load_state(wiki_dir)
    pages_state: dict = state.setdefault("pages", {})

    # staleness de claims: re-hash de la evidencia — 0 llamadas LLM, corre SIEMPRE (dry-run incl.)
    claim_stale = stale_pages(repo, pages_state)
    result.claims_stale_pages = sorted(claim_stale)

    # Scope: which page filenames are eligible this run (None = all). Prune is disabled while any
    # scope is active — scoping documents a zone, it must never delete another zone's page.
    scope_pages = _resolve_scope(nodes, links, specs, flows, claim_stale, repo, state,
                                 module_depth=module_depth, only=only, changed=changed,
                                 since=since, affected_depth=affected_depth, result=result)
    scoped = scope_pages is not None

    contexts: dict[str, tuple[PageSpec, str, str]] = {}
    for spec in specs:
        if scoped and spec.filename not in scope_pages:
            continue      # out of scope: not assembled, not hash-checked, not generated, not touched
        context, warns = assemble_context(repo, spec, max_chars=max_prompt_chars)
        result.warnings.extend(warns)
        prompt = prompt_for(spec, context)
        digest = context_hash(prompt)
        contexts[spec.filename] = (spec, prompt, digest)
        prev = pages_state.get(spec.filename, {})
        if (prev.get("context_hash") != digest
                or spec.filename in claim_stale
                or not (wiki_dir / spec.filename).is_file()):
            result.dirty.append(spec.filename)

    # Deterministic dirty ordering so the --max-calls cap bites the LEAST important pages: pages a
    # previous run left pending (skipped by its cap) drain FIRST — never re-skip the same page
    # forever — then claim-stale pages, then heavily-depended-on (high fan-in) modules, then name.
    def _dirty_key(name: str) -> tuple:
        spec = contexts[name][0]
        prev = pages_state.get(name, {})
        fan_in = sum(c for _m, c in spec.deps_in) if spec.kind == "module" else 0
        return (0 if prev.get("pending") else 1, 0 if name in claim_stale else 1, -fan_in, name)
    result.dirty.sort(key=_dirty_key)

    # --max-calls 0 == unlimited (explicit opt-out of the bounded-cost default).
    unlimited = (max_calls == 0)
    calls_budget = float("inf") if unlimited else max_calls

    if not execute:
        cap = len(result.dirty) if unlimited else max_calls
        result.skipped_by_cap = result.dirty[cap:]
        for name in result.skipped_by_cap:
            result.warnings.append(f"{name}: dirty but over --max-calls={max_calls} cap (pending)")
        return result

    wiki_dir.mkdir(exist_ok=True)
    generate = generator if generator is not None else default_generator()
    known_files = {n["source_file"] for n in nodes if n.get("source_file")}

    calls_made = 0
    for name in result.dirty:
        if calls_made >= calls_budget:
            # over the call budget this run — mark pending so the NEXT run drains it first.
            result.skipped_by_cap.append(name)
            pages_state.setdefault(name, {})["pending"] = True
            result.warnings.append(f"{name}: dirty but over --max-calls={max_calls} cap (pending)")
            continue
        spec, prompt, digest = contexts[name]
        raw = generate(prompt)
        calls_made += 1
        markdown, raw_claims = parse_claims_block(raw)
        markdown, page_findings = parse_findings_block(markdown)

        # Lint gate: a page citing paths that do not exist gets ONE bounded repair retry (the
        # phantom paths are named back to the model). The retry consumes the call budget — honest
        # cost. If it still fails, the page ships with each phantom citation annotated INLINE and
        # is marked quarantined; it is never silently emitted with a dead citation inside (Bug A).
        missing = lint_cited_paths(markdown, repo)
        if missing and calls_made < calls_budget:
            result.retries += 1
            repair = prompt + LINT_REPAIR_ADDENDUM.format(
                paths="\n".join(f"  - {p}" for p in missing))
            raw = generate(repair)
            calls_made += 1
            markdown, raw_claims = parse_claims_block(raw)
            markdown, page_findings = parse_findings_block(markdown)
            missing = lint_cited_paths(markdown, repo)

        quarantined = bool(missing)
        if missing:
            result.lint_findings[name] = missing
            markdown = annotate_unverified_paths(markdown, set(missing))
            result.quarantined.append(name)

        # Absence-hallucination backstop: claims/findings asserting existential absence cannot be
        # evidence-anchored (their "evidence" is the absence of code), so drop them by construction.
        raw_claims, neg_claims = _split_negative_existential(raw_claims, "statement")
        page_findings, neg_findings = _split_negative_existential(page_findings, "note")
        result.claims_dropped_negative += neg_claims
        result.findings_dropped_negative += neg_findings

        claims, claims_dropped, claims_repaired = anchor_claims(repo, raw_claims, known_files)
        result.claims_total += len(claims)
        result.claims_dropped += claims_dropped
        result.claims_repaired += claims_repaired
        kept, dropped = filter_findings(page_findings, repo)
        result.findings_kept += len(kept)
        result.findings_dropped += len(dropped)

        # per-page H2-level changelog: capture the old prose before overwriting, carry the page's
        # history forward, and record what changed in its understanding (0 LLM).
        page_path = wiki_dir / name
        old_content = page_path.read_text(encoding="utf-8") if page_path.is_file() else ""
        prev_history = pages_state.get(name, {}).get("history", [])
        page_path.write_text(markdown, encoding="utf-8", newline="\n")
        pages_state[name] = {"context_hash": digest, "kind": spec.kind, "name": spec.name,
                             "findings": kept, "claims": claims, "quarantined": quarantined,
                             "history": prev_history}
        record_page_change(pages_state[name], commit, old_content, markdown)
        result.generated.append(name)

    # prune only when the MODULE/FLOW left the graph/config — never because of a smaller top-k, and
    # NEVER under a scope (--only/--changed only saw a slice of the repo; deleting the rest would be
    # catastrophic data loss).
    eligible = {s.filename for s in all_modules} | {s.filename for s in flows}
    if not scoped:
        for name in [n for n in pages_state if n not in eligible]:
            page = wiki_dir / name
            if page.is_file():
                page.unlink()
            del pages_state[name]
            result.pruned.append(name)

    module_specs = all_modules[:top_k]
    (wiki_dir / "quickstart.md").write_text(
        render_quickstart(module_specs, flows, commit), encoding="utf-8", newline="\n")
    (wiki_dir / "index.toon").write_text(
        render_toon_index(module_specs, flows, commit), encoding="utf-8", newline="\n")

    # residuo: findings LLM acumulados en el estado (sobreviven compilaciones incrementales)
    # + residuos deterministas recalculados (gratis) — todo a findings.toon, nunca a las páginas
    llm_findings = [f for page in pages_state.values() for f in page.get("findings", [])]
    planned_modules = {s.name for s in module_specs}
    source_files = {n["source_file"] for n in nodes
                    if n.get("source_file") and n.get("file_type") == "code"
                    and module_of(n["source_file"], module_depth) in planned_modules}
    (wiki_dir / FINDINGS_FILENAME).write_text(
        render_findings(
            llm_findings,
            harvest_todos(repo, source_files),
            orphan_file_candidates(nodes, links),
            coverage_gap_candidates(module_specs),
            risk_hotspots(repo, module_specs),
            commit,
        ), encoding="utf-8", newline="\n")

    # AGENTS.md is the one PRE-EXISTING file we touch — preserve its line-ending style so we don't
    # rewrite every line (CRLF->LF) and turn a 6-line insert into a whole-file diff. Read raw bytes
    # to detect CRLF before universal-newline translation hides it.
    agents_md = repo / "AGENTS.md"
    raw = agents_md.read_bytes() if agents_md.is_file() else b""
    uses_crlf = b"\r\n" in raw
    existing = raw.decode("utf-8", errors="replace").replace("\r\n", "\n")
    merged = upsert_agents_block(existing, agents_md_block())
    if uses_crlf:
        merged = merged.replace("\n", "\r\n")
    agents_md.write_bytes(merged.encode("utf-8"))

    (wiki_dir / CLAIMS_FILENAME).write_text(
        render_claims(repo, pages_state, commit), encoding="utf-8", newline="\n")

    # Advance the --changed baseline only when this run actually covered every change since it: a
    # full compile does, and so does --changed (it refreshed the blast radius). --only saw a slice,
    # so it must NOT move the baseline or the next --changed would skip the unscoped changes. The
    # dependency fingerprint (for `isidore impact`'s emergent-edge detection) advances on the same
    # rule — it records the coupling graph the user has acknowledged.
    if not only:
        state["commit"] = commit
        state["deps"] = sorted([ms, mt, c] for (ms, mt), c in
                               module_dep_edges(nodes, links, module_depth).items())

    # journal this run for `isidore stats` (cost telemetry + unstable-page detection, 0 LLM).
    append_run(state, {
        "commit": (commit or "?")[:12],
        "planned": result.planned,
        "dirty": len(result.dirty),
        "generated": len(result.generated),
        "skipped": len(result.skipped_by_cap),
        "quarantined": len(result.quarantined),
        "retries": result.retries,
        "calls_saved": max(0, len(contexts) - len(result.dirty)),
        "generated_pages": list(result.generated),
    })
    save_state(wiki_dir, state)
    return result


__all__ = [
    "CompileResult", "GenerationError", "PageSpec", "assemble_context", "compile_wiki",
    "context_hash", "lint_cited_paths", "load_config", "plan_flows", "plan_pages",
    "prompt_for", "read_excerpt", "suggest_flows",
]
