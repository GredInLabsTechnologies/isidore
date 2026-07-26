## Purpose
`tests/test_surface.py` verifies the correctness of the API surface extraction logic in `isidore.surface`. It tests how the module parses Python source code to identify symbols (functions, classes, methods, constants) and their metadata (qualified names, signatures, visibility). The tests ensure that the surface extraction is precise, handles nested structures, and correctly identifies public vs. private symbols. The module is part of a larger system that tracks API changes for changelog generation, as evidenced by the recent git history (`71afec9`, `ba29200`).

## Architecture
The module uses a test-driven approach to validate the `python_surface` function from `isidore.surface`. It defines a constant `PY_SOURCE` containing a multi-line Python snippet with various symbols (top-level functions, classes, nested classes, private symbols) and tests that the extracted surface matches expectations. The helper function `_by_name` converts the extracted symbols into a dictionary keyed by qualified names for easy lookup in tests. The tests focus on three key aspects:
1. **Symbol coverage**: Ensuring all expected symbols (functions, methods, nested classes, constants) are extracted.
2. **Visibility rules**: Verifying that private symbols (prefixed with `_`) are correctly marked as non-public, even if they are part of a public class.
3. **Signature stability**: Confirming that signatures are preserved exactly, including defaults and formatting, and that changes to parameters or defaults are detected.

## Key entry points
- `test_python_surface_covers_functions_methods_nested_and_constants()`: Validates that all expected symbols are extracted, including nested structures.
- `test_python_surface_marks_visibility_including_inheritance_from_the_container()`: Ensures private symbols are correctly identified.
- `test_python_signature_is_exact_and_survives_reformatting()`: Confirms that signatures are preserved across reformatting.
- `test_python_signature_moves_when_a_default_or_parameter_changes()`: Verifies that changes to parameters or defaults are detected.

## Dependencies
The module depends on `isidore.surface`, which provides the `python_surface` function and related constants (`KIND_CLASS`, `KIND_CONSTANT`, etc.). It does not have cross-module dependencies, as evidenced by the fact that it is not depended on by any other module.

## How to change safely
When modifying `tests/test_surface.py`, ensure that:
1. The `PY_SOURCE` constant is updated to reflect any changes in the expected symbol structure.
2. Tests are added for new features or edge cases in the surface extraction logic.
3. Existing tests are updated if the behavior of `python_surface` changes.
4. The helper function `_by_name` is not modified unless the test structure itself changes.
