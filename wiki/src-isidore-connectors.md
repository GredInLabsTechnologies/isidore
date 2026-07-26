## Purpose
The `src/isidore/connectors` module provides a framework for ingesting raw external evidence into Isidore's knowledge home. It defines a protocol for connectors, which are responsible for deterministically fetching data from external sources (e.g., Git repositories, MCP tools) and storing it in the raw store without using LLMs. The module supports built-in connectors (like `git_repo` and `mcp`) and third-party plugins via the `isidore.connectors` entry-point group, enabling extensibility without modifying the core repository.

## Architecture
The module consists of:
- A **store** (`store.py`) that manages immutable ingested items and cursor state, where each item is uniquely identified by a content hash derived from its normalized content (`src/isidore/connectors/store.py:L3-L7`).
- A **protocol** (`base.py`) defining the `Connector` interface, `IngestResult` dataclass, and `IngestOptions` for scoping runs (`src/isidore/connectors/base.py:L21-L46`).
- Built-in connectors:
  - `git_repo.py`: Ingests Git repository manifests, emitting one item per repo with a unique ID based on the HEAD commit (`src/isidore/connectors/git_repo.py:L1-L8`).
  - `mcp.py`: A read-only connector for MCP tools, enforcing a strict allowlist for operations (`src/isidore/connectors/mcp.py:L1-L8`).

## Key entry points
- `base.py`: The protocol and registry for connectors, including the `register` function and `IngestResult` class (`src/isidore/connectors/base.py:L21-L46`).
- `store.py`: Core storage operations like `write_items`, `update_cursor`, and `record_run` (`src/isidore/connectors/store.py:L23-L26`).
- `__init__.py`: Initializes built-in connectors and exposes the public API (`src/isidore/connectors/__init__.py:L1-L26`).

## Dependencies
- `src/isidore/home.py`: Used for file paths and directory management (`src/isidore/connectors/store.py:L18`).
- `src/isidore/claims.py`: Provides `_hash` and `_normalize` for content fingerprinting (`src/isidore/connectors/store.py:L17`).
- `src/isidore/connect.py`: Depends on this module for connector execution (`src/isidore/connect.py` is not shown but is referenced).

## How to change safely
- **Adding a new connector**: Create a new file in the module, implement the `Connector` protocol, and register it via `register` (`src/isidore/connectors/base.py:L41-L46`). Ensure it adheres to the zero-LLM requirement.
- **Modifying the store**: The raw store is append-only, so changes must preserve immutability and cursor state integrity (`src/isidore/connectors/store.py:L3-L8`).
- **Updating the protocol**: Extend `IngestOptions` or `IngestResult` carefully, as connectors rely on these interfaces (`src/isidore/connectors/base.py:L31-L39`).
