## Purpose
The `tests/test_residue.py` module tests the "residue-mining" functionality of the Isidore system, which includes:
- Section diffing (`section_diff`) to track changes in Markdown headings between versions
- Compile journaling and statistics tracking (`render_stats`) to record pipeline runs
- Per-page history tracking to log section changes over time
- Claims/findings querying (`claims_for_file`, `claims_grep`) to verify documentation assertions

These tests ensure the system correctly identifies and records changes in documentation and code, maintaining accurate historical records and validation mechanisms.

## Architecture
The module uses a test harness that:
1. Creates temporary Git repositories (`_repo()`) with sample Python files
2. Executes the Isidore pipeline (`compile_wiki`) with controlled inputs
3. Verifies the generated outputs against expected results

Key components:
- `_git()` helper for repository operations
- `_repo()` factory for test fixtures
- Four test cases covering different aspects of residue-mining

## Key entry points
- `test_section_diff_reports_changed_headings_and_line_delta()`: Verifies section diffing logic
- `test_journal_and_stats_track_calls_saved_and_unstable()`: Tests compile journaling
- `test_page_history_records_section_changes()`: Validates per-page history tracking
- `test_claims_for_file_and_grep()`: Checks claims/findings querying

## Dependencies
The module depends on:
- `isidore.journal` for `section_diff` and `render_stats`
- `isidore.pipeline` for `compile_wiki` and `load_state`
- `isidore.claims` for claims-related functionality
- Standard library modules (`shutil`, `subprocess`, `pytest`)

## How to change safely
When modifying this module:
1. Preserve the test harness structure (`_git`, `_repo`)
2. Maintain the exact test cases and their assertions
3. Keep the sample repository setup consistent
4. Update dependencies if the underlying APIs change
5. Add new tests for any new residue-mining features
