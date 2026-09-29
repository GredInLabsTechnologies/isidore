## Purpose
The `src/isidore/cli.py` module provides a command-line interface for the Isidore system, which compiles an agent-oriented wiki from a codebase's structure graph. It exposes six subcommands: `scan`, `compile`, `ask`, `suggest-flows`, `claims`, and `impact`. These commands enable users to analyze code structure, generate documentation, query the system, identify potential architectural flows, and analyze change impact, all while integrating with the system's core modules (`graph.py`, `llm.py`, `pipeline.py`, and `qa.py`).

## Architecture
The module is structured around six private command handlers (`_cmd_scan`, `_cmd_compile`, `_cmd_ask`, `_cmd_suggest_flows`, `_cmd_claims`, and `_cmd_impact`), each corresponding to a subcommand. The `_setting` helper function manages configuration precedence, favoring explicit CLI arguments over values from `isidore.json` and falling back to built-in defaults. The module delegates heavy lifting to other modules: `graph.py` for structure analysis, `llm.py` for LLM interactions, `pipeline.py` for wiki compilation, and `qa.py` for answering questions.

## Key entry points
The module's entry point is the `cli.py` module itself, which defines the command-line interface and dispatches to the appropriate subcommand handler. The most significant entry points are:
- `_cmd_scan`: Scans a repository to build a structure graph (`write_scan` from `graph.py`).
- `_cmd_compile`: Compiles the wiki, with configurable parameters like `module_depth` and `top_k` (`compile_wiki` from `pipeline.py`). Supports incremental mode via `--changed`/`--since`/`--affected-depth` and rewrite control via `--rewrite`.
- `_cmd_ask`: Answers questions using the compiled wiki or verified claims (`ask` from `qa.py`). Online questions pass through `assert_may_send_source` as a disclosure gate (`src/isidore/cli.py:129-130`); `--offline` reads verified claims without sending anything.
- `_cmd_suggest_flows`: Identifies cross-module bridges as potential flows (`suggest_flows` from `pipeline.py`).
- `_cmd_impact`: Analyzes changes and their impact (`build_impact` from `impact.py`).

## Dependencies
The module depends on eight other modules:
- `src/isidore/graph.py`: For structure graph operations (`find_graph`, `load_graph`, `write_scan`).
- `src/isidore/llm.py`: For LLM interactions (`default_generator`, `GenerationError`).
- `src/isidore/pipeline.py`: For wiki compilation and flow suggestions (`compile_wiki`, `suggest_flows`, `load_config`, `assert_may_send_source`).
- `src/isidore/qa.py`: For answering questions (`ask`).
- `src/isidore/impact.py`: For change-impact analysis (`build_impact`, `render_impact`).
- `src/isidore/claims.py`: For zero-LLM staleness auditing of claims.
- `src/isidore/export.py`: For wiki export operations.
- `src/isidore/journal.py`: For telemetry and journaling.

## How to change safely
To modify `cli.py` safely:
1. **Add new subcommands**: Introduce a new `_cmd_*` function and update the docstring to reflect the new subcommand.
2. **Modify existing subcommands**: Ensure changes preserve the existing behavior and configuration precedence logic in `_setting`.
3. **Update dependencies**: If a new function is added to a dependency module, import and use it in the relevant `_cmd_*` function.
4. **Test thoroughly**: The module is tested by `tests/test_connect_cli.py`, `tests/test_handoff.py`, `tests/test_pcp_pipeline.py`, `tests/test_pcp_seams.py`, `tests/test_whatsnew.py`, and `tests/test_wiki_dir_config.py` in addition to direct unit tests. Exercise all subcommands with realistic inputs and edge cases.
