## Purpose
The module `tests/test_wiki_not_input.py` enforces a critical invariant: the wiki must never be treated as input to the system. This is a safety measure to prevent the wiki from being processed as source code, which could lead to infinite recursion or incorrect documentation. The tests verify that the wiki is correctly identified as output and excluded from the input pipeline.

## Architecture
The module uses pytest fixtures to create a controlled environment that mimics the structure of the repository where the wiki is nested within a deeper directory structure (`doc/isidore`). The tests validate that the wiki is properly recognized as output and excluded from the input processing pipeline. The key components include:
- `nested_wiki_dir`: A fixture that sets up the wiki directory structure.
- `repo_with_nested_wiki`: A fixture that creates a temporary repository with a nested wiki directory and sample files.
- Test functions that verify the wiki is not indexed as input and is excluded from page planning.

## Key entry points
The primary entry points are the test functions:
- `test_the_prefix_is_a_path_not_a_name`: Verifies that the wiki output prefix is correctly identified as a path, not just a name.
- `test_the_scanner_does_not_index_its_own_output`: Ensures the scanner does not index the wiki as input.
- `test_no_page_is_planned_for_the_wiki_itself`: Confirms that no pages are planned for the wiki itself.

## Dependencies
The module depends on:
- `isidore.graph`: For functions like `_is_wiki_output`, `scan_repo`, and `wiki_output_prefix`.
- `isidore.pipeline`: For functions like `drop_wiki_output` and `plan_pages`.

## How to change safely
When modifying this module, ensure that:
- The wiki directory structure is correctly represented in the fixtures.
- The tests continue to verify that the wiki is not treated as input.
- The dependencies on `isidore.graph` and `isidore.pipeline` are maintained.
