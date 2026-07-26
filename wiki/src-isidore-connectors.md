## Purpose
The `src/isidore/connectors` module ingests raw data from external sources into Isidore's knowledge home. It implements a connector protocol (defined in `base.py`) that standardizes how different data sources are processed. Each connector is responsible for fetching data from its source, normalizing it, and storing it in the raw store (`store.py`). The module supports multiple data sources, including Hacker News, RSS feeds, web searches, and read-only MCP (Minimal Code Protocol) endpoints. The connectors are designed to be deterministic and avoid LLM calls, ensuring consistent and reliable data ingestion.

## Architecture
The module follows a pluggable architecture where connectors are registered via the `base.py` registry. The registry is populated by built-in connectors and can be extended by third-party plugins. Each connector implements the same protocol, defined by the `IngestOptions` and `IngestResult` classes in `base.py`. The raw store (`store.py`) manages the persistent storage of ingested items and connector state. Connectors use shared utilities from `http.py` for HTTP requests and `store.py` for state management. The module is designed to be modular, with each connector handling a specific data source independently.

## Key entry points
- `base.py`: Defines the connector protocol and registry. The `register` decorator is used to register connectors, and the `IngestResult` class standardizes the outcome of ingest runs.
- `store.py`: Manages the raw store, including writing items, updating cursor state, and recording run metadata. The `create_run_id` function generates unique identifiers for each ingest run.
- `hackernews.py`: Implements the Hacker News connector, which fetches stories and searches from Algolia's public API.
- `rss.py`: Implements the RSS/Atom connector, which parses feed entries and stores them in the raw store.
- `websearch.py`: Implements the web search connector, which queries a Tavily-compatible endpoint for search results.
- `mcp.py`: Implements the read-only MCP connector, which interacts with a JSON-RPC 2.0 endpoint to fetch data.

## Dependencies
- `src/isidore/home.py`: Used for directory and file path management, such as `connector_dir`, `raw_dir`, and `state_path`.
- `src/isidore/claims.py`: Provides the `_hash` and `_normalize` functions for content fingerprinting.
- `src/isidore/connect.py`: Depends on the connectors module to execute ingest runs.

## How to change safely
When modifying the connectors module, follow these guidelines:
1. **Preserve the connector protocol**: Ensure that any changes to the protocol in `base.py` are backward-compatible to avoid breaking existing connectors.
2. **Maintain idempotency**: Connectors should be idempotent, meaning running them multiple times with the same input should produce the same output. This is critical for the raw store's stability.
3. **Update documentation**: If you change how a connector works, update its docstring to reflect the new behavior.
4. **Test thoroughly**: Since connectors interact with external systems, test them with real data to ensure they handle edge cases correctly.
5. **Avoid hardcoding secrets**: Ensure that any credentials or secrets are read from environment variables or configuration files, not hardcoded in the source.
