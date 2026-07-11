"""Compile journal + per-page changelog — residue mining, all zero-LLM.

Every compile appends one record to `state["journal"]` (capped): what it planned, how many pages the
content-hash cache saved vs paid for, retries, quarantines. `isidore stats` reads it back to surface
cost telemetry and the MOST-UNSTABLE pages — a page whose context is re-dirtied run after run is an
unstable module contract, an architecture smell no test suite reports. Separately, at write time each
regenerated page's prose is diffed at the H2-heading level and the change is recorded in the page's
own history: the wiki's drift log ("what changed in the understanding of this module").
"""
from __future__ import annotations

from collections import Counter

from .toon import encode

JOURNAL_KEY = "journal"
JOURNAL_CAP = 50
HISTORY_CAP = 5


def append_run(state: dict, record: dict) -> None:
    journal = state.setdefault(JOURNAL_KEY, [])
    journal.append(record)
    del journal[:-JOURNAL_CAP]


def _sections(markdown: str) -> dict[str, str]:
    """Map each `## heading` to its body text (content before the first heading is keyed '(intro)')."""
    out: dict[str, list[str]] = {"(intro)": []}
    current = "(intro)"
    for line in markdown.splitlines():
        if line.startswith("## "):
            current = line[3:].strip()
            out.setdefault(current, [])
        else:
            out[current].append(line)
    return {k: "\n".join(v).strip() for k, v in out.items()}


def section_diff(old: str, new: str) -> tuple[list[str], int]:
    """(H2 headings whose content changed / were added / removed, new_line_count - old_line_count)."""
    old_s, new_s = _sections(old), _sections(new)
    changed: list[str] = []
    for head in sorted(set(old_s) | set(new_s)):
        if old_s.get(head) != new_s.get(head):
            changed.append(head)
    delta = len(new.splitlines()) - len(old.splitlines())
    return changed, delta


def record_page_change(page_state: dict, commit: str | None, old: str, new: str) -> None:
    """Append an H2-level changelog entry to a page's state (capped). No-op if the prose is byte-equal."""
    if old == new:
        return
    changed, delta = section_diff(old, new)
    history = page_state.setdefault("history", [])
    history.append({"commit": (commit or "?")[:12], "sections_changed": changed, "line_delta": delta})
    del history[:-HISTORY_CAP]


def render_stats(state: dict) -> str:
    journal = state.get(JOURNAL_KEY, [])
    pages_state = state.get("pages", {})
    total_saved = sum(r.get("calls_saved", 0) for r in journal)
    total_spent = sum(r.get("generated", 0) + r.get("retries", 0) for r in journal)
    total_quarantined = sum(r.get("quarantined", 0) for r in journal)

    regen = Counter()
    for r in journal:
        regen.update(r.get("generated_pages", []))
    unstable = [{"page": p, "regenerations": n} for p, n in regen.most_common(10) if n > 1]

    quarantined_now = sorted(p for p, e in pages_state.items() if e.get("quarantined"))

    header = (
        f"# isidore stats · {len(journal)} run(s) journaled (0 LLM)\n"
        f"# calls saved by cache: {total_saved} · calls spent (incl. retries): {total_spent} · "
        f"quarantines over time: {total_quarantined}\n")
    runs = [{"commit": r.get("commit", "?"), "planned": r.get("planned", 0),
             "dirty": r.get("dirty", 0), "generated": r.get("generated", 0),
             "saved": r.get("calls_saved", 0), "retries": r.get("retries", 0),
             "quarantined": r.get("quarantined", 0)} for r in journal[-12:]]
    return header + encode(
        ("recent_runs", ["commit", "planned", "dirty", "generated", "saved", "retries", "quarantined"], runs),
        ("most_unstable_pages", ["page", "regenerations"], unstable),
        ("quarantined_now", ["page"], [{"page": p} for p in quarantined_now]),
    ) + "\n"
