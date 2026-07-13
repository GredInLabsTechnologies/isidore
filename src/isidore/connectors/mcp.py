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
from .store import create_run_id, iso_now, read_state, record_run, update_cursor, write_items, write_state


def _allowed(config: dict) -> set[str]:
    return {str(x).strip() for x in config.get("allowed", []) if str(x).strip()}


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
            client.request("initialize", {"protocolVersion": "2025-03-26", "capabilities": {},
                                           "clientInfo": {"name": "isidore", "version": "1"}})
            client.notify("notifications/initialized", {})
            tool_annotations = self._tool_annotations(client)
            items: list[dict] = []
            for entry in sorted(allowed):
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
                params = {"name": name, "arguments": {}} if kind == "tools" else {"uri": name}
                result = client.request(method, params)
                content = json.dumps(result, ensure_ascii=False, sort_keys=True)
                items.append({"id": f"{kind}/{name}", "stream": f"mcp/{kind}/{name}",
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
            req = urllib.request.Request(self.transport["url"],
                                         data=(json.dumps(payload) + "\n").encode(),
                                         headers={"Content-Type": "application/json", **headers}, method="POST")
            try:
                with urllib.request.urlopen(req, timeout=30) as response:
                    body = response.read().decode("utf-8")
            except (OSError, urllib.error.URLError) as exc:
                raise RuntimeError(str(exc)) from exc
            return {} if notification or not body.strip() else json.loads(body)
        assert self.proc.stdin and self.proc.stdout
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.proc.stdin.write(f"Content-Length: {len(body)}\r\n\r\n{body.decode('utf-8')}")
        self.proc.stdin.flush()
        if notification:
            return {}
        headers = {}
        while True:
            line = self.proc.stdout.readline()
            if not line:
                raise RuntimeError("stdio MCP server closed the connection")
            if line in ("\r\n", "\n"):
                break
            key, sep, value = line.partition(":")
            if sep:
                headers[key.lower().strip()] = value.strip()
        length = headers.get("content-length")
        if not length or not length.isdigit():
            raise RuntimeError("stdio MCP response missing Content-Length")
        body = self.proc.stdout.read(int(length))
        if len(body) != int(length):
            raise RuntimeError("stdio MCP server closed the connection")
        return json.loads(body)


register(McpConnector())
