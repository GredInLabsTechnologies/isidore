## Purpose
`tests/test_pipeline.py` tests the compiler pipeline's ability to generate structured documentation from a repository's codebase. It focuses on verifying the correctness of the `plan_pages` function, which selects top-level modules for documentation based on their size and dependencies. The module uses synthetic repositories (`_make_repo`) to simulate real code structures, ensuring the pipeline handles cross-module relationships and filters out small or conceptual nodes.

## Architecture
The module consists of helper functions to create test repositories (`_make_repo`, `_graph`, `_gp`) and test cases for `plan_pages`. The synthetic repositories are structured with modules, symbols, and links to mimic real code dependencies. The tests validate that `plan_pages` correctly filters modules by size (`min_symbols`) and limits output (`top_k`), while preserving cross-module dependencies.

## Key entry points
- `_make_repo`: Generates a synthetic repository with configurable modules and symbols (`tests/test_pipeline.py:L35`).
- `test_plan_pages_selects_top_modules_excluding_small_and_concepts`: Verifies `plan_pages` excludes small modules and conceptual nodes (`tests/test_pipeline.py:L70`).
- `test_plan_pages_top_k_and_none_means_all`: Ensures `top_k` limits output correctly (`tests/test_pipeline.py:L81`).

## Dependencies
The module depends on `isidore.pipeline` for the `plan_pages` function and `pytest` for testing. It does not have external dependencies.

## How to change safely
When modifying `test_pipeline.py`, ensure:
1. Synthetic repositories (`_make_repo`) maintain the expected structure for tests to pass.
2. Test cases for `plan_pages` cover edge cases like small modules and conceptual nodes.
3. Helper functions (`_graph`, `_gp`) correctly parse and return repository data.
