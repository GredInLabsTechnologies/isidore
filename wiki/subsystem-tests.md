## What this area is responsible for
The `tests` area ensures the correctness and reliability of the system by validating its core functionality. It verifies claims, connectors, language specifications, and security policies, while also testing the pipeline, surface interactions, and unit behaviors. This area acts as a safety net, catching regressions and ensuring the system behaves as expected.

## How the work is divided
The modules split responsibilities based on their domain:
- `test_claims.py` validates claim classification, extraction, and staleness detection.
- `test_verify.py` ensures claims are anchored correctly and predicates are verified.
- `test_whatsnew.py` tracks changes in the repository and reports deltas accurately.
- Other modules test connectors, language specs, security, and pipeline behavior.
The split aligns with functional boundaries: claims, verification, and change tracking are distinct concerns.

## What it depends on, and what depends on it
This area depends on the system's core modules to test them. It promises to catch issues early, ensuring the rest of the system remains stable. No other area depends on it directly, but its results inform broader development and deployment decisions.

## Where to start reading
- `tests-test_verify_py.md` for understanding how claims are anchored and predicates verified.
- `tests-test_whatsnew_py.md` to see how changes are tracked and reported.
- `tests-test_claims_py.md` for details on claim classification and extraction.
