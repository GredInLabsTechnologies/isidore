"""Change-set detection: which graph symbols a git diff touched, and which modules that affects.

Pure functions — no LLM, no wiki I/O. The compiler uses this to scope a `--changed` compile to the
symbols that actually moved PLUS the modules that depend on them (fan-in), so an incremental compile
covers the blast radius of a change instead of the whole repo, and `isidore impact` (T3) can report
emergent interactions. `git` is the source of truth for WHAT changed; the graph maps that to symbols.
"""
from __future__ import annotations

import re
import subprocess
from collections import defaultdict, deque
from pathlib import Path

from .graph import module_of

# new-side of a unified-diff hunk header: @@ -a,b +c,d @@  -> (c, d)  (d omitted means 1)
_HUNK = re.compile(r"^@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@")
# a graph source_location: "L<start>" or "L<start>-L<end>"
_LOC = re.compile(r"L(\d+)(?:-L(\d+))?")

WHOLE_FILE = 0   # sentinel line meaning "treat the entire file as changed" (rename / mode-only)


def _git_diff(repo: Path, since: str) -> str:
    try:
        out = subprocess.run(
            ["git", "diff", "-U0", "--find-renames", "--no-color", since],
            cwd=repo, capture_output=True, encoding="utf-8", errors="replace",
            timeout=60, check=False)
        return out.stdout if out.returncode == 0 else ""
    except (OSError, subprocess.TimeoutExpired):
        return ""


def changed_lines(repo: Path, since: str) -> dict[str, set[int]]:
    """Map each changed tracked file (current/new path) -> set of new-side line numbers touched.

    A pure rename (no content change) yields the sentinel {WHOLE_FILE} on the new path — its symbols
    kept their content but moved, so the page must refresh. Added files come back with their added
    line ranges (git emits `@@ -0,0 +1,N @@`). Deletions produce no current-path entry (the symbols
    simply leave the graph on the next scan).
    """
    files: dict[str, set[int]] = defaultdict(set)
    current: str | None = None
    for line in _git_diff(repo, since).splitlines():
        if line.startswith("+++ "):
            target = line[4:].strip()
            if target == "/dev/null":
                current = None
            else:
                current = target[2:] if target.startswith("b/") else target
        elif line.startswith("rename to "):
            files[line[len("rename to "):].strip()].add(WHOLE_FILE)
        elif line.startswith("@@") and current:
            m = _HUNK.match(line)
            if not m:
                continue
            start = int(m.group(1))
            count = int(m.group(2)) if m.group(2) is not None else 1
            if count == 0:                       # pure deletion point — mark the anchor line
                files[current].add(start)
            else:
                files[current].update(range(start, start + count))
    return dict(files)


def symbol_spans(nodes: list[dict]) -> dict[str, list[tuple[int, int, str, str]]]:
    """Per file, the sorted line spans of its code symbols: (start, end, node_id, label).

    Accepts both `L<start>-L<end>` (current scanner) and legacy start-only `L<start>` locations: a
    start-only symbol spans until the next symbol's start (the last one to end-of-file). Together the
    spans partition the file, so every changed line maps to exactly one node.
    """
    by_file: dict[str, list[list]] = defaultdict(list)
    for n in nodes:
        if n.get("file_type") != "code" or not n.get("source_file"):
            continue
        m = _LOC.match(n.get("source_location") or "")
        if not m:
            continue
        start = int(m.group(1))
        end = int(m.group(2)) if m.group(2) else None
        by_file[n["source_file"]].append([start, end, n["id"], n.get("label", n["id"])])
    out: dict[str, list[tuple[int, int, str, str]]] = {}
    for f, spans in by_file.items():
        spans.sort(key=lambda s: s[0])
        for i, s in enumerate(spans):
            if s[1] is None:
                s[1] = spans[i + 1][0] - 1 if i + 1 < len(spans) else 10 ** 9
        out[f] = [tuple(s) for s in spans]
    return out


def changed_symbols(nodes: list[dict], changed: dict[str, set[int]]) -> set[str]:
    """Graph node ids whose line span intersects a changed line (or whose file changed wholesale)."""
    spans = symbol_spans(nodes)
    hit: set[str] = set()
    for f, lines in changed.items():
        file_spans = spans.get(f)
        if not file_spans:
            continue
        if WHOLE_FILE in lines:
            hit.update(s[2] for s in file_spans)
            continue
        for ln in lines:
            for start, end, nid, _label in file_spans:
                if start <= ln <= end:
                    hit.add(nid)
                    break
    return hit


def _module_fan_in(nodes: list[dict], links: list[dict], module_depth: int) -> dict[str, set[str]]:
    """module -> the set of modules that DEPEND ON it (an edge src->tgt means src depends on tgt)."""
    by_id = {n["id"]: n for n in nodes if "id" in n}

    def mod(nid: str | None) -> str | None:
        n = by_id.get(nid) if nid is not None else None
        return module_of(n.get("source_file"), module_depth) if n else None

    fan_in: dict[str, set[str]] = defaultdict(set)
    for link in links:
        s, t = mod(link.get("source")), mod(link.get("target"))
        if s and t and s != t:
            fan_in[t].add(s)
    return fan_in


def modules_of(nodes: list[dict], node_ids: set[str], module_depth: int) -> set[str]:
    by_id = {n["id"]: n for n in nodes if "id" in n}
    out: set[str] = set()
    for nid in node_ids:
        n = by_id.get(nid)
        if n and n.get("source_file"):
            out.add(module_of(n["source_file"], module_depth))
    return out


def affected_modules(nodes: list[dict], links: list[dict], changed_syms: set[str], *,
                     module_depth: int, depth: int = 1) -> set[str]:
    """Modules where the change lives, unioned with modules that depend on them (fan-in), BFS `depth`
    hops over the module dependency graph. depth=0 = only the modules that directly changed."""
    seed = modules_of(nodes, changed_syms, module_depth)
    if depth <= 0:
        return seed
    fan_in = _module_fan_in(nodes, links, module_depth)
    affected = set(seed)
    frontier = deque(seed)
    hops = {m: 0 for m in seed}
    while frontier:
        m = frontier.popleft()
        if hops[m] >= depth:
            continue
        for dependant in fan_in.get(m, ()):
            if dependant not in affected:
                affected.add(dependant)
                hops[dependant] = hops[m] + 1
                frontier.append(dependant)
    return affected


__all__ = ["WHOLE_FILE", "affected_modules", "changed_lines", "changed_symbols",
           "modules_of", "symbol_spans"]
