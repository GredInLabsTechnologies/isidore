"""Deterministic outputs: quickstart.md, index.toon, and the AGENTS.md reference block.

None of these cost an LLM call. `index.toon` is the machine-first face of the wiki: the same
catalog as quickstart.md but in TOON tables, cheaper in tokens for an agent to load.
"""
from __future__ import annotations

import os

from .toon import encode

MARKER_START = "<!-- ISIDORE:START -->"
MARKER_END = "<!-- ISIDORE:END -->"
# Output directory for the compiled wiki, relative to the repo root. Defaults to
# "wiki"; override with ISIDORE_WIKI_DIR so a repo/org can keep its living docs
# elsewhere (e.g. "doc/isidore"). Read once at import; every module imports this
# constant, so the whole toolchain (scan, compile, certs, state, AGENTS.md block)
# resolves to the same directory.
WIKI_DIRNAME = os.environ.get("ISIDORE_WIKI_DIR", "wiki").strip() or "wiki"


def render_quickstart(module_specs, flow_specs, commit: str | None) -> str:
    lines = [
        "# Wiki (isidore)",
        "",
        f"Compiled from the repository structure graph at commit `{commit or '?'}`.",
        "Pages are generated from exact structural facts; cited `path:line` references are",
        "mechanically lint-checked against the repository.",
        "",
        "For agents: [index.toon](index.toon) is this same catalog in TOON (cheaper to load).",
        "Side observations harvested during compilation live in [findings.toon](findings.toon)",
        "(unverified suspects + mechanical facts — a triage queue, not a report).",
        "",
        "## Modules",
        "",
        "| module | files | symbols | page |",
        "|---|---|---|---|",
    ]
    for s in module_specs:
        lines.append(f"| {s.name} | {s.files} | {s.symbols} | [{s.filename}]({s.filename}) |")
    if flow_specs:
        lines += ["", "## Cross-cutting flows", "", "| flow | modules | page |", "|---|---|---|"]
        for s in flow_specs:
            lines.append(f"| {s.name} | {', '.join(s.modules)} | [{s.filename}]({s.filename}) |")
    lines.append("")
    return "\n".join(lines)


def render_toon_index(module_specs, flow_specs, commit: str | None) -> str:
    header = (
        f"# isidore wiki index · commit {commit or '?'}\n"
        "# same catalog as quickstart.md, in TOON tables (cheap for agents to load)\n"
    )
    hot_rows = []
    for s in module_specs:
        hot_rows.extend(
            {"module": s.name, "symbol": lbl, "file": f, "line": (loc or "").lstrip("L"), "degree": d}
            for lbl, f, loc, d in s.hot_symbols
        )
    tables = [
        ("modules", ["module", "files", "symbols", "page"],
         [{"module": s.name, "files": s.files, "symbols": s.symbols, "page": s.filename}
          for s in module_specs]),
        ("flows", ["flow", "modules", "page"],
         [{"flow": s.name, "modules": "+".join(s.modules), "page": s.filename}
          for s in flow_specs]),
        ("hot_symbols", ["module", "symbol", "file", "line", "degree"], hot_rows),
        ("module_deps", ["from", "to", "links"],
         [{"from": s.name, "to": m, "links": c} for s in module_specs for m, c in s.deps_out]),
    ]
    return header + encode(*tables) + "\n"


def agents_md_block(wiki_dir: str = WIKI_DIRNAME) -> str:
    return "\n".join([
        MARKER_START,
        "## Wiki (isidore)",
        "",
        f"This repository has an agent-oriented wiki in `{wiki_dir}/`, compiled from its structure graph.",
        f"Start at [{wiki_dir}/quickstart.md]({wiki_dir}/quickstart.md) — or load"
        f" [{wiki_dir}/index.toon]({wiki_dir}/index.toon) (same catalog, fewer tokens).",
        "Module and flow pages explain purpose, architecture, entry points and how to change each",
        "area safely, with `path:line` citations.",
        MARKER_END,
    ])


def upsert_agents_block(existing: str, block: str) -> str:
    """Insert or replace the delimited block without touching the rest of the file (idempotent)."""
    if MARKER_START in existing and MARKER_END in existing:
        pre = existing.split(MARKER_START)[0]
        post = existing.split(MARKER_END, 1)[1]
        return pre + block + post
    sep = "" if existing.endswith("\n\n") else ("\n" if existing.endswith("\n") else "\n\n")
    return existing + sep + block + "\n"
