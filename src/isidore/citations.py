"""Prose citations that follow the code they cite.

A page cites code as `path:line` (or `path:a-Lb`). Claims were already anchored by the CONTENT of the
cited line, so a claim survives lines shifting above it; the prose around them was not. Once an
incremental compile stopped rewriting pages whose facts had not changed, a kept section's citations
drifted a few lines with every edit above them — measured on isidore's own wiki right after that
change: `prompt_id` cited at handoff.py:58 while defined at :54, `assert_may_send_source` cited at
pipeline.py:193 while defined at :195.

So a citation is anchored the same way a claim is, and re-pointed at 0 LLM:

- `anchors_for` fingerprints each cited line together with the next non-empty lines (one line alone —
  `return result`, a closing bracket — matches too many places to relocate safely). Lines too short
  to identify are not tracked.
- `repoint` finds each fingerprint again, nearest to where it was, and rewrites the line number;
  a range keeps its length. A citation whose content really changed is left as written and reported
  stale — the page's facts moved too, so an incremental revision is due anyway.
- `migrate_by_symbol` handles pages written before anchors existed, conservatively: only a citation
  written right after the symbol it names (`` `prompt_id` (`handoff.py:58`) ``), whose line no longer
  holds that symbol while exactly one nearby line defines it, is moved. Anything it cannot validate
  it leaves alone.

Code blocks are never touched: a path inside a fence is an example, not a citation.
"""
from __future__ import annotations

import re
from pathlib import Path

from .claims import _hash, _normalize, _read_lines

CITE = re.compile(r"(?<![\w/.-])(?P<path>[\w][\w./-]*\.[A-Za-z0-9]+):(?P<a>\d+)"
                  r"(?:-(?P<L>L?)(?P<b>\d+))?(?!\d)")
_FENCE = re.compile(r"```.*?```", re.S)
_IDENT = re.compile(r"`(?P<name>[A-Za-z_][A-Za-z0-9_]*)(?:\([^`\n]*\))?`")
_CLAUSE_BREAK = re.compile(r"\n\s*\n|\n\s*[-*]\s|\n\s*\d+\.\s|[.;:]\s")
RADIUS = 400            # lines searched either side; nearest match wins
_CONTEXT = 3            # non-empty lines in one fingerprint
_MIN_CHARS = 3          # a line shorter than this (blank, `)`, `}`) identifies nothing
_ADJACENT = 40          # chars between a named symbol and its citation for the pair to count
_SYMBOL_REACH = 20      # how far a migrated definition may have moved
_NEAR_REACH = 5         # ...when the symbol is named further back in the clause, not right before


def _fingerprint(lines: list[str], n: int) -> str | None:
    idx = n - 1
    if not 0 <= idx < len(lines):
        return None
    first = _normalize(lines[idx])
    if len(first) < _MIN_CHARS:
        return None
    parts, j = [first], idx + 1
    while len(parts) < _CONTEXT and j < len(lines):
        text = _normalize(lines[j])
        if text:
            parts.append(text)
        j += 1
    # "<window>:<line>" — the window locates the line among look-alikes; the line alone is the
    # fallback when the lines BELOW it changed but it did not (a def whose docstring was edited).
    return f"{_hash(chr(10).join(parts))}:{_hash(first)}"


def _window(anchor: str) -> str:
    return anchor.split(":", 1)[0]


def _relocate(lines: list[str], a: int, want: str) -> int | None:
    """Where the anchored line is now: its window, nearest first; failing that, the line itself if it
    occurs exactly once in the file. Anything less certain is not a relocation."""
    window = _window(want)
    found = next((a + d for k in range(1, RADIUS + 1) for d in (-k, k)
                  if (fp := _fingerprint(lines, a + d)) and _window(fp) == window), None)
    if found is not None or ":" not in want:
        return found
    line = want.split(":", 1)[1]
    same = [i + 1 for i, text in enumerate(lines)
            if len(_normalize(text)) >= _MIN_CHARS and _hash(_normalize(text)) == line]
    return same[0] if len(same) == 1 else None


def _matches(markdown: str):
    """Citations outside code fences, in order."""
    fences = [m.span() for m in _FENCE.finditer(markdown)]
    for m in CITE.finditer(markdown):
        if not any(a <= m.start() < b for a, b in fences):
            yield m


def _render(m: re.Match, a: int, b: int | None) -> str:
    return f"{m['path']}:{a}" + (f"-{m['L']}{b}" if b is not None else "")


def _rewrite(markdown: str, edits: list[tuple[re.Match, str]]) -> str:
    for m, text in sorted(edits, key=lambda e: e[0].start(), reverse=True):
        markdown = markdown[:m.start()] + text + markdown[m.end():]
    return markdown


class _Files:
    def __init__(self, repo: Path):
        self.repo, self._cache = repo, {}

    def lines(self, rel: str) -> list[str] | None:
        if rel not in self._cache:
            self._cache[rel] = _read_lines(self.repo, rel)
        return self._cache[rel]


# Recorded for a citation whose line identifies nothing (blank, a lone bracket): it is remembered as
# unanchorable, so it is never adopted later by whatever content an edit slides onto that line —
# found in a live round trip on isidore's own wiki, where a citation of a blank line got anchored to
# the code that moved under it and then travelled with that code.
UNANCHORED = ""


def anchors_for(repo: Path, markdown: str) -> dict[str, str]:
    """`path:line` -> fingerprint for every citation of an existing file (UNANCHORED when its line
    identifies nothing)."""
    files, out = _Files(repo), {}
    for m in _matches(markdown):
        lines = files.lines(m["path"])
        if lines is not None:
            out[f"{m['path']}:{m['a']}"] = _fingerprint(lines, int(m["a"])) or UNANCHORED
    return out


