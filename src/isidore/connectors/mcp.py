"""Minimal read-only MCP connector (ADR-0032 F3).

The implementation deliberately speaks JSON-RPC 2.0 directly.  Configuration is per instance;
only explicitly allowlisted ``tools/<name>`` and ``resources/<uri>`` operations are attempted.
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import urllib.error
import urllib.request
from typing import Any

from ..home import config_path
from .base import IngestOptions, IngestResult, register
from .store import (
    create_run_id,
    iso_now,
    read_state,
    record_run,
    safe_item_id,
    update_cursor,
    write_items,
    write_state,
)


MCP_PROTOCOL_VERSION = "2025-06-18"


def _allowed(config: dict) -> list[dict]:
    """Normalise the allowlist into `{entry, arguments}` records, sorted for determinism.

    An entry may be the plain string `tools/<name>` / `resources/<uri>`, or an object carrying the
    ARGUMENTS to call it with. The string form calls with no arguments, which was the only form there
    was — and it is why F5's real sources could not be expressed: `search_threads` without a query and
    `conversations_history` without a channel return nothing useful, so the whole MCP path was limited
    to servers whose tools happen to take no parameters. The caps for these sources live in those
    arguments (a Gmail query with `newer_than:`, a Slack `limit`), declared per entry in config because
    every server names them differently — guessing a mapping would be a cap that silently does nothing.
    """
    out: dict[str, dict] = {}
    for raw in config.get("allowed", []):
        if isinstance(raw, dict):
            entry = str(raw.get("entry") or raw.get("tool") or raw.get("resource") or "").strip()
            if entry and "/" not in entry:
                entry = f"tools/{entry}" if raw.get("tool") else f"resources/{entry}"
            args = raw.get("arguments") if isinstance(raw.get("arguments"), dict) else {}
        else:
            entry, args = str(raw).strip(), {}
        if entry:
            out[entry] = {"entry": entry, "arguments": args}
    return [out[k] for k in sorted(out)]


# The AUTHORITATIVE read-only barrier is the MCP protocol's own tool annotation `readOnlyHint`
# (rev. 2025-03-26): a tool declaring `readOnlyHint: true` promises not to mutate its environment;
# `readOnlyHint: false` or `destructiveHint: true` marks it write-capable. We consult tools/list and
# reject anything not affirmatively read-only. The name heuristic below is ONLY a fallback for
# servers that don't annotate — it is deliberately NON-EXHAUSTIVE and must never be trusted alone
# (an earlier version relied on 9 words and let execute_sql/add_user/drop_table/transfer_funds pass).
_MUTATING_VERBS = (
    "write", "create", "update", "delete", "remove", "send", "post", "put", "patch",
    "execute", "exec", "run", "set", "add", "insert", "drop", "modify", "edit", "append",
    "move", "rename", "copy", "upload", "publish", "revoke", "grant", "merge", "push", "commit",
    "destroy", "truncate", "reset", "apply", "install", "deploy", "provision", "terminate",
    "kill", "stop", "start", "enable", "disable", "approve", "reject", "cancel", "pay", "transfer",
    "purchase", "register", "unregister", "clear", "flush", "import",
)


def _result_text(result: Any) -> str:
    """The readable text of an MCP tool result, falling back to compact JSON.

    MCP returns `{"content": [{"type": "text", "text": ...}, ...]}`. Storing the whole envelope made
    the evidence a one-line JSON blob with every newline escaped — unreadable to the human who has to
    judge a citation, and, because the text was no longer on lines of its own, invisible to the
    line-anchored check that defuses forged excerpt delimiters. A mail body has to be stored as a mail
    body. Anything that is not text blocks (a resource read, a structured result) still round-trips as
    JSON: losing it would be worse than it being ugly.
    """
    if isinstance(result, dict) and isinstance(result.get("content"), list):
        parts = [block.get("text", "") for block in result["content"]
                 if isinstance(block, dict) and block.get("type") == "text"]
        text = "\n".join(p for p in parts if p)
        if text.strip():
            return text
    return json.dumps(result, ensure_ascii=False, sort_keys=True)


def _name_looks_mutating(name: str) -> bool:
    """Fallback heuristic ONLY (not exhaustive): does the tool name contain a mutating verb?"""
    lowered = re.sub(r"([a-z])([A-Z])", r"\1_\2", name).lower()
    return any(re.search(rf"(?:^|_){verb}(?:_|$)", lowered) for verb in _MUTATING_VERBS)


def _tool_read_only(name: str, annotations: dict | None) -> tuple[bool, str]:
    """(allowed, reason). Authority order: explicit readOnlyHint/destructiveHint > name heuristic.

    Fail-closed: an affirmative readOnlyHint is required to trust an annotated tool; an unannotated
    tool only passes if its NAME is not visibly mutating (a best-effort net, never a guarantee).
    """
    if annotations:
        if annotations.get("readOnlyHint") is True:
            return True, "readOnlyHint=true"
        if annotations.get("readOnlyHint") is False or annotations.get("destructiveHint") is True:
            return False, "server annotation marks it write-capable"
    if _name_looks_mutating(name):
        return False, "name looks mutating and the server gave no readOnlyHint"
    return True, "no readOnlyHint; name is not visibly mutating (heuristic)"


class McpConnector:
    id = "mcp"
    backend = "mcp-http"
    required_env: list[str] = []

    def ingest(self, options: IngestOptions) -> IngestResult:
        config = options.config or self._load_config()
        transport = config.get("transport") or {}
        allowed = _allowed(config)
        run_id = create_run_id()
        warnings: list[str] = []
        if not allowed:
            return IngestResult(self.id, "skipped", warnings=["MCP allowlist is empty"], run_id=run_id)
        try:
            client = _JsonRpcClient(transport)
            client.request("initialize", {"protocolVersion": MCP_PROTOCOL_VERSION, "capabilities": {},
                                           "clientInfo": {"name": "isidore", "version": "1"}})
            client.notify("notifications/initialized", {})
            tool_annotations = self._tool_annotations(client)
            items: list[dict] = []
            for spec in allowed:
                entry, arguments = spec["entry"], spec["arguments"]
                kind, _, name = entry.partition("/")
                if kind not in {"tools", "resources"} or not name:
                    warnings.append(f"invalid MCP allowlist entry skipped: {entry}")
                    continue
                if kind == "tools":
                    # resources/read is inherently read-only; a tool must prove it (readOnlyHint or,
                    # failing that, a non-mutating name). The barrier is fail-closed.
                    ok, reason = _tool_read_only(name, tool_annotations.get(name))
                    if not ok:
                        warnings.append(f"write-capable MCP tool rejected ({reason}): {entry}")
                        continue
                method = "tools/call" if kind == "tools" else "resources/read"
                params = ({"name": name, "arguments": arguments} if kind == "tools"
                          else {"uri": name})
                result = client.request(method, params)
                content = _result_text(result)
                # `f"{kind}/{name}"` was unaddressable: a '/' in an id breaks src:// (the store now
                # refuses it outright, which is how this was found).
                items.append({"id": safe_item_id(f"mcp-{kind}", name),
                              "stream": f"mcp/{kind}/{name}",
                              "ts": iso_now(), "content": content,
                              "meta": {"instance": config.get("instance", ""), "method": method}})
                if options.limit is not None and len(items) >= options.limit:
                    break
            raw_files = [write_items(self.id, config.get("instance"), run_id, items)] if items else []
            state = read_state(self.id, config.get("instance"))
            for item in items:
                update_cursor(state, item["stream"], item["id"])
            record_run(state, {"run_id": run_id, "at": iso_now(), "status": "success",
                               "raw_files": raw_files, "items": len(items)})
            write_state(self.id, config.get("instance"), state)
            return IngestResult(self.id, "success", raw_files, warnings,
                                {"items": len(items)}, run_id)
        except Exception as exc:  # fail closed: no raw file or cursor mutation on server failure
            return IngestResult(self.id, "error", warnings=[f"MCP server failed: {exc}"], run_id=run_id)
        finally:
            if "client" in locals():
                client.close()

    @staticmethod
    def _tool_annotations(client: "_JsonRpcClient") -> dict[str, dict]:
        """Map tool name -> its MCP annotations via tools/list (paginated). Empty if the server
        doesn't support tools/list — callers then fall back to the name heuristic (fail-closed)."""
        out: dict[str, dict] = {}
        cursor = None
        for _ in range(50):          # bound pagination
            try:
                res = client.request("tools/list", {"cursor": cursor} if cursor else {})
            except RuntimeError:
                break                # server doesn't advertise tools/list -> no annotations
            for tool in res.get("tools", []):
                if tool.get("name"):
                    out[tool["name"]] = tool.get("annotations") or {}
            cursor = res.get("nextCursor")
            if not cursor:
                break
        return out

    def _load_config(self) -> dict:
        path = config_path(self.id)
        try:
            return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}
        except (OSError, ValueError):
            return {}


