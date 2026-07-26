## Purpose
The `tests/test_recertify.py` module tests the `recertify` functionality in the Isidore system, specifically focusing on repairing certificates for wiki pages when the code has evolved beyond the original extractor's capabilities. It ensures that certificates are updated to reflect current code state without altering the prose content of the pages. The module addresses a "GIMO" (Graph Is More Outdated) case where a module-level constant was missed by an older extractor, leading to a certificate that was less correct than the actual code.

## Architecture
The module uses a test-driven approach to verify the behavior of the `recertify` function. It constructs synthetic repositories with code and wiki pages, creates certificates with predefined claims, and then tests how the system handles these cases. Key components include:
- `_repo()`: Creates a temporary repository with a Python module and a wiki page.
- `_cert()`: Generates a certificate for a wiki page with specified claims.
- `_claim()`: Creates a claim verdict with configurable predicate and verdict.
- Test functions that exercise different scenarios of certificate repair and validation.

## Key entry points
The primary entry points are the test functions:
- `test_a_certificate_the_code_outgrew_is_repaired_without_a_model_call()`: Tests that a certificate for a page with a module-level constant is repaired without calling an LLM.
- `test_the_prose_is_not_touched()`: Verifies that the prose content of a wiki page remains unchanged during recertification.
- `test_a_dry_run_reports_but_writes_nothing()`: Ensures that a dry run of recertification reports changes but does not write them to disk.
- `test_the_verified_mass_is_recomputed_not_carried_over()`: Confirms that the verified mass is recomputed rather than carried over from the previous certificate.

## Dependencies
The module depends on:
- `pytest` for test execution.
- `isidore.pcp` for certificate and claim handling.
- `isidore.recertify` for the core recertification logic.
- `isidore.verify` for verifying page certificates.

## How to change safely
When modifying this module:
1. Preserve the existing test structure and helper functions (`_repo`, `_cert`, `_claim`).
2. Ensure that new tests follow the same pattern of creating synthetic repositories and certificates.
3. Do not introduce LLM calls in the test logic, as the module explicitly avoids them.
4. Maintain the separation between test cases and helper functions to keep the codebase clean and maintainable.
