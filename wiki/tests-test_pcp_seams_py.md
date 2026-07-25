## Purpose
The `tests/test_pcp_seams.py` module serves as a gatekeeper for the Proof-Carrying Prose (PCP) system's frozen seam, ensuring that the system's golden fixtures (graph, certificates, contracts, and predicate grammar) are correctly parsed and exposed. It does NOT verify the logic of each lane's gate (e.g., the actual verification of claims), but rather checks that the system's public surface is stable and self-consistent. This includes verifying that types round-trip, the registry is wired fail-closed, and CLI subcommands are registered.

## Architecture
The module is organized into three main sections:
1. **Fixtures Parsing**: Tests for loading and validating golden fixtures (graph, certificates, contracts, marks, and pyramid configuration).
2. **Predicate Grammar**: Tests for parsing and serializing predicates, including round-trip validation and rejection of invalid predicates.
3. **Registry Fail-Closed**: Tests for ensuring the predicate registry is fail-closed, meaning unregistered predicates degrade to `UNDECIDABLE` rather than failing.

## Key entry points
- `test_golden_graph_loads()`: Validates the structure of the golden graph (nodes, links, and commit hash).
- `test_golden_certificate_round_trips()`: Ensures certificates can be read, written, and re-read without loss of data.
- `test_golden_contracts_load()`: Checks that contracts are loaded correctly and have the expected predicate.
- `test_golden_marks_and_pyramid_config_parse()`: Validates the parsing of marks and pyramid configuration.
- `test_predicate_parse_and_serialize_round_trip()`: Tests the round-trip serialization of predicates.
- `test_predicate_rejects_absent_or_unknown()`: Ensures invalid predicates are rejected.
- `test_wiki_uri_parsing()`: Validates the parsing of wiki URIs.
- `test_registry_has_every_kind_and_is_fail_closed()`: Ensures the predicate registry is fail-closed.

## Dependencies
The module depends on the `isidore` package, specifically:
- `contracts`, `detectors`, `humanpack`, `pyramid`, `reconcile`, `verify` modules.
- `isidore.cli.main` for CLI subcommand registration.
- `isidore.graph.load_graph` for loading the golden graph.
- `isidore.pcp` for PCP-related functionality, including `Certificate`, `Mark`, `Predicate`, and `VerifyContext`.

## How to change safely
When modifying this module, ensure that:
1. **Golden Fixtures**: Any changes to the golden fixtures (graph, certificates, contracts, marks, or pyramid configuration) must be reflected in the corresponding tests.
2. **Predicate Grammar**: If the predicate grammar changes, update the tests to reflect the new grammar and ensure round-trip serialization works as expected.
3. **Registry Fail-Closed**: If new predicate kinds are added, ensure they are registered in the `VerifyContext` and that the registry remains fail-closed.
