## Purpose
The `src/isidore/cli.py` module provides a command-line interface for the Isidore system, which compiles an agent-oriented wiki from a codebase's structure graph. It exposes five subcommands: `scan`, `compile`, `ask`, `suggest-flows`, and `claims`. These commands enable users to analyze code structure, generate documentation, query the system, and identify potential architectural flows, all while integrating with the system's core modules (`graph.py`, `llm.py`, `pipeline.py`, and `qa.py`).

## Architecture
The module is structured around five private command handlers (`_cmd_scan`, `_cmd_compile`, `_cmd_ask`, `_cmd_suggest_flows`, and `_cmd_impact`), each corresponding to a subcommand. The `_setting` helper function manages configuration precedence, favoring explicit CLI arguments over values from `isidore.json` and falling back to built-in defaults. The module delegates heavy lifting to other modules: `graph.py` for structure analysis, `llm.py` for LLM interactions, `pipeline.py` for wiki compilation, and `qa.py` for answering questions.

## Key entry points
The module's entry point is the `cli.py` module itself, which defines the command-line interface and dispatches to the appropriate subcommand handler. The most significant entry points are:
- `_cmd_scan`: Scans a repository to build a structure graph (`write_scan` from `graph.py`).
- `_cmd_compile`: Compiles the wiki, with configurable parameters like `module_depth` and `top_k` (`compile_wiki` from `pipeline.py`).
- `_cmd_ask`: Answers questions using the compiled wiki or verified claims (`ask` from `qa.py`).
- `_cmd_suggest_flows`: Identifies cross-module bridges as potential flows (`suggest_flows` from `pipeline.py`).
- `_cmd_impact`: Analyzes changes and their impact (`build_impact` from `impact.py`).

## Dependencies
The module depends on four other modules:
- `src/isidore/graph.py`: For structure graph operations (`find_graph`, `load_graph`, `write_scan`).
- `src/isidore/llm.py`: For LLM interactions (`default_generator`, `GenerationError`).
- `src/isidore/pipeline.py`: For wiki compilation and flow suggestions (`compile_wiki`, `suggest_flows`, `load_config`).
- `src/isidore/qa.py`: For answering questions (`ask`).

## How to change safely
To modify `cli.py` safely:
1. **Add new subcommands**: Introduce a new `_cmd_*` function and update the docstring to reflect the new subcommand.
2. **Modify existing subcommands**: Ensure changes preserve the existing behavior and configuration precedence logic in `_setting`.
3. **Update dependencies**: If a new function is added to a dependency module, import and use it in the relevant `_cmd_*` function.
4. **Test thoroughly**: Since the module is the primary user-facing interface, test all subcommands with realistic inputs and edge cases.
