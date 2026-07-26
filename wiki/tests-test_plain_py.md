## Purpose
`tests/test_plain.py` tests the plain-language gate, a module that enforces ISO 24495-1 compliance by rejecting jargon and enforcing structural rules. The tests verify that the gate correctly identifies and explains violations, ensuring documents are usable by non-technical readers. The module's one-sided verdicts (pass/fail) and named rules (e.g., `jargon-term`, `camel-case`) are central to its purpose, as evidenced by the test cases that assert specific rule names and rejection reasons (`tests/test_plain.py:L15-L20`).

## Architecture
The module is tested through four key test functions:
1. `test_a_sentence_written_for_a_person_passes()` — Validates that plain-language sentences pass the gate (`tests/test_plain.py:L7-L11`).
2. `test_each_rule_names_the_reason_it_fired()` — Ensures each rule violation is named and reported (`tests/test_plain.py:L14-L20`).
3. `test_a_rejection_can_be_explained_to_whoever_wrote_it()` — Confirms that rejections include actionable explanations (`tests/test_plain.py:L23-L26`).
4. `test_the_gate_is_one_sided_and_carries_no_readability_score()` — Demonstrates the gate's binary outcome and rejection of short jargon sentences (`tests/test_plain.py:L36-L43`).

The tests also address edge cases, such as case insensitivity (`tests/test_plain.py:L29-L33`) and proper noun handling (`tests/test_plain.py:L46-L52`), ensuring the gate's rules are precise and balanced.

## Key entry points
The module's behavior is exposed through three functions imported from `isidore.plain`:
- `is_plain()` — Determines if a sentence is plain language (`tests/test_plain.py:L8`).
- `check()` — Returns a list of rule violations (`tests/test_plain.py:L15`).
- `explain()` — Provides human-readable explanations for violations (`tests/test_plain.py:L24`).

These functions are the primary interfaces for testing the gate's correctness and usability.

## Dependencies
The module depends on `isidore.plain`, which defines the `RULES` set and the core logic for checking and explaining plain-language compliance (`tests/test_plain.py:L4`). The tests do not depend on any other modules, as evidenced by the absence of cross-module links in the structure graph.

## How to change safely
To modify `tests/test_plain.py`, follow these guidelines:
1. **Preserve the gate's one-sided nature** — Ensure the gate remains binary (pass/fail) and does not introduce readability scores (`tests/test_plain.py:L37-L38`).
2. **Maintain named rules** — Each violation must be explicitly named and explained (`tests/test_plain.py:L15-L20`).
3. **Test edge cases** — Add tests for new rules or edge cases, such as proper nouns or case insensitivity (`tests/test_plain.py:L29-L33`, `tests/test_plain.py:L46-L52`).
4. **Avoid global case insensitivity** — Ensure `(?i)` is scoped to vocabulary rules to prevent false positives (`tests/test_plain.py:L30-L31`).
