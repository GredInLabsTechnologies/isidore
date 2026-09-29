## Purpose
`tests/test_overview.py` verifies the behavior of the product overview generator, ensuring it correctly processes verified claims, handles dry runs, and enforces integrity constraints. The tests focus on three key aspects: claim verification, dry-run behavior, and composed integrity. The module exists to validate that the overview page is built from verified claims and that the system correctly handles dependencies between pages.

## Architecture
The test module uses pytest fixtures to create a mock repository with a module page (`mod.md`) that contains verified claims. The tests then exercise the `compile_overview` function, which generates the overview page, with different configurations to verify its behavior. The key components are:
- A `repo` fixture that sets up a temporary repository with a module page and its certificate.
- Test functions that verify specific behaviors of the overview compilation process.

## Key entry points
The primary entry points are the test functions:
- `test_only_proven_claims_become_citable_facts`: Verifies that only claims with a `TRUE` verdict are included in the overview (`tests/test_overview.py:53`).
- `test_dry_run_makes_no_call_and_reports_the_material`: Ensures that a dry run does not call the LLM and correctly reports the material (`tests/test_overview.py:59`).
- `test_a_wiki_claim_is_chained_and_verified_instead_of_being_dropped`: Validates that wiki claims are correctly chained and verified, and that the child certificate is hashed into the overview's (`tests/test_overview.py:66`).
- `test_a_page_that_can_prove_nothing_is_refused`: Confirms that pages with no verifiable claims are refused (`tests/test_overview.py:82`).
- `test_a_claim_citing_a_refuted_fact_does_not_count_as_proof`: Pins that a page citing the child claim that came back `FALSE` proves nothing and is not written (`tests/test_overview.py:92`).
- `test_jargon_earns_one_rewrite_and_then_the_page_is_refused`: Exercises the plain-language gate — technical wording gets one rewrite before the page is refused (`tests/test_overview.py:99`).

## Dependencies
The module imports from two places. From `isidore.pcp` it takes the certificate primitives it uses to build its fixture — `CERT_SUFFIX`, `Certificate`, `ClaimVerdict` and `write_certificate` (`tests/test_overview.py:8`). From `isidore.pyramid` it takes the functions under test — `compile_overview`, `compile_subsystems`, `missing_sections`, `relink_wiki_uris`, `subsystem_page_name` and `verified_claims` (`tests/test_overview.py:9`). It also depends on `src/isidore/verify.py`.

## How to change safely
When modifying `tests/test_overview.py`, ensure that:
- The `repo` fixture correctly sets up the test environment with the necessary files and certificates.
- Test functions accurately reflect the expected behavior of the overview compilation process.
- Changes do not introduce new dependencies or break existing ones.
- The test coverage remains comprehensive, including edge cases like dry runs and unverifiable claims.
