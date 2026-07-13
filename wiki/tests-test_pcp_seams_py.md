## Purpose
The `tests/test_pcp_seams.py` module serves as a gatekeeper for the PCP (Policy Control Plane) seam, ensuring that the frozen interface between lanes A–E remains stable and self-consistent. It verifies that types round-trip correctly, the registry is wired fail-closed, and CLI subcommands are properly registered. The tests do not check verification logic (which is lane-specific) but instead validate the public surface of the PCP seam against golden fixtures. This module exists to prevent regressions in the PCP's interface, ensuring that lanes can start against a consistent and verifiable foundation.

## Architecture
The module is organized into three main sections:
1. **Fixture Parsing**: Tests that load and validate golden fixtures, including graphs, certificates, contracts, marks, and pyramid configurations. These tests ensure that the PCP's data structures can be parsed and serialized correctly.
2. **Predicate Grammar**: Tests the parsing and serialization of predicates, which are used to describe relationships between components in the PCP. The tests verify that predicates can be round-tripped between string and object representations.
3. **Registry Validation**: Tests that the predicate registry is fail-closed, meaning that unregistered predicates are handled gracefully and do not result in unexpected behavior.

## Key entry points
- `test_golden_graph_loads()`: Validates that the golden graph fixture can be loaded and contains the expected number of nodes and links.
- `test_golden_certificate_round_trips()`: Ensures that certificates can be read, written, and read again without loss of information.
- `test_golden_contracts_load()`: Verifies that contracts can be loaded from the golden fixture.
- `test_golden_marks_and_pyramid_config_parse()`: Checks that marks and pyramid configurations can be parsed from their respective fixtures.
- `test_predicate_parse_and_serialize_round_trip()`: Tests the round-trip parsing and serialization of predicates.
- `test_registry_has_every_kind_and_is_fail_closed()`: Validates that the predicate registry is fail-closed and handles unregistered predicates correctly.

## Dependencies
The module depends on the `isidore` package, specifically:
- `contracts`, `detectors`, `humanpack`, `pyramid`, `reconcile`, `verify` for core functionality.
- `isidore.cli.main` for CLI subcommand registration.
- `isidore.graph.load_graph` for loading graph fixtures.
- `isidore.pcp` for PCP-related types and functions, including `Certificate`, `Mark`, `Predicate`, and `VerifyContext`.

## How to change safely
When modifying this module, follow these guidelines:
1. **Golden Fixtures**: If changing the structure of the golden fixtures (e.g., `graph.json`, `contracts.json`), ensure that the corresponding tests (`test_golden_graph_loads`, `test_golden_contracts_load`) are updated to reflect the new structure.
2. **Predicate Grammar**: If adding or modifying predicate types, update the `test_predicate_parse_and_serialize_round_trip` test to include the new types.
3. **Registry**: If adding new predicate kinds, ensure they are registered in the `VerifyContext` and that the `test_registry_has_every_kind_and_is_fail_closed` test is updated to include the new kind.
4. **Certificate Handling**: If modifying the `Certificate` or `Mark` types, ensure that the `test_golden_certificate_round_trips` and `test_golden_marks_and_pyramid_config_parse` tests are updated to reflect the changes.
