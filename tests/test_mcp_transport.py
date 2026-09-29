"""The MCP client against servers written from the SPEC (2025-06-18, basic/transports), not from the
client: each server here does something the spec allows and the old client could not survive.

- stdio: the server sends a notification and a `ping` request BEFORE its response, and floods stderr
  (the old client returned the notification as the reply, never answered the ping, and never read
  stderr, so a chatty server filled the pipe and both sides blocked);
- stdio: a server that never answers must fail within the bound, not hang `isidore sync`;
- Streamable HTTP: the reply arrives as an SSE stream, the server assigns an `Mcp-Session-Id` and
  refuses any later request without it, and a notification gets 202 with no body.
"""
from __future__ import annotations

import json
import sys
import textwrap
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import pytest

from isidore.connectors import mcp
from isidore.connectors.base import IngestOptions
from isidore.connectors.mcp import McpConnector, _JsonRpcClient

CHATTY_STDIO = textwrap.dedent('''
    import json, sys
    def send(obj):
        sys.stdout.write(json.dumps(obj) + "\\n"); sys.stdout.flush()
    pending_ping = None
    while True:
        line = sys.stdin.readline()
        if not line:
            break
        msg = json.loads(line)
        if msg.get("id") == "srv-ping" and "result" in msg:
            pending_ping = "answered"
            continue
        if msg.get("id") is None:
            continue
        sys.stderr.write("log " + "x" * 2000 + "\\n" * 1)   # far past any pipe buffer over the run
        for _ in range(600):
            sys.stderr.write("noise " + "y" * 2000 + "\\n")
        sys.stderr.flush()
        send({"jsonrpc": "2.0", "method": "notifications/message", "params": {"level": "info"}})
        send({"jsonrpc": "2.0", "id": "srv-ping", "method": "ping"})
        if msg["method"] == "tools/list":
            result = {"tools": [{"name": "read_it", "annotations": {"readOnlyHint": True}}]}
        elif msg["method"] == "tools/call":
            result = {"content": [{"type": "text", "text": "ping was " + str(pending_ping)}]}
        else:
            result = {"protocolVersion": "2025-06-18", "capabilities": {}}
        send({"jsonrpc": "2.0", "id": msg["id"], "result": result})
''')

SILENT_STDIO = "import sys\nwhile sys.stdin.readline():\n    pass\n"


def _stdio(tmp_path, source: str) -> dict:
    path = tmp_path / "server.py"
    path.write_text(source, encoding="utf-8")
    return {"type": "stdio", "command": sys.executable, "args": [str(path)]}


def test_stdio_skips_notifications_answers_pings_and_survives_a_flood_of_stderr(tmp_path, monkeypatch):
    monkeypatch.setenv("ISIDORE_HOME", str(tmp_path / "home"))
    result = McpConnector().ingest(IngestOptions(config={
        "instance": "chatty", "transport": _stdio(tmp_path, CHATTY_STDIO),
        "allowed": ["tools/read_it"]}))
    assert result.status == "success", result.warnings
    assert result.counts == {"items": 1}

    client = _JsonRpcClient(_stdio(tmp_path, CHATTY_STDIO))
    try:
        assert client.request("initialize", {})["protocolVersion"] == "2025-06-18"
        text = client.request("tools/call", {"name": "read_it"})["content"][0]["text"]
        assert text == "ping was answered"           # the server's own request got its reply
    finally:
        client.close()


def test_stdio_server_that_never_answers_fails_within_the_bound(tmp_path, monkeypatch):
    monkeypatch.setattr(mcp, "RPC_TIMEOUT_S", 1)
    client = _JsonRpcClient(_stdio(tmp_path, SILENT_STDIO))
    try:
        with pytest.raises(RuntimeError, match="no reply to 'initialize' within 1s"):
            client.request("initialize", {})
    finally:
        client.close()


class _SpecServer(BaseHTTPRequestHandler):
    """Streamable HTTP as the spec allows it: SSE replies, a session, 202 for notifications."""
    SESSION = "sess-1868a90c"
    seen: list = []

    def log_message(self, format, *args):  # noqa: A002 - keep pytest output clean
        pass

    def do_POST(self):
        msg = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        type(self).seen.append((msg.get("method"), self.headers.get("Mcp-Session-Id")))
        if msg.get("method") != "initialize" and self.headers.get("Mcp-Session-Id") != self.SESSION:
            self.send_response(400)
            self.end_headers()
            return
        if msg.get("id") is None:          # a notification (or a client response): 202, no body
            self.send_response(202)
            self.end_headers()
            return
        if msg["method"] == "tools/list":
            result = {"tools": [{"name": "read_it", "annotations": {"readOnlyHint": True}}]}
        elif msg["method"] == "tools/call":
            result = {"content": [{"type": "text", "text": "over sse"}]}
        else:
            result = {"protocolVersion": "2025-06-18", "capabilities": {}}
        events = [
            ": a comment line",
            'event: message\ndata: {"jsonrpc": "2.0", "method": "notifications/progress",\n'
            'data:  "params": {}}',
            "data: " + json.dumps({"jsonrpc": "2.0", "id": msg["id"], "result": result}),
        ]
        body = ("\n\n".join(events) + "\n\n").encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream; charset=utf-8")
        if msg["method"] == "initialize":
            self.send_header("Mcp-Session-Id", self.SESSION)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_DELETE(self):
        type(self).seen.append(("DELETE", self.headers.get("Mcp-Session-Id")))
        self.send_response(405)
        self.end_headers()


@pytest.fixture()
def spec_server():
    _SpecServer.seen = []
    httpd = ThreadingHTTPServer(("127.0.0.1", 0), _SpecServer)
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    yield f"http://127.0.0.1:{httpd.server_address[1]}/mcp"
    httpd.shutdown()
    httpd.server_close()


def test_http_reads_sse_replies_and_keeps_the_session(spec_server, tmp_path, monkeypatch):
    monkeypatch.setenv("ISIDORE_HOME", str(tmp_path / "home"))
    result = McpConnector().ingest(IngestOptions(config={
        "instance": "spec", "transport": {"type": "http", "url": spec_server},
        "allowed": ["tools/read_it"]}))
    assert result.status == "success", result.warnings
    assert result.counts == {"items": 1}
    # every request after initialize carried the session, and the session was closed at the end
    assert _SpecServer.seen[0] == ("initialize", None)
    assert all(sid == _SpecServer.SESSION for _m, sid in _SpecServer.seen[1:])
    assert _SpecServer.seen[-1][0] == "DELETE"


@pytest.mark.parametrize("url", ["file:///etc/passwd", "ftp://host/x", "http:///no-host"])
def test_http_transport_refuses_anything_but_http_urls(url):
    with pytest.raises(ValueError, match="http\\(s\\) URL"):
        _JsonRpcClient({"type": "http", "url": url})
