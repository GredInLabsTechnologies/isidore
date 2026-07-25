## Purpose
The module `tests/test_connectors_f1.py` tests the idempotency of the git-repo connector in Isidore's knowledge home system. Its core assertion is that re-ingesting a git repository with no changes should yield zero new items, ensuring the connector properly tracks and persists its cursor state. This is critical for the system's reliability, as the first draft failed to persist the cursor, leading to duplicate items on re-ingestion.

## Architecture
The test suite uses helper functions to manage git repositories and interact with Isidore's storage system. Key components include:
- `_make_repo`: Creates a test git repository with a single commit.
- `_git`: Wraps git commands for repository operations.
- `_head`: Retrieves the current git commit hash.
- `store`: The raw storage system that persists items and state.

The tests verify:
1. Environment variable overrides for the knowledge home directory.
2. Content hashing (`chash`) and normalization of stored items.
3. State management, including handling missing or corrupt state files.
4. Run history retention, ensuring only the last 20 runs are kept.

## Key entry points
- `test_home_env_override`: Tests environment variable configuration for the knowledge home.
- `test_write_items_stamps_chash_and_does_not_mutate`: Validates content hashing and immutability of input items.
- `test_read_state_missing_and_corrupt_return_default`: Ensures graceful handling of missing or corrupt state files.
- `test_record_run_keeps_last_20`: Verifies run history retention limits.

## Dependencies
The module depends on:
- `isidore.connectors.base.IngestOptions`: For ingestion configuration.
- `isidore.connectors.git_repo.GitRepoConnector`: The git-repo connector under test.
- `isidore.connectors.store`: The raw storage system.
- `isidore.home`: For knowledge home and state path management.

## How to change safely
When modifying this module:
1. Preserve the idempotency assertion as the load-bearing test.
2. Maintain the helper functions (`_make_repo`, `_git`, `_head`) to ensure consistent test setup.
3. Do not alter the state file structure or run history retention logic, as these are critical for the system's reliability.
4. When adding new tests, ensure they do not interfere with the existing idempotency guarantees.
