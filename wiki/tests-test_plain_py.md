## Purpose
`tests/test_plain.py` is a test module for the plain-language gate, a component that enforces ISO 24495-1 compliance by rejecting jargon and enforcing structural rules. It verifies that the gate correctly identifies and explains violations of plain-language principles, ensuring documentation is usable by non-technical readers. The module focuses on named rules, one-sided verdicts, and the absence of readability scores, as documented in the module's docstring (`tests/test_plain.py:L1`).

## Architecture
The module imports `RULES`, `check`, `explain`, and `is_plain` from `isidore.plain` (`tests/test_plain.py:L4`). It defines six test functions, each targeting a specific aspect of the plain-language gate:
1. `test_a_sentence_written_for_a_person_passes` — Validates that plain-language sentences pass the gate.
2. `test_each_rule_names_the_reason_it_fired` — Ensures each rule violation is named and reported.
3. `test_a_rejection_can_be_explained_to_whoever_wrote_it` — Confirms explanations include the rule name and audience.
4. `test_case_insensitivity_is_scoped_to_the_vocabulary_rule` — Tests that case insensitivity is limited to vocabulary rules.
5. `test_the_gate_is_one_sided_and_carries_no_readability_score` — Verifies the gate's one-sided verdict and lack of readability scoring.
6. `test_ordinary_proper_nouns_are_not_mistaken_for_identifiers` — Confirms the gate distinguishes between ordinary proper nouns and code identifiers.

## Key entry points
The module's entry points are the test functions, which collectively validate the plain-language gate's behavior. Each test function exercises a specific rule or edge case, ensuring the gate adheres to its design principles.

## Dependencies
The module depends on `isidore.plain`, which provides the `RULES`, `check`, `explain`, and `is_plain` symbols (`tests/test_plain.py:L4`). These symbols are used to test the plain-language gate's functionality.

## How to change safely
To modify `tests/test_plain.py`, ensure that changes:
1. Preserve the module's docstring and test structure.
2. Maintain the one-sided verdict and lack of readability scoring.
3. Do not introduce new dependencies or alter the existing ones.
4. Add new test functions for any new rules or edge cases introduced in the plain-language gate.
