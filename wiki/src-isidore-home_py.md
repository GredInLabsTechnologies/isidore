## Purpose
The `src/isidore/home.py` module defines the filesystem layout and path resolution for Isidore's knowledge home directory. It centralizes the logic for locating and constructing paths to connectors' raw data, configuration, state, and the compiled knowledge wiki. The module ensures a consistent directory structure (`~/.isidore` by default, overridable via `ISIDORE_HOME`) and provides utilities for safe filesystem operations (e.g., `safe_mkdir`, `safe_chmod`) to handle cross-platform permissions gracefully.

## Architecture
The module exposes a set of functions that return `Path` objects, each representing a specific location within the knowledge home. The core function `home()` resolves the base directory, while other functions build upon it to construct paths for connectors, raw data, configuration, state, and the knowledge directory. The `safe_*` functions abstract away platform-specific filesystem quirks, ensuring operations like directory creation and permission changes do not raise exceptions.

## Key entry points
- `home()`: Resolves the base knowledge home directory (`~/.isidore` or `$ISIDORE_HOME`).
- `connector_dir(cid, instance)`: Returns the directory for a connector's instance.
- `raw_dir(cid, instance, run_id)`: Returns the path to a connector's raw data for a specific run.
- `config_path(cid, instance)`: Returns the path to a connector's configuration file.
- `state_path(cid, instance)`: Returns the path to a connector's state file.
- `knowledge_dir()`: Returns the path to the compiled knowledge wiki directory.
- `safe_mkdir(path, mode)`: Creates a directory with restrictive permissions, handling errors gracefully.
- `safe_chmod(path, mode)`: Changes file permissions, skipping on Windows or if the operation fails.

## Dependencies
The module depends only on Python's standard library (`os`, `pathlib.Path`). It has no external dependencies and is used by other modules in the `isidore` package, such as `connectors`, `connect.py`, and `knowledge.py`.

## How to change safely
1. **Add new paths**: If adding a new path function, ensure it builds upon `home()` or existing path functions to maintain consistency. Use `safe_mkdir` and `safe_chmod` for filesystem operations to handle cross-platform quirks.
2. **Modify path logic**: When changing how paths are constructed, verify that the new logic aligns with the module's purpose of centralizing filesystem resolution. Test on both Unix-like and Windows systems.
3. **Update permissions**: If adjusting default permissions (e.g., `0o700` in `safe_mkdir`), ensure the new mode is restrictive enough for sensitive data but still functional across platforms.
