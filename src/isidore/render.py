"""Deterministic outputs: quickstart.md, index.toon, llms.txt, and the AGENTS.md reference block.

None of these cost an LLM call. `index.toon` is the machine-first face of the wiki: the same
catalog as quickstart.md but in TOON tables, cheaper in tokens for an agent to load. `llms.txt` is
the same catalog again in the shape the wider ecosystem has settled on for handing documentation to
an agent — see `render_llms_txt`.
"""
from __future__ import annotations

import os
from pathlib import Path

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


def agents_md_block(wiki_dir: str = WIKI_DIRNAME, knowledge: dict | None = None) -> str:
    """The self-reference an agent reads before touching the repo. 0 LLM, idempotent.

    `knowledge` describes the local knowledge home when one has been compiled: `{path, pages,
    streams}`. It is mentioned only when it exists and is NOT a link — the knowledge home is
    per-user and local-only, so a path in a committed file would point at a directory the next
    reader does not have.
    """
    lines = [
        MARKER_START,
        "## Wiki (isidore)",
        "",
        f"This repository has an agent-oriented wiki in `{wiki_dir}/`, compiled from its structure graph.",
        f"Start at [{wiki_dir}/quickstart.md]({wiki_dir}/quickstart.md) — or load"
        f" [{wiki_dir}/index.toon]({wiki_dir}/index.toon) (same catalog, fewer tokens).",
        "Module and flow pages explain purpose, architecture, entry points and how to change each",
        "area safely, with `path:line` citations.",
    ]
    if knowledge and knowledge.get("pages"):
        lines += [
            "",
            "### Knowledge home (local, not in this repo)",
            "",
            f"This machine also has a compiled knowledge home with {knowledge['pages']} topic page(s)"
            f" over {knowledge.get('streams', 0)} ingested stream(s): external evidence — repositories,"
            " feeds, discussions, mail — each claim citing a `src://` URI that resolves to the stored"
            " item.",
            "Run `isidore sync` to refresh it and `isidore claims --check` to see what has gone stale.",
            "It is per-user and never travels with the repository, so no path is linked here.",
        ]
    lines.append(MARKER_END)
    return "\n".join(lines)


def knowledge_summary() -> dict:
    """`{path, pages, streams}` for the local knowledge home, or {} if there is none. Never raises."""
    try:
        from .home import home
        from .knowledge import load_knowledge_state
        root = home()
        pages = len(load_knowledge_state().get("pages", {}))
        conn = root / "connectors"
        streams = 0
        if conn.is_dir():
            from .connectors.store import read_state
            for cdir in conn.iterdir():
                if cdir.is_dir():
                    streams += len(read_state(cdir.name, "").get("cursors", {}))
        return {"path": str(root), "pages": pages, "streams": streams} if pages else {}
    except Exception:                      # a knowledge home is optional; never break a compile
        return {}


def upsert_agents_block(existing: str, block: str) -> str:
    """Insert or replace the delimited block without touching the rest of the file (idempotent)."""
    if MARKER_START in existing and MARKER_END in existing:
        pre = existing.split(MARKER_START)[0]
        post = existing.split(MARKER_END, 1)[1]
        return pre + block + post
    sep = "" if existing.endswith("\n\n") else ("\n" if existing.endswith("\n") else "\n\n")
    return existing + sep + block + "\n"


# ------------------------------------------------------------------ llms.txt

LLMS_FILENAME = "llms.txt"
_SUBSYSTEM_PREFIX = "subsystem-"
_OVERVIEW = "overview.md"
_NOISE = ("quickstart.md", _OVERVIEW)


def _first_sentence(text: str) -> str:
    for line in text.splitlines():
        stripped = line.strip()
        if stripped and not stripped.startswith(("#", ">", "-", "*", "|", "`")):
            return stripped.split(". ")[0].rstrip(".") + "."
    return ""


def render_llms_txt(repo: Path, wiki_dir: str = WIKI_DIRNAME) -> str:
    """The wiki, in the layout agents are converging on for being handed documentation.

    `llms.txt` is a community convention, not a ratified standard, and its own authors say so. It is
    worth emitting anyway for a plain reason: the tools that actually read it are coding agents
    fetching docs on demand, which is this wiki's primary audience, and the format costs nothing to
    produce — an H1, a blockquote summary, then H2 lists of links. Everything here is already on
    disk; this is a second index over it, not a new artifact to keep true.

    The layering is the point. The product page becomes the summary, area pages come first because
    they orient, module pages follow, and everything an agent can skip when its context is short
    goes under the reserved `## Optional` heading, which is exactly what that heading means in the
    spec.
    """
    wiki = repo / wiki_dir
    name = repo.resolve().name
    pages = sorted(p.name for p in wiki.glob("*.md")) if wiki.is_dir() else []

    summary = ""
    overview = wiki / _OVERVIEW
    if overview.is_file():
        summary = _first_sentence(overview.read_text(encoding="utf-8", errors="replace"))

    lines = [f"# {name}", ""]
    if summary:
        lines += [f"> {summary}", ""]
    lines += ["Documentation compiled by isidore from this repository's structure. Every page ships "
              "a `.cert.json` recording which of its statements were mechanically verified against "
              "the code.", ""]

    def _section(title: str, entries: list[tuple[str, str]]) -> None:
        if not entries:
            return
        lines.append(f"## {title}")
        lines.append("")
        for link, note in entries:
            lines.append(f"- [{link}]({wiki_dir}/{link})" + (f": {note}" if note else ""))
        lines.append("")

    if overview.is_file():
        _section("Start here", [(_OVERVIEW, "what this project is, in plain language")])
    _section("Areas", [(p, "") for p in pages if p.startswith(_SUBSYSTEM_PREFIX)])
    _section("Modules", [(p, "") for p in pages
                         if not p.startswith(_SUBSYSTEM_PREFIX) and p not in _NOISE])

    optional = [("quickstart.md", "deterministic catalog of every module")] if \
        (wiki / "quickstart.md").is_file() else []
    optional += [(f, note) for f, note in (
        ("index.toon", "the same catalog as TOON tables, fewer tokens"),
        ("claims.toon", "every claim with its evidence and freshness"),
        ("findings.toon", "unverified residue: suspected bugs, TODOs, open questions"),
    ) if (wiki / f).is_file()]
    _section("Optional", optional)
    return "\n".join(lines).rstrip() + "\n"


def write_llms_txt(repo: Path, wiki_dir: str = WIKI_DIRNAME) -> Path:
    """Write llms.txt at the repo root — where the convention puts it, so a fetcher finds it."""
    path = repo / LLMS_FILENAME
    path.write_text(render_llms_txt(repo, wiki_dir), encoding="utf-8")
    return path


def register_cli(sub) -> None:
    """Add `isidore llms` (regenerate llms.txt from whatever is compiled). 0 LLM."""
    parser = sub.add_parser("llms", help="write llms.txt: the wiki as an agent-facing index (0 LLM)")
    parser.add_argument("--repo", type=Path, default=Path("."))
    parser.set_defaults(func=_cmd_llms)


def _cmd_llms(args) -> int:
    wiki = args.repo / WIKI_DIRNAME
    if not wiki.is_dir():
        print(f"[isidore] no wiki at {wiki} — run `isidore compile --execute` first")
        return 2
    path = write_llms_txt(args.repo)
    print(f"[isidore] wrote {path} ({len(render_llms_txt(args.repo).splitlines())} lines, 0 LLM)")
    return 0
