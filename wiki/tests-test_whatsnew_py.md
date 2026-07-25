## Purpose
The `tests/test_whatsnew.py` module tests the `isidore.whatsnew` subsystem, which generates change reports for codebases. It verifies that the system accurately detects and categorizes changes like added/removed files, renamed files, signature changes, and symbol additions. The module uses real Git repositories in temporary directories to simulate changes and validate the correctness of the delta reports. The tests ensure that the system does not invent changes (anti-invention) and precisely records both old and new signatures for modified symbols.

## Architecture
The module constructs a Git repository with a controlled set of changes (e.g., adding a method to a class, creating a new file, modifying a signature, deleting a file, and renaming a file) and then uses the `build_delta` function to generate a delta report. The tests assert that the delta report includes all expected changes and excludes untouched symbols. The repository is set up as a pytest fixture (`repo`), which is reused across tests to avoid duplication.

## Key entry points
- `repo`: A pytest fixture that creates a temporary Git repository with a predefined set of changes.
- `test_delta_reports_exactly_the_real_changes_and_invents_nothing`: Validates that the delta report includes all real changes and excludes untouched symbols.
- `test_signature_change_records_both_sides`: Ensures that signature changes are recorded with both the old and new signatures.

## Dependencies
The module depends on the `isidore.whatsnew` subsystem, which provides the `build_delta`, `FILE_ADDED`, `FILE_REMOVED`, `FILE_RENAMED`, `SIGNATURE_CHANGED`, and `SYMBOL_ADDED` constants. It also uses standard Python libraries like `subprocess` for Git operations and `pytest` for testing.

## How to change safely
When modifying this module, ensure that:
1. The `repo` fixture continues to create a repository with the same set of changes to maintain test consistency.
2. New tests follow the same pattern of validating the delta report against the expected changes.
3. The module does not introduce new dependencies or assumptions about the structure of the repository.
