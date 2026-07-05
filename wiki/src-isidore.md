## Purpose
`src/isidore` implements an **agent‑oriented wiki compiler** that turns a repository’s structure graph into a set of markdown pages enriched with LLM‑generated prose and machine‑verified *claims* about the code. The core goal is to keep documentation **deterministic and up‑to‑date**: every claim is anchored to a hash of its source lines, enabling *zero‑LLM* staleness detection (i.e. the system can tell when a claim is out of sync without re‑invoking the model)【src/isidore/claims.py:5】.

## Architecture
The module is split into a handful of tightly‑coupled files:

| File | Role | Notable connections |
|------|------|----------------------|
| `pipeline.py` | Orchestrates the compile steps (plan → assemble → generate → cache → lint) and enforces hard limits for LLM calls【src/isidore/pipeline.py:1】. All steps are deterministic except a single bounded LLM call per *dirty* page【src/isidore/pipeline.py:3】. |
| `claims.py` | Defines the *claim* data model, hashing logic (SHA‑256 over ±2 lines, truncated)【src/isidore/claims.py:13】, and utilities for parsing/rendering claim blocks. |
| `graph.py` | Loads the *structure graph* (JSON with `nodes` and `links`) and can scan a repo using the stdlib `ast` to produce such a graph【src/isidore/graph.py:3‑5】. |
| `cli.py` | Exposes user‑facing commands: `scan`, `compile`, `ask`, `suggest-flows`, and `claims`. The `claims` subcommand runs the zero‑LLM staleness audit and can fail the CI run if any claim is stale【src/isidore/cli.py:8】. |
| `findings.py` | Collects *side observations* (LLM residue and deterministic code‑analysis residue) and writes them to `wiki/findings.toon`【src/isidore/findings.py:1‑3】. |
| `qa.py` | Provides a single‑call Q&A interface over the compiled wiki, using keyword scoring rather than embeddings【src/isidore/qa.py:1‑4】. |
| `toon.py`, `llm.py`, `utils.py` (not shown) | Support encoding, LLM interaction, and miscellaneous helpers. |

The most‑connected symbols (`pipeline.py`, `claims.py`, `cli.py`, `graph.py`) form the backbone: the CLI calls into the graph loader, which supplies data to the pipeline; the pipeline calls claim utilities; QA re‑uses pipeline context assembly.

## Key entry points
- **CLI** (`src/isidore/cli.py`): `isidore compile`, `isidore claims --check`, `isidore ask "<question>"`, etc.  
- **Pipeline functions** (`pipeline.py`): `compile_wiki`, `plan_pages`, `assemble_context`, `load_config`, plus default limits (`DEFAULT_MAX_CALLS`, `DEFAULT_MAX_PROMPT_CHARS`, …).  
- **Graph loader** (`graph.py`): `load_graph`, `find_graph`, `scan_repo` (produces `.isidore/graph.json`).  
- **Claims API** (`claims.py`): `anchor_claims`, `parse_claims_block`, `render_claims`, constants `CLAIMS_FILENAME`, `SEARCH_RADIUS`.  

These entry points are the only public surfaces; all other modules are imported exclusively by them.

## Dependencies
`src/isidore` is **self‑contained**: it has **no external cross‑module dependencies** (the “depends on” list is empty). It only relies on the Python standard library (`hashlib`, `json`, `re`, `subprocess`, `ast`, `pathlib`, etc.) and internal sibling modules (`.graph`, `.claims`, `.llm`, `.toon`). No third‑party packages are referenced in the provided excerpts.

## How to change safely
1. **Preserve deterministic behaviour** – The pipeline’s hard limits (max calls, prompt size, timeout) are enforced in code【src/isidore/pipeline.py:7‑9】. Any modification that relaxes these limits must also update the associated documentation and tests, otherwise you risk unbounded LLM usage.  
2. **Do not break claim anchoring** – Claim hashes are derived from a *whitespace‑normalized* window of ±2 lines and truncated to 12 hex chars【src/isidore/claims.py:13‑15】. Changing the hash algorithm or the window size will invalidate existing claim files and break the zero‑LLM staleness gate.  
3. **Maintain graph schema** – The JSON graph format expects `nodes` and `links` (or `edges`) arrays【src/isidore/graph.py:3‑5】. Adding new top‑level keys is safe (they’re ignored), but removing or renaming existing ones will break `scan_repo` and downstream compilation.  
4. **CLI contract** – The `claims` subcommand’s exit‑code semantics (exit 1 on stale claims) are relied on by CI pipelines【src/isidore/cli.py:8】. Preserve this behaviour when refactoring CLI options.  
5. **Run the full test matrix** – Recent commits hardened the system for hostile input and scale【e2a3c37】【4271e60】. After any change, run the suite that includes large‑scale stress tests and CI lint checks to ensure no regression.


<!-- isidore lint: unverified paths: isidore/graph.json -->
