## Purpose
The `tests/test_recertify.py` module tests the `recertify` functionality in the Isidore system, specifically focusing on repairing certificates that have become outdated due to code changes. The module addresses a "GIMO" (Gone In My Outgrowth) case where a certificate's claims no longer match the current code state, causing verification to fail. The tests ensure that the `recertify` function can update certificates without modifying the prose content and that it correctly handles various edge cases like dry runs and mass verification updates.

## Architecture
The module uses a test-driven approach to verify the behavior of the `recertify` function. It constructs synthetic repositories with code and certificates, then tests how the system handles different scenarios:
- Certificates that need repair due to code changes
- Cases where prose content should not be altered
- Dry runs that report changes without writing them
- Verified mass updates that reflect current verification results

Key helper functions create test repositories (`_repo`), generate certificates (`_cert`), and define claims (`_claim`), allowing the tests to simulate real-world scenarios with controlled inputs.

## Key entry points
The module's helpers and test functions are:
- `_repo()`: Creates a synthetic repository with a `svc.py` module defining `LIMIT` and a `handler`, a graph, and a wiki page (`tests/test_recertify.py:18-L28`).
- `_cert()`: Writes a certificate with given claims, optional mass and children (`tests/test_recertify.py:31-L36`).
- `_claim()`: Builds a `ClaimVerdict` defaulting to `predicate="defines:svc.py;LIMIT"` and `verdict=FALSE` (`tests/test_recertify.py:39-L41`).
- `test_a_certificate_the_code_outgrew_is_repaired_without_a_model_call`: The GIMO case — a certificate recorded FALSE but the current oracle proves TRUE; recertify repairs it and `verify_page` passes (`tests/test_recertify.py:46-L57`).
- `test_the_prose_is_not_touched`: Asserts the wiki page bytes are unchanged after recertification (`tests/test_recertify.py:60-L65`).
- `test_a_dry_run_reports_but_writes_nothing`: Asserts `recertify(root)` without `write=True` reports `ACT_RECERTIFY` but writes nothing (`tests/test_recertify.py:68-L75`).
- `test_the_verified_mass_is_recomputed_not_carried_over`: Asserts mass moves from `yellow=1` to `green=1` after recertification (`tests/test_recertify.py:78-L84`).

## Dependencies
The module depends on five cross-module imports:
- `src/isidore/pcp.py` (1 link) — for `CERT_SUFFIX`, `FALSE`, `TRUE`, `UNDECIDABLE`, `Certificate`, `ClaimVerdict`, `VerifiedMass`, `prose_hash`, `read_certificate`, `write_certificate` (`tests/test_recertify.py:11`).
- `src/isidore/recertify.py` (1 link) — for `ACT_NO_CERT`, `ACT_RECERTIFY`, `ACT_REFUTED`, `ACT_TAMPERED`, `recertify` (`tests/test_recertify.py:12`).
- `src/isidore/verify.py` (1 link) — for `CERT_DRIFTED`, `CERT_OK`, `certificate_status`, `verify_page` (`tests/test_recertify.py:13`).
- `src/isidore/pipeline.py` (1 link) — imported by the test module.
- `src/isidore/graph.py` (1 link) — imported by the test module.

## How to change safely
When modifying this module:
1. Maintain the existing test structure and helper functions
2. Ensure all changes are covered by tests that verify the core functionality
3. Preserve the separation between test cases and helper functions
4. Keep the module focused on testing certificate repair scenarios
5. Update the test data to reflect any changes in the certificate format or verification logic
