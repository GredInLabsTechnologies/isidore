## Purpose
The `tests/test_mcp_barrier.py` module tests the read-only barrier for MCP connectors, ensuring that tools are properly classified as read-only or mutating based on their annotations and names. It addresses a regression from a previous 9-word denylist that allowed certain destructive operations (e.g., `execute_sql`, `drop_table`) to bypass the barrier. The authoritative barrier is now the `readOnlyHint` annotation, with a name heuristic as a fallback. The tests verify that:
- Tools with `readOnlyHint: true` are allowed, regardless of their names.
- Tools with `readOnlyHint: false` are rejected, even if their names suggest they are read-only.
- Tools with `destructiveHint: true` are rejected.
- The name heuristic correctly identifies mutating tools (e.g., `deleteUser`, `publish`) and read-only tools (e.g., `search`, `get_weather`).

## Architecture
The module is structured into three logical sections:
1. **Annotation Authority Tests**: Verify the behavior of the `readOnlyHint` and `destructiveHint` annotations.
2. **Name-Heuristic Fallback Tests**: Test the `_name_looks_mutating` function to ensure it correctly classifies tool names as mutating or read-only.
3. **End-to-End Ingest Tests**: Simulate a fake server with a mix of annotated and unannotated tools to test the barrier's integration with the MCP connector.

The tests use a `_FakeClient` class to mimic a server exposing tools with different annotations, allowing the barrier's behavior to be tested in isolation.

## Key entry points
- `test_readonly_hint_true_allows`: Verifies that tools with `readOnlyHint: true` are allowed.
- `test_readonly_hint_false_rejects_even_innocent_name`: Ensures that tools with `readOnlyHint: false` are rejected, even if their names suggest they are read-only.
- `test_destructive_hint_rejects`: Confirms that tools with `destructiveHint: true` are rejected.
- `test_mutating_names_are_rejected_without_annotation`: Tests that the name heuristic correctly identifies mutating tools.
- `test_read_names_pass_without_annotation`: Tests that the name heuristic correctly identifies read-only tools.

## Dependencies
The module depends on:
- `pytest` for test execution.
- `isidore.connectors.mcp` for the `McpConnector`, `_name_looks_mutating`, and `_tool_read_only` functions.

## How to change safely
When modifying this module, follow these guidelines:
1. **Preserve the Barrier's Behavior**: Ensure that the authoritative barrier (`readOnlyHint`) and the name heuristic remain consistent with their documented behavior.
2. **Update Tests for New Tools**: If new tools are added to the MCP connector, update the tests to include them in the appropriate test cases.
3. **Maintain the Fake Server**: Ensure that the `_FakeClient` class accurately represents the tools and annotations of a real MCP server.
