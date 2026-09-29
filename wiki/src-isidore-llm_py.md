## Purpose
`src/isidore/llm.py` is a single-provider LLM client that speaks the OpenAI-compatible chat completions protocol. It is fail-closed by design: one model, temperature 0, one timeout, and deliberately NO model fallback — if the configured provider fails, the run fails, never silently escalating to a different (possibly paid) model. It can point at any OpenAI-compatible endpoint via `ISIDORE_BASE_URL` (a local server like llama.cpp, vLLM, Ollama, LM Studio, or a hosted API like OpenAI, OpenRouter, Together, Groq), or route through the local Claude Code CLI to keep source code inside the user's own subscription (`src/isidore/llm.py:1`).

## Architecture
The module has two generation paths, selected by `ISIDORE_PROVIDER`:

**OpenAI-compatible HTTP** (`generate`, `build_request`): Builds a JSON `POST` to `{base_url}/chat/completions` with the standard messages format, temperature 0, and no streaming. Uses only `urllib` — no third-party HTTP library. The `Authorization: Bearer` header is added only when an API key is provided.

**Claude Code CLI** (`generate_via_cli`): Spawns `claude -p --model <model>` as a subprocess with the prompt on STDIN (not argv, to avoid Windows's 32767-character command-line limit). Uses `shutil.which` to resolve the executable (Windows npm installs create `.CMD` shims that `subprocess` does not find without `PATHEXT` expansion). Detects expired OAuth sessions by probing STDOUT for auth-failure strings.

**`default_generator()`** reads the environment variables and returns a one-argument callable shaped like `generate(prompt) -> str`.

## Key entry points
- `default_generator()`: The primary entry point. Reads `ISIDORE_PROVIDER`, `ISIDORE_BASE_URL`, `ISIDORE_MODEL`, `ISIDORE_API_KEY`, and `ISIDORE_TIMEOUT_S` from the environment and returns a generator function. Raises `GenerationError` if `ISIDORE_MODEL` is unset (`src/isidore/llm.py:L112-L134`).
- `generate(prompt, *, base_url, model, api_key, timeout_s)`: Direct HTTP generation against an OpenAI-compatible endpoint (`src/isidore/llm.py:L49-L61`).
- `generate_via_cli(prompt, *, model, timeout_s)`: Generation through the Claude Code CLI in headless mode (`src/isidore/llm.py:L68-L109`).
- `GenerationError`: The single failure type. Raised on network errors, malformed responses, missing models, and expired CLI sessions (`src/isidore/llm.py:L30-L31`).

## Dependencies
The module depends only on Python's standard library (`json`, `os`, `urllib.request`, `urllib.error`, `shutil`, `subprocess`). It has no cross-module dependencies within isidore. It is used by:
- `src/isidore/cli.py` (for the `--execute` compile path)
- `src/isidore/handoff.py` (for `GenerationError` type)
- `src/isidore/knowledge.py` (for knowledge compilation)
- Tested by: `tests/test_handoff.py`, `tests/test_incremental.py`, `tests/test_pipeline.py`, `tests/test_source_disclosure_gate.py`, `tests/test_units.py`

## How to change safely
1. **No model fallback**: The fail-closed design is intentional. Adding a fallback model would silently escalate spend and potentially leak source code to an untrusted provider.
2. **STDIN, not argv**: `generate_via_cli` passes the prompt on STDIN. Changing to argv would work in tests but fail on real pages that exceed Windows's command-line limit.
3. **Auth-failure probing**: `generate_via_cli` checks STDOUT for expired-session strings (`src/isidore/llm.py:L105`). The CLI reports these with exit 0, so a healthy-looking run can carry an auth failure as its "answer".
4. **`shutil.which`**: Required for Windows `.CMD` shim resolution. Reverting to a bare command name breaks on Windows npm installs.
5. **Environment variables**: `ISIDORE_MODEL` is required for `--execute`. `ISIDORE_BASE_URL` defaults to `http://localhost:11434/v1` (the conventional local-server port, not an endorsement of any provider).
