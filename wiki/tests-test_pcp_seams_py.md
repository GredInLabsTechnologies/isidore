## Purpose
The `tests/test_pcp_seams.py` module serves as a gatekeeper for the Proof-Carrying Prose (PCP) system's frozen seam, ensuring that the system's golden fixtures (graph, certificates, contracts, and predicate grammar) are correctly parsed and exposed. It does NOT verify the logic of each lane's gate (e.g., the actual verification of claims), but rather checks that the system's public surface is stable and self-consistent. This includes verifying that types round-trip, the registry is wired fail-closed, and CLI subcommands are registered.

## Architecture
The module is organized into three main sections:
1. **Fixtures Parsing**: Tests for loading and validating golden fixtures (graph, certificates, contracts, marks, and pyramid configuration).
2. **Predicate Grammar**: Tests for parsing and serializing predicates, including round-trip validation and rejection of invalid predicates.
3. **Registry Fail-Closed**: Tests for ensuring the predicate registry is fail-closed, meaning unregistered predicates degrade to `UNDECIDABLE` rather than failing.

## Key entry points
- `test_golden_graph_loads()`: Validates the structure of the golden graph — 5 nodes, 4 links, and a commit hash starting with `0f1e5ba` (`tests/test_pcp_seams.py:36-L39`).
- `test_golden_certificate_round_trips()`: Reads the golden certificate, asserts 6 claims (5 typed with predicate, 1 existence-anchored), checks `marks[0].family == "entropy"`, then proves `write_certificate` → `read_certificate` is byte-deterministic (`tests/test_pcp_seams.py:42-L54`).
- `test_golden_contracts_load()`: Loads the golden contracts fixture and asserts exactly one contract with predicate `calls:authenticate;verify_jwt` (`tests/test_pcp_seams.py:57-L59`).
- `test_golden_marks_and_pyramid_config_parse()`: Parses `marks.json` (3 families: entropy, sink, topology) and `pyramid_config.json` (first subsystem is authentication) (`tests/test_pcp_seams.py:62-L67`).
- `test_predicate_parse_and_serialize_round_trip()`: Parametrized over `calls:a;b`, `value:X;5`, `env:KEY` — asserts `parse_predicate(raw).serialize() == raw` (`tests/test_pcp_seams.py:77-L80`).
- `test_predicate_rejects_absent_or_unknown()`: Parametrized over `""`, `None`, `"no-colon"`, `"bogus:x"`, `"calls:"` — all return `None` (`tests/test_pcp_seams.py:83-L85`).
- `test_wiki_uri_parsing()`: Asserts `parse_wiki_uri("wiki://svc.md#c-d64d0c93")` returns `("svc.md", "c-d64d0c93")` and a plain path returns `None` (`tests/test_pcp_seams.py:88-L90`).
- `test_registry_has_every_kind_and_is_fail_closed()`: Constructs a `VerifyContext`, verifies four predicate kinds all return `UNDECIDABLE` with `ORACLE_NONE`, and confirms an unregistered kind also degrades to `UNDECIDABLE` — never `TRUE` (`tests/test_pcp_seams.py:95-L102`).

## Dependencies
The module depends on eight cross-module imports:
- `src/isidore/__init__.py` (1 link) — imported as `from isidore import contracts, detectors, humanpack, pyramid, reconcile, verify` (`tests/test_pcp_seams.py:12`).
- `src/isidore/contracts.py` (1 link) — accessed via the `contracts` namespace.
- `src/isidore/detectors.py` (1 link) — accessed via the `detectors` namespace.
- `src/isidore/humanpack.py` (1 link) — accessed via the `humanpack` namespace.
- `src/isidore/pyramid.py` (1 link) — accessed via the `pyramid` namespace.
- `src/isidore/reconcile.py` (1 link) — accessed via the `reconcile` namespace.
- `src/isidore/verify.py` (1 link) — accessed via the `verify` namespace.
- `src/isidore/cli.py` (1 link) — for `main` (`tests/test_pcp_seams.py:13`).

## How to change safely
When modifying this module, ensure that:
1. **Golden Fixtures**: Any changes to the golden fixtures (graph, certificates, contracts, marks, or pyramid configuration) must be reflected in the corresponding tests.
2. **Predicate Grammar**: If the predicate grammar changes, update the tests to reflect the new grammar and ensure round-trip serialization works as expected.
3. **Registry Fail-Closed**: If new predicate kinds are added, ensure they are registered in the `VerifyContext` and that the registry remains fail-closed.
