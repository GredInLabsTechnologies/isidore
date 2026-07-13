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
Also append a fenced block distilling the page's key FACTUAL assertions as verifiable claims. Each
claim is `<statement> | <path:line>` and SHOULD carry a third field — a MACHINE-CHECKABLE predicate —
whenever the fact is exactly one of the decidable forms below. That predicate is verified against the
code with ZERO extra LLM calls, turning the claim from merely "cited" into "PROVEN". Give as many
claims a predicate as you honestly can.

```isidore-claims
<statement> | path:line | <predicate>
```

Predicate grammar (third field) — `<kind>:<arg1>;<arg2>` (separate args with SEMICOLONS, never commas):
- calls:CALLER;CALLEE   — CALLER's body calls CALLEE            e.g. calls:authenticate;verify_jwt
- defines:FILE;SYMBOL   — FILE defines a top-level SYMBOL        e.g. defines:src/auth.py;authenticate
- imports:FILE;TARGET   — FILE imports TARGET module/file        e.g. imports:src/auth.py;src/tokens.py
- value:NAME;LITERAL    — module-level NAME equals LITERAL        e.g. value:MAX_ATTEMPTS;5
- signature:FN;A1;A2    — FN's parameter names, in order          e.g. signature:authenticate;request
- env:NAME              — the env var NAME is read somewhere      e.g. env:AUTH_SIGNING_KEY

Predicate rules:
- Add it ONLY when the statement IS exactly that fact, and copy the args verbatim from the FACTS
  (function/const/file names as the code spells them; for `calls`, the callee is the called name,
  e.g. the last part of a dotted call). A WRONG predicate is verified FALSE — worse than none.
- If no form fits, OMIT the third field: a two-field claim is still valid (it stays "cited", not
  "proven"). Never invent a predicate just to fill the field.

Common mistakes that get a predicate REFUTED — do NOT make these:
- `env:` is ONLY for real environment variables read via os.environ/os.getenv/process.env. NEVER
  use it for a function, class, constant, or registry name (e.g. `env:scan_repo` is wrong — scan_repo
  is a function, not an env var).
- `value:` needs the EXACT literal as written in the code. Copy it character-for-character. If the
  value is anything but a plain literal (a call like `Path(...)`, an expression, another name), do
  NOT use `value:` at all. Never guess the number/string.
- `defines:` is for a symbol DECLARED in that file. A symbol the file IMPORTS is not defined there.
- `calls:CALLER;CALLEE` only if CALLEE literally appears called inside CALLER's body.

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
- Assert only what the evidence SHOWS. NEVER claim that something does not exist, is not defined,
  or is not handled anywhere — your excerpts are partial, so absence is unprovable and such claims
  are dropped mechanically before they are stored.
"""

_FENCE = re.compile(r"```isidore-claims\s*\n(.*?)```", re.DOTALL)

# Absence-hallucination backstop. A claim/finding asserting that something does NOT exist / is not
# defined / is not handled cannot be evidence-anchored: its "evidence" would be the ABSENCE of code,
# and the excerpts a page sees are partial by construction (report from claude-gimo, 2026-07-07: two
# false positives from absence-in-excerpt). Such statements are dropped mechanically. Deliberately
# CONSERVATIVE — it fires only on existential/definitional absence, never on property or behavioral
# negations about evidenced code ("X is not thread-safe", "the lock is not released on error").
_NEG_EXISTENTIAL = re.compile(
    r"(?i)("
    r"\bthere\s+(?:is|are)\s+no\b"
    r"|\bno\s+\w[\w./-]*(?:\s+\w+){0,3}?\s+(?:exists?|is\s+defined|are\s+defined|is\s+present|"
    r"is\s+used|is\s+handled|is\s+configured|is\s+implemented)"
    r"|\b(?:is|are)\s+(?:not|never)\s+(?:defined|declared|implemented|configured|present|"
    r"registered|initialized|instantiated|imported|exported|handled|referenced|found|set\s+up)\b"
    r"|\b(?:does\s+not|doesn't|do\s+not|don't)\s+(?:exist|define|declare|implement|configure|"
    r"register|import|handle|reference)\b"
    r"|\bis\s+missing\b|\bare\s+missing\b|\bis\s+absent\b|\bare\s+absent\b"
    r"|\bno\s+longer\s+exists?\b|\bnot\s+implemented\b|\bnonexistent\b"
    r")"
)


def is_negative_existential(statement: str) -> bool:
    """True for statements asserting existential/definitional ABSENCE (unanchorable). Conservative:
    behavioral negations ('not released', 'not called', 'not thread-safe') are NOT flagged."""
    return bool(_NEG_EXISTENTIAL.search(statement or ""))


def parse_predicate_field(raw: str | None):
    """Parse a claim's optional third field into a pcp.Predicate (or None). PCP typed-claim grammar."""
    from .pcp import parse_predicate
    return parse_predicate(raw)


