"""Claims: the atomic, evidence-anchored form of wiki knowledge.

A claim is a single falsifiable statement about the code, anchored to its evidence with a
content hash of the cited lines. That anchor buys the core property of Isidore v2:
**claim-level staleness detection with zero LLM calls** — when code changes, the hash of the
cited window changes, and exactly the affected claims (not whole pages, not the whole wiki)
are flagged stale. `isidore claims --check` turns this into a CI gate for documentation.

Claims ride the SAME generation call as the page (a second fenced block), so their marginal
cost is a few output tokens. Like findings, they are quarantined mechanically: a claim citing
a path that does not exist in the repo is dropped before it is ever stored.

Hash design: sha256 over the cited line ±2 lines, whitespace-normalized, truncated to 12 hex.
A trivial reformat of the evidence window therefore re-flags the claim — deliberately: a cheap
false-stale beats a silent true-stale. Evidence without a line number hashes the whole file.
"""
from __future__ import annotations

import hashlib
import re
from pathlib import Path

from .toon import encode

CLAIMS_FILENAME = "claims.toon"
SEARCH_RADIUS = 40      # how far from the recorded line to look for the shifted cited content

CLAIMS_PROMPT_ADDENDUM = """
Also append a fenced block distilling the page's key FACTUAL assertions as verifiable claims:

```isidore-claims
<single falsifiable statement about the code> | path:line
```

HARD rules for the `path:line` — a claim is WORTHLESS if its citation is invented:
- Copy the path VERBATIM from the FACTS. The exact strings you may cite appear as
  `--- excerpt <path>:<line> ---` headers and in the file/symbol lists above. Do NOT shorten,
  guess, pluralize, or reconstruct a path (e.g. never turn `src/pkg/x.py` into `pkg/x.py`).
- The `line` MUST be a line number that actually appears inside one of those excerpts, and the
  statement must be verifiable from THAT line's code — anchor each claim on the single most
  specific line of evidence.
- If you cannot point to an exact `path:line` from the FACTS that proves the statement, DROP the
  claim. Fewer, exactly-cited claims are far better than many with invented citations.
Other rules: 3-8 claims; each is one specific checkable fact (behavior, constraint, relationship),
never an opinion or a summary.
"""

_FENCE = re.compile(r"```isidore-claims\s*\n(.*?)```", re.DOTALL)


def parse_claims_block(markdown: str) -> tuple[str, list[dict]]:
    """Split a generated page into (clean page, raw claim rows). Tolerant of malformed lines."""
    rows: list[dict] = []

    def _consume(match: re.Match) -> str:
        for raw in match.group(1).splitlines():
            parts = [p.strip() for p in raw.rsplit("|", 1)]
            if len(parts) != 2 or not parts[0] or not parts[1]:
                continue
            rows.append({"statement": parts[0], "evidence": parts[1]})
        return ""

    clean = _FENCE.sub(_consume, markdown).rstrip() + "\n"
    return clean, rows


def _split_evidence(evidence: str) -> tuple[str, int | None]:
    path_part, sep, line_part = evidence.replace("\\", "/").rpartition(":")
    if sep and line_part.lstrip("L").isdigit():
        return path_part.strip(), int(line_part.lstrip("L"))
    return evidence.replace("\\", "/").strip(), None


def _normalize(text: str) -> str:
    """Collapse all whitespace runs to single spaces and trim — so re-indentation, trailing, and
    internal whitespace churn never change the fingerprint. Only the token sequence matters."""
    return " ".join(text.split())


def _hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:12]


def _read_lines(repo: Path, rel: str) -> list[str] | None:
    path = repo / rel
    if not rel or not path.is_file():
        return None
    try:
        return path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return None


