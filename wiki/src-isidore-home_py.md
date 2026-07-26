## Purpose
The `src/isidore/home.py` module defines the filesystem layout and path resolution for Isidore's knowledge home directory. It centralizes the logic for locating and constructing paths to connectors' raw data, configuration, state, and the compiled knowledge wiki. The module ensures consistent path resolution across the system, with support for environment variable overrides and platform-specific permission handling.

## Architecture
The module exposes a set of functions that return `Path` objects, each representing a specific location within the knowledge home directory. The directory structure is hierarchical, with connectors organized by their IDs and instances, and raw data further segmented by run IDs. The `home()` function serves as the root of this hierarchy, resolving to either the default `~/.isidore` or the path specified by the `ISIDORE_HOME` environment variable.

## Key entry points
- `home()`: Resolves the base knowledge home directory.
- `connector_dir(cid, instance)`: Returns the directory for a connector, optionally scoped to an instance.
- `raw_dir(cid, instance, run_id)`: Returns the path to raw data for a specific connector run.
- `config_path(cid, instance)`: Returns the path to a connector's configuration file.
- `state_path(cid, instance)`: Returns the path to a connector's state file.
- `knowledge_dir()`: Returns the directory for the compiled knowledge wiki.
- `safe_chmod(path, mode)`: Changes file permissions without raising exceptions on Windows or permission errors.
- `safe_mkdir(path, mode)`: Creates directories recursively with restrictive permissions, handling errors gracefully.

## Dependencies
The module depends only on Python's standard library (`os` and `pathlib`), making it self-contained and easy to maintain.

## How to change safely
When modifying this module:
1. Ensure all path constructions remain relative to `home()` to maintain consistency.
2. Preserve the existing directory structure and naming conventions for backward compatibility.
3. Test changes on both Unix-like and Windows systems, as permission handling differs.
4. Avoid introducing new dependencies to keep the module lightweight.
