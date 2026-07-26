## Purpose
The `src/isidore/cli.py` module implements the command-line interface for Isidore, a tool that compiles an agent-oriented wiki from a codebase's structure graph. It provides subcommands to scan repositories, compile wikis, answer questions, suggest module flows, and audit claims. The module bridges Isidore's core functionality with user interaction, handling configuration, error reporting, and execution flow.

## Architecture
The module is structured around subcommands, each implemented as a separate function (`_cmd_*`). These functions parse arguments, delegate to other modules (`graph.py`, `llm.py`, `pipeline.py`, `qa.py`), and handle success/error cases. The `_setting()` helper manages configuration precedence (CLI args > `isidore.json` > defaults). The module does not define any classes or top-level constants.

## Key entry points
- `_cmd_scan()`: Scans a repository and writes a structure graph to disk (`write_scan()` from `graph.py`).
- `_cmd_compile()`: Compiles the wiki, using `compile_wiki()` from `pipeline.py` with configurable parameters.
- `_cmd_ask()`: Answers questions using `ask()` from `qa.py`, supporting both LLM-backed and offline (claims-only) modes.
- `_cmd_suggest_flows()`: Identifies cross-module bridges using `suggest_flows()` from `pipeline.py`.
- `_cmd_impact()`: Builds an impact report for changes (imported from `impact.py` at runtime).

## Dependencies
The module depends on:
- `src/isidore/graph.py`: For graph operations (`find_graph`, `load_graph`, `write_scan`).
- `src/isidore/llm.py`: For LLM interactions (`default_generator`, `GenerationError`).
- `src/isidore/pipeline.py`: For wiki compilation and flow suggestions (`compile_wiki`, `suggest_flows`, default constants).
- `src/isidore/qa.py`: For question answering (`ask`).

## How to change safely
1. **Add a new subcommand**: Create a new `_cmd_*` function, add it to the argument parser, and document it in the module docstring.
2. **Modify configuration handling**: Update `_setting()` to support new precedence rules or defaults.
3. **Add error handling**: Extend the `try`/`except` blocks in subcommands to handle new exceptions.
4. **Update dependencies**: Ensure new functions from dependencies are properly imported and used.
