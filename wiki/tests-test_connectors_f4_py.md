> [!WARNING]
> **SECURITY — deterministic detectors flagged this code (0 LLM). Verify; never document as an intended feature.**
>
> - `tests/test_connectors_f4.py:291` — high-entropy literal (>=24 chars, >=3.5 bits/char)
> - `tests/test_connectors_f4.py:291` — high-entropy literal (>=24 chars, >=3.5 bits/char)
## Purpose
The `tests/test_connectors_f4.py` module tests the RSS, Hacker News, and web-search connectors in the `isidore` system. It focuses on validating the behavior of these connectors without making live network requests, ensuring tests are reliable and isolated. The module addresses two critical concerns: (1) proper handling of feed formats (RSS and Atom) and (2) security defenses against injection attacks. The tests use predefined XML snippets and mocked responses to simulate real-world scenarios, as documented in ADR-0032.

## Architecture
The module is structured around three main sections:
1. **Fetch Helper Tests**: Validate URL safety and JSON parsing robustness.
2. **RSS/Atom Parser Tests**: Ensure consistent parsing of feed formats.
3. **Ingestion Tests**: Verify idempotent ingestion of RSS feeds.

Key fixtures and constants include:
- `isolated_home`: A pytest fixture to isolate test environments.
- `RSS_XML` and `ATOM_XML`: Predefined XML snippets for testing.
- `IngestOptions`: Configuration for connector ingestion.

## Key entry points
- `test_only_http_and_https_are_openable()`: Ensures only HTTP/HTTPS URLs are accepted.
- `test_a_partial_json_body_is_never_parsed()`: Validates JSON parsing safety.
- `test_rss_and_atom_go_through_one_parser()`: Tests unified parsing of RSS and Atom feeds.
- `test_unparseable_xml_is_an_error_not_an_empty_feed()`: Confirms XML parsing failures.
- `test_rss_ingest_is_idempotent()`: Validates repeatable RSS feed ingestion.

## Dependencies
The module depends on:
- `isidore.connectors`: Core connector implementations.
- `pytest`: Testing framework.
- `isidore.connectors.base.IngestOptions`: Configuration for ingestion.

## How to change safely
1. **Add New Tests**: Follow the existing pattern of isolated, mocked tests.
2. **Update XML Snippets**: Modify `RSS_XML` or `ATOM_XML` only if the feed format changes.
3. **Expand Coverage**: Add new test cases for edge cases in parsing or ingestion.
4. **Avoid Live Requests**: Maintain the isolation principle by using mocked responses.
