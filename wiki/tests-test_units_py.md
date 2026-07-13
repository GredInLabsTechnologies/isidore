> [!WARNING]
> **SECURITY — deterministic detectors flagged this code (0 LLM). Verify; never document as an intended feature.**
>
> - `tests/test_units.py:268` — credential-shaped literal (sk- prefix)
## Purpose
`tests/test_units.py` contains unit tests for core Isidore subsystems: the toon encoder, graph scanner, findings residue, QA retrieval, and LLM request helpers. It verifies that small, isolated components behave as expected under controlled inputs, ensuring that parsing, encoding, and graph-building utilities remain reliable as the codebase evolves.

## Architecture
The file is organized into thematic test groups introduced by comments (`# ----------------------------------------------------------------------- toon`, `# ---------------------------------------------------------------------- graph`). Each test imports only the symbols it exercises, keeping dependencies explicit and tests independent. The module does not depend on other test modules and is not depended on by them, making it a leaf in the test hierarchy.

## Key entry points
- `test_toon_encode_table_quoting_and_counts`: validates that `encode_table` in `isidore.toon` produces correct quoted CSV lines and counts for mixed scalar and None values.
- `test_module_of_normalizes_and_buckets`: checks that `module_of` in `isidore.graph` normalizes path separators and buckets files under the correct module path, including a sentinel for non-file inputs.
- `test_scan_repo_extracts_symbols_imports_and_docs`: exercises `scan_repo` in `isidore.graph` to confirm it indexes Python files, classes, functions, and Markdown docs while excluding `.venv` artifacts.
- `test_scan_tolerates_syntax_errors`: verifies that `scan_repo` still produces a node for a syntactically invalid file rather than crashing.
- `test_write_scan_and_find_graph_roundtrip`: tests that `write_scan` and `find_graph` in `isidore.graph` produce consistent graph artifacts and that `load_graph` can read them back.
- `test_scan_excludes_gitignored_build_artifacts`: ensures `scan_repo` respects `.gitignore` and does not index ignored build artifacts.

## Dependencies
- Standard library: `json`, `pytest`
- Internal modules:
  - `isidore.toon.encode_table`
  - `isidore.graph.{GraphError, find_graph, load_graph, module_of, scan_repo, write_scan}`
  - `isidore.findings.{filter_findings, harvest_todos, orphan_file_candidates, parse_findings_block, render_findings, coverage_gap_candidates}`
  - `isidore.llm.build_request`
  - `isidore.pipeline.PageSpec`
  - `isidore.qa.{ask, gather_evidence, question_terms}`
  - `isidore.render.render_toon_index`

## How to change safely
- Add new tests under the appropriate section comment to keep related cases together.
- When modifying graph-related tests, ensure they still pass after changes to `scan_repo`, `write_scan`, or `find_graph`; these functions are the primary contract for repository introspection.
- If a test exercises a helper that is later removed, delete the test and update the imports accordingly to keep the file buildable.
- Keep assertions focused on one behavior per test to simplify failure diagnosis and reduce merge conflicts when multiple features change.
