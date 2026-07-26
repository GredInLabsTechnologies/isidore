## Purpose
The `src/isidore/connectors` module ingests raw data from external sources into Isidore's knowledge home. It implements a connector protocol (ADR-0032 F1) that standardizes how data is fetched, stored, and tracked. Each connector is responsible for one source type (e.g., RSS, Hacker News) and writes items to the raw store (`store.py`) in a consistent format. The module supports pluggable connectors via the `isidore.connectors` entry-point group, allowing third-party extensions without modifying the core repository.

## Architecture
The module consists of:
- A **base protocol** (`base.py`) defining the `IngestResult` dataclass and connector registry.
- **Connector implementations** (e.g., `hackernews.py`, `rss.py`) that fetch data and write it to the store.
- The **raw store** (`store.py`), which persists items as `{id, stream, ts, content, meta, chash}` and tracks cursor state for incremental ingestion.
- **Transport layers** (`mcp.py`) for interacting with external systems (e.g., MCP over HTTP or stdio).

Connectors follow a common pattern: they read configuration, fetch data, and write items to the store. The store ensures idempotency by using content hashes (`chash`) and cursor tracking.

## Key entry points
- `base.py`: Defines the `IngestResult` dataclass and connector registry. Connectors register themselves via the `register` decorator.
- `store.py`: Core storage logic for raw items and cursor state. Key functions include `write_items`, `update_cursor`, and `create_run_id`.
- `hackernews.py`/`rss.py`/`websearch.py`: Example connectors implementing the protocol. They use `fetch_json`/`fetch` (from `http.py`) to retrieve data and `write_items` to store it.

## Dependencies
- Cross-module: `src/isidore/home.py` (for paths like `connector_dir`) and `src/isidore/claims.py` (for `_hash` and `_normalize`).
- Internal: `base.py` is used by all connectors, and `store.py` is imported by most connectors to write items.

## How to change safely
1. **Add a new connector**: Create a new file (e.g., `newsource.py`) and implement the `IngestOptions` and `IngestResult` protocol. Register it with `@register`.
2. **Modify the store**: Changes to `store.py` must preserve the item format (`{id, stream, ts, content, meta, chash}`) and cursor state schema.
3. **Update the base protocol**: Avoid breaking changes to `IngestResult` or the registry mechanism, as they are used by all connectors.
