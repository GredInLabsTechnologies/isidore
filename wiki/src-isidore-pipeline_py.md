## Purpose
The `pipeline.py` module implements the core compiler pipeline for Isidore, a system that generates documentation from code. Its purpose is to transform a codebase's structure graph into a set of Markdown pages, each describing a module or workflow. The pipeline ensures that documentation is deterministic, with only bounded LLM calls used for prose generation, while the rest of the process is handled by deterministic code. Key constraints include hard limits on LLM calls per run, character budgets per prompt, and a single model with fixed timeout settings (`src/isidore/pipeline.py:1-10`).

## Architecture
The pipeline follows a four-stage process:
1. **Planning**: Determines which modules or workflows to document (`plan_pages`, `src/isidore/pipeline.py:202-255`).
2. **Assembly**: Gathers context for each page (e.g., dependencies, hot symbols).
3. **Generation**: Uses an LLM to produce prose for each page (`src/isidore/pipeline.py:133-148`).
4. **Linting**: Validates citations and claims to ensure accuracy (`degenerate_certificate`, `src/isidore/pipeline.py:177-185`).

The pipeline relies on the structure graph to identify what exists and where, delegating only prose generation to the LLM. This separation ensures that the documentation process is repeatable and verifiable.

## Key entry points
- `plan_pages`: Selects modules or workflows to document based on the graph (`src/isidore/pipeline.py:202-255`).
- `PageSpec`: A dataclass representing a page's metadata, including dependencies and hot symbols (`src/isidore/pipeline.py:133-148`).
- `module_dep_edges`: Computes cross-module dependency edges for impact analysis (`src/isidore/pipeline.py:153-167`).
- `degenerate_certificate`: Identifies certificates that are too large or have too many violations (`src/isidore/pipeline.py:177-185`).
- `drop_wiki_output`: Filters out nodes that belong to the wiki output directory (`src/isidore/pipeline.py:188-199`).

## Dependencies
The module depends on several other Isidore modules:
- `changeset.py`: For tracking changes between versions (`src/isidore/changeset.py`).
- `journal.py`: For recording telemetry and run history (`src/isidore/journal.py`).
- `claims.py`: For managing claims and their validation (`src/isidore/claims.py`).
- `findings.py`: For handling findings and linting results (`src/isidore/findings.py`).
- `graph.py`: For working with the structure graph (`src/isidore/graph.py`).
- `llm.py`: For interacting with the LLM (`src/isidore/llm.py`).
- `pcp.py`: For Proof-Carrying Prose certificates (`src/isidore/pcp.py`).
- `verify.py`: For verifying claims and citations (`src/isidore/verify.py`).

## How to change safely
To modify `pipeline.py`, follow these guidelines:
1. **Preserve determinism**: Ensure that all steps except the LLM call are deterministic.
2. **Respect hard limits**: Do not exceed the maximum number of LLM calls or character budget per prompt.
3. **Update documentation**: If adding new functionality, update the module's docstring and any relevant comments.
4. **Test thoroughly**: Changes to the pipeline can significantly impact documentation quality, so test with a representative codebase.
