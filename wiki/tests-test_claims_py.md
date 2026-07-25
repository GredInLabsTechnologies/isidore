## Purpose
The `tests/test_claims.py` module tests the claims parsing, anchoring, and evidence-hashing functionality of the Isidore system. It verifies that claims are correctly extracted from Markdown blocks, that evidence citations are resolved to their content, and that the system detects staleness when cited code changes. The tests ensure the "zero-LLM staleness" property, where claims are only considered stale if their cited evidence changes, not if the codebase evolves elsewhere.

## Architecture
The module consists of:
1. A test for `is_negative_existential()`, which distinguishes between existential claims (e.g., "no retry logic here") and behavioral claims (e.g., "the lock is not released on the error path").
2. Helper functions `_make_repo()` and `_gp()` to create a test repository and locate its graph file.
3. Tests for `parse_claims_block()`, which extracts claims from Markdown blocks and strips them for further processing.
4. Tests for `evidence_hash()`, which verifies that the hash of a cited line matches its content and changes when the line is modified.
5. Tests for `evidence_state()`, which ensures that staleness is only triggered by changes to the cited line, not neighboring lines.

## Key entry points
- `test_is_negative_existential_flags_absence_not_behavior()`: Tests the classification of existential vs. behavioral claims.
- `test_parse_claims_block_extracts_and_strips()`: Verifies that claims are extracted from Markdown blocks and the block is stripped of claims.
- `test_evidence_hash_is_the_cited_line_content()`: Ensures that the hash of a cited line matches its content and changes when the line is modified.
- `test_evidence_state_ignores_neighbors_whitespace_and_line_shifts()`: Confirms that staleness is only triggered by changes to the cited line.

## Dependencies
The module depends on:
- `isidore.claims`: For the `anchor_claims`, `check_claims`, `claim_id`, `evidence_hash`, `evidence_state`, `is_negative_existential`, `parse_claims_block`, `render_claims`, and `stale_pages` functions.
- `isidore.pipeline`: For the `compile_wiki` function.

## How to change safely
When modifying `tests/test_claims.py`, ensure that:
1. All tests pass after changes to ensure the claims system remains correct.
2. New tests are added for any new functionality in the claims system.
3. The test repository structure and content in `_make_repo()` are updated to match the actual repository structure and content.
