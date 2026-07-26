> [!WARNING]
> **SECURITY — unverified suspect(s) flagged automatically while compiling this page.**
> Detected from the evidence, not from a security scan. Treat as review items to VERIFY, never as intended features to preserve:
>
> - `tests/test_detectors.py:22` — security risk: hardcoded secret (sk_live_) is flagged as dangerous

## Purpose
The `tests/test_detectors.py` module serves as a test suite for the `isidore.detectors` subsystem, specifically validating the correctness, determinism, and robustness of security detectors. It focuses on three critical properties: (1) detectors must flag specific security issues (e.g., high-entropy strings) without false positives, (2) they must be deterministic (producing identical results on repeated runs), and (3) they must handle edge cases gracefully (e.g., missing files). The tests use golden fixtures to verify behavior against known-good inputs, ensuring detectors meet the system's security and reliability requirements.

## Architecture
The module is structured around a shared test context (`_ctx()`) that loads a predefined graph and repository state from fixtures. Each test function exercises a distinct aspect of the detectors:
- `test_entropy_flags_the_backdoor_token`: Confirms high-entropy strings (e.g., secrets) are flagged with the correct severity.
- `test_specificity_no_false_positive_on_ordinary_strings`: Ensures detectors do not flag non-secret strings.
- `test_topology_reaches_tokens_from_auth`: Validates that topology-based detectors correctly identify sensitive tokens.
- `test_determinism`: Verifies that the detector output is consistent across runs.
- `test_unreadable_file_does_not_crash`: Confirms the system degrades gracefully when files are missing.
- `test_shannon_entropy_basic`: Tests the entropy calculation function directly.

The tests rely on the `isidore.detectors` and `isidore.graph` modules to scan repositories and load graph data, respectively. The `VerifyContext` class provides the execution context for the detectors.

## Key entry points
The module's entry points are the test functions:
- `_ctx()`: Initializes the test context by loading the graph and repository state.
- `test_entropy_flags_the_backdoor_token`: The primary test for entropy-based detection.
- `test_specificity_no_false_positive_on_ordinary_strings`: Ensures specificity in detection.
- `test_topology_reaches_tokens_from_auth`: Validates topology-based detection.
- `test_determinism`: Confirms deterministic behavior.
- `test_unreadable_file_does_not_crash`: Tests error handling for missing files.
- `test_shannon_entropy_basic`: Tests the entropy calculation function.

## Dependencies
The module depends on:
- `isidore.detectors`: Provides the `scan` and `shannon_entropy` functions for scanning repositories and calculating entropy.
- `isidore.graph`: Provides the `load_graph` function to load graph data from JSON files.
- `isidore.pcp`: Provides the `VerifyContext` class for the test context.

## How to change safely
To modify this module safely:
1. **Add new tests**: Follow the pattern of existing tests, ensuring they validate a specific property (e.g., determinism, specificity) and use the shared `_ctx()` function.
2. **Update fixtures**: If tests fail due to changes in the detectors or graph structure, update the fixtures in `tests/fixtures/pcp` to reflect the new expected behavior.
3. **Preserve determinism**: Ensure new tests do not introduce non-deterministic behavior, as this could break the `test_determinism` check.
4. **Handle edge cases**: When adding new tests, consider edge cases like missing files or invalid inputs, and ensure the system degrades gracefully.
