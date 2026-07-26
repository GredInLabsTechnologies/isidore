## What this area is responsible for
The `tests` area ensures the correctness, robustness, and security of the Isidore system by validating its core functionality through unit, integration, and regression tests. It verifies that claims, connectors, detectors, and pipelines behave as expected, enforcing integrity constraints and tamper-evident certificates.

## How the work is divided
The tests are split by subsystem: claims parsing, change detection, connector behavior, security enforcement, and pipeline validation. This division mirrors the system's architecture, ensuring that each test module focuses on a specific component's correctness. For example, `tests/test_claims.py` validates claim handling, while `tests/test_pcp_pipeline.py` ensures the PCP pipeline generates valid certificates.

## What it depends on, and what depends on it
This area depends on the core system's modules but makes no assumptions about external dependencies. It is the final gatekeeper for correctness, as it verifies the system's behavior before deployment. No other area depends on it directly, but its results inform confidence in the system's reliability.

## Where to start reading
- `tests/test_claims.py.md` for understanding how claims are parsed and verified.
- `tests/test_pcp_pipeline.py.md` to see how tamper-evident certificates are generated.
- `tests/test_detectors.py.md` for security detector validation.