def parse_claims_block(markdown: str) -> tuple[str, list[dict]]:
    """Split a generated page into (clean page, raw claim rows). Tolerant of malformed lines.

    Claim line grammar: `<statement> | <path:line>` with an OPTIONAL PCP third field
    `| <kind>:<arg;arg>` (see pcp.parse_predicate). Two-field claims stay valid (backwards
    compatible): the predicate is simply absent and the claim is existence-anchored only.
    """
    rows: list[dict] = []

    def _consume(match: re.Match) -> str:
        for raw in match.group(1).splitlines():
            parts = [p.strip() for p in raw.split("|")]
            if len(parts) < 2 or not parts[0] or not parts[1]:
                continue
            row = {"statement": parts[0], "evidence": parts[1]}
            if len(parts) >= 3 and parts[2]:
                row["predicate"] = parts[2]
            rows.append(row)
        return ""

    clean = _FENCE.sub(_consume, markdown).rstrip() + "\n"
    return clean, rows


def _split_evidence(evidence: str) -> tuple[str, int | None]:
    if evidence.startswith("src://"):
        path_part, sep, line_part = evidence.rpartition(":")
        if sep and line_part.lstrip("L").isdigit():
            return path_part.strip(), int(line_part.lstrip("L"))
        return evidence.strip(), None
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
    if evidence.startswith("src://"):
        from .connectors.store import resolve_uri
        uri, line = _split_evidence(evidence)
        item = resolve_uri(uri)
        if item is None:
            return None
        if line is None:
            return item.get("chash")
        content = item.get("content", "")
        lines = content.splitlines()
        if not (1 <= line <= len(lines)):
            return None
        return _hash(_normalize(lines[line - 1]))

    rel, line = _split_evidence(evidence)
    lines = _read_lines(repo, rel)
    if lines is None:
        return None
    if line is None:
        return _hash("\n".join(n for n in (_normalize(ln) for ln in lines) if n))
    if not (1 <= line <= len(lines)):
        return None
    return _hash(_normalize(lines[line - 1]))


def evidence_state(repo: Path, evidence: str, stored_hash: str, compiled_at: str | None = None) -> str:
    """"ok" | "stale" | "orphan" | "superseded" — content-anchored, tolerant of line shifts.

    ok         the cited line's fingerprint is found at or near its recorded line (maybe shifted);
    stale      the path exists but the cited content changed / is no longer near the recorded line;
    orphan     the evidence path is gone;
    superseded the stream has items newer than the compiled_at watermark.
    """
    if evidence.startswith("src://"):
        from .connectors.store import resolve_uri, iter_items
        uri, line = _split_evidence(evidence)
        item = resolve_uri(uri)
        if item is None:
            return "orphan"

        parts = uri[len("src://"):].split("/")
        if len(parts) == 2:
            cid, instance = parts[0], None
        elif len(parts) == 3:
            cid, instance = parts[0], parts[1]
        else:
            return "orphan"

        stream = item.get("stream")
        if compiled_at:
            for other in iter_items(cid, instance, stream):
                other_ts = other.get("ts", "")
                if other_ts > compiled_at:
                    return "superseded"

        if line is None:
            current = item.get("chash")
            return "ok" if current == stored_hash else "stale"

        content = item.get("content", "")
        lines = content.splitlines()
        for offset in range(0, SEARCH_RADIUS + 1):
            for idx in {line - 1 - offset, line - 1 + offset}:
                if 0 <= idx < len(lines) and _hash(_normalize(lines[idx])) == stored_hash:
                    return "ok"
        return "stale"

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


