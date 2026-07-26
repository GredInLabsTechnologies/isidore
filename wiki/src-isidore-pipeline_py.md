## Purpose
The `pipeline.py` module implements the core compiler pipeline for generating documentation pages from code. It defines a deterministic process that transforms static analysis results into structured documentation, with the only non-deterministic step being a single bounded LLM call per dirty page. The pipeline ensures that all documentation is grounded in the actual code structure, with strict limits on LLM interactions (e.g., `--max-calls` and character budgets) to prevent unbounded generation.

## Architecture
The pipeline consists of four main phases:
1. **Planning**: Determines which modules and flows to document based on the code graph.
2. **Assembly**: Gathers context for each page (e.g., hot symbols, dependencies).
3. **Generation**: Delegates prose generation to an LLM, with built-in lints to validate citations.
4. **Linting**: Validates citations and repairs hallucinations (e.g., phantom paths).

The `PageSpec` class centralizes metadata for each page, including its kind (module or flow), dependencies, and hot symbols. The pipeline relies on the code graph (`nodes` and `links`) to answer "what exists and where" — everything else is deterministic.

## Key entry points
- `plan_pages()`: Selects top-K modules to document, filtering by symbol count and excluding trivial modules.
- `plan_flows()`: Generates cross-cutting flow pages by BFS from user-declared seeds.
- `module_dep_edges()`: Computes cross-module dependency edges, shared with the impact fingerprint for consistency.

## Dependencies
The module depends on:
- `changeset.py`: For tracking changed lines and symbols.
- `journal.py`: For recording page changes and run telemetry.
- `claims.py`: For managing claims and linting citations.
- `graph.py`: For the code structure graph.
- `llm.py`: For prose generation.
- `pcp.py`: For tamper-evident certificates.
- `verify.py`: For validating claims.

## How to change safely
- **Planning logic**: Modify `plan_pages()` or `plan_flows()` to adjust page selection criteria, but ensure the graph remains the sole source of truth for "what exists".
- **Linting**: Update `LINT_REPAIR_ADDENDUM` to refine citation validation, but preserve the requirement that all citations must appear in the `FACTS` block.
- **Dependencies**: Avoid introducing new dependencies unless they are explicitly required for the pipeline's deterministic phases.
