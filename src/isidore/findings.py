"""Side observations ("residue") harvested during compilation — at ~zero marginal cost.

Two sources, kept strictly separate from the wiki prose:

1. LLM residue — the model is already reading the excerpts with attention to document them;
   asking for structured observations rides the SAME call (same input, a few more output lines).
   The page prompt asks for an optional fenced block after the page:

       ```isidore-findings
       bug | src/x.py:42 | lock not released on the error path
       drift | README.md:10 | README says retries=3, code hardcodes 1
       question | | why is the cache disabled for flows?
       ```

   These are UNVERIFIED hypotheses from a model reading bounded excerpts — a triage queue,
   never a bug report. Findings citing paths that do not exist in the repo are dropped
   mechanically (the same hallucination filter as page citations).

2. Deterministic residue — pure code over the graph + git, no LLM at all: TODO/FIXME/HACK
   harvest, orphan-file candidates, modules with no test coverage links, and risk hotspots
   (connection degree x recent churn).

Everything lands in wiki/findings.toon, one table per kind.
"""
from __future__ import annotations

import re
import subprocess
from collections import Counter
from pathlib import Path

from .toon import encode

FINDING_KINDS = ("bug", "drift", "question", "term")
FINDINGS_FILENAME = "findings.toon"

FINDINGS_PROMPT_ADDENDUM = """
After the page, IF (and only if) you noticed something noteworthy while reading the facts, append
a fenced block with structured observations — suspected bugs, contradictions between docs and
code, or open questions the evidence could not answer:

```isidore-findings
bug | path:line | one-line description of the suspicion
drift | path:line | doc claim vs code behavior
question | | what remains unclear and why it matters
```

Rules for this block: kinds are bug|drift|question|term; cite only paths present in the facts;
one line per observation; omit the block entirely if you have none. These are triage hypotheses,
not conclusions — do not mention them in the page itself.
"""

_FENCE = re.compile(r"```isidore-findings\s*\n(.*?)```", re.DOTALL)
_TODO = re.compile(r"\b(TODO|FIXME|HACK|XXX)\b[:\s]*(.{0,120})")
_ENTRYPOINT_HINTS = ("main", "cli", "app", "index", "setup", "conftest", "__init__")


def parse_findings_block(markdown: str) -> tuple[str, list[dict]]:
    """Split a generated page into (clean page, findings rows). Tolerant of malformed lines."""
    findings: list[dict] = []

    def _consume(match: re.Match) -> str:
        for raw in match.group(1).splitlines():
            parts = [p.strip() for p in raw.split("|", 2)]
            if len(parts) != 3 or parts[0] not in FINDING_KINDS:
                continue
            findings.append({"kind": parts[0], "where": parts[1], "note": parts[2]})
        return ""

    clean = _FENCE.sub(_consume, markdown).rstrip() + "\n"
    return clean, findings


def filter_findings(findings: list[dict], repo: Path) -> tuple[list[dict], list[dict]]:
    """Drop findings whose cited path does not exist (mechanical hallucination filter).

    Returns (kept, dropped). `question` findings may cite nothing and always pass.
    """
    kept: list[dict] = []
    dropped: list[dict] = []
    for f in findings:
        where = f.get("where", "")
        path_part = where.split(":", 1)[0].replace("\\", "/").strip()
        if not path_part:
            (kept if f["kind"] == "question" else dropped).append(f)
            continue
        (kept if (repo / path_part).exists() else dropped).append(f)
    return kept, dropped


# ------------------------------------------------------- deterministic residue

MAX_TODO_FILE_BYTES = 2_000_000       # skip pathologically large files (generated/vendored)
MAX_TODO_FILES = 4000                 # bound total files scanned so a huge repo can't stall a compile


def harvest_todos(repo: Path, source_files: set[str], cap: int = 200) -> list[dict]:
    """TODO/FIXME/HACK/XXX with file:line — regex over the files the graph already knows.

    Bounded for scale: skips files over MAX_TODO_FILE_BYTES and scans at most MAX_TODO_FILES
    (sorted for determinism), so this stays fast even on very large repos.
    """
    rows: list[dict] = []
    for rel in sorted(source_files)[:MAX_TODO_FILES]:
        path = repo / rel
        if not path.is_file():
            continue
        try:
            if path.stat().st_size > MAX_TODO_FILE_BYTES:
                continue
            lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError:
            continue
        for i, line in enumerate(lines, 1):
            m = _TODO.search(line)
            if m:
                rows.append({"marker": m.group(1), "file": rel, "line": i,
                             "note": m.group(2).strip()})
                if len(rows) >= cap:
                    return rows
    return rows


