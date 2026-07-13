## Purpose
The `tests/test_connectors_f1.py` module tests the idempotency of the `GitRepoConnector` in the context of ADR-0032, which defines a system combining a knowledge home, raw store, and git-repo connector. The load-bearing test ensures that re-ingesting a git repository with no changes yields zero new items, verifying that the cursor state is properly persisted. This prevents regressions like the initial implementation that failed to persist the cursor.

## Architecture
The module uses pytest fixtures and helper functions to create a controlled test environment. Key components include:
- `_make_repo`: Creates a git repository with a single commit for testing.
- `_git`: Wraps git commands for repository operations.
- `_head`: Retrieves the current git commit hash.
- Test functions that verify the behavior of the `GitRepoConnector` and related components.

## Key entry points
The module's entry points are the test functions:
- `test_home_env_override`: Verifies that the knowledge home directory can be overridden via environment variables.
- `test_write_items_stamps_chash_and_does_not_mutate`: Ensures that items are written to the store with a content hash (`chash`) and that the original item dictionary remains unmodified.
- `test_read_state_missing_and_corrupt_return_default`: Confirms that missing or corrupt state files return a default state structure.
- `test_record_run_keeps_last_20`: Validates that only the last 20 runs are retained in the state.

## Dependencies
The module depends on:
- `pytest` for testing.
- `subprocess` for executing git commands.
- `isidore.connectors.base.IngestOptions` for ingestion options.
- `isidore.connectors.git_repo.GitRepoConnector` for the connector under test.
- `isidore.connectors.store` for interacting with the raw store.
- `isidore.home` for managing the knowledge home directory.

## How to change safely
When modifying this module:
1. Preserve the idempotency test as the load-bearing test.
2. Ensure that helper functions like `_make_repo` and `_git` remain stable to avoid breaking test setup.
3. Do not change the default state structure returned by `store.read_state` unless necessary, as it is a critical contract for the system.
4. Maintain the constraint that only the last 20 runs are kept in the state.
