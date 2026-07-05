## Purpose
Isidore exists to **compile an agent‑oriented wiki from a repository’s structure graph** — a deterministic knowledge base that agents can query with minimal LLM usage 【src/isidore/cli.py:1】. It turns the graph’s structural facts into prose pages, an index, and ancillary observations, while keeping every LLM interaction bounded and auditable 【src/isidore/pipeline.py:1-5】.

## Architecture
The module is a self‑contained pipeline made of several tightly coupled files:

| Component | Role | Key connections |
|----------|------|-----------------|
| **cli.py** | Entry‑point for users; defines subcommands (`scan`, `compile`, `ask`, `suggest-flows`, `claims`) 【src/isidore/cli.py:3-8】 | imports `graph`, `llm`, `pipeline` |
| **graph.py** | Loads or builds the **structure graph** (JSON format with `nodes` and `links`) 【src/isidore/graph.py:3-9】; provides `scan_repo()` that uses only the stdlib `ast` module to create nodes from top‑level functions/classes and links from imports 【src/isidore/graph.py:16-18】 | consumed by `pipeline`, `qa`, `cli` |
| **pipeline.py** | Core compilation steps: **plan → assemble → generate → cache → lint**, each deterministic; the only non‑deterministic step is a single bounded LLM call per dirty page 【src/isidore/pipeline.py:1-5】. It also defines runtime limits (max calls, prompt size, timeout) 【src/isidore/pipeline.py:7-9】. | exposed via `compile_wiki`, `load_config` to `cli` |
| **render.py** | Generates **deterministic artefacts** (`quickstart.md`, `index.toon`, `AGENTS.md`) without any LLM call 【src/isidore/render.py:1-4】; defines `WIKI_DIRNAME`, marker constants, and `render_quickstart`. | called after `pipeline` completes |
| **findings.py** | Harvests **side observations** (“residue”) during compilation: *LLM residue* (model‑generated hypotheses) and *deterministic residue* (TODO/FIXME, orphan files, risk hotspots) 【src/isidore/findings.py:1-9】【src/isidore/findings.py:19-22】. All output lands in `wiki/findings.toon`. | consumes data from `pipeline` |
| **qa.py** | Provides a **single‑call Q&A** interface over the compiled wiki + graph; relevance is computed by keyword scoring, not embeddings 【src/isidore/qa.py:1-5】. | uses `graph.load_graph` and `pipeline` helpers (`plan_pages`, `assemble_context`, `read_excerpt`) |
| **Other helpers** (`claims`, `llm`, `toon`) are imported but not listed among the nine core files; they supply claim handling, LLM generation, and TOON encoding respectively. |

The architecture deliberately avoids external services: there are **no cross‑module dependencies** and **no external dependants** 【Facts】, making the wiki generation fully reproducible from the graph alone.

## Key entry points
- **CLI subcommands** (entry for agents or developers):
  - `scan` – builds `.isidore/graph.json` via the AST scanner 【src/isidore/cli.py:4】  
  - `compile` – runs the full compilation pipeline (dry‑run by default) 【src/isidore/cli.py:5】  
  - `ask` – answers a single question with one LLM call 【src/isidore/cli.py:6】  
  - `suggest-flows` – prints heavy cross‑module bridges for `isidore.json` 【src/isidore/cli.py:7】  
  - `claims` – audits claim staleness without LLM 【src/isidore/cli.py:8】  

- **Programmatic functions**
  - `pipeline.compile_wiki` – orchestrates the five deterministic stages plus the bounded LLM call 【src/isidore/pipeline.py:1-5】  
  - `graph.find_graph`, `graph.load_graph`, `graph.write_scan` – graph I/O utilities 【src/isidore/cli.py:17】  
  - `render.render_quickstart` – builds the human‑readable quickstart markdown 【src/isidore/render.py:15-23】  
  - `qa.QA_PROMPT` and helper functions (`assemble_context`, `plan_pages`, `read_excerpt`) for answering queries 【src/isidore/qa.py:13-20】  

## Dependencies
Isidore is **stand‑alone**:
- **Internal imports only** (e.g., `from .graph import …`, `from .pipeline import …`). No third‑party libraries are referenced in the extracted files.  
- The only external tool used is the Python **stdlib** `ast` module for graph scanning 【src/isidore/graph.py:23】.  
- LLM interaction is abstracted behind `llm.default_generator` and `GenerationError`, but these are confined to the `pipeline`/`cli` layer and do not introduce additional package dependencies.

## How to change safely
1. **Preserve the JSON graph schema** – nodes must still contain `id`, `label`, `file_type`, `source_file`, `source_location`; extra fields are ignored 【src/isidore/graph.py:5-14】. Altering field names will break `pipeline` planning.  
2. **Do not remove the single LLM call contract** – the pipeline expects **exactly one bounded call per dirty page**; any change that adds calls must also respect the hard limits (`DEFAULT_MAX_CALLS`, `DEFAULT_MAX_PROMPT_CHARS`, timeout) documented in `pipeline.py` 【src/isidore/pipeline.py:7-9】.  
3. **Maintain deterministic stages** – `plan`, `assemble`, `generate`, `cache`, `lint` must remain pure functions; introducing nondeterminism will invalidate the “deterministic except LLM” guarantee.  
4. **Update CLI help strings** if you rename subcommands or alter their behavior, keeping the documentation in sync with the code 【src/isidore/cli.py:3-8】.  
5. **Run the `claims` audit** after modifications that affect generated prose; it will exit with status 1 if any claim becomes stale 【src/isidore/cli.py:8】.  
6. **Regenerate `quickstart.md` and `index.toon` via `render.render_quickstart`** to verify that no new LLM calls were introduced, as these files are required to be deterministic 【src/isidore/render.py:1-4】.  

Following these steps ensures that the wiki remains reproducible, auditable, and safe for downstream coding agents.


<!-- isidore lint: unverified paths: isidore/graph.json -->