class _JsonRpcClient:
    def __init__(self, transport: dict):
        self.transport = transport
        self._next_id = 0
        typ = transport.get("type")
        if typ == "stdio":
            command = transport.get("command")
            if not command:
                raise ValueError("stdio transport requires command")
            args = [str(a) for a in transport.get("args", [])]
            self.proc = subprocess.Popen([str(command), *args], stdin=subprocess.PIPE,
                                         stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                         text=True, encoding="utf-8", errors="replace")
        elif typ == "http":
            self.proc = None
            if not transport.get("url"):
                raise ValueError("http transport requires url")
        else:
            raise ValueError("transport.type must be http or stdio")

    def close(self) -> None:
        if self.proc is None:
            return
        self.proc.terminate()
        try:
            self.proc.wait(timeout=2)
        except subprocess.TimeoutExpired:
            self.proc.kill()
            self.proc.wait(timeout=2)

    def request(self, method: str, params: dict) -> Any:
        self._next_id += 1
        payload = {"jsonrpc": "2.0", "id": self._next_id, "method": method, "params": params}
        raw = self._send(payload)
        if raw.get("error") is not None:
            raise RuntimeError(str(raw["error"]))
        return raw.get("result", {})

    def notify(self, method: str, params: dict) -> None:
        self._send({"jsonrpc": "2.0", "method": method, "params": params}, notification=True)

    def _send(self, payload: dict, *, notification: bool = False) -> dict:
        if self.proc is None:
            headers = {}
            for key, value in (self.transport.get("headers") or {}).items():
                # `headers` accepts literal values; `env` is the only secret-bearing map.
                headers[str(key)] = str(value)
            for key, env_name in (self.transport.get("env") or {}).items():
                if str(env_name) in os.environ:
                    headers[str(key)] = os.environ[str(env_name)]
            # Streamable HTTP: the client MUST send an Accept listing BOTH content types, because the
            # server chooses between one JSON object and an SSE stream (spec 2025-06-18). Sending
            # neither is how a request gets rejected by a compliant server for no visible reason.
            req = urllib.request.Request(
                self.transport["url"], data=(json.dumps(payload) + "\n").encode(),
                headers={"Content-Type": "application/json",
                         "Accept": "application/json, text/event-stream",
                         "MCP-Protocol-Version": MCP_PROTOCOL_VERSION, **headers},
                method="POST")
            try:
                with urllib.request.urlopen(req, timeout=30) as response:
                    body = response.read().decode("utf-8")
            except (OSError, urllib.error.URLError) as exc:
                raise RuntimeError(str(exc)) from exc
            return {} if notification or not body.strip() else json.loads(body)
        # MCP stdio is NEWLINE-delimited JSON, not LSP's `Content-Length` framing: "Messages are
        # delimited by newlines, and MUST NOT contain embedded newlines" (spec 2025-06-18,
        # basic/transports#stdio). This spoke LSP, so it could not have exchanged a single message
        # with a real MCP server — and the only stub it was ever tested against spoke LSP too, so the
        # suite was green over an interoperability failure. Found by pointing it at a server written
        # from the spec rather than from this file.
        assert self.proc.stdin and self.proc.stdout
        self.proc.stdin.write(json.dumps(payload, ensure_ascii=False) + "\n")
        self.proc.stdin.flush()
        if notification:
            return {}
        while True:
            line = self.proc.stdout.readline()
            if not line:
                raise RuntimeError("stdio MCP server closed the connection")
            line = line.strip()
            if not line:
                continue                    # blank keep-alive line: not a message, not an error
            try:
                return json.loads(line)
            except ValueError as exc:
                # A server that writes anything but MCP messages to stdout is out of spec. Say which
                # line, because "invalid JSON" with no sample is unactionable.
                raise RuntimeError(
                    f"stdio MCP server wrote a non-message line to stdout: {line[:120]!r}") from exc


register(McpConnector())
