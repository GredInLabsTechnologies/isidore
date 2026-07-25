## Purpose
The `tests/test_verify.py` module tests the Proof-Carrying Prose (PCP) system, which verifies typed claims against two oracles (a code graph and prose text) and generates tamper-evident certificates. The module ensures that claims are correctly parsed, anchored, and verified, and that the resulting certificates match golden expectations. It serves as a "Lane A gate" — a critical checkpoint where claims are decided and certificates are built for offline verification.

## Architecture
The module uses a test-driven approach to validate the PCP pipeline. It defines helper functions to create a `VerifyContext` and anchor claims, then tests the claim parsing, predicate verification, and certificate generation. The tests rely on golden fixtures (predefined inputs and outputs) to verify behavior.

## Key entry points
- `_ctx()`: Creates a `VerifyContext` with a loaded code graph and repository path.
- `_anchored()`: Parses and anchors claims from a Markdown file.
- `test_three_field_parser_captures_predicate()`: Verifies that three-field claims are parsed correctly.
- `test_each_predicate_kind_decides_correctly()`: Tests that each predicate type (e.g., `calls`, `value`) is verified correctly.
- `test_certificate_matches_golden_verdicts()`: Ensures the generated certificate matches expected verdicts.

## Dependencies
The module depends on:
- `isidore.claims`: For parsing and anchoring claims.
- `isidore.graph`: For loading the code graph.
- `isidore.pcp`: For the `VerifyContext` and predicate verification logic.
- `isidore.verify`: For building certificates and verifying pages.

## How to change safely
When modifying this module:
1. **Preserve the golden fixtures**: Changes to the claim parsing or verification logic may require updating the fixtures in `tests/fixtures/pcp`.
2. **Update test cases**: If new predicate types are added, ensure they are tested in `test_each_predicate_kind_decides_correctly()`.
3. **Maintain certificate structure**: Any changes to certificate generation should be reflected in `test_certificate_matches_golden_verdicts()`.
