## Purpose
The `tests/test_whatsnew.py` module tests the "whatsnew" functionality of the Isidore system, which generates a typed surface delta (API changes) and verifies them against certified prose (human-written descriptions). It ensures that the delta accurately reflects real changes in a git repository and that the prose tier correctly documents those changes. The module uses real git repositories in temporary paths and injects an LLM (though the LLM is not actually called in these tests).

## Architecture
The module creates a synthetic git repository with a controlled set of changes (symbol additions, file modifications, deletions, and renames) and verifies that the `build_delta` function correctly identifies and categorizes these changes. It tests three main aspects:
1. The delta reports exactly the real changes without inventing non-existent changes.
2. Signature changes are recorded with both the old and new signatures.
3. The delta correctly maps renames to the new paths and handles deleted files appropriately.

## Key entry points
- `_git()`: Runs a git command in the given path via `subprocess.run` (`tests/test_whatsnew.py:39-L40`).
- `_commit()`: Stages all, commits with `--no-gpg-sign`, and returns the HEAD rev-parse (`tests/test_whatsnew.py:43-L48`).
- `repo()`: Pytest fixture creating a synthetic git repo with a base commit (client.py, node.ts, old.py, util.py) and a subsequent commit adding methods, a new file, a signature change, a deletion, and a rename (`tests/test_whatsnew.py:52-L100`).
- `test_delta_reports_exactly_the_real_changes_and_invents_nothing()`: Asserts the delta contains exactly 7 expected entries (2 Python SYMBOL_ADDED, 1 TypeScript SYMBOL_ADDED, 1 FILE_ADDED, 1 SIGNATURE_CHANGED, 1 FILE_REMOVED, 1 FILE_RENAMED) and no inventions (`tests/test_whatsnew.py:105-L121`).
- `test_signature_change_records_both_sides()`: Asserts `GICSClient.put`'s new sig contains `verify=False` while old sig does not (`tests/test_whatsnew.py:124-L129`).
- `test_multiline_typescript_signature_is_cited_at_its_declaration()`: Asserts `NodeClient.putManyConditional` line points at `async putManyConditional` and the sig includes `Options = {}` (`tests/test_whatsnew.py:132-L138`).
- `test_rename_maps_to_the_new_path()`: Asserts `FILE_RENAMED` entry has `file=="helpers.py"` and `old_file=="util.py"` (`tests/test_whatsnew.py:141-L144`).
- `test_deleted_file_is_reported_but_carries_no_line_to_cite()`: Asserts `FILE_REMOVED` entry for `old.py` (`tests/test_whatsnew.py:147-L149`).

## Dependencies
The module depends on three cross-module imports:
- `src/isidore/render.py` (1 link) — for `WIKI_DIRNAME` (`tests/test_whatsnew.py:11`).
- `src/isidore/whatsnew.py` (1 link) — for `FILE_ADDED`, `FILE_REMOVED`, `FILE_RENAMED`, `SIGNATURE_CHANGED`, `SYMBOL_ADDED`, `WhatsnewError`, `build_delta`, `impact_summary`, `parse_plain_block`, `render_whatsnew_md`, `render_whatsnew_toon`, `run_whatsnew`, `strip_inline_claim_rows`, `surface_verify_ctx` (`tests/test_whatsnew.py:12-L26`).
- `src/isidore/cli.py` (1 link) — imported by the test module.

## How to change safely
When modifying this module, ensure that:
1. The synthetic repository setup in the `repo` fixture accurately reflects the types of changes the system should detect.
2. All test cases verify specific, measurable aspects of the delta and prose verification.
3. New tests are added for any new change types or edge cases in the whatsnew functionality.
4. The module continues to use real git repositories in temporary paths to ensure realistic testing.
