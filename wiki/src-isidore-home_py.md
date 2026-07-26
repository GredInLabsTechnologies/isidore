## Purpose
The `src/isidore/home.py` module defines the filesystem layout and utilities for Isidore's "knowledge home" — a user-specific directory (defaulting to `~/.isidore`) where connectors store their raw ingested data, configuration, and state. It abstracts away the physical location of these files, allowing them to be overridden via the `ISIDORE_HOME` environment variable. The module also provides helper functions to construct paths for connector-specific directories, raw data storage, and configuration/state files, ensuring consistent directory structures across connectors.

## Architecture
The module is a collection of pure functions that return `Path` objects, with no shared state or side effects. It relies on Python's `pathlib` and `os` modules to handle filesystem operations. The key functions are organized hierarchically: `home()` defines the root directory, while `connector_dir()`, `raw_dir()`, `config_path()`, and `state_path()` build paths relative to it. Additional utilities like `safe_chmod()` and `safe_mkdir()` handle filesystem operations with best-effort error handling, particularly for permission-sensitive operations.

## Key entry points
- `home()`: The root of the knowledge home, resolved from `ISIDORE_HOME` or the default `~/.isidore`.
- `connector_dir(cid, instance)`: Returns the base directory for a connector, optionally scoped to an instance.
- `raw_dir(cid, instance, run_id)`: Constructs a path for raw data storage, organized by connector, instance, and run ID.
- `config_path(cid, instance)` and `state_path(cid, instance)`: Locate the connector's configuration and state files.
- `knowledge_dir()`: The directory where compiled knowledge is stored.
- `safe_chmod()` and `safe_mkdir()`: Utility functions for filesystem operations with error suppression.

## Dependencies
The module depends only on Python's standard library (`os`, `pathlib`), with no external dependencies. It is used by `src/isidore/connectors`, `src/isidore/connect.py`, and `src/isidore/knowledge.py` to manage filesystem interactions.

## How to change safely
- **Adding new paths**: Introduce new functions following the existing pattern (e.g., `new_feature_dir()`) to maintain consistency.
- **Modifying paths**: Ensure changes to path construction are backward-compatible to avoid breaking existing connectors.
- **Error handling**: When adding new filesystem operations, use the existing `safe_*` utilities to preserve the module's best-effort error handling.
- **Environment variables**: Avoid introducing new environment variables; use `ISIDORE_HOME` for overrides.
