## Purpose
`tests/test_pipeline.py` houses **unit tests for the compiler pipeline**.  
The module’s docstring makes it clear the tests run **without network access**, injecting a deterministic LLM generator instead of calling an external service【tests/test_pipeline.py:1】.  
Its goal is to verify that pipeline helpers (e.g., `plan_pages`) behave correctly on a synthetic repository graph.

## Architecture
The file is self‑contained except for imports from the `isidore` package and `pytest`.  

* **Helper factories** – `_node`, `_link`, `_make_repo`, `_graph`, and `_gp` build a temporary repository, materialise a JSON graph (`graph.json`) and expose it to the tests.  
  * `_node` returns a dict describing a graph node【tests/test_pipeline.py:27】.  
  * `_link` returns a dict describing an edge【tests/test_pipeline.py:32】.  
  * `_make_repo` writes `graph.json` under `graphify-out` with the collected nodes/links【tests/test_pipeline.py:54】.  
  * `_graph` reads that file and yields the `nodes` and `links` arrays【tests/test_pipeline.py:61】.  
  * `_gp` simply returns the path to `graph.json`【tests/test_pipeline.py:65】.  

* **Test cases** – each `test_*` function exercises a public pipeline routine imported from `isidore.pipeline`.  
  * `test_plan_pages_selects_top_modules_excluding_small_and_concepts` checks that `plan_pages` filters out “concept” nodes and tiny modules, returning only the three core module directories【tests/test_pipeline.py:78】.  
  * `test_plan_pages_top_k_and_none_means_all` validates the `top_k` parameter: `top_k=2` yields exactly two specs, while `top_k=None` yields all three【tests/test_pipeline.py:85】.  
  * `test_plan_pages_records_cross_module_deps` is declared to verify cross‑module dependencies, though its body is not shown in the excerpt【tests/test_pipeline.py:88】.

The tests combine the synthetic graph with the real pipeline logic to assert correct selection and ordering of documentation pages.

## Key entry points
| Entry point | Role |
|-------------|------|
| `test_plan_pages_selects_top_modules_excluding_small_and_concepts` | Validates module‑level filtering in `plan_pages`. |
| `test_plan_pages_top_k_and_none_means_all` | Checks `top_k` handling (limiting vs. full output). |
| `_make_repo` | Constructs a mock repository and writes `graph.json`. |
| `_graph` | Loads the mock graph for test consumption. |
| `_node`, `_link` | Simple factories that produce the JSON‑serialisable graph elements used by `_make_repo`. |

## Dependencies
* **Standard library** – `json`, `pathlib.Path`.  
* **Third‑party** – `pytest`.  
* **isidore package** –  
  * `isidore.llm.GenerationError` (imported but not used in the shown tests).  
  * Pipeline utilities: `assemble_context`, `compile_wiki`, `context_hash`, `lint_cited_paths`, `plan_flows`, `plan_pages`, `prompt_for`, `read_excerpt`, `suggest_flows`.  
  * Rendering symbols: `MARKER_END`, `MARKER_START`, `agents_md_block`, `upsert_agents_block`.  

No other modules import or depend on `tests/test_pipeline.py`.

## How to change safely
1. **Maintain the synthetic graph contract** – if you adjust `_node` or `_link`, ensure the resulting JSON still contains the keys asserted by the tests (`id`, `source_file`, `file_type`, `label`, `source_location` for nodes; `source`, `target`, `relation` for links).  
2. **Preserve the file layout** – `plan_pages` expects the module directory string (e.g., `"mod0/core"`). Changing the output path in `_make_repo` will break the assertions in `test_plan_pages_*`.  
3. **Do not introduce network calls** – the purpose clause explicitly forbids external LLM calls; keep the test environment self‑contained.  
4. **Update corresponding assertions** – if you modify the filtering criteria (e.g., the `min_symbols` threshold), adjust the expected list in `test_plan_pages_selects_top_modules_excluding_small_and_concepts` (line 78) and the length checks in `test_plan_pages_top_k_and_none_means_all` (lines 84‑85).  
5. **Run the full pytest suite** after any change to catch regressions in both helper functions and the imported pipeline logic.
