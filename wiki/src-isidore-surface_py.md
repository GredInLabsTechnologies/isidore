## Purpose
`src/isidore/surface.py` extracts the API surface of a file's text, capturing declared symbols and their signatures. It serves as the foundation for `isidore whatsnew`, comparing file revisions to detect API changes. Unlike `graph.py`, which identifies symbols in a working tree, this module works on raw text and includes signatures, which are critical for detecting changes like parameter list modifications. The module handles multi-line headers and brace-bearing parameter defaults, which are missed by simpler line-based scanners.

## Architecture
The module defines a `SurfaceSymbol` dataclass to represent symbols with fields like `qualname`, `kind`, and `sig`. Key functions include:
- `_HEADER` and `_CONST` regex patterns to match callable and value declarations.
- `clean_sig()` to normalize signatures for comparison, removing whitespace and trailing braces.
- `_declaration_tail()` and `_is_declaration()` to distinguish declarations from calls.
- `_is_public()` to determine symbol visibility using the underscore convention.
- Language-specific handlers (e.g., `_py_signature()` for Python) to extract signatures from ASTs.

## Key entry points
- `SurfaceSymbol`: The core data structure representing a symbol's API surface, with `qualname` (identity across revisions), `kind`, `sig`, and `end_line` (`src/isidore/surface.py:88-L103`).
- `clean_sig()`: Normalizes signatures for stable comparison — whitespace collapsed, trailing brace dropped, truncated to `MAX_SIG_CHARS` (`src/isidore/surface.py:106-L116`).
- `_declaration_tail()`: What follows the parameter list, or `None` if parens never close — separates a definition from a call (`src/isidore/surface.py:119-L137`).
- `_is_declaration()`: Body opens after parameters close and no arrow intervenes — rejects test-framework blocks (`src/isidore/surface.py:140-L149`).
- `_is_public()`: Underscore convention; dunders are surface, single-underscore is not (`src/isidore/surface.py:152-L155`).

## Dependencies
The module depends on `src/isidore/langspec.py` for language-specific rules, such as comment/string sanitization and declaration keywords. It is used by `src/isidore/whatsnew.py` to generate changelogs and by `src/isidore/verify.py` for signature verification.

## How to change safely
When modifying `surface.py`, focus on:
1. **Signature handling**: Ensure `clean_sig()` preserves the exact signature text for readability in changelogs.
2. **Declaration detection**: Adjust `_is_declaration()` to avoid false positives for test-framework blocks.
3. **Language support**: Add new handlers (e.g., `_js_signature()`) following the pattern of `_py_signature()`.
