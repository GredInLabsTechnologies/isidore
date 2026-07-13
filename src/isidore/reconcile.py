"""Lane B (part 1) — the reconciler: the model's own outputs cross-checked, 0 LLM. (T-8dfc)

Implement the three checks (prose-omits-finding, prose-contradicts-finding, mark-uncovered)
to detect internal contradictions. Pure, 0-LLM.
"""
from __future__ import annotations

import re
from .pcp import Mark, Violation


def _split_evidence(evidence: str) -> tuple[str, int | None]:
    """Helper to split file:line into (file, line)."""
    if not evidence:
        return "", None
    evidence = evidence.replace("\\", "/").strip()
    path_part, sep, line_part = evidence.rpartition(":")
    if sep and line_part.lstrip("L").isdigit():
        return path_part.strip(), int(line_part.lstrip("L"))
    return evidence, None


# Regex for statements describing a region in positive/secure/intended terms
_POSITIVE_RE = re.compile(
    r"(?i)\b(safe|secure|correct|valid|intended|proper|authorized|verifies|authenticates|legitimate|intentional|keeps?|conserves?)\b"
)


def reconcile(prose: str, findings: list[dict], claims: list[dict],
              marks: list[Mark] | None = None) -> list[Violation]:
    """Cross-check prose vs findings vs claims vs marks -> internal contradictions. Pure, 0-LLM.

    Checks:
    1. prose-omits-finding: finding bug/drift whose file is not mentioned in the prose.
    2. prose-contradicts-finding: finding bug/drift in a region described in positive terms
       by a claim or denied by the prose.
    3. mark-uncovered: danger/warn marks without covering claims.
    """
    violations: list[Violation] = []
    prose_norm = prose.replace("\\", "/")
    prose_lower = prose.lower()
    marks = marks or []

    # 1 & 2: Check findings
    for f in findings:
        if f.get("resolved") is True:
            continue
        kind = f.get("kind", "")
        if kind not in ("bug", "drift"):
            continue

        where = f.get("where", "")
        f_path, f_line = _split_evidence(where)
        if not f_path:
            continue

        # Check prose-omits-finding
        if f_path not in prose_norm:
            violations.append(Violation(
                kind="prose-omits-finding",
                where=where,
                detail=f"Prose omits mention of file '{f_path}' cited in finding."
            ))

        # Check prose-contradicts-finding
        finding_note = f.get("note", "").lower()
        contradicts = False

        # (a) Check if a claim in the same region is positive
        for c in claims:
            c_path, c_line = _split_evidence(c.get("evidence", ""))
            if f_path == c_path and f_line is not None and c_line is not None:
                if abs(f_line - c_line) <= 5:
                    if _POSITIVE_RE.search(c.get("statement", "")):
                        violations.append(Violation(
                            kind="prose-contradicts-finding",
                            where=where,
                            detail=f"Claim '{c['statement']}' describes the region in positive, contradicting finding: {f['note']}"
                        ))
                        contradicts = True
                        break

        if contradicts:
            continue

        # (b) Check if prose describes the region/file in positive terms in its vicinity
        for match in re.finditer(re.escape(f_path), prose_norm):
            start = max(0, match.start() - 150)
            end = min(len(prose_norm), match.end() + 150)
            vicinity = prose_norm[start:end]
            if _POSITIVE_RE.search(vicinity):
                violations.append(Violation(
                    kind="prose-contradicts-finding",
                    where=where,
                    detail=f"Prose describes region near '{f_path}' in positive terms, contradicting finding: {f['note']}"
                ))
                contradicts = True
                break

        if contradicts:
            continue

        # (c) Check if prose denies the risk specifically
        if "hardcoded" in finding_note or "hard-coded" in finding_note:
            if any(neg in prose_lower for neg in [
                "never hardcoded", "never hard-coded", "not hardcoded", "not hard-coded",
                "read from the environment", "read from environment", "loaded from environment"
            ]):
                violations.append(Violation(
                    kind="prose-contradicts-finding",
                    where=where,
                    detail=f"Prose claims secrets are not hardcoded, contradicting finding: {f['note']}"
                ))
        elif "bypass" in finding_note:
            if any(neg in prose_lower for neg in [
                "never bypassed", "no bypass", "not bypassed", "always verifies", "always authenticates"
            ]):
                violations.append(Violation(
                    kind="prose-contradicts-finding",
                    where=where,
                    detail=f"Prose claims authentication is enforced, contradicting finding: {f['note']}"
                ))

    # 3: Check mark-uncovered
    for m in marks:
        if m.severity not in ("danger", "warn"):
            continue

        covered = False
        for c in claims:
            c_path, c_line = _split_evidence(c.get("evidence", ""))
            if m.file == c_path and c_line is not None:
                if abs(c_line - m.line) <= 5:
                    covered = True
                    break

        if not covered:
            violations.append(Violation(
                kind="mark-uncovered",
                where=f"{m.file}:{m.line}",
                detail=f"Security-relevant mark ({m.family}) at {m.file}:{m.line} has no covering claim."
            ))

    return violations
