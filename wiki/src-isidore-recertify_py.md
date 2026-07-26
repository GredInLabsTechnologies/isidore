## Purpose
The `recertify.py` module addresses a gap in the documentation verification pipeline: it re-runs claim oracles over unchanged prose to update certificates without modifying the prose itself. This resolves a discrepancy where `isidore verify` would fail a page whose recorded verdicts no longer matched the current graph, while `isidore compile` would only recompute dirtiness based on context changes, claim staleness, or missing pages. The module specifically targets certificates that have drifted (e.g., a module-level constant that was previously unproven is now verified TRUE) without touching prose that might now contradict the code (`TRUE -> FALSE` claims). This avoids the need for manual deletion of pages to force regeneration, which would incur an LLM call per page.

## Architecture
The module defines a structured workflow to recertify pages:
1. **PageRecert**: A dataclass tracking the action taken for a page (`ok`, `recertify`, `refuted`, `tampered`, or `no-cert`), along with drift details and moved children.
2. **RecertifyResult**: Aggregates results across pages, including written certificates and warnings.
3. **Helper functions**:
   - `_level()`: Determines the pyramid level of a page to ensure children are recertified before parents.
   - `_child_digest()`: Computes the SHA-256 hash of a child page's certificate for dependency tracking.
   - `rebuild_certificate()`: Recomputes verdicts for a certificate while preserving non-model-derived fields like `prose_sha256`, marks, and violations.

## Key entry points
- `rebuild_certificate()`: The primary function that recomputes verdicts for a certificate while preserving non-model-derived fields. It parses the claims block, re-runs verifiable predicates, and updates child certificate hashes for `wikichain` claims.

## Dependencies
The module depends on:
- `src/isidore/pcp.py`: For certificate handling (`Certificate`, `parse_stored_predicate`, `parse_wiki_uri`, `write_certificate`).
- `src/isidore/verify.py`: For certificate status checks (`CertStatus`, `verify_predicate_ctx`).

## How to change safely
To modify `recertify.py` safely:
1. **Preserve behavior**: Ensure that `rebuild_certificate()` continues to recompute verdicts without altering prose or non-model-derived fields.
2. **Maintain pyramid levels**: Verify that `_level()` correctly assigns levels to ensure children are recertified before parents.
3. **Child digest integrity**: Confirm that `_child_digest()` accurately computes and returns the SHA-256 hash of child certificates.
4. **Action consistency**: Ensure that `PageRecert` actions (`ok`, `recertify`, etc.) are consistently applied and documented.
