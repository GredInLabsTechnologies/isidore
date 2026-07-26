## Purpose
The `tests/test_changeset.py` module tests the change-set detection logic in the `isidore.changeset` package. It verifies four core functions: `symbol_spans`, `changed_symbols`, `affected_modules`, and `changed_lines`. These functions work together to identify which code symbols and modules are impacted by changes, enabling incremental compilation and efficient build systems. The tests ensure that symbol spans are correctly calculated, changed lines are accurately mapped to symbols, and affected modules are properly identified based on dependency relationships.

## Architecture
The module consists of four test functions:
1. `test_symbol_spans_accepts_span_and_start_only_forms` — Validates that `symbol_spans` correctly computes line ranges for symbols, handling both explicit spans and start-only locations.
2. `test_changed_symbols_maps_lines_and_whole_file` — Tests that `changed_symbols` maps changed lines to the correct symbols, including whole-file changes and lines outside any symbol.
3. `test_affected_modules_is_changed_plus_fan_in_dependents` — Ensures `affected_modules` correctly identifies modules impacted by changes, including dependencies at configurable depths.
4. `test_changed_lines_parses_new_side_hunks` — Verifies that `changed_lines` accurately parses Git diffs to identify changed lines in the working tree.

The tests use a helper function `_code` to create mock code nodes with IDs, source files, and line locations. The `DEPTH` constant (set to 2) controls how many levels of dependencies are considered when computing affected modules.

## Key entry points
- `test_symbol_spans_accepts_span_and_start_only_forms` — The primary test for `symbol_spans`, which computes line ranges for symbols.
- `test_changed_symbols_maps_lines_and_whole_file` — The main test for `changed_symbols`, which maps changed lines to symbols.
- `test_affected_modules_is_changed_plus_fan_in_dependents` — The core test for `affected_modules`, which identifies modules impacted by changes.
- `test_changed_lines_parses_new_side_hunks` — The test for `changed_lines`, which parses Git diffs to find changed lines.

## Dependencies
The module depends on:
- `pytest` for test execution.
- `subprocess` to run Git commands.
- `shutil` to check for Git availability.
- The `isidore.changeset` package, which provides the functions under test (`symbol_spans`, `changed_symbols`, `affected_modules`, and `changed_lines`).

## How to change safely
When modifying `tests/test_changeset.py`, follow these guidelines:
1. **Preserve test structure** — Do not remove or rename existing test functions. New tests should follow the same pattern.
2. **Update mock data** — If changing the behavior of the tested functions, update the mock data in the tests to reflect the new behavior.
3. **Maintain test isolation** — Ensure tests do not depend on external state or shared resources.
4. **Keep assertions precise** — Use specific assertions to verify behavior, avoiding overly broad checks.
