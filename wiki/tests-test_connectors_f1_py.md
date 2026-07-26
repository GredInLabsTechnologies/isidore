## Purpose
The module `tests/test_connectors_f1.py` tests the idempotency of the Isidore 1.1 Knowledge system's git-repo connector. Its core assertion is that re-ingesting a git repository with no changes should produce zero new items, ensuring the system correctly tracks and persists ingestion state. This is critical for the system's reliability, as the initial implementation failed to persist cursor state, leading to duplicate items on re-ingestion.

## Architecture
The test suite uses a combination of helper functions and pytest fixtures to simulate a git repository and verify the connector's behavior. Key components include:
- `_make_repo`: Creates a temporary git repository with a single commit.
- `_git`: Wraps git commands for repository manipulation.
- `_head`: Retrieves the current HEAD commit hash.
- `store` module: Handles item storage, state management, and content hashing.

The tests focus on two main areas:
1. **Knowledge home and store functionality**: Verifying environment variable overrides and item storage behavior.
2. **Idempotency**: Ensuring re-ingestion of an unchanged repository produces no new items.

## Key entry points
- `test_home_env_override`: Tests that the `ISIDORE_HOME` environment variable correctly overrides the knowledge home directory.
- `test_write_items_stamps_chash_and_does_not_mutate`: Verifies that items are stored with a content hash (`chash`) and that the original item dictionary remains unmodified.
- `test_read_state_missing_and_corrupt_return_default`: Ensures the system returns a default state when the state file is missing or corrupted.
- `test_record_run_keeps_last_20`: Tests that the system retains only the last 20 runs in the state.

## Dependencies
The module depends on:
- `pytest` for test execution.
- `subprocess` for git command execution.
- `isidore.connectors.base.IngestOptions` for ingestion configuration.
- `isidore.connectors.git_repo.GitRepoConnector` for the git-repo connector implementation.
- `isidore.connectors.store` for item storage and state management.
- `isidore.home` for knowledge home directory resolution.

## How to change safely
When modifying this module, follow these guidelines:
1. **Preserve idempotency**: Ensure any changes do not break the core assertion that re-ingestion of an unchanged repository produces zero items.
2. **Maintain helper functions**: The `_make_repo`, `_git`, and `_head` functions are critical for test setup. Avoid changing their behavior unless necessary.
3. **Test state management**: Any changes to state handling (e.g., `store.read_state`, `store.record_run`) must be thoroughly tested to ensure they do not introduce regressions.
4. **Document changes**: Update the module's docstring and comments to reflect any changes in behavior or assumptions.
