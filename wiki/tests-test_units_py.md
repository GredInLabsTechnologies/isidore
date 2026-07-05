## Purpose
`tests/test_units.py` houses unit tests that verify core *isidore* functionality:  

* the **toon** table encoder (`encode_table`)  【tests/test_units.py:26】  
* graph utilities (`module_of`, `scan_repo`, `write_scan`, `find_graph`, `load_graph`)  【tests/test_units.py:33】‑​【tests/test_units.py:69】  
* findings parsing and filtering (`parse_findings_block`, `filter_findings`)  【tests/test_units.py:74】‑​【tests/test_units.py:87】  

The file exists to catch regressions and to stress‑test edge cases (e.g., hostile input and syntax errors 【git:4271e60】).

## Architecture
The module is a single‑file test suite organized by comment “section” headers:

| Section | Covered symbols | Representative test |
|---------|----------------|----------------------|
| **toon** | `isidore.toon.encode_table` | `test_toon_encode_table_quoting_and_counts` 【tests/test_units.py:26】 |
| **graph** | `isidore.graph.module_of`, `scan_repo`, `write_scan`, `find_graph`, `load_graph`, `GraphError` | `test_module_of_normalizes_and_buckets`, `test_scan_repo_extracts_symbols_imports_and_docs`, `test_scan_tolerates_syntax_errors`, `test_write_scan_and_find_graph_roundtrip` 【tests/test_units.py:33】‑​【tests/test_units.py:69】 |
| **findings** | `isidore.findings.parse_findings_block`, `filter_findings`, `harvest_todos`, `orphan_file_candidates`, `coverage_gap_candidates`, `render_findings` | `test_parse_findings_block_extracts_and_strips`, `test_filter_findings_drops_hallucinated_paths` 【tests/test_units.py:74】‑​【tests/test_units.py:87】 |

All tests import the same set of public APIs at the top of the file 【tests/test_units.py:8‑21】, keeping the suite self‑contained.

## Key entry points
Each `def test_*` function is a pytest entry point:

| Function | What it checks | Key line |
|----------|----------------|----------|
| `test_toon_encode_table_quoting_and_counts` | `encode_table` quoting & count output | 【tests/test_units.py:28】 |
| `test_module_of_normalizes_and_buckets` | `module_of` path normalization & default bucket | 【tests/test_units.py:34】 |
| `test_scan_repo_extracts_symbols_imports_and_docs` | `scan_repo` extracts file symbols, respects `.venv` exclusion, produces *contains* & *imports* edges | 【tests/test_units.py:52】‑​【tests/test_units.py:55】 |
| `test_scan_tolerates_syntax_errors` | `scan_repo` still yields a node for a syntactically broken file | 【tests/test_units.py:61】 |
| `test_write_scan_and_find_graph_roundtrip` | `write_scan` → graph file → `find_graph` equality & loadability | 【tests/test_units.py:67】‑​【tests/test_units.py:69】 |
| `test_parse_findings_block_extracts_and_strips` | `parse_findings_block` strips the fenced block and returns only supported kinds | 【tests/test_units.py:84】 |
| `test_filter_findings_drops_hallucinated_paths` | `filter_findings` removes findings whose paths do not exist (setup begins at line 87) | 【tests/test_units.py:87】 |

## Dependencies
* **Standard library** – `json`, `__future__` annotations.  
* **Third‑party** – `pytest`.  
* **Internal isidore modules** – `findings`, `graph`, `llm`, `pipeline`, `qa`, `render`, `toon` (imported lines 8‑21).  
No other repository components depend on this test file (no inbound imports).

## How to change safely
1. **Preserve imports** – the test suite expects the exact symbols listed at lines 8‑21; adding or removing imports may hide missing coverage.  
2. **Maintain section boundaries** – comment headers (`# ----------------------------------------------------------------------- toon`, etc.) are used by developers for navigation; keep them intact.  
3. **When updating expectations** (e.g., new fields in `scan_repo` output), adjust assertions on the specific lines cited (52‑55, 61, 67‑69) to reflect the new shape, otherwise unrelated tests may fail.  
4. **Run the full pytest suite** after any change to confirm that all six functional areas still pass.  
5. **Avoid hard‑coding temporary‑path structures** beyond what is exercised in the existing tests; the current fixtures (e.g., creating a `.venv` folder) are part of the correctness contract.
