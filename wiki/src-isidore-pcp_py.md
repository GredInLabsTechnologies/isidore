> [!WARNING]
> **SECURITY — deterministic detectors flagged this code (0 LLM). Verify; never document as an intended feature.**
>
> - `src/isidore/pcp.py:233` — high-entropy literal (>=24 chars, >=3.5 bits/char)
## Purpose
`src/isidore/pcp.py` is the frozen seam for Proof-Carrying Prose (PCP), a system that verifies typed claims about code. It defines the shared types, predicate grammar, and certificate structure that five lanes (A–E) import and extend. The module enforces invariants like fail-closed verification (never returning `TRUE` for an unregistered language) and monotonic escalation (marks are never removed by the model). It serves as the single point of coupling for ADR-0033, ensuring consistency across lanes.

## Architecture
The module consists of:
- `Predicate`: A frozen dataclass representing a decidable assertion with a `kind` and `args`.
- `Verdict`: A dataclass for the result of checking a predicate, with `value` (TRUE/FALSE/UNDECIDABLE), `oracle`, and `detail`.
- `VerifyContext`: A read-only dataclass providing verifiers with the repo path, graph data, and commit hash.
- `Verifier`: A protocol for deterministic, 0-LLM verifiers that return `UNDECIDABLE` for unsupported predicates.
- `VERIFIERS`: A registry of verifiers, filled by lanes A–D and used by lane A to verify claims.

## Key entry points
- `parse_predicate()`: Parses a predicate from model output, returning `None` for malformed or unsupported kinds.
- `parse_stored_predicate()`: Parses a predicate from a certificate, allowing kinds registered in `VERIFIERS`.
- `undecidable()`: Returns a `Verdict` with `UNDECIDABLE` and no oracle.

## Dependencies
The module has no cross-module dependencies but is imported by seven other modules (`contracts.py`, `detectors.py`, etc.).

## How to change safely
- **Adding a predicate kind**: Extend `PREDICATE_KINDS` and implement a verifier in the relevant lane.
- **Modifying the grammar**: Ensure backward compatibility with existing certificates by keeping `parse_stored_predicate()` permissive.
- **Adding a verifier**: Register it in `VERIFIERS` using the lane's reserved kind.
