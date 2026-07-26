## Purpose
The `src/isidore/connectors` module ingests raw data from external sources into Isidore's knowledge home. It implements a connector protocol (ADR-0032 F1) to standardize how different data sources are processed. Each connector is responsible for fetching data from a specific source (e.g., RSS feeds, Hacker News, web searches) and storing it in the raw store (`store.py`) in a structured format. The module ensures that ingested data is immutable and idempotent, with each item uniquely identified by a content hash (`chash`) derived from normalized content (`src/isidore/connectors/store.py:L3`).

## Architecture
The module follows a pluggable architecture where connectors are registered via the `base.py` registry. Each connector implements the `IngestOptions` and `IngestResult` protocols to define how data is ingested and reported. The raw store (`store.py`) manages the persistent storage of ingested items and cursor state, ensuring that each run is tracked and items are never rewritten. Connectors like `hackernews.py` and `rss.py` (ADR-0032 F4) handle specific data sources, while `mcp.py` (ADR-0032 F3) provides a read-only interface to the Minimal Code Protocol (MCP).

## Key entry points
- `store.py`: The raw store interface, including functions like `create_run_id`, `write_items`, and `write_state` to manage ingested data and cursor state.
- `base.py`: Defines the connector protocol, including the `IngestResult` dataclass and the `register` decorator for plugging in connectors.
- `hackernews.py` and `rss.py`: Implement connectors for Hacker News and RSS/Atom feeds, respectively, using the Algolia API and `xml.etree` for parsing.
- `websearch.py`: A web-search connector that uses a Tavily-compatible endpoint, configured via environment variables (`ISIDORE_WEBSEARCH_URL` and `ISIDORE_WEBSEARCH_KEY`).
- `mcp.py`: A read-only MCP connector that interacts with JSON-RPC 2.0 endpoints.

## Dependencies
The module depends on `src/isidore/home.py` (for directory paths and file operations) and `src/isidore/claims.py` (for content hashing). It is used by `src/isidore/connect.py` to orchestrate connector execution.

## How to change safely
When modifying connectors, ensure that:
1. The raw store's item structure (`{id, stream, ts, content, meta, chash}`) remains unchanged to preserve stability of anchored claims.
2. New connectors follow the protocol defined in `base.py` and register themselves via the `register` decorator.
3. Environment variables for configurable connectors (e.g., `ISIDORE_WEBSEARCH_KEY`) are documented and handled securely.
4. Changes to `store.py` do not alter the immutability of stored items or the cursor state format.
