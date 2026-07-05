"""Single-provider LLM client (OpenAI-compatible), fail-closed by design.

One model, temperature 0, one timeout. There is deliberately NO model fallback: if the
configured provider fails, the run fails — it never silently escalates to a different
(possibly paid) model. Point it at any OpenAI-compatible endpoint: a local/cloud Ollama
(default), OpenRouter, vLLM, llama.cpp server, or a commercial API.

Environment:
  ISIDORE_BASE_URL  default http://localhost:11434/v1  (Ollama)
  ISIDORE_MODEL     required for --execute (e.g. gpt-oss:120b-cloud, z-ai/glm-5.2)
  ISIDORE_API_KEY   optional (Bearer token)
  ISIDORE_TIMEOUT_S optional, default 300
"""
from __future__ import annotations

import json
import os
import urllib.error
import urllib.request

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
    headers = {"Content-Type": "application/json"}
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


def default_generator():
    """Build the env-configured generator. Fails closed if no model is set."""
    base_url = os.environ.get("ISIDORE_BASE_URL", DEFAULT_BASE_URL)
    model = os.environ.get("ISIDORE_MODEL", "")
    if not model:
        raise GenerationError(
            "ISIDORE_MODEL is not set (e.g. gpt-oss:120b-cloud for Ollama, z-ai/glm-5.2 for OpenRouter)")
    api_key = os.environ.get("ISIDORE_API_KEY") or None
    timeout_s = int(os.environ.get("ISIDORE_TIMEOUT_S", str(DEFAULT_TIMEOUT_S)))

    def _generate(prompt: str) -> str:
        return generate(prompt, base_url=base_url, model=model, api_key=api_key,
                        timeout_s=timeout_s)

    return _generate
