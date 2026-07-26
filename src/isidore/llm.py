"""Single-provider LLM client (OpenAI-compatible), fail-closed by design.

One model, temperature 0, one timeout. There is deliberately NO model fallback: if the
configured provider fails, the run fails — it never silently escalates to a different
(possibly paid) model. Point it at ANY OpenAI-compatible endpoint via ISIDORE_BASE_URL:
a local server (llama.cpp, vLLM, Ollama, LM Studio) or a hosted API (OpenAI, OpenRouter,
Together, Groq, ...). Isidore has no preferred provider — the default is only the
conventional local-server address for convenience, not an endorsement.

Environment:
  ISIDORE_BASE_URL  OpenAI-compatible base URL; default {DEFAULT_BASE_URL}
                    (the common local-server port — override for any hosted API)
  ISIDORE_MODEL     required for --execute; the model id as your endpoint names it
  ISIDORE_API_KEY   optional (Bearer token), needed by most hosted APIs
  ISIDORE_TIMEOUT_S optional, default 300
"""
from __future__ import annotations

import json
import os
import urllib.error
import urllib.request

# The de-facto local OpenAI-compatible server port. Not provider-specific: several local
# runtimes bind it. Override ISIDORE_BASE_URL for any hosted API.
DEFAULT_BASE_URL = "http://localhost:11434/v1"
DEFAULT_TIMEOUT_S = 300


class GenerationError(RuntimeError):
    """The provider failed. No retry with a different model — fail closed."""


def build_request(base_url: str, model: str, prompt: str,
                  api_key: str | None) -> urllib.request.Request:
    body = json.dumps({
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0,
        "stream": False,
    }).encode("utf-8")
    headers = {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0 (isidore-wiki)"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    return urllib.request.Request(
        base_url.rstrip("/") + "/chat/completions", data=body, headers=headers, method="POST")


def generate(prompt: str, *, base_url: str, model: str, api_key: str | None = None,
             timeout_s: int = DEFAULT_TIMEOUT_S) -> str:
    request = build_request(base_url, model, prompt, api_key)
    try:
        with urllib.request.urlopen(request, timeout=timeout_s) as resp:  # noqa: S310
            payload = json.loads(resp.read().decode("utf-8"))
    except urllib.error.URLError as exc:
        raise GenerationError(f"provider unreachable ({base_url}): {exc}") from exc
    try:
        return payload["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError) as exc:
        raise GenerationError(
            f"response missing choices[0].message.content: {str(payload)[:300]}") from exc


CLI_PROVIDER = "claude-cli"
CLI_COMMAND = "claude"


def generate_via_cli(prompt: str, *, model: str, timeout_s: int = DEFAULT_TIMEOUT_S) -> str:
    """Generate through the local Claude Code CLI in headless mode, over the user's own session.

    Why this exists: a hosted endpoint means handing your source code to whoever runs it, and a FREE
    endpoint usually means handing it to a training set — measured on 2026-07-26, when a free tier
    that trains by default received 87 prompts of private source before anyone checked the setting.
    Routing through the CLI keeps the compile inside a subscription the user already has and already
    trusts, at the cost of the weekly cap rather than the cost of confidentiality.

    The prompt goes on STDIN, never in argv: a page prompt runs to tens of thousands of characters
    and Windows caps a command line at 32767, so passing it as an argument works in testing and then
    truncates or fails on a real page.
    """
    import shutil
    import subprocess

    # `shutil.which`, not the bare name: on Windows the npm install is a `claude.CMD` shim, and
    # CreateProcess does not apply PATHEXT the way a shell does — so `subprocess([...])` reports "not
    # on PATH" for a command the shell finds instantly. Same trap that broke the Codex adapter once.
    exe = shutil.which(CLI_COMMAND)
    if exe is None:
        raise GenerationError(
            f"{CLI_COMMAND!r} is not on PATH. Install Claude Code, or unset "
            f"ISIDORE_PROVIDER={CLI_PROVIDER} to use an OpenAI-compatible endpoint.")
    try:
        proc = subprocess.run(
            [exe, "-p", "--model", model], input=prompt, capture_output=True, text=True,
            encoding="utf-8", errors="replace", timeout=timeout_s, shell=False)
    except subprocess.TimeoutExpired as exc:
        raise GenerationError(f"{CLI_COMMAND} timed out after {timeout_s}s") from exc

    text = (proc.stdout or "").strip()
    if proc.returncode != 0 or not text:
        detail = (proc.stderr or "").strip() or text or f"exit {proc.returncode}"
        raise GenerationError(f"{CLI_COMMAND} failed: {detail[:300]}")
    # The CLI reports an expired session on STDOUT with exit 0, so a healthy-looking run can carry an
    # auth failure as its "answer". Caught by probing it: the page would have been written from it.
    if "Failed to authenticate" in text or "OAuth access token has expired" in text:
        raise GenerationError(
            f"{CLI_COMMAND} is not authenticated (its OAuth token has expired). Run `claude login` "
            f"and retry — nothing was generated.")
    return text


def default_generator():
    """Build the env-configured generator. Fails closed if no model is set."""
    model = os.environ.get("ISIDORE_MODEL", "")
    if os.environ.get("ISIDORE_PROVIDER", "").strip().lower() == CLI_PROVIDER:
        if not model:
            raise GenerationError(
                f"ISIDORE_PROVIDER={CLI_PROVIDER} needs ISIDORE_MODEL (e.g. 'sonnet' or 'haiku').")
        timeout_s = int(os.environ.get("ISIDORE_TIMEOUT_S", str(DEFAULT_TIMEOUT_S)))
        return lambda prompt: generate_via_cli(prompt, model=model, timeout_s=timeout_s)

    base_url = os.environ.get("ISIDORE_BASE_URL", DEFAULT_BASE_URL)
    if not model:
        raise GenerationError(
            "ISIDORE_MODEL is not set. Set it to the model id your endpoint exposes, and "
            "ISIDORE_BASE_URL to any OpenAI-compatible endpoint (local server or hosted API).")
    api_key = os.environ.get("ISIDORE_API_KEY") or None
    timeout_s = int(os.environ.get("ISIDORE_TIMEOUT_S", str(DEFAULT_TIMEOUT_S)))

    def _generate(prompt: str) -> str:
        return generate(prompt, base_url=base_url, model=model, api_key=api_key,
                        timeout_s=timeout_s)

    return _generate
