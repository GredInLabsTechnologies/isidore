## Purpose
The `recertify.py` module addresses a gap in the documentation verification pipeline: when a page's recorded verdicts no longer match the current code graph, but the certificate itself is not marked as drifted. This creates a discrepancy between `isidore verify` and `isidore compile`, where the latter computes dirtiness based on context changes, stale claims, or missing pages, while the former fails verification for drifted certificates. The module re-runs the claim oracles over unchanged prose to rewrite the certificate, ensuring consistency without modifying the prose itself. It specifically handles cases where a claim recorded as `FALSE` now verifies as `TRUE` due to improved oracles, but refuses to rewrite certificates for claims that have transitioned from `TRUE` to `FALSE` (as this would hide incorrect prose).

## Architecture
The module defines a structured workflow for recertifying pages:
1. **PageRecert**: A dataclass tracking the action taken for a page (`ok`, `recertify`, `refuted`, `tampered`, or `no-cert`), along with drift details and moved children.
2. **RecertifyResult**: Aggregates results across pages, including written certificates and warnings.
3. **Helper functions**:
   - `_level`: Determines the pyramid level of a page to ensure children are recertified before parents.
   - `_child_digest`: Computes the SHA-256 hash of a child page's certificate for dependency tracking.
   - `rebuild_certificate`: Recomputes the certificate for a page by re-running verifiable claims while preserving non-verifiable claims, marks, and violations.

## Key entry points
- `rebuild_certificate`: The primary function that recomputes a certificate for a page, re-running verifiable claims while preserving the original prose hash and marks.

## Dependencies
- `src/isidore/pcp.py`: Provides certificate-related utilities like `parse_stored_predicate`, `parse_wiki_uri`, and `write_certificate`.
- `src/isidore/verify.py`: Imports certificate status constants and verification utilities like `verify_predicate_ctx`.

## How to change safely
1. **Preserve behavior**: When modifying `rebuild_certificate`, ensure that non-verifiable claims, marks, and violations are carried over unchanged. The prose hash should only be updated if the caller has already verified it.
2. **Dependency order**: Maintain the dependency order enforced by `_level` to ensure children are recertified before parents.
3. **Certificate integrity**: Avoid modifying the certificate structure or fields that are not explicitly handled by the module (e.g., marks and violations).
