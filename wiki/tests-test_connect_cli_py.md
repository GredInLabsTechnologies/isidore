> [!WARNING]
> **SECURITY — deterministic detectors flagged this code (0 LLM). Verify; never document as an intended feature.**
>
> - `tests/test_connect_cli.py:66` — high-entropy literal (>=24 chars, >=3.5 bits/char)
> - `tests/test_connect_cli.py:70` — credential-shaped literal (ghp_ prefix)
## Purpose
`tests/test_connect_cli.py` tests the configuration and CLI behavior of the `isidore connect` and `isidore ingest` commands, which were missing from the original library. The module verifies that:
- Configuration settings are parsed correctly, including JSON-shaped values (e.g., `limit=5` becomes `("limit", 5)`).
- Invalid settings (e.g., missing `=`) are rejected.
- Repeated keys are aggregated into lists (e.g., `repos=/a` and `repos=/b` become `{"repos": ["/a", "/b"]}`).
- Sensitive values (e.g., tokens) are refused and never stored in config files.
- Corrupt or empty configs are handled gracefully.

The tests also pin a specific Git behavior observed during live runs, ensuring the CLI interacts correctly with Git repositories.

## Architecture
The module uses pytest fixtures and helper functions to simulate a Git repository (`_make_repo`) and isolate the `ISIDORE_HOME` environment variable (`isolated_home`). It tests the `parse_setting`, `apply_settings`, `save_config`, and `load_config` functions from `isidore.connect`, as well as the `IngestOptions` class from `isidore.connectors.base`.

## Key entry points
- `_make_repo`: Creates a Git repository with a test commit.
- `isolated_home`: A pytest fixture that sets up a temporary `ISIDORE_HOME` directory.
- `test_a_json_shaped_value_keeps_its_type`: Verifies that JSON-shaped values (e.g., `limit=5`) are parsed correctly.
- `test_a_setting_without_an_equals_is_rejected`: Ensures invalid settings (e.g., `justakey`) are rejected.
- `test_repeating_a_key_builds_a_list`: Confirms repeated keys are aggregated into lists.
- `test_a_credential_shaped_value_is_refused_and_never_written`: Validates that sensitive values (e.g., tokens) are refused and never stored.
- `test_a_corrupt_config_reads_as_empty_rather_than_crashing`: Ensures corrupt configs are handled gracefully.

## Dependencies
The module depends on:
- `isidore.connect` (for `parse_setting`, `apply_settings`, `save_config`, `load_config`).
- `isidore.connectors.base` (for `IngestOptions`).
- `isidore.connectors.git_repo` (for `GitRepoConnector`, `_cap_content`, `_window_floor`).
- `pytest` (for testing).
- `subprocess` (to run Git commands).

## How to change safely
To modify this module:
1. **Add new tests**: Follow the existing pattern of testing one behavior per function. Use `_make_repo` and `isolated_home` to set up test environments.
2. **Update dependencies**: If new functions are added to `isidore.connect` or `isidore.connectors.base`, update the imports and tests accordingly.
3. **Preserve invariants**: Ensure that sensitive values (e.g., tokens) are still refused and never stored, and that corrupt configs are handled gracefully.
