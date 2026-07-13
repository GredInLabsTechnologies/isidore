## Purpose
The `tests/test_langspec.py` module serves as a regression test suite for the multi-language scanner's declarative engine (`langspec`). It verifies the scanner's ability to extract symbols, sanitize source code, and handle language-specific syntax across multiple languages. The tests focus on critical behaviors like comment/string immunity, brace-depth detection, and exact line spans, ensuring the scanner's output matches expectations for a structure wiki.

## Architecture
The module consists of a collection of test functions, each targeting a specific aspect of the scanner's behavior. The tests are organized into three main sections:
1. **Sanitization tests** (`test_sanitize_*`), which verify that the scanner correctly removes comments, strings, and other non-structural elements while preserving line structure.
2. **Symbol extraction tests** (`test_*_functions_types_and_spans`), which check that the scanner accurately identifies symbols and their line spans for specific languages.
3. **Helper functions** (`_names`), which provide a reusable way to extract symbol names from test cases.

## Key entry points
The primary entry points are the test functions themselves, which are executed by the test runner. The most significant ones include:
- `test_sanitize_blanks_comments_and_strings_preserving_lines()`: Validates that the scanner removes comments and strings while preserving line structure (`tests/test_langspec.py:L20-L28`).
- `test_rust_functions_types_and_spans()`: Ensures the scanner correctly extracts Rust symbols and their line spans (`tests/test_langspec.py:L38-L53`).
- `test_typescript_class_and_arrow_and_imports()`: Tests TypeScript symbol extraction, including classes, arrow functions, and imports (`tests/test_langspec.py:L56-L67`).

## Dependencies
The module depends on the `isidore.langspec` module, which provides the `extract`, `sanitize`, and `spec_for` functions used to process source code and generate language specifications (`tests/test_langspec.py:L10`). It also depends on `isidore.graph.scan_repo`, though the exact usage is not detailed in the provided facts.

## How to change safely
When modifying this module, follow these guidelines:
1. **Add new tests for new languages**: If adding support for a new language, include a corresponding test function to verify symbol extraction and sanitization.
2. **Preserve existing behavior**: Ensure that changes do not break existing tests, as they serve as the regression net for the scanner's behavior.
3. **Update test cases**: If the scanner's behavior changes (e.g., due to a new feature or bug fix), update the corresponding test cases to reflect the new expectations.
