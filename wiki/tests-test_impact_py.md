## Purpose
The `tests/test_impact.py` module tests the emergent interaction detection capabilities of Isidore's impact analysis system. It verifies that the system can identify new cross-module dependencies (edges) and removed dependencies in a real Git repository, using a synthetic test setup with two Python packages (`aaa` and `bbb`). The tests ensure that the impact analysis correctly reports changes in the dependency graph and identifies affected modules and pages.

## Architecture
The module uses a test fixture (`_seed_repo`) to create a temporary Git repository with two Python packages, each containing a simple module. The test cases then modify the code to introduce new dependencies or remove existing ones, and verify that the impact analysis detects these changes. The key components are:

1. `_seed_repo`: Creates a Git repository with two packages (`aaa` and `bbb`), each containing a module with a simple function.
2. Test cases: Modify the code to introduce or remove dependencies and verify the impact analysis results.

## Key entry points
- `_seed_repo`: Initializes a test repository with two packages and commits the initial state.
- `test_impact_reports_a_new_cross_module_edge_as_emergent`: Tests detection of new cross-module dependencies.
- `test_impact_reports_a_removed_edge`: Tests detection of removed cross-module dependencies.
- `test_impact_check_exit_signal_and_clean`: Verifies the exit signal and cleanup behavior of the impact analysis.

## Dependencies
The module depends on:
- `isidore.graph.write_scan`: For scanning the repository and generating the dependency graph.
- `isidore.impact.build_impact`: For building the impact analysis results.
- `isidore.impact.render_impact`: For rendering the impact analysis results.
- `isidore.pipeline.compile_wiki`: For compiling the wiki pages based on the dependency graph.

## How to change safely
When modifying this module, follow these guidelines:
1. Preserve the test repository setup (`_seed_repo`) and the test cases' structure.
2. Ensure that any changes to the test cases maintain the same assertions and verification logic.
3. Do not remove or alter the existing test cases unless they are obsolete.
4. When adding new test cases, follow the same pattern of modifying the code and verifying the impact analysis results.
