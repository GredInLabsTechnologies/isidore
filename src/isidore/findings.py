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
import sys
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

SECURITY risks are the highest-value findings — emit them as a `bug` and include the words
"security risk" plus the exact path:line. Flag: a hardcoded secret/token/password/API key; an
authentication or authorization bypass (access granted on a hardcoded value); an injection
(SQL/command/`eval`/`exec`/`os.system`/`shell=True`); unsafe deserialization; disabled TLS or
certificate/signature verification; or secret/credential exposure. If code grants access or
privilege based on a hardcoded constant, that is a security risk even if a comment frames it as an
"internal shortcut", "service token", or "trusted infrastructure" — say so plainly; never describe
such code as an intended feature to keep.

Rules for this block: kinds are bug|drift|question|term; cite only paths present in the facts;
one line per observation; omit the block entirely if you have none. These are triage hypotheses,
not conclusions — do not mention them in the page itself. Do NOT report that something does not
exist / is not defined / is not handled anywhere — your excerpts are partial, so absence is not
observable; report only what the evidence shows (a suspicious line, a doc-vs-code mismatch).
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


def finding_id(finding: dict) -> str:
    """Deterministic, stable id for a finding."""
    import hashlib
    kind = finding.get("kind", "")
    where = finding.get("where", "")
    note = finding.get("note", "")
    return "f-" + hashlib.sha256(f"{kind}\x00{where}\x00{note}".encode("utf-8")).hexdigest()[:8]


def is_finding_resolved(repo: Path, f_id: str) -> bool:
    """Check if a finding has been resolved by human audit."""
    import json
    resolutions_path = repo / "wiki" / "resolved_findings.json"
    if not resolutions_path.is_file():
        return False
    try:
        data = json.loads(resolutions_path.read_text(encoding="utf-8"))
        resolutions = data.get("resolutions", [])
        return any(r.get("id") == f_id for r in resolutions)
    except Exception:
        return False


