> [!WARNING]
> **SECURITY — deterministic detectors flagged this code (0 LLM). Verify; never document as an intended feature.**
>
> - `tests/test_source_disclosure_gate.py:114` — high-entropy literal (>=24 chars, >=3.5 bits/char)
## Purpose
`tests/test_source_disclosure_gate.py` tests the source disclosure gate — the compiler's refusal to send a repository's source to an undeclared host. The gate exists because `pipeline.py` historically asked only whether a provider was *configured*, never where it was: measured 2026-07-26, a key pointing at a free tier whose training toggle is on by default exfiltrated 87 prompts (~26,000 lines) of private source before anyone read the setting (`tests/test_source_disclosure_gate.py:1-L6`). The gate must be strict enough to have stopped that, and loose enough never to block the two modes that send nothing at all — a model on this machine, and the handoff (`tests/test_source_disclosure_gate.py:8-L9`).

## Architecture
The module uses a synthetic repo created by `_make_repo()` (`tests/test_source_disclosure_gate.py:34-L46`) and a `clean_env` fixture (`tests/test_source_disclosure_gate.py:50-L53`) that strips all Isidore provider env vars (`ISIDORE_PROVIDER`, `ISIDORE_BASE_URL`, `ISIDORE_MODEL`, `TRUST_ENV`) so each test starts from a known-empty configuration. Tests classify the destination via `source_destination()` and assert against the five destination constants: `DEST_LOCAL`, `DEST_CLI`, `DEST_TRUSTED`, `DEST_DECLARED`, `DEST_UNDECLARED`.

## Key entry points
- `_make_repo()`: Creates a synthetic repository with 12 Python files and a `graph.json` (`tests/test_source_disclosure_gate.py:34-L46`).
- `clean_env()`: Pytest fixture that clears all provider env vars via `monkeypatch` (`tests/test_source_disclosure_gate.py:50-L53`).
- `_gp()`: Returns the path to `graph.json` (`tests/test_source_disclosure_gate.py:56-L57`).
- `test_the_default_destination_is_this_machine`: Unconfigured means `DEST_LOCAL` — the out-of-the-box posture sends nothing anywhere (`tests/test_source_disclosure_gate.py:62-L65`).
- `test_a_model_on_this_machine_is_local_however_it_is_addressed`: Parametrized over localhost/127.0.0.1/::1/0.0.0.0 — all resolve to `DEST_LOCAL` (`tests/test_source_disclosure_gate.py:70-L72`).
- `test_the_operators_own_claude_session_is_not_a_third_party`: `ISIDORE_PROVIDER=claude-cli` resolves to `DEST_CLI` regardless of `ISIDORE_BASE_URL` (`tests/test_source_disclosure_gate.py:75-L78`).
- `test_an_endpoint_under_an_agreement_is_trusted`: `api.anthropic.com` resolves to `DEST_TRUSTED` (`tests/test_source_disclosure_gate.py:81-L83`).
- `test_anything_else_is_undeclared_until_someone_says_otherwise`: A free-tier host is `DEST_UNDECLARED`; setting `TRUST_ENV=yes` upgrades it to `DEST_DECLARED` (`tests/test_source_disclosure_gate.py:86-L91`).
- `test_a_truthy_looking_value_is_not_a_decision`: Parametrized over truthy-looking strings (`"true"`, `"1"`, `"YES please"`, `"y"`, `" si "`, `""`) — these do NOT satisfy the trust gate (`tests/test_source_disclosure_gate.py:94-L95`).

## Dependencies
The module depends on four cross-module imports:
- `src/isidore/llm.py` (1 link) — for `GenerationError` (`tests/test_source_disclosure_gate.py:18`).
- `src/isidore/pipeline.py` (1 link) — for `DEST_CLI`, `DEST_DECLARED`, `DEST_LOCAL`, `DEST_TRUSTED`, `DEST_UNDECLARED`, `TRUST_ENV`, `assert_may_send_source`, `compile_wiki`, `source_destination` (`tests/test_source_disclosure_gate.py:19-L28`).
- `src/isidore/handoff.py` (1 link) — imported by the test module.
- `src/isidore/whatsnew.py` (1 link) — imported by the test module.

## How to change safely
1. The `clean_env` fixture must strip all four env vars — adding a new trust signal means adding it there too.
2. When adding a new destination kind, add a test that classifies a representative URL and update the parametrized lists.
3. The gate's decision logic lives in `pipeline.source_destination()`; tests here are the *contract* — change the logic there, verify the contract here.
