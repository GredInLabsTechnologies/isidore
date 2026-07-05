## Purpose
`src/isidore` implements an **agent‑oriented wiki generator** for a Python codebase.  
It transforms a *structure graph* (a JSON representation of modules, symbols and imports) into deterministic wiki pages, enriches them with optional **LLM‑generated prose**, and exposes a small CLI for scanning, compiling and querying the wiki — all while keeping the number of LLM calls bounded to a single call per dirty page or per question 【src/isidore/pipeline.py:1】, 【src/isidore/cli.py:1】, 【src/isidore/qa.py:1】.

The module’s core responsibilities are:

* **Graph ingestion** – reading or building the repository graph (nodes, links, commit)【src/isidore/graph.py:1】.  
* **Compilation pipeline** – planning pages, assembling contexts, generating prose, caching results, and linting citations【src/isidore/pipeline.py:1】.  
* **Side‑effect harvesting** – collecting deterministic “findings” (TODOs, orphan files, risk hotspots) and LLM‑produced observations, stored separately from wiki prose【src/isidore/findings.py:1】.  
* **Question answering** – a single bounded LLM call that scores keyword relevance against the compiled wiki and graph, returning citations or a “no evidence” response【src/isidore/qa.py:1】.  
* **Rendering** – producing deterministic artefacts (`quickstart.md`, `index.toon`, `AGENTS.md`) that cost no LLM calls【src/isidore/render.py:1】.

## Architecture
The module is organized around a small set of tightly coupled files:

| File | Role | Notable symbols |
|------|------|-----------------|
| **pipeline.py** | Orchestrates the compile workflow: `plan_pages`, `assemble_context`, `compile_wiki`, plus hard limits (`DEFAULT_MAX_CALLS`, etc.)【src/isidore/pipeline.py:1】 |
| **cli.py** | User‑facing entry point exposing subcommands (`scan`, `compile`, `ask`, `suggest-flows`) that delegate to the other modules【src/isidore/cli.py:1】 |
| **graph.py** | Loads, validates and (if missing) generates the structure graph via a pure‑stdlib AST scanner【src/isidore/graph.py:1】 |
| **findings.py** | Defines the file naming constants (`FINDINGS_FILENAME`, `FINDINGS_PROMPT_ADDENDUM`) and helper functions (`filter_findings`, `harvest_todos`, `orphan_file_candidates`) used by the pipeline【src/isidore/pipeline.py:21】 |
| **qa.py** | Implements the `ask` subcommand: pulls the graph, assembles context, and runs a single LLM call using the pipeline’s prompt templates【src/isidore/qa.py:1】 |
| **render.py** | Generates deterministic, LLM‑free outputs (`quickstart.md`, markers, `WIKI_DIRNAME`) and encodes tables via `toon.encode`【src/isidore/render.py:1】 |
| **toon.py** (imported) | Provides the `encode` function used by `render.py` (import shown)【src/isidore/render.py:8】 |
| **llm.py** (imported) | Supplies `default_generator` and `GenerationError` used by the CLI for LLM calls【src/isidore/cli.py:17】 |

The **dependency graph** is flat: `src/isidore` has **no external module dependencies** beyond the Python standard library and its own sibling files【depends on (cross-module, link count): (none)】. This isolation simplifies testing and versioning.

## Key entry points
| Entry point | File & line | How it is used |
|------------|-------------|----------------|
| `cli.main()` (implicit) | `src/isidore/cli.py:1` | Parses `argparse` subcommands (`scan`, `compile`, `ask`, `suggest-flows`). |
| `compile_wiki` | `src/isidore/pipeline.py:...` (imported in CLI) | Drives the full compile sequence; respects limits (`DEFAULT_MAX_CALLS`, `DEFAULT_MAX_PROMPT_CHARS`, etc.) |
| `plan_pages` / `assemble_context` | `src/isidore/pipeline.py:...` | Internal helpers for page planning and context construction, consumed by both compile and QA. |
| `load_graph`, `write_scan` | `src/isidore/graph.py:...` (imported in CLI) | Load an existing graph JSON or generate one via `scan_repo` when missing. |
| `ask` (CLI subcommand) | `src/isidore/cli.py:...` → `src/isidore/qa.py:1` | Performs a single LLM call after keyword scoring, returns citations. |
| `render_quickstart` | `src/isidore/render.py:15` | Produces the human‑readable `quickstart.md` that references the generated wiki and findings. |

These functions are the only public surfaces that external tooling or CI should invoke.

## Dependencies
* **Standard library**: `hashlib`, `json`, `re`, `subprocess`, `collections`, `dataclasses`, `pathlib`, `ast` (used across `pipeline.py`, `graph.py`, etc.).  
* **Internal sibling modules**: `findings`, `graph`, `qa`, `render`, `llm`, `toon`. All imports are relative (`from .module import …`) and resolve within `src/isidore`. No third‑party packages are referenced in the extracted snippets.  
* **No external dependents**: The module is not imported by any other package in the repository【depended on by: (none)】.

## How to change safely
1. **Preserve the JSON graph contract** – `graph.py` documents the exact schema expected (`nodes`, `links`, optional `built_at_commit`)【src/isidore/graph.py:3-9】. Any modification to node/link fields must retain backward‑compatible keys or be ignored by the pipeline (extra fields are deliberately ignored)【src/isidore/graph.py:14】.  
2. **Do not increase LLM calls** – The pipeline enforces a single bounded LLM call per dirty page and per QA request. Changing default limits (`DEFAULT_MAX_CALLS`, `DEFAULT_MAX_PROMPT_CHARS`, etc.) should be done with care, and the associated constants are imported by the CLI【src/isidore/cli.py:18-24】.  
3. **Update CLI subcommands atomically** – When adding a new subcommand, route it through `argparse` in `cli.py` and import the implementation from a dedicated module to keep the dependency graph flat.  
4. **Maintain deterministic rendering** – `render.py` must continue to produce outputs without invoking the LLM. Adding side‑effects or external data sources here would break the “no LLM cost” guarantee.  
5. **Test both graph generation and compile paths** – Use the `scan_repo` path (when no graph exists) to ensure the AST scanner still produces a valid JSON structure, then run `compile_wiki` in dry‑run mode (`--execute` omitted) to verify that no unexpected LLM calls are triggered.  
6. **Keep findings separation** – New residue categories should be added to `findings.py` constants and handled by `filter_findings` to remain distinct from the main wiki content, preserving the triage semantics described in the docstring【src/isidore/findings.py:1-9】.

Following these guidelines maintains the deterministic, low‑cost behavior that `src/isidore` promises to coding agents.
