## Purpose
The module `tests/test_wiki_not_input.py` enforces a critical invariant: the wiki must never be treated as input to the system. This is a safety measure to prevent the wiki from being processed as source code, which could lead to infinite recursion or incorrect documentation. The tests verify that the wiki is correctly identified as output and excluded from the input pipeline.

## Architecture
The module uses pytest fixtures to create a controlled environment that mimics the structure of the repository where the wiki is nested within a deeper directory structure (`doc/isidore`). The tests validate that the wiki is properly recognized as output and excluded from the input processing pipeline. The key components include:
- `nested_wiki_dir`: A fixture that sets up the wiki directory structure.
- `repo_with_nested_wiki`: A fixture that creates a temporary repository with a nested wiki directory and sample files.
- Test functions that verify the wiki is not indexed as input and is excluded from page planning.

## Key entry points
- `nested_wiki_dir()`: Pytest fixture that monkeypatches `isidore.render.WIKI_DIRNAME` to `"doc/isidore"`, mirroring GIMO's layout (`tests/test_wiki_not_input.py:28-L33`).
- `repo_with_nested_wiki()`: Pytest fixture creating a repo with `src/app/core.py [⚠ isidore: path not found]` and 6 wiki pages under `doc/isidore/`, plus `index.toon` and a certificate (`tests/test_wiki_not_input.py:37-L53`).
- `test_the_prefix_is_a_path_not_a_name()`: Asserts `wiki_output_prefix()` returns `"doc/isidore"` and `_is_wiki_output` matches paths under that prefix but not similarly-named files (`tests/test_wiki_not_input.py:57-L65`).
- `test_the_scanner_does_not_index_its_own_output()`: Asserts `scan_repo` indexes `src/app/core.py [⚠ isidore: path not found]` but not any `doc/isidore` files (`tests/test_wiki_not_input.py:68-L73`).
- `test_no_page_is_planned_for_the_wiki_itself()`: Builds a foreign graph with 2 real nodes + 40 wiki nodes, asserts `drop_wiki_output` returns 2 and `plan_pages` excludes all wiki entries (`tests/test_wiki_not_input.py:77-L92`).
- `test_a_compile_of_a_repo_with_a_committed_wiki_stays_clean()`: End-to-end scan → plan asserting no wiki pages survive (`tests/test_wiki_not_input.py:95-L101`).

## Dependencies
The module depends on three cross-module imports:
- `src/isidore/graph.py` (1 link) — for `_is_wiki_output`, `scan_repo`, `wiki_output_prefix` (`tests/test_wiki_not_input.py:18`).
- `src/isidore/pipeline.py` (1 link) — for `MAX_CERT_VIOLATIONS`, `degenerate_certificate`, `drop_wiki_output`, `plan_pages` (`tests/test_wiki_not_input.py:19-L24`).
- `src/isidore/render.py` (1 link) — accessed via monkeypatch of `WIKI_DIRNAME` in the `nested_wiki_dir` fixture (`tests/test_wiki_not_input.py:31-L32`).

## How to change safely
When modifying this module, ensure that:
- The wiki directory structure is correctly represented in the fixtures.
- The tests continue to verify that the wiki is not treated as input.
- The dependencies on `isidore.graph` and `isidore.pipeline` are maintained.
