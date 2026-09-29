## Purpose
`tests/test_surface.py` verifies the correctness of the API surface extraction logic in `isidore.surface`. It tests how the module parses Python source code to identify symbols (functions, classes, methods, constants) and their metadata (qualified names, signatures, visibility). The tests ensure that the surface extraction is precise, handles nested structures, and correctly identifies public vs. private symbols. The module is part of a larger system that tracks API changes for changelog generation, as evidenced by the recent git history (`71afec9`, `ba29200`).

## Architecture
The module uses a test-driven approach to validate the `python_surface` function from `isidore.surface`. It defines a constant `PY_SOURCE` containing a multi-line Python snippet with various symbols (top-level functions, classes, nested classes, private symbols) and tests that the extracted surface matches expectations. The helper function `_by_name` converts the extracted symbols into a dictionary keyed by qualified names for easy lookup in tests. The tests focus on three key aspects:
1. **Symbol coverage**: Ensuring all expected symbols (functions, methods, nested classes, constants) are extracted.
2. **Visibility rules**: Verifying that private symbols (prefixed with `_`) are correctly marked as non-public, even if they are part of a public class.
3. **Signature stability**: Confirming that signatures are preserved exactly, including defaults and formatting, and that changes to parameters or defaults are detected.

## Key entry points
- `_by_name()`: Converts a list of symbols into a dict keyed by `qualname` for easy lookup (`tests/test_surface.py:18-L19`).
- `test_python_surface_covers_functions_methods_nested_and_constants()`: Validates all expected symbols are extracted — functions, methods, nested classes, constants (`tests/test_surface.py:64-L76`).
- `test_python_surface_marks_visibility_including_inheritance_from_the_container()`: Ensures private symbols are correctly identified, including methods of private classes (`tests/test_surface.py:79-L89`).
- `test_python_signature_is_exact_and_survives_reformatting()`: Confirms signatures are preserved verbatim across reformatting (`tests/test_surface.py:92-L101`).
- `test_python_signature_moves_when_a_default_or_parameter_changes()`: Verifies that changes to parameters or defaults are detected, but reindenting is not (`tests/test_surface.py:104-L109`).
- `test_python_constant_value_change_is_visible()`: Asserts that changing a constant's value (e.g. `VERSION = '1.5.1'` → `'1.5.2'`) produces a different signature (`tests/test_surface.py:112-L116`).
- `test_python_surface_returns_none_on_syntax_error()`: Asserts `None` (not empty list) on syntax error, so "not comparable" is distinct from "everything deleted" (`tests/test_surface.py:119-L121`).
- `test_python_line_spans_point_at_the_declaration()`: Asserts the `line` field of `put_many_conditional` points at its `async def` declaration (`tests/test_surface.py:124-L127`).

## Dependencies
The module depends on two cross-module imports:
- `src/isidore/surface.py` (1 link) — for `KIND_CLASS`, `KIND_CONSTANT`, `KIND_FUNCTION`, `KIND_METHOD`, `MAX_SIG_CHARS`, `clean_sig`, `extract_surface`, `logical_lines`, `python_surface` (`tests/test_surface.py:5-L15`).
- `src/isidore/toon.py` (1 link) — imported by the test module.

## How to change safely
When modifying `tests/test_surface.py`, ensure that:
1. The `PY_SOURCE` constant is updated to reflect any changes in the expected symbol structure.
2. Tests are added for new features or edge cases in the surface extraction logic.
3. Existing tests are updated if the behavior of `python_surface` changes.
4. The helper function `_by_name` is not modified unless the test structure itself changes.
