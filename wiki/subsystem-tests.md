## What this area is responsible for
`tests` is the evidence that the machinery in `src` does what its pages say. Most modules pin one behaviour of one part of the system, and many are regression tests named after the failure they prevent — a stale claim that went unnoticed, a wiki read back as input, source sent to a host nobody declared.

## How the work is divided
- **The proving core.** Claims, verification and certificates are tested from several sides: `tests-test_claims_py.md` (parsing, hashing, staleness), `tests-test_verify_py.md`, `tests-test_recertify_py.md`, `tests-test_reconcile_py.md`, `tests-test_pcp_pipeline_py.md` and `tests-test_pcp_seams_py.md`, which guards the frozen seam against golden fixtures kept in `tests-fixtures-pcp.md`.
- **The compiler.** `tests-test_pipeline_py.md`, `tests-test_incremental_py.md` (a page is rewritten only where its facts changed), `tests-test_changeset_py.md` and `tests-test_impact_py.md` cover planning, change detection and incremental compilation; `tests-test_pyramid_py.md` and `tests-test_overview_py.md` cover the pages built on top of module pages.
- **The boundaries.** What may leave the machine and what may enter the wiki: `tests-test_source_disclosure_gate_py.md`, `tests-test_classification_gate_py.md`, `tests-test_wiki_not_input_py.md`, `tests-test_security_prose_py.md` and `tests-test_detectors_py.md`.
- **The knowledge home.** Connectors and their hostile inputs: `tests-test_connectors_f1_py.md`, `tests-test_connectors_f4_py.md`, `tests-test_connectors_f5_py.md`, `tests-test_mcp_barrier_py.md` and `tests-test_hostile_f6_py.md`.

The split mirrors `src`, so the test page to open is the one named after the module being changed.

## What it depends on, and what depends on it
The area depends on `src` alone and builds its own inputs — temporary git repositories and golden fixtures such as an auth module whose limits and calls are known in advance — so every expectation is checked against something the test controls.

## Where to start reading
- `tests-test_claims_py.md` — how a claim is anchored and when it goes stale.
- `tests-test_pipeline_py.md` — the compiler end to end.
- `tests-test_pcp_seams_py.md` — the contract the proving layer must keep.
- `tests-test_source_disclosure_gate_py.md` — the boundary a change must not cross.