def orphan_file_candidates(nodes: list[dict], links: list[dict], cap: int = 40) -> list[dict]:
    """Code FILE nodes nothing links to — dead-code candidates (entrypoint-looking names excluded)."""
    targeted = {link.get("target") for link in links}
    rows = []
    for n in nodes:
        if n.get("file_type") != "code" or n.get("source_location") != "L1":
            continue  # only file-level nodes (convention: files anchor at L1)
        if n.get("id") in targeted:
            continue
        stem = Path(n.get("source_file", "")).stem.lower()
        if any(h in stem for h in _ENTRYPOINT_HINTS) or stem.startswith("test"):
            continue
        rows.append({"file": n.get("source_file", "?")})
        if len(rows) >= cap:
            break
    return rows


def coverage_gap_candidates(module_specs) -> list[dict]:
    """Module pages with no inbound link from any test-looking module."""
    rows = []
    for spec in module_specs:
        if "test" in spec.name.lower():
            continue
        has_tests = any("test" in m.lower() for m, _c in spec.deps_in)
        if not has_tests:
            rows.append({"module": spec.name, "symbols": spec.symbols})
    return rows


def _churn(repo: Path, pathspec: str, n: int = 50) -> int:
    try:
        out = subprocess.run(["git", "log", "--oneline", f"-{n}", "--", pathspec],
                             cwd=repo, capture_output=True, encoding="utf-8", errors="replace",
                             timeout=30, check=False)
        return len(out.stdout.strip().splitlines()) if out.returncode == 0 else 0
    except (OSError, subprocess.TimeoutExpired):
        return 0


def risk_hotspots(repo: Path, module_specs, cap: int = 15) -> list[dict]:
    """Where a mistake hurts most: top symbol degree x recent module churn."""
    rows = []
    for spec in module_specs:
        churn = _churn(repo, spec.name)
        if not churn or not spec.hot_symbols:
            continue
        lbl, f, loc, deg = spec.hot_symbols[0]
        rows.append({"module": spec.name, "symbol": lbl, "file": f,
                     "line": (loc or "").lstrip("L"), "degree": deg, "churn": churn,
                     "risk": deg * churn})
    rows.sort(key=lambda r: -r["risk"])
    return rows[:cap]


def render_findings(llm_findings: list[dict], todos: list[dict], orphans: list[dict],
                    gaps: list[dict], hotspots: list[dict], commit: str | None) -> str:
    header = (
        f"# isidore findings · commit {commit or '?'}\n"
        "# suspects/drift/questions: UNVERIFIED model observations (triage queue).\n"
        "# todos/orphans/test_gaps/hotspots: mechanical facts from graph+git, no LLM.\n"
    )
    by_kind = Counter(f["kind"] for f in llm_findings)
    tables = [
        ("suspects", ["kind", "where", "note"],
         [f for f in llm_findings if f["kind"] in ("bug", "drift")]),
        ("questions", ["where", "note"],
         [{"where": f["where"], "note": f["note"]} for f in llm_findings
          if f["kind"] == "question"]),
        ("terms", ["where", "note"],
         [{"where": f["where"], "note": f["note"]} for f in llm_findings if f["kind"] == "term"]),
        ("todos", ["marker", "file", "line", "note"], todos),
        ("orphan_files", ["file"], orphans),
        ("test_gaps", ["module", "symbols"], gaps),
        ("hotspots", ["module", "symbol", "file", "line", "degree", "churn", "risk"], hotspots),
    ]
    summary = (f"# summary: {by_kind.get('bug', 0)} bug suspects, {by_kind.get('drift', 0)} drift, "
               f"{by_kind.get('question', 0)} questions, {len(todos)} todos, "
               f"{len(orphans)} orphan files, {len(gaps)} test gaps\n")
    return header + summary + encode(*tables) + "\n"
