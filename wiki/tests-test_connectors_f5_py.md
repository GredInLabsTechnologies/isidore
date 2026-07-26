## Purpose
The `tests/test_connectors_f5.py` module tests the integration of the F5 connector with the MCP (Multi-Cloud Platform) framework, focusing on OAuth-heavy sources delivered as MCP instance recipes. It verifies that the connector can handle real-world scenarios, including argument passing, read-only operations, and authentication failures, while interacting with a stub MCP server over stdio. The tests ensure that the connector properly enforces read-only hints, rejects write operations, and fails closed when credentials are revoked, as specified in ADR-0032.

## Architecture
The module uses a pytest fixture `server` to create a stub MCP server that simulates a real Gmail server, implementing JSON-RPC over stdin/stdout. The server handles methods like `initialize`, `tools/list`, and `tools/call`, and can simulate authentication failures. The `_config` function generates configuration for the MCP connector, specifying the server path and allowed tools. The tests exercise the connector's ability to pass arguments to tools, enforce read-only operations, and handle authentication errors.

## Key entry points
- `server`: A pytest fixture that sets up the stub MCP server and environment.
- `_config`: A helper function to generate configuration for the MCP connector.
- `test_an_allowlist_entry_can_carry_the_arguments_a_real_tool_needs`: Tests that allowlist entries can carry tool-specific arguments.
- `test_the_arguments_actually_reach_the_server`: Verifies that arguments are correctly passed to the server.
- `test_a_write_tool_is_refused_even_when_the_recipe_asks_for_it`: Ensures that write tools are rejected.
- `test_a_revoked_token_fails_closed_and_writes_nothing`: Tests that a revoked token results in a closed failure.

## Dependencies
The module depends on pytest, the `McpConnector` and `IngestOptions` classes from `isidore.connectors`, and the `iter_items` function from `isidore.connectors.store`. It also uses standard Python libraries like `json`, `re`, and `pathlib`.

## How to change safely
When modifying this module, ensure that changes to the stub server's behavior do not break existing tests. The server's response to `tools/call` should maintain the format of including `[arguments received]` followed by the JSON-encoded arguments. When adding new tests, follow the pattern of using `_config` to set up the connector and verify the expected behavior. Avoid hardcoding paths or environment variables unless necessary, and ensure that all changes are covered by tests.
