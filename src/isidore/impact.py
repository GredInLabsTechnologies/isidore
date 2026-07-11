"""isidore impact — the zero-LLM emergent-interaction detector.

Regenerating a neighbour's prose does NOT detect an emergent interaction; a NEW graph edge does, and
it is free. This command diffs the CURRENT dependency graph against the fingerprint persisted at the
last compile (`state["deps"]`) and cross-references the git change-set, reporting — with no LLM call —
what a change touched, who depends on it, which cross-module edges appeared/vanished, which anchored
claims are now at risk, and which pages a `--changed` compile would regenerate.
"""
from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path

from .changeset import affected_modules, changed_lines, changed_symbols
from .claims import check_claims
from .graph import load_graph, module_of, restrict_to_tracked
from .pipeline import (
    DEFAULT_MIN_SYMBOLS,
    DEFAULT_MODULE_DEPTH,
    DEFAULT_TOP_K_PAGES,
    WIKI_DIRNAME,
    compile_wiki,
    load_state,
    module_dep_edges,
)
from .toon import encode


@dataclass
class ImpactReport:
    ref: str | None = None
    changed_files: list[str] = field(default_factory=list)
    changed_symbols: list[str] = field(default_factory=list)
    affected_modules: list[str] = field(default_factory=list)
    new_edges: list[tuple[str, str]] = field(default_factory=list)
    removed_edges: list[tuple[str, str]] = field(default_factory=list)
    fan_in: list[dict] = field(default_factory=list)
    claims_at_risk: list[dict] = field(default_factory=list)
    dirty_pages: list[str] = field(default_factory=list)
    todos_in_zone: list[dict] = field(default_factory=list)
    note: str = ""

    def has_signal(self) -> bool:
        return bool(self.dirty_pages or self.claims_at_risk or self.new_edges or self.removed_edges)


def build_impact(repo: Path, *, graph_path: Path, since: str | None = None,
                 module_depth: int = DEFAULT_MODULE_DEPTH, affected_depth: int = 1,
                 min_symbols: int = DEFAULT_MIN_SYMBOLS,
                 top_k: int = DEFAULT_TOP_K_PAGES) -> ImpactReport:
    from .findings import harvest_todos

    nodes, links, _commit = load_graph(graph_path)
    nodes, links, _dropped = restrict_to_tracked(nodes, links, repo)
    by_id = {n["id"]: n for n in nodes if "id" in n}
    state = load_state(repo / WIKI_DIRNAME)
    ref = since or state.get("commit")

    report = ImpactReport(ref=ref)
    if not ref:
        report.note = "no baseline commit (never compiled here) — run `isidore compile --execute` first"

    clines = changed_lines(repo, ref) if ref else {}
    csyms = changed_symbols(nodes, clines)
    amods = affected_modules(nodes, links, csyms, module_depth=module_depth, depth=affected_depth)
    report.changed_files = sorted(clines)
    report.changed_symbols = sorted(by_id[s].get("label", s) for s in csyms if s in by_id)
    report.affected_modules = sorted(amods)

    # emergent interactions: current cross-module edges vs the fingerprint from the last compile
    current = set(module_dep_edges(nodes, links, module_depth))
    stored = {(d[0], d[1]) for d in state.get("deps", [])}
    report.new_edges = sorted(current - stored)
    report.removed_edges = sorted(stored - current)

    # fan-in: for each changed symbol, who depends on it (consumers) across modules
    consumers: dict[str, set[str]] = defaultdict(set)
    for link in links:
        if link.get("target") in csyms and link.get("source") in by_id:
            consumers[link["target"]].add(link["source"])
    for sym in sorted(csyms):
        if sym not in by_id:
            continue
        cons = consumers.get(sym, set())
        report.fan_in.append({
            "symbol": by_id[sym].get("label", sym),
            "module": module_of(by_id[sym].get("source_file"), module_depth),
            "consumers": len(cons),
            "sample": ", ".join(sorted(by_id[c].get("label", c) for c in cons)[:4]),
        })

    # claims at risk: anchored claims whose evidence is in a changed file, or already stale/orphan
    changed_set = set(report.changed_files)
    for row in check_claims(repo, state.get("pages", {})):
        ev_path = row["evidence"].replace("\\", "/").rsplit(":", 1)[0]
        if row["state"] != "ok" or ev_path in changed_set:
            report.claims_at_risk.append(row)

    # pages a --changed compile would regenerate (dry-run — 0 LLM)
    if ref:
        dry = compile_wiki(repo, graph_path=graph_path, execute=False, changed=True, since=ref,
                           module_depth=module_depth, affected_depth=affected_depth,
                           min_symbols=min_symbols, top_k=top_k)
        report.dirty_pages = dry.dirty

    # TODO/FIXME in the changed files (residue of this change)
    code_changed = {f for f in changed_set if f.endswith((".py",))}
    if code_changed:
        report.todos_in_zone = harvest_todos(repo, code_changed)
    return report


def _edges(pairs) -> list[dict]:
    return [{"from": a, "to": b} for a, b in pairs]


def render_impact(r: ImpactReport, *, md: bool = False) -> str:
    tables = [
        ("changed", ["file"], [{"file": f} for f in r.changed_files]),
        ("emergent_new_edges", ["from", "to"], _edges(r.new_edges)),
        ("removed_edges", ["from", "to"], _edges(r.removed_edges)),
        ("fan_in", ["symbol", "module", "consumers", "sample"], r.fan_in),
        ("claims_at_risk", ["page", "state", "statement", "evidence"],
         [{k: c[k] for k in ("page", "state", "statement", "evidence")} for c in r.claims_at_risk]),
        ("would_regenerate", ["page"], [{"page": p} for p in r.dirty_pages]),
        ("todos_in_changed", ["where", "note"],
         [{"where": t.get("where", ""), "note": t.get("note", "")} for t in r.todos_in_zone]),
    ]
    if md:
        out = [f"# isidore impact · since {r.ref or '?'}"]
        if r.note:
            out.append(f"> {r.note}")
        out.append(f"- changed: {len(r.changed_files)} file(s), {len(r.changed_symbols)} symbol(s)")
        out.append(f"- affected modules: {', '.join(r.affected_modules) or '(none)'}")
        out.append(f"- **emergent edges: {len(r.new_edges)} new, {len(r.removed_edges)} removed**")
        out.append(f"- claims at risk: {len(r.claims_at_risk)} · would regenerate: {len(r.dirty_pages)}")
        return "\n".join(out) + "\n"
    header = (f"# isidore impact · since {r.ref or '?'} · {len(r.new_edges)} new / "
              f"{len(r.removed_edges)} removed edges · {len(r.dirty_pages)} pages would regenerate\n")
    if r.note:
        header += f"# {r.note}\n"
    return header + encode(*tables) + "\n"
