## Purpose
`tests/test_units.py` provides a suite of **unit tests** that verify core functionality of the Isidore codebase: the toon table encoder, graph‑scanning utilities, findings‑block parsing, and the round‑trip persistence of scans. The file’s docstring (tests/test_units.py:1) declares these focus areas explicitly.

## Architecture
The module is organized into three logical sections, each introduced by a visual delimiter comment:

* **Toon encoder tests** – introduced at tests/test_units.py:22, containing `test_toon_encode_table_quoting_and_counts` (tests/test_units.py:24‑26). This test checks quoting rules and count columns of `encode_table`.

* **Graph utilities tests** – introduced at tests/test_units.py:29, comprising:
  * `test_module_of_normalizes_and_buckets` (tests/test_units.py:31‑34) – validates `module_of` path normalisation.
  * `test_scan_repo_extracts_symbols_imports_and_docs` (tests/test_units.py:37‑53) – builds a temporary package, runs `scan_repo`, and asserts presence of source symbols and proper exclusion of virtual‑environment files.
  * `test_scan_tolerates_syntax_errors` (tests/test_units.py:56‑60) – confirms that `scan_repo` still yields a node for a file with a syntax error.
  * `test_write_scan_and_find_graph_roundtrip` (tests/test_units.py:62‑68) – verifies that `write_scan` produces data consumable by `find_graph` and `load_graph`.

* **Findings parsing tests** – introduced at tests/test_units.py:70, containing:
  * `test_parse_findings_block_extracts_and_strips` (tests/test_units.py:72‑83) – checks that a markdown‑embedded findings block is stripped from the surrounding text and that only recognized kinds are returned.
  * `test_filter_findings_drops_hallucinated_paths` (starts at tests/test_units.py:85) – ensures `filter_findings` removes entries whose file paths do not exist.

Each test function follows the pytest convention (`test_` prefix) so the suite is automatically discovered.

## Key entry points
The public “entry points” for this test suite are the individual test functions:

| Function | What it exercises | Location |
|----------|-------------------|----------|
| `test_toon_encode_table_quoting_and_counts` | `encode_table` handling of commas and `None` values | tests/test_units.py:24‑26 |
| `test_module_of_normalizes_and_buckets` | `module_of` path normalization | tests/test_units.py:31‑34 |
| `test_scan_repo_extracts_symbols_imports_and_docs` | `scan_repo` symbol extraction, import detection, exclusion of `.venv` files | tests/test_units.py:37‑53 |
| `test_scan_tolerates_syntax_errors` | Robustness of `scan_repo` on malformed Python files | tests/test_units.py:56‑60 |
| `test_write_scan_and_find_graph_roundtrip` | Persistence round‑trip via `write_scan`, `find_graph`, `load_graph` | tests/test_units.py:62‑68 |
| `test_parse_findings_block_extracts_and_strips` | `parse_findings_block` markdown parsing and cleanup | tests/test_units.py:72‑83 |
| `test_filter_findings_drops_hallucinated_paths` | `filter_findings` path validation | tests/test_units.py:85‑?? |

These functions are the sole hooks that external test runners interact with.

## Dependencies
The module imports a broad set of symbols from the Isidore package (tests/test_units.py:6‑19):

* `filter_findings`, `harvest_todos`, `orphan_file_candidates`, `parse_findings_block`, `render_findings`, `coverage_gap_candidates` from `isidore.findings`
* `find_graph`, `load_graph`, `module_of`, `scan_repo`, `write_scan` from `isidore.graph`
* `build_request` from `isidore.llm`
* `PageSpec` from `isidore.pipeline`
* `ask`, `gather_evidence`, `question_terms` from `isidore.qa`
* `render_toon_index` from `isidore.render`
* `encode_table` from `isidore.toon`

Only a subset of these imports is exercised by the tests (e.g., `encode_table`, `module_of`, `scan_repo`, `write_scan`, `find_graph`, `load_graph`, `parse_findings_block`, `filter_findings`). The rest appear unused in this file.

The test suite also relies on the standard library `json` (tests/test_units.py:4) and the `tmp_path` fixture supplied by pytest.

## How to change safely
1. **Preserve pytest naming** – keep the `test_` prefix; otherwise the test runner will miss new cases.  
2. **Maintain section delimiters** – the comment lines (`# ----------------------------------------------------------------------- toon`, etc.) help developers locate related tests; add new tests under the appropriate delimiter.  
3. **Use `tmp_path` for filesystem isolation** – existing tests create temporary directories and files (e.g., tests/test_units.py:38‑46). Follow the same pattern to avoid polluting the repository.  
4. **Do not alter import signatures** – the module expects the imported symbols to exist with the signatures used in the assertions (e.g., `encode_table(name, cols, rows)` at tests/test_units.py:25). Removing an import that a test indirectly depends on will cause import errors.  
5. **Update assertions when underlying library behavior changes** – if a function’s output format evolves (e.g., `scan_repo` adds new relation types), adjust the corresponding assertions (e.g., the `"contains"` and `"imports"` checks at tests/test_units.py:52‑53).  
6. **Avoid introducing unused imports** – the current file already imports several symbols that aren’t referenced; adding more unused imports can increase import time and obscure intent.  

When extending the suite, mirror the existing style: create a temporary environment, invoke the target API, and assert on concrete, small‑scale outputs.
