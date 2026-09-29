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
- `test_detects_the_camouflaged_backdoor`: Asserts the BACKDOOR fixture (hardcoded service token `sk_live_ops_2f9d1a7c`) is a security suspect (`tests/test_security_prose.py:21-L22`).
- `test_detects_common_security_vocabulary`: Parametrized over 7 notes (auth bypass, SQL injection, eval, os.system, TLS disabled, credential leak, hardcoded password) — all flagged (`tests/test_security_prose.py:25-L35`).
- `test_ignores_non_security_and_wrong_kinds`: Asserts non-security bugs, drift findings, and question/term kinds are not suspects (`tests/test_security_prose.py:38-L42`).
- `test_negation_guard_does_not_escalate_safety_affirming_notes`: Parametrized over 6 notes that CLEAR the code (NOT a secret, not hardcoded, fake mock, safe eval, NOT disabled, example only) — none escalate (`tests/test_security_prose.py:45-L55`).
- `test_hardcoded_with_intervening_word_is_caught`: Asserts "hardcoded service token" and "hard-coded internal api key" are caught despite intervening words (`tests/test_security_prose.py:58-L63`).
- `test_banner_is_loud_and_lists_evidence`: Asserts banner contains `[!WARNING]`, `SECURITY`, and the file location (`tests/test_security_prose.py:66-L72`).
- `test_no_banner_without_security_suspects`: Asserts an empty banner for non-security findings (`tests/test_security_prose.py:75-L76`).
- `test_banner_goes_under_the_h1`: Asserts the H1 title stays first after banner insertion (`tests/test_security_prose.py:79-L83`).

## Dependencies
The module depends on one cross-module import:
- `src/isidore/findings.py` (1 link) — for `insert_security_banner`, `is_security_finding`, `render_findings`, `security_banner`, `security_suspects` (`tests/test_security_prose.py:9-L15`).

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
