## Purpose
`src/isidore/connect.py` serves as the CLI interface for `isidore connect` and `isidore ingest`, bridging the gap between the connector layer and user commands. It handles configuration management, settings application, and connector state inspection without involving any LLM operations. The module ensures connectors can be configured and inspected safely, with credentials never stored directly in configs (invariant I9).

## Architecture
The module consists of pure functions that:
1. Load and save connector configurations (`load_config`, `save_config`)
2. Parse and apply user-provided settings (`parse_setting`, `apply_settings`)
3. Generate summaries of connector states (`connector_summary`)
4. Register CLI commands (`register_cli`)

All operations are file-based, using JSON for configuration storage, and avoid network access.

## Key entry points
- `load_config()`: Safely reads a connector's config, returning `{}` for missing/corrupt files
- `save_config()`: Writes configs with restrictive permissions (0o600)
- `apply_settings()`: Merges CLI settings into configs, accumulating repeated keys into lists
- `connector_summary()`: Generates a status row for `--list` output

## Dependencies
- `src/isidore/connectors`: For connector implementations and state management
- `src/isidore/home.py`: Provides filesystem paths and permission utilities
- `src/isidore/toon.py`: Used for table encoding (though not directly in this module)

## How to change safely
1. **Configuration handling**: When modifying `load_config` or `save_config`, ensure permissions remain restrictive (0o600) and error handling remains silent (never raises)
2. **Settings application**: `apply_settings` has special behavior for credentials and repeated keys - any changes must preserve these rules
3. **CLI registration**: New CLI arguments must follow the existing pattern in `register_cli`