def repoint(repo: Path, markdown: str, anchors: dict[str, str]
            ) -> tuple[str, dict[str, str], int, list[str]]:
    """(page, anchors, citations moved, stale citations). Citations with no anchor yet are anchored
    where they stand; the rest follow their fingerprint."""
    files, new_anchors, edits, stale = _Files(repo), {}, [], []
    for m in _matches(markdown):
        lines = files.lines(m["path"])
        if lines is None:
            continue
        a, b = int(m["a"]), (int(m["b"]) if m["b"] else None)
        key = f"{m['path']}:{a}"
        want = anchors.get(key)
        if want is None:                        # a citation not seen before: anchor it where it stands
            new_anchors[key] = _fingerprint(lines, a) or UNANCHORED
            continue
        if want == UNANCHORED:                  # nothing to follow; never adopt what lands here later
            new_anchors[key] = UNANCHORED
            continue
        here = _fingerprint(lines, a)
        if here and _window(here) == _window(want):
            new_anchors[key] = here              # (also upgrades an anchor in an older format)
            continue
        found = _relocate(lines, a, want)
        if found is None:
            stale.append(key)
            new_anchors[key] = want          # keep reporting it until the section is revised
            continue
        if found == a:                       # the line itself stayed; only what follows it changed
            new_anchors[key] = here or want
            continue
        edits.append((m, _render(m, found, None if b is None else b + (found - a))))
        new_anchors[f"{m['path']}:{found}"] = _fingerprint(lines, found) or want
    return _rewrite(markdown, edits), new_anchors, len(edits), sorted(set(stale))


_DEF_LINE = re.compile(r"^\s*(?:async\s+def|def|class)\s+\w")


def _inside_block(lines: list[str], start: int, n: int) -> bool:
    """Is line `n` in the indented body of the definition on line `start`?"""
    if not 0 < start < n <= len(lines):
        return False
    indent = len(lines[start - 1]) - len(lines[start - 1].lstrip())
    for i in range(start, n):
        text = lines[i]
        if text.strip() and len(text) - len(text.lstrip()) <= indent:
            return False
    return True


def _definition_lines(lines: list[str], name: str) -> list[int]:
    pat = re.compile(rf"^\s*(?:async\s+def|def|class)\s+{re.escape(name)}\b"
                     rf"|^\s*{re.escape(name)}\s*(?::[^=]*)?=(?!=)")
    return [i + 1 for i, text in enumerate(lines) if pat.search(text)]


def migrate_by_symbol(repo: Path, markdown: str) -> tuple[str, int]:
    """Re-point legacy citations that name their symbol and no longer land on it. Conservative by
    construction: moved only when the pairing is adjacent, the cited line lacks the symbol, and one
    definition of it sits within reach. Returns (page, citations moved)."""
    files, edits = _Files(repo), []
    for m in _matches(markdown):
        lines = files.lines(m["path"])
        if lines is None:
            continue
        a, b = int(m["a"]), (int(m["b"]) if m["b"] else None)
        if not 0 < a <= len(lines):
            continue
        before = markdown[max(0, m.start() - 200):m.start()]
        # A citation landing on a blank line (or a lone bracket) is off for certain — nobody cites
        # one — so its symbol may be looked for anywhere in the same bullet or sentence, within the
        # full reach. A symbol right before the citation gets the same reach. One further back in the
        # clause only pairs with a definition a few lines away: the shifts real edits leave are small
        # (+1, +2, +3, +5 on isidore's own wiki), the false pairings were all far.
        blank = len(_normalize(lines[a - 1])) < _MIN_CHARS
        clause = before[max((x.end() for x in _CLAUSE_BREAK.finditer(before)), default=0):]
        named = list(_IDENT.finditer(clause))
        if not named:
            continue
        adjacent = len(clause) - named[-1].end() <= _ADJACENT
        reach = _SYMBOL_REACH if blank or adjacent else _NEAR_REACH
        name = named[-1]["name"]
        cited = "\n".join(lines[a - 1:(b or a)])
        # Every way a citation that LOOKS off is in fact deliberate — each one a real miss of a first
        # version of this rule on isidore's own wiki (9 of 14 moves would have broken a good citation):
        sentence = markdown[max(0, m.start() - 200):m.end() + 120]
        mentioned = {i["name"] for i in _IDENT.finditer(sentence)}
        if any(re.search(rf"\b{re.escape(n)}\b", cited) for n in mentioned):
            continue                            # the line holds this or another symbol it names
        if _DEF_LINE.search(lines[a - 1]):
            continue                            # it cites some other definition on purpose
        hits = [n for n in _definition_lines(lines, name) if abs(n - a) <= reach]
        if len(hits) != 1 or (not blank and _inside_block(lines, hits[0], a)):
            continue                            # ambiguous, or a line inside the symbol's own body
        found = hits[0]
        edits.append((m, _render(m, found, None if b is None else b + (found - a))))
    return _rewrite(markdown, edits), len(edits)


def reprose_certificate(cert_path: Path, markdown: str) -> None:
    """After citations moved, the page's certificate must describe the new bytes: same claims, same
    verdicts, the prose hash and verified mass recomputed. Nothing else changed, and nothing else is
    touched. A page without a certificate is left without one."""
    if not cert_path.is_file():
        return
    from .claims import parse_claims_block
    from .pcp import prose_hash, read_certificate, write_certificate
    from .verify import classify_mass
    cert = read_certificate(cert_path)
    clean, _rows = parse_claims_block(markdown)
    cert.prose_sha256 = prose_hash(clean)
    cert.mass = classify_mass(clean, cert.claims)
    write_certificate(cert, cert_path)