def evidence_hash(repo: Path, evidence: str) -> str | None:
    """Fingerprint of the CITED LINE's normalized content (whole normalized file if no line).

    Anchoring on the cited line's CONTENT — not a line-number window — is what makes the gate
    production-grade: inserting or deleting lines ABOVE a claim shifts its line number but not its
    content, so `evidence_state` finds it nearby and does NOT cry wolf. Only a real change to the
    cited line itself flips the fingerprint. Returns None if the path is gone (orphan).
    """
    rel, line = _split_evidence(evidence)
    lines = _read_lines(repo, rel)
    if lines is None:
        return None
    if line is None:
        return _hash("\n".join(n for n in (_normalize(ln) for ln in lines) if n))
    if not (1 <= line <= len(lines)):
        return None
    return _hash(_normalize(lines[line - 1]))


def evidence_state(repo: Path, evidence: str, stored_hash: str) -> str:
    """"ok" | "stale" | "orphan" — content-anchored, tolerant of line shifts.

    ok     the cited line's fingerprint is found at or near its recorded line (maybe shifted);
    stale  the path exists but the cited content changed / is no longer near the recorded line;
    orphan the evidence path is gone.
    """
    rel, line = _split_evidence(evidence)
    lines = _read_lines(repo, rel)
    if lines is None:
        return "orphan"
    if line is None:
        current = _hash("\n".join(n for n in (_normalize(ln) for ln in lines) if n))
        return "ok" if current == stored_hash else "stale"
    # search outward from the recorded line for a line matching the stored fingerprint
    for offset in range(0, SEARCH_RADIUS + 1):
        for idx in {line - 1 - offset, line - 1 + offset}:
            if 0 <= idx < len(lines) and _hash(_normalize(lines[idx])) == stored_hash:
                return "ok"
    return "stale"


def claim_id(statement: str, evidence: str) -> str:
    """Deterministic, ledger-friendly id: stable across runs for the same (statement, evidence)."""
    return "c-" + hashlib.sha256(f"{statement}\x00{evidence}".encode("utf-8")).hexdigest()[:8]


def anchor_claims(repo: Path, raw_claims: list[dict]) -> tuple[list[dict], int]:
    """Quarantine filter + anchoring. Returns (anchored claims, dropped count).

    A claim whose evidence path does not exist is dropped BEFORE storage — same mechanical
    hallucination filter as findings.
    """
    anchored: list[dict] = []
    dropped = 0
    for c in raw_claims:
        ehash = evidence_hash(repo, c["evidence"])
        if ehash is None:
            dropped += 1
            continue
        anchored.append({"id": claim_id(c["statement"], c["evidence"]),
                         "statement": c["statement"], "evidence": c["evidence"], "ehash": ehash})
    return anchored, dropped


def check_claims(repo: Path, pages_state: dict) -> list[dict]:
    """Re-hash every stored claim's evidence — the zero-LLM staleness audit.

    Returns rows {page, id, statement, evidence, state} with state ok | stale | orphan.
    """
    rows: list[dict] = []
    for page, entry in sorted(pages_state.items()):
        for c in entry.get("claims", []):
            state = evidence_state(repo, c["evidence"], c["ehash"])
            rows.append({"page": page, "id": c["id"], "statement": c["statement"],
                         "evidence": c["evidence"], "state": state})
    return rows


def stale_pages(repo: Path, pages_state: dict) -> set[str]:
    """Pages owning at least one stale/orphan claim — they must regenerate even if their
    assembled context hash did not move (the change may sit outside the excerpt windows)."""
    return {row["page"] for row in check_claims(repo, pages_state) if row["state"] != "ok"}


def render_claims(repo: Path, pages_state: dict, commit: str | None) -> str:
    rows = check_claims(repo, pages_state)
    n_stale = sum(1 for r in rows if r["state"] != "ok")
    header = (
        f"# isidore claims · commit {commit or '?'}\n"
        "# each claim is anchored to its evidence by a content hash; state is re-checked\n"
        "# mechanically on every compile (zero LLM calls). stale/orphan => page regenerates.\n"
        f"# summary: {len(rows)} claims, {n_stale} stale/orphan\n"
    )
    return header + encode(
        ("claims", ["page", "id", "statement", "evidence", "state"], rows)) + "\n"
