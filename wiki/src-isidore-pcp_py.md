> [!WARNING]
> **SECURITY — deterministic detectors flagged this code (0 LLM). Verify; never document as an intended feature.**
>
> - `src/isidore/pcp.py:207` — high-entropy literal (>=24 chars, >=3.5 bits/char)
## Purpose
`src/isidore/pcp.py` is the frozen seam for Proof-Carrying Prose (PCP), a system where claims about code are verified against the code itself. It defines the shared types, predicate grammar, and verifier registry that all PCP lanes (A–E) import. The module ensures consistency across lanes by enforcing a strict contract (ADR-0033) and providing a fail-closed design where undecidable predicates default to `UNDECIDABLE`.

## Architecture
The module consists of:
- A `Predicate` class for parsing and serializing decidable assertions (e.g., `calls`, `defines`, `imports`).
- A `Verdict` class to record the result of checking a predicate against an oracle.
- A `VerifyContext` dataclass providing read-only access to the repository state, graph data, and commit hash.
- A `Verifier` protocol for implementing deterministic, LLM-free predicate checkers.
- A global `VERIFIERS` registry to map predicate kinds to their verifiers.

## Key entry points
- `parse_predicate()`: Parses a string into a `Predicate` or returns `None` for malformed/unknown kinds.
- `undecidable()`: Returns a `Verdict` with `UNDECIDABLE` as the safe default.
- `register_verifier()`: Adds a verifier to the registry for a given predicate kind.
- `get_verifier()`: Retrieves a verifier by kind (returns `None` if unregistered).

## Dependencies
The module has no cross-module dependencies but is imported by all PCP lanes (A–E) to share the frozen types and registry.

## How to change safely
- **Adding a new predicate kind**: Register a verifier for it in the `VERIFIERS` dict. Ensure the verifier is deterministic and LLM-free.
- **Modifying the predicate grammar**: Avoid changes that break existing serialized predicates. New kinds should be added, not removed.
- **Updating the `VerifyContext`**: Add new fields only if all lanes can safely ignore them (backward compatibility is critical).
