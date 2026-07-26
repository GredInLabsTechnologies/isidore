## Purpose
The `src/isidore/connectors` module provides a framework for ingesting raw evidence into Isidore's knowledge home. It defines a connector protocol that standardizes how external data sources (e.g., Git repositories, MCP tools) are ingested deterministically, without relying on LLM calls. The module ensures that ingested items are stored immutably in the raw store, with cursor state tracked per connector. This design supports idempotent ingestion (re-ingesting the same data produces no new items) and anchors external evidence to stable identifiers (`src://<cid>/<instance>/<item-id>`).

## Architecture
The module consists of:
- A **store** (`store.py`) that manages immutable ingested items and cursor state. Each item is a structured record with a content hash (`chash`) derived from claims.py's fingerprinting logic.
- A **protocol** (`base.py`) defining the `Connector` interface, `IngestResult`, and `IngestOptions`. Connectors register themselves via the `register` function, and the module supports third-party plugins via the `isidore.connectors` entry-point group.
- Built-in connectors: `git_repo.py` (for local Git repositories) and `mcp.py` (for read-only MCP tools). These connectors emit items in a structured format and update cursor state to enable idempotent re-ingestion.

## Key entry points
- `store.py`: Core storage logic for raw items and cursor state. Key functions include `write_items`, `update_cursor`, and `record_run`.
- `base.py`: Defines the `Connector` protocol and registry. The `register` function is called by connectors to self-register.
- `git_repo.py`: Implements the Git repository connector, which emits a manifest per repository and uses the store to track cursor state.
- `mcp.py`: Implements the MCP connector, which interacts with MCP tools via JSON-RPC 2.0 and enforces read-only operations.

## Dependencies
- `src/isidore/home.py`: Used for file system operations (e.g., `connector_dir`, `raw_dir`).
- `src/isidore/claims.py`: Provides fingerprinting logic (`_hash`, `_normalize`) for content hashing.

## How to change safely
- **Adding a new connector**: Create a new file in the module, implement the `Connector` protocol, and register it via `base.register`. Ensure the connector adheres to the idempotent ingestion pattern.
- **Modifying the store**: The store is append-only, so changes must preserve backward compatibility for existing items. Avoid modifying existing items or cursor state.
- **Updating the protocol**: Changes to `base.py` (e.g., `IngestResult`, `IngestOptions`) should be backward-compatible to avoid breaking existing connectors.
