## Purpose
`tests/test_pcp_pipeline.py` is an integration test for the Proof-Carrying Prose (PCP) pipeline, verifying that the system correctly generates tamper-evident certificates, enforces security banners, and handles refuted claims. The test ensures the pipeline's five lanes (compilation, reconciliation, verification, deterministic marking, and certificate generation) work together end-to-end. It uses a golden fixture repository to simulate a real compile and validate the output.

## Architecture
The module defines helper functions and tests that exercise the PCP pipeline:
- `_fake_generator()` and `_fake_generator_with_a_lie()` create synthetic pages with embedded claims.
- `_compile()` sets up a test repository and runs the pipeline.
- Tests validate:
  - Certificate generation with typed verdicts (`test_compile_writes_a_certificate_with_typed_verdicts`).
  - Security banner enforcement despite calm prose (`test_deterministic_mark_forces_the_banner_despite_calm_prose`).
  - Refuted claims are quarantined (`test_refuted_claim_is_quarantined_not_published`).

## Key entry points
- `_compile()`: Sets up the test environment and runs the pipeline.
- `test_compile_writes_a_certificate_with_typed_verdicts()`: Verifies certificate generation and verdicts.
- `test_deterministic_mark_forces_the_banner_despite_calm_prose()`: Ensures security banners are enforced.
- `test_refuted_claim_is_quarantined_not_published()`: Validates refuted claims are kept in certificates.

## Dependencies
The module depends on:
- `isidore.pcp` (for `CERT_SUFFIX` and `read_certificate`).
- `isidore.pipeline` (for `WIKI_DIRNAME` and `compile_wiki`).
- `isidore.verify` (for `verify_page`).

## How to change safely
- To add a new test case, extend the existing test functions or add new ones following the pattern of existing tests.
- To modify the test data, update the fixture repository (`FIX`) and ensure the changes align with the test assertions.
- When changing the pipeline behavior, update the corresponding test assertions to reflect the new behavior.