def resolve_citation(cited_path: str, known_files: set[str] | None) -> str | None:
    """Repair a shortened citation to a real file, or None if it can't be resolved uniquely.

    Models (especially on TS/JS) drop the module prefix — citing `src/App.tsx` for the real
    `apps/web/src/App.tsx`. Rather than quarantine those valid claims, resolve the cited path as a
    UNIQUE suffix of a known file. Ambiguous (>1 match) or unknown → None (still quarantined). This
    recovers coverage on polyglot repos without ever accepting a guess.
    """
    if not known_files:
        return None
    norm = cited_path.replace("\\", "/").lstrip("./").lstrip("/")
    if not norm:
        return None
    matches = [f for f in known_files if f == norm or f.replace("\\", "/").endswith("/" + norm)]
    return matches[0] if len(matches) == 1 else None


def anchor_claims(repo: Path, raw_claims: list[dict],
                  known_files: set[str] | None = None) -> tuple[list[dict], int, int]:
    """Quarantine filter + anchoring. Returns (anchored claims, dropped, repaired).

    A claim whose evidence path does not exist is first RESOLVED against known files (a shortened
    path is repaired to its unique real match); only if it still can't be found is it dropped.
    """
    anchored: list[dict] = []
    dropped = repaired = 0
    for c in raw_claims:
        evidence = c["evidence"]
        ehash = evidence_hash(repo, evidence)
        if ehash is None:
            path_part, _sep, line_part = evidence.replace("\\", "/").rpartition(":")
            resolved = resolve_citation(path_part or evidence, known_files)
            if resolved is not None:
                evidence = f"{resolved}:{line_part}" if _sep else resolved
                ehash = evidence_hash(repo, evidence)
                if ehash is not None:
                    repaired += 1
            if ehash is None:
                dropped += 1
                continue
        anchored.append({"id": claim_id(c["statement"], evidence),
                         "statement": c["statement"], "evidence": evidence, "ehash": ehash,
                         "predicate": c.get("predicate", "")})
    return anchored, dropped, repaired


def check_claims(repo: Path, pages_state: dict) -> list[dict]:
    """Re-hash every stored claim's evidence — the zero-LLM staleness audit.

    Returns rows {page, id, statement, evidence, state} with state ok | stale | orphan.
    """
    rows: list[dict] = []
    for page, entry in sorted(pages_state.items()):
        compiled_at = entry.get("compiled_at")
        for c in entry.get("claims", []):
            state = evidence_state(repo, c["evidence"], c["ehash"], compiled_at)
            rows.append({"page": page, "id": c["id"], "statement": c["statement"],
                         "evidence": c["evidence"], "state": state})
    return rows


def claims_for_file(repo: Path, pages_state: dict, path: str) -> list[dict]:
    """The documentation contract of a file: every anchored claim whose evidence points at it. Agent
    pre-flight — 'before editing X, these wiki assertions depend on X (recompile its pages after)'."""
    norm = path.replace("\\", "/").lstrip("./").lstrip("/")
    rows = []
    for r in check_claims(repo, pages_state):
        ev, _ = _split_evidence(r["evidence"])
        ev = ev.replace("\\", "/")
        if ev == norm or ev.endswith("/" + norm) or norm.endswith("/" + ev):
            rows.append(r)
    return rows


def claims_grep(repo: Path, pages_state: dict, term: str) -> list[dict]:
    """Free-text search over verified atomic facts — answers many questions with 0 LLM calls."""
    needle = term.lower()
    return [r for r in check_claims(repo, pages_state)
            if needle in r["statement"].lower() or needle in r["evidence"].lower()]


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
