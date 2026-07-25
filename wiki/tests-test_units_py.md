> [!WARNING]
> **SECURITY — deterministic detectors flagged this code (0 LLM). Verify; never document as an intended feature.**
>
> - `tests/test_units.py:268` — credential-shaped literal (sk- prefix)
## Purpose
The `tests/test_units.py` module contains unit tests for core functionality of the Isidore system, focusing on four key areas: the toon encoder, graph scanner, findings residue, and QA retrieval. The tests verify that these components handle edge cases, syntax errors, and file exclusions correctly, ensuring the system's reliability when processing codebases.

## Architecture
The module is organized into four logical sections, each corresponding to a major component of Isidore:
1. **Toon encoder tests** (`test_toon_encode_table_quoting_and_counts()`) verify the formatting of tabular data for the toon format.
2. **Graph scanner tests** (`test_module_of_normalizes_and_buckets()`, `test_scan_repo_extracts_symbols_imports_and_docs()`, `test_scan_tolerates_syntax_errors()`, `test_write_scan_and_find_graph_roundtrip()`, `test_scan_excludes_gitignored_build_artifacts()`) ensure the scanner correctly processes Python files, handles syntax errors, and excludes ignored files.
3. **Findings residue tests** (not shown in excerpts) would validate the extraction and rendering of findings from code.
4. **QA retrieval tests** (not shown in excerpts) would verify the question-answering pipeline.

Each test is self-contained and uses pytest fixtures like `tmp_path` to create isolated test environments.

## Key entry points
The module's entry points are the test functions themselves, which are called by pytest during test execution. The most connected symbol is the module itself (`test_units.py`), which imports all dependencies and defines the test suite.

## Dependencies
The module depends on:
- `isidore.toon.encode_table` for toon encoding tests (`tests/test_units.py:L21`)
- `isidore.graph` for graph-related tests (`tests/test_units.py:L16`)
- `isidore.findings` for findings-related tests (`tests/test_units.py:L8-L15`)
- `isidore.qa` for QA-related tests (`tests/test_units.py:L19`)

## How to change safely
To modify this module safely:
1. **Add new tests** by following the existing patterns, ensuring they are isolated and use pytest fixtures.
2. **Update existing tests** to reflect changes in the corresponding modules, but avoid breaking existing test cases.
3. **Maintain consistency** with the module's structure and naming conventions.
