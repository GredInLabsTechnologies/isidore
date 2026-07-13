## Purpose
`tests/test_claims.py` tests the claims parsing, anchoring, and staleness detection logic in the Isidore system. It verifies that claims are correctly extracted from Markdown blocks, that evidence citations are hashed deterministically, and that the system can detect when cited code lines have changed (staleness). The module ensures the "zero-LLM staleness" property (ADR-0030) by validating that claims remain anchored to their original evidence.

## Architecture
The module imports functions from `isidore.claims` and `isidore.pipeline` to test their behavior. It uses a synthetic repository (`_make_repo`) to simulate a codebase with claims and evidence. Key components include:
- `parse_claims_block`: Extracts claims from Markdown and strips the block for further processing.
- `evidence_hash`: Computes a hash of the cited line's content to detect changes.
- `is_negative_existential`: Classifies claims about absence (e.g., "no retry logic") vs. behavioral claims.

## Key entry points
- `test_is_negative_existential_flags_absence_not_behavior`: Validates the classification of existential vs. behavioral claims.
- `test_parse_claims_block_extracts_and_strips`: Ensures claims are parsed correctly and evidence citations are preserved.
- `test_evidence_hash_is_the_cited_line_content`: Verifies that the hash changes when the cited line is modified.

## Dependencies
The module depends on:
- `isidore.claims`: For claim parsing, anchoring, and staleness detection.
- `isidore.pipeline`: For compiling the wiki (though only `compile_wiki` is imported, it is unused in the tests).

## How to change safely
To modify this module:
1. **Add new tests**: Follow the pattern of existing tests, using `_make_repo` to create a synthetic repository for isolated testing.
2. **Update evidence handling**: Changes to `evidence_hash` or `evidence_state` must preserve the deterministic property (tests verify this).
3. **Refactor claims parsing**: Ensure `parse_claims_block` still strips the block and preserves evidence citations.