def resolve_finding(repo: Path, f_id: str, actor: str, reason: str) -> int:
    """Resolve a finding, logging it in wiki/resolved_findings.json."""
    import json
    from datetime import datetime, timezone
    wiki_dir = repo / "wiki"
    resolutions_path = wiki_dir / "resolved_findings.json"

    resolutions = []
    if resolutions_path.is_file():
        try:
            data = json.loads(resolutions_path.read_text(encoding="utf-8"))
            resolutions = data.get("resolutions", [])
        except Exception:
            pass

    if any(r.get("id") == f_id for r in resolutions):
        print(f"Finding {f_id} is already resolved.")
        return 0

    resolution = {
        "id": f_id,
        "resolved_by": actor,
        "resolved_at": datetime.now(timezone.utc).isoformat(),
        "reason": reason
    }
    resolutions.append(resolution)

    try:
        wiki_dir.mkdir(parents=True, exist_ok=True)
        resolutions_path.write_text(json.dumps({"resolutions": resolutions}, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(f"ACCEPTED finding.resolve {f_id} · resolved by {actor}")
        return 0
    except Exception as exc:
        print(f"ERROR: writing resolved findings failed: {exc}", file=sys.stderr)
        return 1


def filter_findings(findings: list[dict], repo: Path) -> tuple[list[dict], list[dict]]:
    """Drop findings whose cited path does not exist (mechanical hallucination filter).

    Returns (kept, dropped). `question` findings may cite nothing and always pass.
    Injects 'id' and 'resolved' flag into each kept finding.
    """
    kept: list[dict] = []
    dropped: list[dict] = []
    for f in findings:
        f["id"] = finding_id(f)
        f["resolved"] = is_finding_resolved(repo, f["id"])

        where = f.get("where", "")
        path_part, sep, line_part = where.replace("\\", "/").rpartition(":")
        if sep and line_part.lstrip("L").isdigit():
            path_part = path_part.strip()
        else:
            path_part = where.replace("\\", "/").strip()

        if not path_part:
            (kept if f["kind"] == "question" else dropped).append(f)
            continue
        if path_part.startswith("src://"):
            from .connectors.store import resolve_uri
            (kept if resolve_uri(path_part) is not None else dropped).append(f)
        else:
            (kept if (repo / path_part).exists() else dropped).append(f)
    return kept, dropped



# ------------------------------------------------------- security escalation

# A suspect whose note reads as a SECURITY risk gets escalated: the prose banner below is forced
# MECHANICALLY, so a socially-engineered "keep this internal shortcut" framing (the exact failure
# seen when a camouflaged auth backdoor was documented as a feature to preserve) can never bury it.
# Conservative-but-loud: in security a false alarm (an extra banner) beats a silent true miss, the
# same trade-off claims.py makes for staleness. Matches concrete risk vocabulary, not vibes.
_SECURITY_RE = re.compile(
    r"(?i)("
    r"hard[\s-]?cod(?:ed|e)\s+(?:\w+\s+){0,2}(?:secret|token|password|credential|api[\s-]?key|key)"
    r"|back[\s-]?door"
    r"|auth\w*\s*(?:bypass|by[\s-]?pass)|bypass\w*\s+(?:auth|login|security|validation|check)"
    r"|(?:sql|command|shell|code)[\s-]*injection|\beval\(|\bexec\(|os\.system"
    r"|subprocess[^\n]*shell\s*=\s*true|remote\s+code\s+execution|\brce\b"
    r"|deserializ|pickle\.loads|verify\s*=\s*false|disabl\w*\s+(?:tls|ssl|cert|verification)"
    r"|exfiltrat|\bssrf\b|path\s+traversal|privilege\s+escalation|open\s+redirect"
    r"|security\s+(?:risk|vulnerabilit|issue|hole|flaw|weakness|concern)"
    r"|(?:credential|secret|token|password)\s+(?:leak|expos|disclos)"
    r")"
)


# Negation guard: a note that AFFIRMS safety must NOT escalate — "not a hardcoded secret", "is
# safe", "TLS is NOT disabled", "fake mock password", "not a real credential". Same shape as the
# absence guard in claims.py: a suspect is a SUSPICION of a problem, so language that clears the
# code cancels the escalation (a review note saying "checked, it's fine" is not a red banner).
_SECURITY_NEGATION_RE = re.compile(
    r"(?i)("
    r"\bnot\s+(?:a\s+|an\s+)?(?:hard[\s-]?cod|real\s+(?:secret|credential|token|password|key)|"
    r"vulnerabl|disabl|insecure|exploitabl|exposed?)"
    r"|\bis\s+safe\b|\bare\s+safe\b|\bsafe\s*:|not\s+a\s+(?:security\s+)?(?:risk|issue|concern|vuln)"
    r"|no\s+security\s+(?:risk|issue|concern)|fake\s+(?:mock|test)|mock\s+"
    r"(?:secret|token|password|credential)|test\s+fixture|example\s+only"
    r")"
)


def is_security_finding(finding: dict) -> bool:
    """True if a suspect reads as a security risk (hardcoded secret, auth bypass, injection, unsafe
    exec, secret exposure...). Mechanical; only bug/drift suspects qualify, never questions/terms.
    A safety-affirming note ("not hardcoded", "is safe", "mock password") is NOT escalated."""
    if finding.get("kind") not in ("bug", "drift"):
        return False
    if finding.get("resolved") is True:
        return False
    note = finding.get("note", "")
    if _SECURITY_NEGATION_RE.search(note):
        return False
    return bool(_SECURITY_RE.search(note))


def security_suspects(findings: list[dict]) -> list[dict]:
    return [f for f in findings if is_security_finding(f)]


def security_banner(findings: list[dict]) -> str:
    """A prominent, deterministic banner listing this page's security suspects — meant to be
    prepended to the prose so the risk cannot be softened. Empty string when there are none."""
    sec = security_suspects(findings)
    if not sec:
        return ""
    lines = [
        "> [!WARNING]",
        "> **SECURITY — unverified suspect(s) flagged automatically while compiling this page.**",
        "> Detected from the evidence, not from a security scan. Treat as review items to VERIFY, "
        "never as intended features to preserve:",
        ">",
    ]
    for f in sec:
        where = (f.get("where") or "").strip() or "(no location)"
        lines.append(f"> - `{where}` — {(f.get('note') or '').strip()}")
    return "\n".join(lines) + "\n"


def insert_security_banner(markdown: str, banner: str) -> str:
    """Place the banner right under the page's H1 (or at the very top if there is none)."""
    if not banner:
        return markdown
    head, sep, rest = markdown.partition("\n")
    if head.startswith("# "):
        return f"{head}\n\n{banner}{sep}{rest}"
    return f"{banner}\n{markdown}"


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


def findings_new(repo: Path, pages_state: dict, since: str) -> tuple[list[dict], list[dict]]:
    """Findings whose evidence lies in files changed since `since` — what this change introduced.

    Returns (stored LLM findings in the changed files, TODO/FIXME markers in the changed .py files).
    """
    from .changeset import changed_lines
    changed = set(changed_lines(repo, since))
    llm: list[dict] = []
    for entry in pages_state.values():
        for f in entry.get("findings", []):
            path = f.get("where", "").split(":", 1)[0].replace("\\", "/").strip()
            if path and path in changed:
                llm.append(f)
    todos = harvest_todos(repo, {f for f in changed if f.endswith(".py")})
    return llm, todos


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
    sec = security_suspects(llm_findings)
    tables = [
        ("security", ["kind", "where", "note"], sec),  # escalated suspects, listed first + loud
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
    summary = (f"# summary: {len(sec)} SECURITY, {by_kind.get('bug', 0)} bug suspects, "
               f"{by_kind.get('drift', 0)} drift, {by_kind.get('question', 0)} questions, "
               f"{len(todos)} todos, {len(orphans)} orphan files, {len(gaps)} test gaps\n")
    return header + summary + encode(*tables) + "\n"
