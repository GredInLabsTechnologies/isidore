## Purpose
`tests/test_surface.py` tests the API surface extraction logic in `isidore.surface`. It verifies that the module correctly identifies and classifies Python symbols (functions, methods, classes, constants) by their qualified names, signatures, and visibility. The tests ensure that the surface extraction is precise, handles nested structures, and distinguishes between public and private symbols. The module operates purely on text input, without external dependencies like git or disk access.

## Architecture
The test module uses a helper function `_by_name()` to index extracted symbols by their qualified names (`tests/test_surface.py:L18-L19`). It defines a constant `PY_SOURCE` containing a multi-line Python snippet with various symbol declarations (`tests/test_surface.py:L24-L61`). The tests then call `python_surface()` on this snippet and assert properties of the extracted symbols, such as their kind, visibility, and signature.

## Key entry points
- `test_python_surface_covers_functions_methods_nested_and_constants()`: Validates that the surface extraction correctly identifies functions, methods, nested classes, and constants (`tests/test_surface.py:L64-L76`).
- `test_python_surface_marks_visibility_including_inheritance_from_the_container()`: Ensures that visibility rules (public/private) are applied correctly, including inheritance from container classes (`tests/test_surface.py:L79-L89`).
- `test_python_signature_is_exact_and_survives_reformatting()`: Confirms that signatures are preserved exactly, even when reformatted across lines (`tests/test_surface.py:L92-L100`).
- `test_python_signature_moves_when_a_default_or_parameter_changes()`: Checks that signature changes are detected when defaults or parameters are modified (`tests/test_surface.py:L103-L108`).

## Dependencies
The module depends on `isidore.surface`, which provides the `python_surface()` function and related constants (`tests/test_surface.py:L5-L15`). It does not have cross-module dependencies.

## How to change safely
When modifying `tests/test_surface.py`, ensure that:
1. The `PY_SOURCE` constant remains syntactically valid Python to avoid test failures due to syntax errors.
2. Changes to assertions reflect the actual behavior of `isidore.surface` to maintain test accuracy.
3. New tests follow the same pattern of extracting symbols and asserting their properties.
