> [!WARNING]
> **SECURITY — deterministic detectors flagged this code (0 LLM). Verify; never document as an intended feature.**
>
> - `tests/test_reconcile.py:46` — high-entropy literal (>=24 chars, >=3.5 bits/char)
> - `tests/test_reconcile.py:63` — high-entropy literal (>=24 chars, >=3.5 bits/char)
> - `tests/test_reconcile.py:73` — credential-shaped literal (sk_ prefix)
## Purpose
The `tests/test_reconcile.py` module tests the `reconcile` functionality introduced in commit `ff902eb`, which enables "Proof-Carrying Prose" — a system where typed claims about code are verified against the actual implementation, producing tamper-evident certificates. The tests ensure that the reconciliation logic correctly identifies and reports violations between code findings, prose documentation, and claims, including cases where prose omits findings, contradicts them, or fails to address marks (e.g., entropy-based secrets).

## Architecture
The module consists of seven test functions, each targeting a specific reconciliation scenario:
1. `test_pure_reconcile_imports_constraint()` verifies that `reconcile.py` does not import certain modules (`pipeline`, `claims`, `verify`), enforcing a frozen boundary constraint.
2. `test_reconcile_prose_omits_finding()` checks that prose documentation correctly omits or includes file paths mentioned in findings.
3. `test_reconcile_prose_contradicts_finding_via_prose_denial()` tests for contradictions where prose explicitly denies a finding.
4. `test_reconcile_prose_contradicts_finding_via_positive_claim()` tests for contradictions where a positive claim in prose contradicts a finding.
5. `test_reconcile_mark_uncovered()` ensures that marks (e.g., entropy-based secrets) are properly covered by claims or prose.
6. `test_reconcile_ignores_resolved_findings()` confirms that resolved findings are ignored during reconciliation.

## Key entry points
The module has no external dependencies and is self-contained. The key entry points are the test functions, which are executed by the test runner. Each function calls `reconcile.reconcile()` with specific inputs (prose, findings, claims, marks) and asserts the expected violations.

## Dependencies
The module depends on:
- `isidore.reconcile` for the reconciliation logic.
- `isidore.pcp.Mark` for representing marks (e.g., entropy-based secrets).
- `pathlib.Path` for file operations.

## How to change safely
To modify this module:
1. **Add new test cases**: If introducing a new reconciliation scenario, add a new test function following the existing pattern. Ensure it covers a distinct violation type (e.g., a new kind of prose contradiction).
2. **Update existing tests**: If the reconciliation logic changes, update the test inputs and assertions to reflect the new behavior.
3. **Preserve the frozen boundary constraint**: Do not modify `test_pure_reconcile_imports_constraint()` or the imports in `reconcile.py` to maintain the frozen boundary constraint.
