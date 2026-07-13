"""MCP connector read-only barrier (ADR-0032 F3). Regression for the review of T-db84: the original
9-word denylist let execute_sql/add_user/drop_table/transfer_funds through. The authoritative barrier
is now the protocol's readOnlyHint; the name heuristic is a documented, non-exhaustive fallback."""
from __future__ import annotations

import pytest

from isidore.connectors import mcp
from isidore.connectors.mcp import McpConnector, _name_looks_mutating, _tool_read_only


# ---------------------------------------------------------------- annotation authority

def test_readonly_hint_true_allows():
    ok, why = _tool_read_only("anything", {"readOnlyHint": True})
    assert ok and "readOnlyHint" in why


def test_readonly_hint_false_rejects_even_innocent_name():
    ok, _ = _tool_read_only("get_weather", {"readOnlyHint": False})
    assert not ok                       # server authority beats a harmless-looking name


def test_destructive_hint_rejects():
    assert not _tool_read_only("fetch", {"destructiveHint": True})[0]


# ---------------------------------------------------------------- name-heuristic fallback

@pytest.mark.parametrize("name", [
    # the 14 mutators the old 9-word denylist let through
    "execute_sql", "add_user", "set_config", "drop_table", "insert_row", "run_command",
    "exec", "modify", "revoke_grant", "transfer_funds", "publish", "rename_file", "kill_process",
    # plus the ones it already caught
    "deleteUser", "sendMessage", "createIssue", "updateRow",
])
def test_mutating_names_are_rejected_without_annotation(name):
    assert _name_looks_mutating(name), name
    assert not _tool_read_only(name, None)[0]


@pytest.mark.parametrize("name", ["search", "list_posts", "read_file", "get_weather", "fetch_page"])
def test_read_names_pass_without_annotation(name):
    assert not _name_looks_mutating(name), name
    assert _tool_read_only(name, None)[0]


# ---------------------------------------------------------------- end-to-end ingest with a fake server

class _FakeClient:
    """Stands in for _JsonRpcClient: a server exposing one read tool, one write tool (annotated),
    and one unannotated mutator. Records which tools were actually called."""
    def __init__(self, transport):
        self.called: list[str] = []

    def request(self, method, params):
        if method == "initialize":
            return {}
        if method == "tools/list":
            return {"tools": [
                {"name": "search", "annotations": {"readOnlyHint": True}},
                {"name": "delete_all", "annotations": {"readOnlyHint": False}},
                {"name": "provision_box", "annotations": {}},        # unannotated mutator
            ]}
        if method == "tools/call":
            self.called.append(params["name"])
            return {"content": [{"type": "text", "text": f"ran {params['name']}"}]}
        return {}

    def notify(self, method, params):
        pass

    def close(self):
        pass


def test_ingest_invokes_only_read_only_tools(monkeypatch, tmp_path):
    from isidore import home
    monkeypatch.setenv("ISIDORE_HOME", str(tmp_path))
    monkeypatch.setattr(home, "home", lambda: tmp_path)

    fake = {}
    def _factory(transport):
        fake["client"] = _FakeClient(transport)
        return fake["client"]
    monkeypatch.setattr(mcp, "_JsonRpcClient", _factory)

    from isidore.connectors.base import IngestOptions
    config = {"instance": "t", "transport": {"type": "http", "url": "http://x"},
              "allowed": ["tools/search", "tools/delete_all", "tools/provision_box",
                          "resources/doc://readme"]}
    result = McpConnector().ingest(IngestOptions(config=config))

    called = fake["client"].called
    assert "search" in called                       # readOnlyHint=true -> invoked
    assert "delete_all" not in called               # readOnlyHint=false -> rejected (authority)
    assert "provision_box" not in called            # unannotated mutator -> rejected (heuristic)
    assert any("delete_all" in w for w in result.warnings)
    assert any("provision_box" in w for w in result.warnings)
