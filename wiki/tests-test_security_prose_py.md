> [!WARNING]
> **SECURITY — unverified suspect(s) flagged automatically while compiling this page.**
> Detected from the evidence, not from a security scan. Treat as review items to VERIFY, never as intended features to preserve:
>
> - `tests/test_security_prose.py:17` — security risk: hardcoded service token in BACKDOOR constant

## Purpose
`tests/test_security_prose.py` tests the security escalation logic in the `isidore.findings` module. It verifies that security-related findings are correctly identified and that the system raises a loud, deterministic banner when such findings are detected. The module is motivated by a real-world case where a camouflaged authentication backdoor was caught in findings but the prose recommended keeping it. The tests ensure the banner is mechanical and cannot be softened into a feature.

## Architecture
The module defines a set of test functions that exercise the `is_security_finding` and `security_banner` functions from `isidore.findings`. The tests cover:
- Detection of security-related vocabulary in findings
- Ignoring non-security findings and wrong kinds
- False-positive regression tests for notes that affirm safety
- False-negative regression tests for hardcoded secrets with intervening words
- Banner formatting and placement

## Key entry points
- `test_detects_the_camouflaged_backdoor()`: Verifies detection of a hardcoded service token
- `test_detects_common_security_vocabulary()`: Tests detection of security-related terms
- `test_ignores_non_security_and_wrong_kinds()`: Ensures non-security findings are ignored
- `test_negation_guard_does_not_escalate_safety_affirming_notes()`: Confirms safety-affirming notes do not trigger the banner
- `test_hardcoded_with_intervening_word_is_caught()`: Tests detection of hardcoded secrets with words between "hardcoded" and "token"
- `test_banner_is_loud_and_lists_evidence()`: Verifies the banner's formatting and content
- `test_no_banner_without_security_suspects()`: Ensures no banner is shown for non-security findings
- `test_banner_goes_under_the_h1()`: Confirms the banner is placed correctly in markdown

## Dependencies
The module depends on the `isidore.findings` module, which provides:
- `insert_security_banner`: Inserts a security banner into markdown
- `is_security_finding`: Determines if a finding is security-related
- `render_findings`: Renders findings
- `security_banner`: Generates a security banner
- `security_suspects`: Defines security-related vocabulary

## How to change safely
When modifying this module:
1. Ensure all test cases remain valid by updating them alongside the implementation
2. Maintain the deterministic nature of the banner and its placement
3. Preserve the negation guard that prevents safety-affirming notes from triggering the banner
4. Keep the test coverage comprehensive for all security-related vocabulary and edge cases
