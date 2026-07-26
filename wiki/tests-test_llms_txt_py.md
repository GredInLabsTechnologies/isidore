## Purpose
The `tests/test_llms_txt.py` module verifies the correctness of the `llms.txt` file generation, which serves as a structured wiki for coding agents. The file must adhere to a specific format: starting with an H1 project name, followed by a blockquote summary, and then H2 file lists. The tests ensure the file is written deterministically to the repository root and that it follows the required structure, including the order of sections (`## Start here`, `## Areas`, `## Modules`) and the handling of optional content under `## Optional`.

## Architecture
The module uses a helper function `_wiki(tmp_path)` to create a temporary directory structure with sample Markdown files in a `wiki` subdirectory. These files simulate the expected content of a project's documentation. The main tests then verify that `render_llms_txt` processes this structure correctly, producing a file that meets the specification. The `write_llms_txt` function is tested to ensure it writes the file to the correct location (`LLMS_FILENAME` in the repository root) and that the output is deterministic.

## Key entry points
- `_wiki(tmp_path)`: Creates a temporary directory with sample wiki files for testing.
- `test_the_required_shape_of_the_format(tmp_path)`: Validates the basic structure of the generated `llms.txt` file.
- `test_the_summary_is_the_plain_language_sentence_already_written(tmp_path)`: Ensures the summary is reused from the product page.
- `test_pages_are_layered_and_areas_come_before_modules(tmp_path)`: Checks the section order and content placement.
- `test_skippable_material_sits_under_the_reserved_optional_heading(tmp_path)`: Verifies optional content is correctly marked.
- `test_it_is_written_where_a_fetcher_looks_and_is_deterministic(tmp_path)`: Confirms the file is written to the expected location and is deterministic.
- `test_a_repo_without_a_product_page_still_produces_a_valid_file(tmp_path)`: Tests fallback behavior when the product page is missing.

## Dependencies
The module depends on the `isidore.render` module, which provides the `render_llms_txt` and `write_llms_txt` functions. These functions are imported directly (`tests/test_llms_txt.py:L4`).

## How to change safely
To modify this module, ensure that any changes to the test cases or helper functions do not break the existing structure of the `llms.txt` file. The tests are tightly coupled with the specification, so changes to the file format or generation logic must be reflected in the tests. When adding new tests, follow the existing pattern of verifying the file's structure and content. Avoid introducing non-deterministic behavior in the file generation process.
