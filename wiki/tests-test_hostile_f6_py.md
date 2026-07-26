## Purpose
`tests/test_hostile_f6.py` tests the resilience of the knowledge home system when its own data is corrupted, enormous, or lying. It focuses on failure modes that have actually occurred in production, such as truncated JSONL files from interrupted writes, half-flushed state files, and sources that return more data than expected. The tests ensure that the system does not crash and that incorrect answers are never presented as correct ones. The module verifies that claims are properly marked as "orphan" when their evidence is lost, and that partial corruption (like a half-written JSONL line) does not invalidate the rest of the data.

## Architecture
The module uses pytest fixtures and helper functions to simulate and test hostile conditions. The `home` fixture sets up a temporary environment, and `_store` and `_item` functions create test data. Each test case manipulates the data in a specific way (e.g., deleting raw files, truncating JSONL lines) and verifies the system's response. The tests cover three main scenarios:
1. A purged item makes its claim an "orphan" instead of a "lie" (`test_a_purged_item_makes_its_claim_an_orphan_not_a_lie`).
2. A half-written JSONL line does not invalidate the rest of the data (`test_a_half_written_jsonl_line_costs_only_that_line`).
3. A corrupt state file is re-ingested from scratch instead of crashing (`test_a_corrupt_state_re_ingests_from_scratch_instead_of_crashing`).

## Key entry points
- `home`: A pytest fixture that sets up a temporary environment for testing.
- `_store`: A helper function that writes test items to the knowledge home and records the run.
- `_item`: A helper function that creates a test item with a given ID and content.
- `test_a_purged_item_makes_its_claim_an_orphan_not_a_lie`: Tests that a claim is marked as "orphan" when its evidence is deleted.
- `test_a_half_written_jsonl_line_costs_only_that_line`: Tests that a truncated JSONL line does not invalidate the rest of the data.
- `test_a_corrupt_state_re_ingests_from_scratch_instead_of_crashing`: Tests that a corrupt state file is recovered and the data is still accessible.

## Dependencies
The module depends on the following external modules:
- `pytest` for testing.
- `isidore.claims` for checking claims and evidence hashing.
- `isidore.connectors.base` for ingest options.
- `isidore.connectors.store` for functions like `create_run_id`, `iso_now`, `iter_items`, `read_state`, `record_run`, `resolve_uri`, `write_items`, and `write_state`.
- `isidore.home` for `connector_dir` and `state_path`.

## How to change safely
To modify `tests/test_hostile_f6.py`, follow these guidelines:
1. **Add new tests for new failure modes**: If a new failure mode is discovered, add a new test case that simulates the condition and verifies the system's response.
2. **Update helper functions**: If the test data needs to be changed, update the `_store` and `_item` functions to reflect the new requirements.
3. **Ensure existing tests pass**: Before committing changes, ensure that all existing tests pass to maintain the system's resilience guarantees.
