## Purpose
The `src/isidore/connect.py` module serves as the CLI interface for the connector layer in Isidore, handling configuration and inspection of connectors without involving the LLM. It provides commands like `isidore connect` and `isidore ingest` to manage connectors, ensuring they operate within strict security constraints (e.g., no network access for `connect`, and connectors failing closed if required environment variables are missing).

## Architecture
The module is structured around four key functions:
1. **Configuration Management**: `load_config()` and `save_config()` handle reading and writing connector configurations, ensuring they are stored with restrictive permissions.
2. **Settings Parsing**: `parse_setting()` and `apply_settings()` process key-value pairs from CLI arguments, accumulating repeated keys into lists and rejecting values that appear to be secrets.
3. **Connector Inspection**: `connector_summary()` generates a summary of a connector's status, including readiness, missing environment variables, and ingestion history.

## Key entry points
- `register_cli()`: Registers the `connect` and `ingest` commands with the CLI framework.
- `connector_summary()`: Generates a summary of a connector's state for the `--list` flag.
- `apply_settings()`: Processes CLI-provided settings into a connector's configuration.

## Dependencies
The module depends on:
- `src/isidore/connectors`: For connector implementations and utilities like `missing_env()`.
- `src/isidore/home.py`: For filesystem paths and permissions (`config_path`, `safe_chmod`).
- `src/isidore/toon.py`: For table encoding utilities.

## How to change safely
- **Configuration Handling**: When modifying `load_config()` or `save_config()`, ensure permissions remain restrictive (0o600) and paths are resolved via `config_path()`.
- **Settings Parsing**: Changes to `parse_setting()` or `apply_settings()` must preserve the invariant that secrets are never stored in the config.
- **Connector Inspection**: Updates to `connector_summary()` should not introduce new network calls or LLM interactions.
