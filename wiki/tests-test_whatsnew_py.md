## Purpose
The `tests/test_whatsnew.py` module tests the "whatsnew" functionality of the Isidore system, which generates a typed surface delta (API changes) and verifies them against certified prose (human-written descriptions). It ensures that the delta accurately reflects real changes in a git repository and that the prose tier correctly documents those changes. The module uses real git repositories in temporary paths and injects an LLM (though the LLM is not actually called in these tests).

## Architecture
The module creates a synthetic git repository with a controlled set of changes (symbol additions, file modifications, deletions, and renames) and verifies that the `build_delta` function correctly identifies and categorizes these changes. It tests three main aspects:
1. The delta reports exactly the real changes without inventing non-existent changes.
2. Signature changes are recorded with both the old and new signatures.
3. The delta correctly maps renames to the new paths and handles deleted files appropriately.

## Key entry points
- `repo`: A pytest fixture that sets up a synthetic git repository with a base commit and a subsequent commit containing changes.
- `test_delta_reports_exactly_the_real_changes_and_invents_nothing`: Verifies that the delta correctly identifies all real changes and excludes untouched symbols.
- `test_signature_change_records_both_sides`: Ensures that signature changes include both the old and new signatures.
- `test_multiline_typescript_signature_is_cited_at_its_declaration`: Confirms that multiline TypeScript signatures are cited at their declaration.
- `test_rename_maps_to_the_new_path`: Validates that file renames are correctly mapped to the new paths.
- `test_deleted_file_is_reported_but_carries_no_line_to_cite`: Checks that deleted files are reported but do not carry line numbers for citation.

## Dependencies
The module depends on the following imports:
- `subprocess` for running git commands.
- `shutil` for checking if git is available.
- `pytest` for testing.
- Various functions from `isidore.whatsnew` (e.g., `build_delta`, `render_whatsnew_md`, `run_whatsnew`).

## How to change safely
When modifying this module, ensure that:
1. The synthetic repository setup in the `repo` fixture accurately reflects the types of changes the system should detect.
2. All test cases verify specific, measurable aspects of the delta and prose verification.
3. New tests are added for any new change types or edge cases in the whatsnew functionality.
4. The module continues to use real git repositories in temporary paths to ensure realistic testing.
