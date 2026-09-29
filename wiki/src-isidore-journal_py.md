## Purpose
`src/isidore/journal.py` provides compile-journal telemetry and per-page changelog tracking, all zero-LLM. Every compile appends one record to `state["journal"]` (capped at 50 entries): what it planned, how many pages the content-hash cache saved vs paid for, retries, quarantines. `isidore stats` reads it back to surface cost telemetry and the most-unstable pages — a page whose context is re-dirtied run after run is an unstable module contract, an architecture smell no test suite reports. Separately, at write time each regenerated page's prose is diffed at the H2-heading level and the change is recorded in the page's own history: the wiki's drift log (`src/isidore/journal.py:1`).

## Architecture
The module has two independent responsibilities:

**Run journal** — `append_run()` adds a compile record to `state["journal"]`, capped at `JOURNAL_CAP` (50) entries. `render_stats()` reads the journal back and produces a toon-encoded report with three tables: recent runs, most-unstable pages, and currently quarantined pages.

**Per-page changelog** — `section_diff()` diffs two Markdown strings at the `## heading` level, returning which sections changed and the line-count delta. `record_page_change()` uses it to append a capped history entry (`HISTORY_CAP` = 5) to a page's state whenever its prose changes.

## Key entry points
- `append_run(state, record)`: Appends a compile record to the journal, evicting the oldest if over cap (`src/isidore/journal.py:L21-L24`).
- `section_diff(old, new)`: Returns `(list_of_changed_H2_headings, line_delta)` (`src/isidore/journal.py:L40-L48`).
- `record_page_change(page_state, commit, old, new)`: Appends an H2-level changelog entry to a page's state; no-op if prose is byte-equal (`src/isidore/journal.py:L51-L58`).
- `render_stats(state)`: Produces a toon-encoded stats report from the journal (`src/isidore/journal.py:L61-L87`).

## Dependencies
- `src/isidore/toon.py`: Provides `encode` for table serialization in `render_stats`.
- Used by:
  - `src/isidore/cli.py` (for the `isidore stats` subcommand)
  - `src/isidore/pipeline.py` (for recording compile runs and page changes)
- Tested by:
  - `tests/test_residue.py`

## How to change safely
1. **Journal cap**: `JOURNAL_CAP` (50) bounds memory. Increasing it stores more history; decreasing it loses the oldest entries on the next append.
2. **History cap**: `HISTORY_CAP` (5) bounds per-page changelog depth. Same trade-off.
3. **Section diff granularity**: `section_diff` splits on `## ` headings. Changing to `#` or `###` changes what counts as a "section changed" — the drift log contract would shift.
4. **Stats tables**: `render_stats` produces three named toon-encoded tables (`recent_runs`, `most_unstable_pages`, `quarantined_now`). Column names and order are consumed by downstream tools.
