> [!WARNING]
> **SECURITY — deterministic detectors flagged this code (0 LLM). Verify; never document as an intended feature.**
>
> - `tests/test_units.py:302` — credential-shaped literal (sk- prefix)
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
- `test_toon_encode_table_quoting_and_counts()`: Verifies toon table encoding with quoting and count formatting (`tests/test_units.py:26-L28`).
- `test_module_of_normalizes_and_buckets()`: Asserts `module_of` normalizes backslashes and buckets `None` as `(concepts)` (`tests/test_units.py:33-L36`).
- `test_scan_repo_extracts_symbols_imports_and_docs()`: Creates a pkg with alpha.py, beta.py, notes.md, and .venv — asserts all symbols extracted, .venv excluded, and `contains`/`imports` relations present (`tests/test_units.py:39-L55`).
- `test_scan_tolerates_syntax_errors()`: Writes broken Python and asserts the file still appears as a node (`tests/test_units.py:58-L61`).
- `test_write_scan_and_find_graph_roundtrip()`: Asserts `write_scan` → `find_graph` roundtrips and `load_graph` returns valid data (`tests/test_units.py:64-L69`).
- `_git_repo()`: Helper that initializes a minimal git repo, skipping if git is unavailable (`tests/test_units.py:72-L79`).
- `test_scan_excludes_gitignored_build_artifacts()`: The GIMO bug — a gitignored `build_copy/` directory must NOT be indexed as source (`tests/test_units.py:82-L89`).

## Dependencies
The module depends on eight cross-module imports:
- `src/isidore/findings.py` (1 link) — for `filter_findings`, `harvest_todos`, `orphan_file_candidates`, `parse_findings_block`, `render_findings`, `coverage_gap_candidates` (`tests/test_units.py:8-L15`).
- `src/isidore/graph.py` (1 link) — for `GraphError`, `find_graph`, `load_graph`, `module_of`, `scan_repo`, `write_scan` (`tests/test_units.py:16`).
- `src/isidore/llm.py` (1 link) — for `build_request` (`tests/test_units.py:17`).
- `src/isidore/pipeline.py` (1 link) — for `PageSpec` (`tests/test_units.py:18`).
- `src/isidore/qa.py` (1 link) — for `ask`, `gather_evidence`, `question_terms` (`tests/test_units.py:19`).
- `src/isidore/render.py` (1 link) — for `render_toon_index` (`tests/test_units.py:20`).
- `src/isidore/toon.py` (1 link) — for `encode_table` (`tests/test_units.py:21`).
- `src/isidore/__init__.py` (1 link) — imported by the test module.

## How to change safely
To modify this module safely:
1. **Add new tests** by following the existing patterns, ensuring they are isolated and use pytest fixtures.
2. **Update existing tests** to reflect changes in the corresponding modules, but avoid breaking existing test cases.
3. **Maintain consistency** with the module's structure and naming conventions.
