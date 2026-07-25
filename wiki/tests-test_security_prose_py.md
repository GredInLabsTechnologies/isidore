> [!WARNING]
> **SECURITY — deterministic detectors flagged this code (0 LLM). Verify; never document as an intended feature.**
>
> - `tests/test_security_prose.py:29` — eval()
> - `tests/test_security_prose.py:51` — eval()
> - `tests/test_security_prose.py:85` — credential-shaped literal (sk_ prefix)
## Purpose
The `tests/test_security_prose.py` module tests the security escalation system that forces a loud, deterministic prose banner when a security suspect is detected. This system was introduced to address a live adversarial test where a camouflaged authentication backdoor was caught in findings as a bug but the prose recommended keeping it. The banner is mechanical and ensures that security suspects are no longer softened into features.

## Architecture
The module tests the `is_security_finding` function, which checks if a finding is a security suspect. It also tests the `security_banner` function, which generates a loud, deterministic prose banner when security suspects are detected. The tests cover various scenarios, including detecting common security vocabulary, ignoring non-security findings, and ensuring that safety-affirming notes do not escalate the banner.

## Key entry points
- `test_detects_the_camouflaged_backdoor`: Tests that a camouflaged backdoor is detected as a security suspect.
- `test_detects_common_security_vocabulary`: Tests that common security vocabulary is detected as a security suspect.
- `test_ignores_non_security_and_wrong_kinds`: Tests that non-security findings and wrong kinds are ignored.
- `test_negation_guard_does_not_escalate_safety_affirming_notes`: Tests that safety-affirming notes do not escalate the banner.
- `test_hardcoded_with_intervening_word_is_caught`: Tests that hardcoded tokens with intervening words are caught as security suspects.
- `test_banner_is_loud_and_lists_evidence`: Tests that the banner is loud and lists evidence.
- `test_no_banner_without_security_suspects`: Tests that no banner is generated without security suspects.
- `test_banner_goes_under_the_h1`: Tests that the banner is placed under the H1 heading.

## Dependencies
The module depends on the `isidore.findings` module, which provides the `insert_security_banner`, `is_security_finding`, `render_findings`, `security_banner`, and `security_suspects` functions.

## How to change safely
When modifying this module, ensure that:
1. The security escalation system continues to force a loud, deterministic prose banner when security suspects are detected.
2. Common security vocabulary is still detected as a security suspect.
3. Non-security findings and wrong kinds are still ignored.
4. Safety-affirming notes do not escalate the banner.
5. Hardcoded tokens with intervening words are still caught as security suspects.
6. The banner is still loud and lists evidence.
7. No banner is generated without security suspects.
8. The banner is still placed under the H1 heading.
