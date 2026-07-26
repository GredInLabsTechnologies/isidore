## Purpose
`src/isidore/surface.py` extracts the API surface of a file's text, representing it as a set of `SurfaceSymbol` objects. Each symbol captures its qualified name, kind (e.g., function, class), visibility (public/private), line range, and signature. The module exists to compare API surfaces across revisions, enabling `isidore whatsnew` to detect changes like added/removed symbols or modified signatures. It operates on raw text rather than file paths, avoiding the need for a working tree or checkout, and handles multi-line signatures and brace-bearing parameters that other tools miss.

## Architecture
The module uses regex patterns to identify callable declarations (`_HEADER`) and value bindings (`_CONST`). For Python, it leverages `ast` to parse signatures exactly, ensuring formatting differences don't register as API changes. Key functions:
- `_declaration_tail()` determines if a line's parentheses close, distinguishing declarations from calls.
- `_is_declaration()` filters out test-framework blocks by rejecting lines with `=>` in the tail.
- `_is_public()` enforces the underscore convention for visibility.
- `clean_sig()` normalizes whitespace and truncates long signatures for comparison.

## Key entry points
- `SurfaceSymbol`: The dataclass representing a symbol's API surface.
- `clean_sig()`: Converts a declaration header into a stable comparison key.

## Dependencies
- `src/isidore/langspec.py`: Reuses its comment/string sanitizer and declaration keyword table.

## How to change safely
- **Signatures**: Modify `clean_sig()` to handle new formatting cases, but ensure the output remains stable for comparison.
- **Visibility**: Adjust `_is_public()` if the underscore convention changes.
- **Language Support**: Add new patterns for unsupported languages, following the existing structure.
