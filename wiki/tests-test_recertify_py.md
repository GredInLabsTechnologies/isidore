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
The module's main test functions are:
- `test_a_certificate_the_code_outgrew_is_repaired_without_a_model_call`: Verifies that outdated certificates are repaired without modifying the prose content
- `test_the_prose_is_not_touched`: Ensures that the prose content remains unchanged during recertification
- `test_a_dry_run_reports_but_writes_nothing`: Tests that dry runs report changes without writing them
- `test_the_verified_mass_is_recomputed_not_carried_over`: Verifies that the verified mass is recomputed rather than carried over from previous runs

## Dependencies
The module depends on:
- `isidore.pcp` for certificate handling and verification utilities
- `isidore.recertify` for the core recertification functionality
- `isidore.verify` for verification status constants and functions
- Standard library modules like `json`, `pathlib`, and `pytest`

## How to change safely
When modifying this module:
1. Maintain the existing test structure and helper functions
2. Ensure all changes are covered by tests that verify the core functionality
3. Preserve the separation between test cases and helper functions
4. Keep the module focused on testing certificate repair scenarios
5. Update the test data to reflect any changes in the certificate format or verification logic
