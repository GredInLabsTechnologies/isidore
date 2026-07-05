## Purpose
`tests/test_pipeline.py` validates the **compiler pipeline** without making network calls. The top‑level docstring states the suite runs “no network: the LLM generator is always injected and counted”【tests/test_pipeline.py:L1】. Its primary goal is to ensure that page‑planning logic (`plan_pages`) behaves correctly given synthetic repository data.

## Architecture
The file is organized into three layers:

1. **Test helpers** – functions that fabricate a fake repository and supply graph data:
   * `_node` builds a node descriptor dictionary【tests/test_pipeline.py:L26】.
   * `_link` builds a link descriptor dictionary【tests/test_pipeline.py:L31】.
   * `_make_repo` creates a temporary directory hierarchy, writes placeholder Python files, README documents, and a `graph.json` file that aggregates the generated nodes and links【tests/test_pipeline.py:L35-L55】.
   * `_graph` loads that JSON and returns the node and link lists【tests/test_pipeline.py:L59-L61】.
   * `_gp` returns the path to the generated `graph.json` file【tests/test_pipeline.py:L64-L65】.

2. **Test cases** – each `test_…` function invokes the helpers to construct input data, calls a pipeline function, and asserts on its output:
   * `test_plan_pages_selects_top_modules_excluding_small_and_concepts` checks that `plan_pages` drops concept‑type nodes and modules whose symbol count is below `min_symbols`【tests/test_pipeline.py:L70-L78】.
   * `test_plan_pages_top_k_and_none_means_all` verifies that the `top_k` argument limits the number of returned page specs, and that `None` yields all specs【tests/test_pipeline.py:L81-L86】.
   * `test_plan_pages_records_cross_module_deps` begins a scenario meant to exercise cross‑module dependency handling【tests/test_pipeline.py:L88-L89】.

3. **Imports & constants** – the module pulls in the pipeline API (`assemble_context`, `compile_wiki`, `context_hash`, `lint_cited_paths`, `plan_flows`, `plan_pages`, `prompt_for`, `read_excerpt`, `suggest_flows`)【tests/test_pipeline.py:L9-L20】, rendering utilities (`MARKER_END`, `MARKER_START`, `agents_md_block`, `upsert_agents_block`)【tests/test_pipeline.py:L21】, and testing tools (`pytest`, `json`, `Path`)【tests/test_pipeline.py:L4-L8】.

## Key entry points
| Entry point | Role |
|------------|------|
| `_node` | Constructs a node dictionary used by the fake graph. |
| `_link` | Constructs a link dictionary used by the fake graph. |
| `_make_repo` | Generates a synthetic repository with source files, READMEs, and a `graph.json` output. |
| `_graph` | Reads `graph.json` and returns `(nodes, links)`. |
| `test_plan_pages_selects_top_modules_excluding_small_and_concepts` | Asserts that `plan_pages` filters out concept nodes and modules with too few symbols. |
| `test_plan_pages_top_k_and_none_means_all` | Asserts the `top_k` limiting behaviour of `plan_pages`. |
| `test_plan_pages_records_cross_module_deps` | Intended to verify that `plan_pages` records dependencies across modules. |

## Dependencies
* **Standard library** – `json`, `pathlib.Path`, `pytest`.  
* **Isidore packages** – `isidore.llm.GenerationError` (imported but not directly used in the visible tests)【tests/test_pipeline.py:L9】; `isidore.pipeline` symbols listed above【tests/test_pipeline.py:L10-L20】; `isidore.render` markers and helpers【tests/test_pipeline.py:L21】.  
* **No external services** – the tests run entirely offline, matching the “no network” promise.

## How to change safely
1. **Preserve helper signatures** – `_node`, `_link`, `_make_repo`, `_graph`, and `_gp` are relied upon by multiple test cases. Changing parameter names or return types will break imports and assertions.  
2. **Maintain graph schema** – `plan_pages` expects nodes with keys `id`, `source_file`, `file_type`, `label`, `source_location`. Adding or renaming keys requires updating the test expectations (e.g., the assertions in `test_plan_pages_*`).  
3. **Respect filtering logic** – tests encode assumptions about `plan_pages`:
   * Nodes of `file_type="concept"` are ignored (see the addition of a concept node in the first test)【tests/test_pipeline.py:L73-L78】.  
   * Modules with fewer than `min_symbols` symbols are excluded (the “tiny” node added with default `file_type="code"` should not appear)【tests/test_pipeline.py:L74-L78】.  
   * `top_k` limits the number of returned specs; `None` means “all”【tests/test_pipeline.py:L84-L86】.  
   If you modify `plan_pages` or its contract, update these tests accordingly.  
4. **Do not introduce network calls** – the suite’s purpose is to verify offline behaviour; adding HTTP requests or external LLM calls will cause failures unrelated to the pipeline logic.  
5. **Run the full test matrix** after any change to ensure all three `test_plan_pages_*` cases still pass, as they collectively cover filtering, limiting, and cross‑module dependency handling.

---
