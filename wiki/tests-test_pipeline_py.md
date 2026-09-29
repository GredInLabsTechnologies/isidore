## Purpose
`tests/test_pipeline.py` tests the compiler pipeline's ability to generate structured documentation from a repository's codebase. It focuses on verifying the correctness of the `plan_pages` function, which selects top-level modules for documentation based on their size and dependencies. The module uses synthetic repositories (`_make_repo`) to simulate real code structures, ensuring the pipeline handles cross-module relationships and filters out small or conceptual nodes.

## Architecture
The module consists of helper functions to create test repositories (`_make_repo`, `_graph`, `_gp`) and test cases for `plan_pages`. The synthetic repositories are structured with modules, symbols, and links to mimic real code dependencies. The tests validate that `plan_pages` correctly filters modules by size (`min_symbols`) and limits output (`top_k`), while preserving cross-module dependencies.

## Key entry points
- `_node()`: Factory that builds a node dict with `id`, `source_file`, `file_type`, `label`, `source_location` (`tests/test_pipeline.py:26-L28`).
- `_link()`: Factory that builds a link dict with `source`, `target`, `relation` (`tests/test_pipeline.py:31-L32`).
- `_make_repo()`: Generates a synthetic repository with configurable `n_modules` (default 3) and `symbols_per_module` (default 12), writing `graph.json` into `graphify-out/` (`tests/test_pipeline.py:35-L56`).
- `_graph()`: Reads `graph.json` and returns `(nodes, links)` (`tests/test_pipeline.py:59-L61`).
- `_gp()`: Returns the path to `graph.json` (`tests/test_pipeline.py:64-L65`).
- `test_plan_pages_selects_top_modules_excluding_small_and_concepts`: Verifies `plan_pages` excludes small modules and conceptual nodes (`tests/test_pipeline.py:70`).
- `test_plan_pages_top_k_and_none_means_all`: Ensures `top_k` limits output correctly and `None` means all (`tests/test_pipeline.py:81`).
- `test_plan_pages_records_cross_module_deps`: Verifies cross-module dependency recording with `n_modules=2` (`tests/test_pipeline.py:88`).

## Dependencies
The module depends on four cross-module imports:
- `src/isidore/llm.py` (1 link) — for `GenerationError` (`tests/test_pipeline.py:9`).
- `src/isidore/pipeline.py` (1 link) — for `assemble_context`, `compile_wiki`, `context_hash`, `lint_cited_paths`, `plan_flows`, `plan_pages`, `prompt_for`, `read_excerpt`, `suggest_flows` (`tests/test_pipeline.py:10-L19`).
- `src/isidore/render.py` (1 link) — for `MARKER_END`, `MARKER_START`, `agents_md_block`, `upsert_agents_block` (`tests/test_pipeline.py:21`).
- `src/isidore/graph.py` (1 link) — imported by the test module.

## How to change safely
When modifying `test_pipeline.py`, ensure:
1. Synthetic repositories (`_make_repo`) maintain the expected structure for tests to pass.
2. Test cases for `plan_pages` cover edge cases like small modules and conceptual nodes.
3. Helper functions (`_graph`, `_gp`) correctly parse and return repository data.
