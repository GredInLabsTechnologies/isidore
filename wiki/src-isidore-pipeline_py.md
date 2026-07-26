## Purpose
The `pipeline.py` module implements the core compiler pipeline for generating documentation pages from code. It transforms the static structure graph (nodes and links) into dynamic `PageSpec` objects that define what pages to generate, their content, and their relationships. The pipeline is deterministic except for a single bounded LLM call per dirty page, ensuring reproducibility while delegating prose generation to the model. Key constraints are hardcoded: a maximum of `--max-calls` per run, a per-prompt character budget, a single model, and a fixed timeout per call.

## Architecture
The pipeline consists of three main phases:
1. **Planning**: Determines which pages to generate (`plan_pages` and `plan_flows`).
2. **Assembly**: Prepares the content for each page (not shown in the excerpts).
3. **Generation**: Delegates prose generation to the LLM (not shown in the excerpts).

The `PageSpec` dataclass centralizes all page metadata, including dependencies, hot symbols, and flow edges. The pipeline shares the `module_dep_edges` function with the impact fingerprint to ensure consistency in the coupling graph.

## Key entry points
- `plan_pages`: Selects top-K modules with the most code symbols, excluding those below a minimum threshold.
- `plan_flows`: Generates cross-cutting flow pages by BFS from user-declared seeds in `isidore.json`.
- `module_dep_edges`: Computes cross-module dependency edges for both page planning and impact analysis.

## Dependencies
The module depends on:
- `changeset.py`: For affected modules and changed symbols.
- `journal.py`: For telemetry and run recording.
- `claims.py`: For claim anchoring and linting.
- `graph.py`: For the structure graph (nodes and links).
- `llm.py`: For prose generation.
- `pcp.py`: For tamper-evident certificates.
- `verify.py`: For claim verification.

## How to change safely
1. **Add a new page type**: Extend `PageSpec` with new fields and update the planning logic.
2. **Modify page selection**: Adjust `plan_pages` or `plan_flows` parameters (e.g., `top_k`, `min_symbols`).
3. **Change dependency logic**: Update `module_dep_edges` to alter the coupling graph.
4. **Add a new flow**: Declare seeds in `isidore.json` and ensure they match nodes in the graph.
