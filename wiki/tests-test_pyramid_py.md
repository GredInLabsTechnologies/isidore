## Purpose
`tests/test_pyramid.py` is a test module for the `isidore.pyramid` subsystem, specifically focused on verifying the correctness of the `plan_pyramid` function and the `wikichain` verifier. It ensures that the pyramid planning logic (which organizes code into subsystems) works as expected, particularly in handling real-world graph data and configuration. The module also tests the `wikichain` verifier, which resolves claims against certificates in the wiki, ensuring that the verification logic is fail-closed and handles edge cases like `None` predicates correctly.

## Architecture
The module uses a combination of golden fixtures (predefined test data) and synthetic test cases to verify the behavior of `plan_pyramid` and `_wikichain_verifier`. The `_graph()` helper function loads a real graph from a fixture file, while other tests construct minimal graphs to isolate specific behaviors. The tests cover:
- Auto-seeding of subsystems from source files.
- Explicit configuration overrides.
- Inter-subsystem dependency tracking via import links.
- The `wikichain` verifier's handling of `None` predicates and certificate-based resolution.

## Key entry points
- `_graph()`: Loads the real graph from a fixture file.
- `test_autoseed_groups_by_source_file_on_the_real_graph()`: Verifies that auto-seeding groups nodes by their top-level source directory.
- `test_explicit_config_still_works()`: Ensures explicit configuration overrides auto-seeding.
- `test_links_used_for_inter_subsystem_deps()`: Confirms that import links are correctly translated into subsystem dependencies.
- `test_wikichain_none_does_not_crash()`: Tests that the `wikichain` verifier handles `None` predicates without crashing.
- `test_wikichain_resolves_verdict_from_certificate()`: Validates that the verifier correctly resolves verdicts from certificates.

## Dependencies
The module depends on:
- `isidore.graph.load_graph`: To load the graph data.
- `isidore.pcp`: For certificate, claim, and predicate handling.
- `isidore.pyramid`: For the `plan_pyramid` and `_wikichain_verifier` functions.

## How to change safely
When modifying this module, follow these guidelines:
1. **Golden Fixtures**: If changing the behavior of `plan_pyramid`, update the golden fixture (`graph.json`) to reflect the new expected output. This ensures the test remains accurate.
2. **Test Isolation**: When adding new tests, prefer synthetic test cases over the real graph to isolate specific behaviors.
3. **Certificate Handling**: If modifying the `wikichain` verifier, ensure it continues to handle edge cases like `None` predicates and missing claims correctly.
4. **Dependencies**: Avoid introducing new dependencies unless necessary, as this module is designed to be lightweight and focused.
