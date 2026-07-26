> [!WARNING]
> **SECURITY — deterministic detectors flagged this code (0 LLM). Verify; never document as an intended feature.**
>
> - `tests/test_connectors_f4.py:291` — high-entropy literal (>=24 chars, >=3.5 bits/char)
> - `tests/test_connectors_f4.py:291` — high-entropy literal (>=24 chars, >=3.5 bits/char)
## Purpose
The `tests/test_connectors_f4.py` module tests the RSS, Hacker News, and web-search connectors in the Isidore system. It focuses on validating the behavior of these connectors without making live network requests, ensuring tests remain reliable and isolated. The module documents the injection defense mechanisms introduced by ADR-0032, which made network tests necessary. The tests verify critical aspects like URL validation, JSON parsing, feed parsing, and idempotent ingestion of RSS feeds.

## Architecture
The module uses pytest fixtures and mocks to simulate network responses. Key components include:
- `isolated_home`: A fixture that sets up an isolated environment for testing.
- `RSS_XML` and `ATOM_XML`: Sample XML feeds used for testing.
- Test functions that validate URL restrictions, JSON parsing, feed parsing, and idempotent ingestion.

## Key entry points
- `test_only_http_and_https_are_openable()`: Ensures only HTTP/HTTPS URLs are allowed.
- `test_a_partial_json_body_is_never_parsed()`: Validates that incomplete JSON responses are rejected.
- `test_rss_and_atom_go_through_one_parser()`: Confirms RSS and Atom feeds are parsed consistently.
- `test_unparseable_xml_is_an_error_not_an_empty_feed()`: Ensures malformed XML raises an error.
- `test_rss_ingest_is_idempotent()`: Verifies that RSS feed ingestion is idempotent.

## Dependencies
The module depends on:
- `isidore.connectors` modules (`hackernews`, `rss`, `websearch`, `base`, `http`, `store`).
- `pytest` for testing.
- `json` for JSON handling.

## How to change safely
When modifying this module:
1. Ensure all tests remain isolated and do not make live network requests.
2. Maintain the existing structure of test functions and fixtures.
3. Update the sample XML feeds (`RSS_XML`, `ATOM_XML`) if the feed format changes.
4. Verify that all edge cases (e.g., malformed XML, incomplete JSON) are still handled correctly.
