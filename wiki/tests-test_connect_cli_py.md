> [!WARNING]
> **SECURITY — deterministic detectors flagged this code (0 LLM). Verify; never document as an intended feature.**
>
> - `tests/test_connect_cli.py:66` — high-entropy literal (>=24 chars, >=3.5 bits/char)
> - `tests/test_connect_cli.py:70` — credential-shaped literal (ghp_ prefix)
## Purpose
The `tests/test_connect_cli.py` module tests the CLI functionality for F1's two missing commands (`isidore connect` and `isidore ingest`), which were not part of the original library release. It covers two key gaps: the silent dropping of `IngestOptions` caps (capabilities) and the lack of a supported way to write a connector's configuration. The tests also pin a specific git behavior that was only exposed during live runs.

## Architecture
The module uses pytest fixtures and helper functions to simulate a git repository environment. Key components include:
- `_git()`: A helper to run git commands in a specified repository directory (`tests/test_connect_cli.py:L20-L21`).
- `_make_repo()`: Creates a test repository with a commit (`tests/test_connect_cli.py:L24-L32`).
- `isolated_home()`: A fixture that sets up an isolated environment for testing (`tests/test_connect_cli.py:L36-L38`).

## Key entry points
The main test functions are:
- `test_a_json_shaped_value_keeps_its_type()`: Verifies that JSON-shaped values (like numbers, booleans, and strings) retain their type when parsed (`tests/test_connect_cli.py:L43-L48`).
- `test_a_setting_without_an_equals_is_rejected()`: Ensures that settings without an equals sign are rejected (`tests/test_connect_cli.py:L51-L53`).
- `test_repeating_a_key_builds_a_list()`: Confirms that repeating a key builds a list of values (`tests/test_connect_cli.py:L56-L60`).
- `test_a_credential_shaped_value_is_refused_and_never_written()`: Validates that credential-shaped values are refused and never written to config (`tests/test_connect_cli.py:L62-L68`).

## Dependencies
The module depends on:
- `isidore.connect`: For functions like `apply_settings`, `connector_summary`, `load_config`, `parse_setting`, and `save_config`.
- `isidore.connectors.base`: For `IngestOptions`.
- `isidore.connectors.git_repo`: For `GitRepoConnector`, `_cap_content`, and `_window_floor`.

## How to change safely
When modifying this module:
1. Ensure all helper functions (`_git`, `_make_repo`, `isolated_home`) remain functional as they are used across multiple tests.
2. Maintain the invariant that a connector's config holds the NAME of an env var, never its value (`tests/test_connect_cli.py:L64`).
3. Preserve the behavior of `parse_setting` to correctly handle JSON-shaped values and reject malformed settings (`tests/test_connect_cli.py:L43-L53`).
4. Keep the test for corrupt config reading as empty rather than crashing (`tests/test_connect_cli.py:L73-L76`).
