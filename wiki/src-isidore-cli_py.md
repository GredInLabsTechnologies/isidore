## Purpose
The `src/isidore/cli.py` module provides a command-line interface for the Isidore system, which compiles an agent-oriented wiki from a codebase's structure graph. It exposes five subcommands: `scan`, `compile`, `ask`, `suggest-flows`, and `claims`. The `scan` subcommand builds a structure graph for a repository in any language, the `compile` subcommand generates or refreshes the wiki, the `ask` subcommand answers questions using the compiled wiki, the `suggest-flows` subcommand identifies cross-module bridges for configuration, and the `claims` subcommand audits the staleness of claims in the wiki.

## Architecture
The module is structured around five private functions, each corresponding to a subcommand: `_cmd_scan`, `_cmd_compile`, `_cmd_ask`, `_cmd_suggest_flows`, and `_cmd_impact`. These functions are called by the main `cli.py` entry point, which parses command-line arguments and delegates to the appropriate subcommand function. The module also includes a helper function `_setting` to resolve configuration values with precedence: explicit CLI arguments > `isidore.json` > built-in defaults.

## Key entry points
The key entry points are the subcommand functions:
- `_cmd_scan`: Builds a structure graph for a repository.
- `_cmd_compile`: Generates or refreshes the wiki.
- `_cmd_ask`: Answers questions using the compiled wiki.
- `_cmd_suggest_flows`: Identifies cross-module bridges for configuration.
- `_cmd_impact`: Builds an impact report for changes in the repository.

## Dependencies
The module depends on four other modules in the `src/isidore` package:
- `src/isidore/graph.py`: Provides functions for working with structure graphs.
- `src/isidore/llm.py`: Provides functions for interacting with language models.
- `src/isidore/pipeline.py`: Provides functions for compiling the wiki.
- `src/isidore/qa.py`: Provides functions for answering questions.

## How to change safely
To modify the module safely, follow these guidelines:
1. **Preserve the subcommand structure**: Each subcommand function should remain private and called by the main entry point. Do not change the function signatures or remove existing subcommands.
2. **Maintain configuration precedence**: The `_setting` function ensures that configuration values are resolved in the correct order. Do not change the logic of this function.
3. **Handle errors consistently**: Each subcommand function should handle errors consistently and return appropriate exit codes. Do not change the error handling logic.
4. **Preserve dependencies**: The module depends on specific functions from other modules. Do not remove or change these dependencies without ensuring that the changes are compatible with the dependent modules.
