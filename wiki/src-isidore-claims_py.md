## Purpose
`src/isidore/claims.py` implements the core staleness-detection mechanism for Isidore's wiki. Claims are atomic, evidence-anchored statements about the code that are extracted from generated pages. Each claim is tied to a specific line of code via a content hash, allowing for precise detection of staleness when the cited code changes. This design eliminates the need for LLM calls to verify claims, making the system efficient and reliable.

## Architecture
Claims are parsed from markdown pages using a fenced block syntax (````isidore-claims`). The module handles three key operations:
1. **Parsing**: Extracting claims from markdown blocks and splitting them into structured data.
2. **Validation**: Filtering out claims that assert existential absence (e.g., "there is no X") because they cannot be evidence-anchored.
3. **Hashing**: Generating content hashes for the cited lines to enable staleness detection.

The module also supports optional typed claims via Proof-Carrying Prose (PCP), where claims can include machine-checkable predicates that are verified against the code without additional LLM calls.

## Key entry points
- `parse_claims_block(markdown)`: Splits a markdown page into clean content and a list of claim rows.
- `is_negative_existential(statement)`: Checks if a claim asserts existential absence, which are dropped.
- `parse_predicate_field(raw)`: Parses the optional PCP predicate field in a claim.
- `_split_evidence(evidence)`: Splits evidence citations into path and line number.
- `_normalize(text)` and `_hash(text)`: Normalize text and generate content hashes for evidence.

## Dependencies
- `src/isidore/toon.py`: Used for encoding claims (imported as `encode`).
- `src/isidore/pcp.py`: Used for parsing PCP predicates (imported dynamically in `parse_predicate_field`).

## How to change safely
1. **Backward compatibility**: Ensure new claim formats remain backward-compatible with existing pages.
2. **Predicate correctness**: When adding new predicates, verify that the code matches the predicate's claims exactly.
3. **Hash stability**: Avoid changes to the hashing logic that would invalidate existing claims.
4. **Quarantine rules**: Maintain the conservative approach to quarantining claims with existential absence.
