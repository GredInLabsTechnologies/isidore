## Purpose
`src/isidore/cli.py` implements the command-line interface for Isidore, a tool that compiles an agent-oriented wiki from a codebase's structure graph. The module provides subcommands to scan repositories, compile the wiki, answer questions, suggest module flows, and audit claims. It bridges the gap between code analysis and documentation by exposing Isidore's core functionality through a user-friendly CLI.

## Architecture
The module follows a command-driven architecture with a main entry point (`cli.py`) that delegates to specialized subcommands. Each subcommand (`_cmd_scan`, `_cmd_compile`, etc.) handles a specific workflow, while `_setting()` manages configuration precedence (CLI args > `isidore.json` > defaults). The design separates concerns: graph operations are delegated to `graph.py`, LLM interactions to `llm.py`, and wiki compilation to `pipeline.py`.

## Key entry points
- `_cmd_scan`: Scans a repository and writes a structure graph to disk (`write_scan` from `graph.py`).
- `_cmd_compile`: Compiles the wiki, respecting configuration precedence and handling dry-run/execute modes (`compile_wiki` from `pipeline.py`).
- `_cmd_ask`: Answers questions using either verified claims (offline) or the LLM (`ask` from `qa.py`).
- `_cmd_suggest_flows`: Identifies cross-module bridges to suggest for `isidore.json` (`suggest_flows` from `pipeline.py`).

## Dependencies
The module depends on:
- `src/isidore/graph.py`: For graph operations (e.g., `write_scan`, `load_graph`).
- `src/isidore/llm.py`: For LLM interactions (e.g., `default_generator`).
- `src/isidore/pipeline.py`: For wiki compilation and flow suggestions.
- `src/isidore/qa.py`: For answering questions.

## How to change safely
1. **Configuration**: Modify `_setting()` to adjust precedence rules or add new settings.
2. **Subcommands**: Add new subcommands by following the pattern of existing ones (e.g., `_cmd_*` functions).
3. **Error handling**: Extend exception handling in `_cmd_compile` or `_cmd_ask` to cover new edge cases.
4. **Dependencies**: Add new imports only if they are explicitly listed in the FACTS.
