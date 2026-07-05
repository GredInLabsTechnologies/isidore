## Purpose
`tests/test_pipeline.py` validates the **compiler pipeline** logic in an isolated, network‑free environment.  
The module’s docstring states the intention clearly: it “always injects the LLM generator and counts” it, ensuring that pipeline components can be exercised without external calls【tests/test_pipeline.py:1】. The primary focus of the tests is the **page planning** functionality (`plan_pages`) while providing a full synthetic repository to feed the pipeline.

## Architecture
The file is organized into three layers:

1. **Test scaffolding helpers** – Functions that build a fake repository and expose its graph data:
   * `_node` creates a node dictionary for the graph【tests/test_pipeline.py:26】.
   * `_link` creates an edge dictionary between two nodes【tests/test_pipeline.py:31】.
   * `_make_repo` populates a temporary directory with a configurable number of modules, source files, and a `graph.json` file describing the nodes and links【tests/test_pipeline.py:35】‑【tests/test_pipeline.py:56】.
   * `_graph` loads `graph.json` and returns the node/link collections【tests/test_pipeline.py:59】‑【tests/test_pipeline.py:61】.
   * `_gp` yields the path to the generated `graph.json`【tests/test_pipeline.py:64】‑【tests/test_pipeline.py:65】.

2. **Imports** – The test module brings in the pipeline API (`assemble_context`, `compile_wiki`, `context_hash`, `lint_cited_paths`, `plan_flows`, `plan_pages`, `prompt_for`, `read_excerpt`, `suggest_flows`) and rendering markers (`MARKER_END`, `MARKER_START`, `agents_md_block`, `upsert_agents_block`) to ensure the pipeline’s public surface is available during test execution【tests/test_pipeline.py:9-L21】. The `GenerationError` import hints at future LLM‑related checks.

3. **Test cases** – Concrete `pytest` functions that invoke `plan_pages` on the synthetic graph and assert expected outcomes:
   * `test_plan_pages_selects_top_modules_excluding_small_and_concepts` verifies that modules with fewer than `min_symbols` symbols and “concept” nodes are filtered out【tests/test_pipeline.py:70-L78】.
   * `test_plan_pages_top_k_and_none_means_all` checks that `top_k` limits the result set and that `None` selects all modules【tests/test_pipeline.py:81-L86】.
   * Additional tests (e.g., `test_plan_pages_records_cross_module_deps`) are hinted at but not fully shown, indicating broader coverage of cross‑module dependencies.

## Key entry points
| Symbol | Role | Location |
|--------|------|----------|
| `_node` | Constructs a graph node dict used by the synthetic repo | 【tests/test_pipeline.py:26】 |
| `_link` | Constructs a graph edge dict linking nodes | 【tests/test_pipeline.py:31】 |
| `_make_repo` | Generates a temporary repository with source files and a `graph.json` artifact | 【tests/test_pipeline.py:35】‑【tests/test_pipeline.py:56】 |
| `_graph` | Reads the generated `graph.json` into Python structures for the tests | 【tests/test_pipeline.py:59】‑【tests/test_pipeline.py:61】 |
| `test_plan_pages_selects_top_modules_excluding_small_and_concepts` | Asserts that only sufficiently large modules are turned into page specs | 【tests/test_pipeline.py:70】‑【tests/test_pipeline.py:78】 |
| `test_plan_pages_top_k_and_none_means_all` | Confirms the `top_k` parameter’s slicing behavior | 【tests/test_pipeline.py:81】‑【tests/test_pipeline.py:86】 |

These helpers feed the **pipeline** entry point `plan_pages`, which is the core function under test.

## Dependencies
* **Standard library** – `json`, `pathlib.Path`.
* **Third‑party** – `pytest` for test execution.
* **Internal** – `isidore.llm.GenerationError` (imported but not exercised in the shown tests) and a suite of symbols from `isidore.pipeline` and `isidore.render` that provide the public API under test【tests/test_pipeline.py:9-L21】.
* **No external network** – The test environment deliberately avoids external calls, as indicated by the docstring.

## How to change safely
1. **Preserve the synthetic graph contract** – `_make_repo` must continue to emit a `graph.json` with top‑level keys `"nodes"` and `"links"` and a `"built_at_commit"` string. Any structural change will break `_graph` and downstream `plan_pages` expectations.
2. **Maintain node/link schema** – The dictionaries produced by `_node` and `_link` should keep the fields `id`, `source_file`, `file_type`, `label`, `source_location` (for nodes) and `source`, `target`, `relation` (for links). Tests rely on these keys when filtering by `file_type` or counting symbols.
3. **Update test expectations in tandem** – If the `plan_pages` signature or default filtering logic changes (e.g., different `min_symbols` default), adjust the assertions in the test functions accordingly.
4. **Retain import list** – Even if some imported pipeline functions are not used in the currently visible tests, they may be exercised by hidden tests. Removing them could cause import‑time failures.
5. **Do not introduce network calls** – Keep the “no network” guarantee; any new test code should mock or inject LLM generators if LLM interaction becomes necessary.

---
