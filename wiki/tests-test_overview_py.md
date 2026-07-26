## Purpose
`tests/test_overview.py` verifies the behavior of the product overview generator, ensuring it correctly processes verified claims, handles dry runs, and enforces integrity constraints. The tests focus on three key aspects: claim verification, dry-run behavior, and composed integrity. The module exists to validate that the overview page is built from verified claims and that the system correctly handles dependencies between pages.

## Architecture
The test module uses pytest fixtures to create a mock repository with a module page (`mod.md`) that contains verified claims. The tests then exercise the `compile_overview` function, which generates the overview page, with different configurations to verify its behavior. The key components are:
- A `repo` fixture that sets up a temporary repository with a module page and its certificate.
- Test functions that verify specific behaviors of the overview compilation process.

## Key entry points
The primary entry points are the test functions:
- `test_only_proven_claims_become_citable_facts`: Verifies that only claims with a `TRUE` verdict are included in the overview.
- `test_dry_run_makes_no_call_and_reports_the_material`: Ensures that a dry run does not call the LLM and correctly reports the material.
- `test_a_wiki_claim_is_chained_and_verified_instead_of_being_dropped`: Validates that wiki claims are correctly chained and verified.
- `test_a_page_that_can_prove_nothing_is_refused`: Confirms that pages with no verifiable claims are refused.

## Dependencies
The module depends on the `isidore.pyramid` module, which provides functions like `compile_overview`, `verified_claims`, and `write_certificate`. These functions are used to generate the overview page, retrieve verified claims, and write certificates, respectively.

## How to change safely
When modifying `tests/test_overview.py`, ensure that:
- The `repo` fixture correctly sets up the test environment with the necessary files and certificates.
- Test functions accurately reflect the expected behavior of the overview compilation process.
- Changes do not introduce new dependencies or break existing ones.
- The test coverage remains comprehensive, including edge cases like dry runs and unverifiable claims.
