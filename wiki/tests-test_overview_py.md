## Purpose
`tests/test_overview.py` verifies the correctness of the product overview generation logic. It ensures that the overview page is built from verified claims, that claims are properly chained and validated, and that the page is only published when it can be proven. The module tests the `compile_overview` function and its dependencies, including `verified_claims`, to confirm that only TRUE claims are included and that the overview page reflects the project's actual state.

## Architecture
The module uses pytest fixtures to create a test repository with a module page (`mod.md`) that contains verified claims. The test cases then exercise the overview compilation logic, checking that claims are filtered correctly, that the overview page is only written when it can be proven, and that child certificates are properly referenced. The test data includes a TRUE claim (`c-1111`) and a FALSE claim (`c-2222`), allowing the tests to verify the filtering behavior.

## Key entry points
- `repo`: A pytest fixture that creates a test repository with a module page and certificates for verified claims.
- `test_only_proven_claims_become_citable_facts`: Verifies that only TRUE claims are included in the overview facts.
- `test_dry_run_makes_no_call_and_reports_the_material`: Ensures that a dry run does not call the LLM and reports the available material.
- `test_a_wiki_claim_is_chained_and_verified_instead_of_being_dropped`: Confirms that claims from the wiki are properly chained and verified.
- `test_a_page_that_can_prove_nothing_is_refused`: Checks that the overview page is not published if it cannot be proven.

## Dependencies
The module depends on the `isidore.pcp` and `isidore.pyramid` modules, which provide the `Certificate`, `ClaimVerdict`, and overview compilation functions. It also uses pytest for testing.

## How to change safely
When modifying `tests/test_overview.py`, ensure that:
1. The test repository structure remains consistent with the fixture.
2. The test cases continue to verify the correct behavior of the overview compilation logic.
3. The claims and certificates are updated to reflect any changes in the overview generation logic.
4. The test cases are updated to reflect any changes in the expected behavior of the overview page.
