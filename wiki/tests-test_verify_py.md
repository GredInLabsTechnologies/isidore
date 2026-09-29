## Purpose
The `tests/test_verify.py` module tests the Proof-Carrying Prose (PCP) system, which verifies typed claims against two oracles (a code graph and prose text) and generates tamper-evident certificates. The module ensures that claims are correctly parsed, anchored, and verified, and that the resulting certificates match golden expectations. It serves as a "Lane A gate" — a critical checkpoint where claims are decided and certificates are built for offline verification.

## Architecture
The module uses a test-driven approach to validate the PCP pipeline. It defines helper functions to create a `VerifyContext` and anchor claims, then tests the claim parsing, predicate verification, and certificate generation. The tests rely on golden fixtures (predefined inputs and outputs) to verify behavior.

## Key entry points
- `_ctx()`: Creates a `VerifyContext` with a loaded code graph from `graph.json` and the `REPO` path (`tests/test_verify.py:16-L18`).
- `_anchored()`: Reads `svc.md`, parses its claims block, and anchors claims against the repo (`tests/test_verify.py:21-L25`).
- `test_three_field_parser_captures_predicate()`: Verifies three-field claims parse to `predicate="calls:x;y"` while two-field claims have no predicate (`tests/test_verify.py:28-L32`).
- `test_each_predicate_kind_decides_correctly()`: Tests 10 predicate cases against `_ctx()` — `calls`, `value`, `imports`, `env`, `defines`, `signature` prove TRUE; wrong `calls`/`value` prove FALSE; partial-graph `imports` and absent `route` degrade to `UNDECIDABLE` (`tests/test_verify.py:35-L51`).
- `test_certificate_matches_golden_verdicts()`: Builds a certificate from `svc.md` and asserts all five typed predicates prove `TRUE`, the existence-anchored claim stays `UNDECIDABLE`, and `prose_sha256` is 64 chars (`tests/test_verify.py:54-L65`).
- `test_imports_and_value_fail_closed_to_undecidable_not_false()`: Dogfood regression — a missing import degrades to `UNDECIDABLE` (not `FALSE`), a real import proves `TRUE`, and a non-literal value degrades to `UNDECIDABLE` (`tests/test_verify.py:68-L79`).

## Dependencies
The module depends on four cross-module imports:
- `src/isidore/claims.py` (1 link) — for `anchor_claims`, `parse_claims_block`, `parse_predicate_field` (`tests/test_verify.py:7`).
- `src/isidore/graph.py` (1 link) — for `load_graph` (`tests/test_verify.py:8`).
- `src/isidore/pcp.py` (1 link) — for `FALSE`, `TRUE`, `UNDECIDABLE`, `VerifyContext`, `prose_hash`, `verify_predicate` (`tests/test_verify.py:9`).
- `src/isidore/verify.py` (1 link) — for `build_certificate`, `classify_mass`, `ground_symbols`, `verify_page` (`tests/test_verify.py:10`).

## How to change safely
When modifying this module:
1. **Preserve the golden fixtures**: Changes to the claim parsing or verification logic may require updating the fixtures in `tests/fixtures/pcp`.
2. **Update test cases**: If new predicate types are added, ensure they are tested in `test_each_predicate_kind_decides_correctly()`.
3. **Maintain certificate structure**: Any changes to certificate generation should be reflected in `test_certificate_matches_golden_verdicts()`.
