## Purpose
`src/isidore/langspec.py` enables Isidore to extract symbols and imports from source files without external dependencies, using a declarative approach. It bridges the gap between Isidore's native Python scanner and other languages by treating language-specific rules as data (`LanguageSpec`). The module prioritizes simplicity and portability over precision, with three tiers of degradation: exact AST for Python, declarative rules for brace-based languages, and bare files for everything else. This design mirrors Isidore's philosophy of "good enough" structure for a wiki, avoiding false positives while preserving line numbers for accurate navigation.

## Architecture
The module consists of two core components:
1. **`LanguageSpec`**: A dataclass defining a language's syntax rules, including comment delimiters, string delimiters, and symbol patterns (`SymbolRule`). Each language is configured as a row in a table (`LANGUAGES`), interpreted by the engine.
2. **`extract()`**: The engine that processes source text. It first sanitizes the input by blanking out comments and strings (preserving newlines and length) to avoid false positives, then scans for symbols and imports. Symbols are tracked by brace depth, and their line spans are determined by matching opening and closing braces.

## Key entry points
- **`extract(text, spec)`**: The main function that processes a file's text and returns symbols and imports. It uses `sanitize()` to prepare the text and then scans for symbols and imports.
- **`sanitize(text, spec)`**: A state machine that blanks out comments and strings, preserving newlines and length. It handles line comments, block comments, and string literals, with special handling for backslash escapes.

## Dependencies
The module depends only on Python's standard library (`re`, `dataclasses`), ensuring zero external dependencies and portability across architectures.

## How to change safely
To add a new language:
1. Define a `LanguageSpec` with the language's syntax rules (`line_comments`, `block_comments`, `string_delims`, `symbol_rules`, `import_rules`).
2. Add the spec to the `LANGUAGES` table in the consuming module (e.g., `src/isidore/graph.py`).

To modify the engine:
1. Avoid introducing new control flow in `extract()` or `sanitize()` to maintain simplicity.
2. Extend the state machine in `sanitize()` only if new syntax patterns require it.
