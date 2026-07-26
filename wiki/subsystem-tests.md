## What this area is responsible for
The `tests` area ensures the correctness and reliability of the Isidore system by verifying its core functionality through unit, integration, and regression tests. It validates everything from individual components like the `changeset` and `claims` modules to end-to-end systems like Proof-Carrying Prose (PCP) and the compiler pipeline. By catching bugs early and enforcing security and correctness guarantees, this area acts as a safety net for the rest of the system.

## How the work is divided
The tests are split into specialized modules, each targeting a distinct subsystem or feature. For example, `test_changeset.py` focuses on change detection, while `test_pcp_pipeline.py` verifies PCP's certificate generation. The split aligns with the system's architecture: modules test what they depend on, and integration tests (like `test_pcp_pipeline.py`) validate cross-cutting behavior. This division ensures that failures are isolated to the relevant component, simplifying debugging.

## What it depends on, and what depends on it
This area depends on the core modules it tests but has no external dependencies. It promises to the rest of the system that all critical functionality is verified before deployment. No other area relies on the tests themselves, as they are a development-time concern.

## Where to start reading
- `tests-test_changeset_py.md` for understanding how change detection works and is tested.
- `tests-test_pcp_pipeline_py.md` to see how PCP's security guarantees are enforced and verified.
- `tests-test_claims_py.md` for details on how claims are parsed, anchored, and hashed.
