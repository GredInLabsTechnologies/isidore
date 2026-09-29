"""Minimal read-only MCP connector (ADR-0032 F3).

The implementation deliberately speaks JSON-RPC 2.0 directly.  Configuration is per instance;
only explicitly allowlisted ``tools/<name>`` and ``resources/<uri>`` operations are attempted.
"""
from __future__ import annotations

import collections
import json
import os
import queue
import re
import subprocess
import threading
import time
import urllib.error
import urllib.request
from typing import Any
from urllib.parse import urlsplit

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


# Bounds on one exchange. A stdio server that never answers used to block `isidore sync` forever
# (readline has no timeout); an HTTP one could stream without end. Both are now errors that leave the
# connector's state untouched, like any other server failure.
RPC_TIMEOUT_S = 30
MAX_RESPONSE_BYTES = 8_000_000
_STDERR_TAIL_LINES = 20
_SESSION_HEADER = "Mcp-Session-Id"


class _JsonRpcClient:
    """JSON-RPC 2.0 over the two MCP transports (spec 2025-06-18, basic/transports).

    What a real server does and the stub this was tested against never did, each of which broke it:
    - a request's reply may arrive as an SSE stream (`text/event-stream`), which the client MUST
      support — it advertised it in `Accept` and then `json.loads`-ed the stream;
    - the server may send its own notifications and requests BEFORE the response, on stdio and on the
      SSE stream alike — the first message was taken as the reply, so a log notification became an
      empty result;
    - an `Mcp-Session-Id` returned at initialization MUST be sent on every later request — it was
      dropped, so a stateful server answered 400 from the second call on;
    - stderr is the server's log channel — it was piped and never read, so a chatty server filled the
      pipe and deadlocked.
    """

    def __init__(self, transport: dict):
        self.transport = transport
        self._next_id = 0
        self.session_id: str | None = None
        typ = transport.get("type")
        if typ == "stdio":
            command = transport.get("command")
            if not command:
                raise ValueError("stdio transport requires command")
            args = [str(a) for a in transport.get("args", [])]
            self.proc = subprocess.Popen([str(command), *args], stdin=subprocess.PIPE,
                                         stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                         text=True, encoding="utf-8", errors="replace")
            self._lines: queue.Queue = queue.Queue()
            self._stderr: collections.deque[str] = collections.deque(maxlen=_STDERR_TAIL_LINES)
            threading.Thread(target=self._pump_stdout, daemon=True).start()
            threading.Thread(target=self._drain_stderr, daemon=True).start()
        elif typ == "http":
            self.proc = None
            url = str(transport.get("url") or "")
            if not url:
                raise ValueError("http transport requires url")
            parts = urlsplit(url)
            # urllib would open file:// as happily as https://; a connector config is not a licence
            # to read the local filesystem through what looks like a server.
            if parts.scheme not in ("http", "https") or not parts.netloc:
                raise ValueError(f"http transport needs an http(s) URL with a host, got {url!r}")
        else:
            raise ValueError("transport.type must be http or stdio")

    # ------------------------------------------------------------------ lifecycle

    def close(self) -> None:
        if self.proc is None:
            if self.session_id:              # SHOULD end the session explicitly; 405 is a valid no
                try:
                    req = urllib.request.Request(self.transport["url"], method="DELETE",
                                                 headers=self._headers())
                    urllib.request.urlopen(req, timeout=5).close()   # noqa: S310 - scheme checked
                except (OSError, urllib.error.URLError):
                    pass
            return
        # The spec's order: close stdin (the server's cue to exit), then terminate if it does not.
        try:
            if self.proc.stdin:
                self.proc.stdin.close()
        except OSError:
            pass
        try:
            self.proc.wait(timeout=2)
        except subprocess.TimeoutExpired:
            self.proc.terminate()
            try:
                self.proc.wait(timeout=2)
            except subprocess.TimeoutExpired:
                self.proc.kill()
                self.proc.wait(timeout=2)

    def _pump_stdout(self) -> None:
        assert self.proc and self.proc.stdout
        for line in iter(self.proc.stdout.readline, ""):
            self._lines.put(line)
        self._lines.put(None)                # EOF sentinel: the server closed stdout

    def _drain_stderr(self) -> None:
        assert self.proc and self.proc.stderr
        for line in iter(self.proc.stderr.readline, ""):
            self._stderr.append(line.rstrip())

    def _stderr_hint(self) -> str:
        tail = [line for line in getattr(self, "_stderr", ()) if line]
        return f"; server stderr: {' | '.join(tail[-3:])[:300]}" if tail else ""

    # ------------------------------------------------------------------ JSON-RPC

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
            return self._send_http(payload, notification=notification)
        return self._send_stdio(payload, notification=notification)

    def _match(self, message: Any, want_id: Any) -> dict | None:
        """The response to `want_id` if `message` is (or, as a batch, holds) it. Anything else the
        server sends meanwhile is handled here: its requests are answered, its notifications and
        stray responses skipped — never mistaken for the reply."""
        for msg in message if isinstance(message, list) else [message]:
            if not isinstance(msg, dict):
                continue
            if "method" in msg:
                if msg.get("id") is not None:
                    self._answer_server_request(msg)
                continue
            if msg.get("id") == want_id and ("result" in msg or "error" in msg):
                return msg
        return None

    def _answer_server_request(self, msg: dict) -> None:
        """A server may ask the client something mid-request (`ping`, `roots/list`, sampling...).
        Ping gets its empty result; the rest a JSON-RPC 'method not found', which is the truthful
        answer for a read-only ingester — and an answer, so the server is not left waiting."""
        reply: dict = {"jsonrpc": "2.0", "id": msg["id"]}
        if msg.get("method") == "ping":
            reply["result"] = {}
        else:
            reply["error"] = {"code": -32601, "message": f"client does not support {msg.get('method')}"}
        self._send(reply, notification=True)

    # stdio: newline-delimited JSON --------------------------------------------------------------

    def _send_stdio(self, payload: dict, *, notification: bool) -> dict:
        # MCP stdio is NEWLINE-delimited JSON, not LSP's `Content-Length` framing: "Messages are
        # delimited by newlines, and MUST NOT contain embedded newlines" (spec 2025-06-18,
        # basic/transports#stdio). This spoke LSP, so it could not have exchanged a single message
        # with a real MCP server — and the only stub it was ever tested against spoke LSP too, so the
        # suite was green over an interoperability failure. Found by pointing it at a server written
        # from the spec rather than from this file.
        assert self.proc and self.proc.stdin
        try:
            self.proc.stdin.write(json.dumps(payload, ensure_ascii=False) + "\n")
            self.proc.stdin.flush()
        except OSError as exc:
            raise RuntimeError(f"stdio MCP server is gone ({exc}){self._stderr_hint()}") from exc
        if notification:
            return {}
        deadline = time.monotonic() + RPC_TIMEOUT_S
        while True:
            try:
                line = self._lines.get(timeout=max(0.0, deadline - time.monotonic()))
            except queue.Empty:
                raise RuntimeError(f"stdio MCP server sent no reply to {payload['method']!r} within "
                                   f"{RPC_TIMEOUT_S}s{self._stderr_hint()}") from None
            if line is None:
                self._lines.put(None)        # keep EOF visible to any later call
                raise RuntimeError(f"stdio MCP server closed the connection{self._stderr_hint()}")
            line = line.strip()
            if not line:
                continue                    # blank keep-alive line: not a message, not an error
            try:
                message = json.loads(line)
            except ValueError as exc:
                # A server that writes anything but MCP messages to stdout is out of spec. Say which
                # line, because "invalid JSON" with no sample is unactionable.
                raise RuntimeError(
                    f"stdio MCP server wrote a non-message line to stdout: {line[:120]!r}") from exc
            found = self._match(message, payload["id"])
            if found is not None:
                return found

    # Streamable HTTP ----------------------------------------------------------------------------

    def _headers(self) -> dict[str, str]:
        headers = {"MCP-Protocol-Version": MCP_PROTOCOL_VERSION}
        if self.session_id:
            headers[_SESSION_HEADER] = self.session_id
        for key, value in (self.transport.get("headers") or {}).items():
            # `headers` accepts literal values; `env` is the only secret-bearing map.
            headers[str(key)] = str(value)
        for key, env_name in (self.transport.get("env") or {}).items():
            if str(env_name) in os.environ:
                headers[str(key)] = os.environ[str(env_name)]
        return headers

    def _send_http(self, payload: dict, *, notification: bool) -> dict:
        # Streamable HTTP: the client MUST send an Accept listing BOTH content types, because the
        # server chooses between one JSON object and an SSE stream (spec 2025-06-18). Sending
        # neither is how a request gets rejected by a compliant server for no visible reason.
        req = urllib.request.Request(
            self.transport["url"], data=(json.dumps(payload) + "\n").encode(),
            headers={"Content-Type": "application/json",
                     "Accept": "application/json, text/event-stream", **self._headers()},
            method="POST")
        try:
            with urllib.request.urlopen(req, timeout=RPC_TIMEOUT_S) as response:  # noqa: S310
                session = response.headers.get(_SESSION_HEADER)
                if session and payload.get("method") == "initialize":
                    self.session_id = session.strip()
                if notification or response.status == 202:
                    return {}
                ctype = (response.headers.get("Content-Type") or "").split(";")[0].strip().lower()
                if ctype == "text/event-stream":
                    found = self._read_sse(response, payload["id"])
                else:
                    body = response.read(MAX_RESPONSE_BYTES + 1)
                    if len(body) > MAX_RESPONSE_BYTES:
                        raise RuntimeError(f"MCP response exceeds {MAX_RESPONSE_BYTES} bytes")
                    text = body.decode("utf-8")
                    found = self._match(json.loads(text), payload["id"]) if text.strip() else None
        except urllib.error.HTTPError as exc:
            if exc.code == 404 and self.session_id:
                raise RuntimeError("MCP server ended the session (404); the next run starts a new "
                                   "one") from exc
            raise RuntimeError(f"MCP server answered HTTP {exc.code}: {exc.reason}") from exc
        except (OSError, urllib.error.URLError) as exc:
            raise RuntimeError(str(exc)) from exc
        if found is None:
            raise RuntimeError(f"MCP server sent no response to {payload['method']!r}")
        return found

    def _read_sse(self, response, want_id: Any) -> dict | None:
        """Read SSE events until the one carrying the reply to `want_id`. Each event's `data:` lines
        join with newlines into one JSON-RPC message (WHATWG event-stream rules); comments (`:`),
        `event:`/`id:`/`retry:` fields and events of other messages are consumed and passed on."""
        data: list[str] = []
        read = 0
        for raw in response:
            read += len(raw)
            if read > MAX_RESPONSE_BYTES:
                raise RuntimeError(f"MCP event stream exceeds {MAX_RESPONSE_BYTES} bytes")
            line = raw.decode("utf-8").rstrip("\r\n")
            if line.startswith("data:"):
                value = line[5:]
                data.append(value[1:] if value.startswith(" ") else value)
                continue
            if line or not data:
                continue                     # a field we do not need, a comment, or a lone blank
            found = self._match(json.loads("\n".join(data)), want_id)
            data = []
            if found is not None:
                return found
        if data:                             # a stream that ends without its final blank line
            return self._match(json.loads("\n".join(data)), want_id)
        return None


register(McpConnector())
