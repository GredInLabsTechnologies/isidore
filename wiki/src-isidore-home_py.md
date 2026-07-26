## Purpose
The `src/isidore/home.py` module defines the filesystem layout and utilities for Isidore's "knowledge home" — a user-specific directory (defaulting to `~/.isidore`) where connectors store their raw ingested data, configuration, and state. This separation ensures that connector data remains local, user-specific, and independent of any repository structure. The module provides path resolution, directory creation, and permission management utilities to ensure safe and consistent filesystem operations across platforms.

## Architecture
The module is a collection of pure functions that compute paths under the knowledge home directory. It uses `pathlib.Path` for path manipulation and includes platform-aware utilities like `safe_chmod` and `safe_mkdir` to handle filesystem operations robustly. The design avoids global state, relying instead on explicit parameters for connector identifiers (`cid`), instance names, and run identifiers.

## Key entry points
- `home()`: Resolves the knowledge home directory, respecting the `ISIDORE_HOME` environment variable if set.
- `connector_dir(cid, instance)`: Returns the base directory for a connector, optionally scoped to an instance.
- `raw_dir(cid, instance, run_id)`: Constructs the path for raw ingested data for a specific connector run.
- `config_path(cid, instance)`: Locates the connector's configuration file.
- `state_path(cid, instance)`: Locates the connector's state file.
- `knowledge_dir()`: Returns the directory for compiled knowledge wikis.
- `safe_chmod(path, mode)`: Changes file permissions without raising exceptions on Windows or filesystem quirks.
- `safe_mkdir(path, mode)`: Creates directories recursively with restrictive permissions, handling errors gracefully.

## Dependencies
The module depends only on Python's standard library (`os`, `pathlib`), with no external dependencies. It is used by `src/isidore/connectors` and `src/isidore/knowledge.py` to manage filesystem operations for connectors and knowledge compilation.

## How to change safely
1. **Path resolution**: When adding new path functions, ensure they are built on `home()` or existing path functions to maintain consistency.
2. **Platform compatibility**: Test changes on Windows and Unix-like systems, especially for `safe_chmod` and `safe_mkdir`.
3. **Error handling**: Maintain the best-effort, no-crash philosophy for filesystem operations.
4. **Environment variables**: Document any new environment variables introduced to configure paths.
