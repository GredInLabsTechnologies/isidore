"""F1's two missing commands (`isidore connect`, `isidore ingest`) and the caps they pass down.

F1's library shipped with tests; its CLI did not ship at all, so the caps in `IngestOptions` were
accepted and silently dropped, and there was no supported way to write a connector's config. Both are
covered here, and one test pins a git behaviour that only a live run exposed.
"""
from __future__ import annotations

import json
import os
import subprocess

import pytest

from isidore.connect import apply_settings, connector_summary, load_config, parse_setting, save_config
from isidore.connectors.base import IngestOptions
from isidore.connectors.git_repo import GitRepoConnector, _cap_content, _window_floor


def _git(repo, *args):
    subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True, text=True)


def _make_repo(path, message="first"):
    path.mkdir(parents=True)
    _git(path, "init", "-q")
    _git(path, "config", "user.email", "t@example.com")
    _git(path, "config", "user.name", "tester")
    (path / "a.txt").write_text("hi", encoding="utf-8")
    _git(path, "add", "-A")
    _git(path, "commit", "-qm", message)
    return path


@pytest.fixture()
def isolated_home(tmp_path, monkeypatch):
    monkeypatch.setenv("ISIDORE_HOME", str(tmp_path / "home"))
    return tmp_path


# ------------------------------------------------------------------ config: key=value

def test_a_json_shaped_value_keeps_its_type():
    assert parse_setting("limit=5") == ("limit", 5)
    assert parse_setting("enabled=true") == ("enabled", True)
    assert parse_setting("name=hello") == ("name", "hello")
    # A Windows path is not JSON and must survive verbatim, backslashes included.
    assert parse_setting(r"repos=C:\Users\x\repo") == ("repos", r"C:\Users\x\repo")


def test_a_setting_without_an_equals_is_rejected():
    with pytest.raises(ValueError):
        parse_setting("justakey")


def test_repeating_a_key_builds_a_list():
    # This is the whole reason plural config works from a shell: no quoting rules to remember.
    config, _refused = apply_settings({}, ["repos=/a", "repos=/b", "repos=/b"])
    assert config == {"repos": ["/a", "/b"]}          # and it does not duplicate


@pytest.mark.usefixtures("isolated_home")
def test_a_credential_shaped_value_is_refused_and_never_written():
    """Invariant I9: a connector's config holds the NAME of an env var, never its value."""
    config, refused = apply_settings({"repos": ["/a"]},
                                     ["token=ghp_A9f3KxQ7mZp2Lw8Rt5Yv1Nb4Hc6Jd0Se3Uk"])
    assert refused == ["token"]
    assert "token" not in config                      # not stored, not even redacted
    save_config("git-repo", "", config)
    assert "ghp_" not in json.dumps(load_config("git-repo", ""))


@pytest.mark.usefixtures("isolated_home")
def test_a_corrupt_config_reads_as_empty_rather_than_crashing():
    from isidore.home import config_path, safe_mkdir
    path = config_path("git-repo", "")
    safe_mkdir(path.parent)
    path.write_text("{not json", encoding="utf-8")
    assert load_config("git-repo", "") == {}


@pytest.mark.usefixtures("isolated_home")
def test_the_listing_reports_readiness_without_reading_a_secret():
    class NeedsKey:
        id, backend, required_env = "needs-key", "direct-api", ["ISIDORE_TEST_ABSENT_KEY"]

        def ingest(self, options):                    # pragma: no cover - never called here
            raise AssertionError("must not run")

    row = connector_summary(NeedsKey())
    assert row["ready"] == "no"
    assert row["missing_env"] == "ISIDORE_TEST_ABSENT_KEY"   # the NAME, which is not a secret


# ------------------------------------------------------------------ the caps (I2)

def test_a_window_that_cannot_be_expressed_reports_instead_of_returning_nothing():
    """A window is only trustworthy if the cases it cannot express SAY so instead of coming back empty.

    Both were measured, not imagined: `git log --since=999999 hours ago` returns ZERO commits with
    exit status 0 (approxidate gives up), and a window reaching past the epoch has no floor at all.
    """
    floor, note = _window_floor(24)
    assert isinstance(floor, int) and floor > 0 and note is None

    for impossible in (0, -5, 10 ** 9):
        floor, note = _window_floor(impossible)
        assert floor is None and note and str(impossible) in note

    assert _window_floor(None) == (None, None)


def test_a_window_excludes_old_commits_without_pruning_the_walk(tmp_path):
    """A window has to REMOVE something to be a window, and only what it was asked to remove.

    This repo is the shape that broke `git log --since`: HEAD is back-dated, so `--since` prunes the
    traversal there and loses the commit made seconds ago BEHIND it — a 24h window returning nothing
    at all. Filtering git's output instead keeps the recent commit and drops only the old one.
    """
    repo = _make_repo(tmp_path / "r")           # commit #1: now
    env = {"GIT_COMMITTER_DATE": "2026-01-01T00:00:00+0000",
           "GIT_AUTHOR_DATE": "2026-01-01T00:00:00+0000"}
    subprocess.run(["git", "-C", str(repo), "commit", "-qm", "old", "--allow-empty"],
                   check=True, capture_output=True, text=True, env={**os.environ, **env})

    conn = GitRepoConnector()
    assert len(conn._commits(str(repo), None)) == 2                   # both, unbounded
    kept = conn._commits(str(repo), _window_floor(24)[0])
    assert [c["subject"] for c in kept] == ["first"]                  # "old" is out


@pytest.mark.usefixtures("isolated_home")
def test_a_windowed_manifest_says_it_is_windowed(tmp_path):
    """Measured live: agora's manifest under a 24h window listed no commits at all. Correct — and
    indistinguishable, as written, from a repository with no history. The window has to be on the page.
    """
    repo = tmp_path / "r"                       # every commit older than the window
    repo.mkdir()
    env = {**os.environ, "GIT_COMMITTER_DATE": "2026-01-01T00:00:00+0000",
           "GIT_AUTHOR_DATE": "2026-01-01T00:00:00+0000"}
    for args in (["init", "-q"], ["config", "user.email", "t@example.com"],
                 ["config", "user.name", "tester"], ["commit", "-qm", "old", "--allow-empty"]):
        subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True,
                       text=True, env=env)

    item, _w = GitRepoConnector()._manifest(str(repo), {}, _window_floor(1)[0], 1)
    assert "Commit window: last 1 hour(s)" in item["content"]
    assert "(none in range)" in item["content"]          # not silence where commits would be
    assert item["meta"]["window_hours"] == 1

    unbounded, _w = GitRepoConnector()._manifest(str(repo), {})
    assert "Commit window" not in unbounded["content"]   # no window, no claim about one
    assert "window_hours" not in unbounded["meta"]


def test_truncation_is_reported_and_measurable():
    item = {"id": "x", "stream": "s", "content": "a" * 100, "meta": {"repo": "/r"}}
    capped, note = _cap_content(item, 40)

    assert note and "40 of 100 bytes" in note        # the reader is TOLD, never quietly shortchanged
    assert capped["meta"]["content_bytes"] == 100    # and the loss is measurable afterwards
    assert capped["meta"]["truncated"] is True
    assert len(capped["content"].encode("utf-8")) <= 40 + len("\n[truncated by --max-bytes]")
    assert item["content"] == "a" * 100              # the caller's dict is not mutated


def test_a_cap_that_does_not_bite_changes_nothing():
    item = {"id": "x", "stream": "s", "content": "short", "meta": {}}
    assert _cap_content(item, 1000) == (item, None)


def test_truncation_never_splits_a_character():
    # A byte cap landing mid-codepoint must not produce a broken item.
    item = {"id": "x", "stream": "s", "content": "ñ" * 20, "meta": {}}
    capped, note = _cap_content(item, 15)
    assert note
    capped["content"].encode("utf-8").decode("utf-8")      # would raise if the cut were mid-char


@pytest.mark.usefixtures("isolated_home")
def test_the_streams_filter_leaves_other_repos_untouched(tmp_path):
    a = _make_repo(tmp_path / "alpha")
    b = _make_repo(tmp_path / "beta")
    conn = GitRepoConnector()

    res = conn.ingest(IngestOptions(config={"repos": [str(a), str(b)]}, streams=["beta"]))
    assert res.counts["items"] == 1

    from isidore.connectors.store import read_state
    cursors = read_state("git-repo", "").get("cursors", {})
    assert list(cursors) == ["beta"]        # alpha was not read, so its cursor was not invented


@pytest.mark.usefixtures("isolated_home")
def test_max_bytes_reaches_the_connector_through_ingest(tmp_path):
    repo = _make_repo(tmp_path / "r")
    res = GitRepoConnector().ingest(
        IngestOptions(config={"repos": [str(repo)]}, max_bytes=50))
    assert res.counts["items"] == 1
    assert any("truncated" in w for w in res.warnings)


# ------------------------------------------------------------------ the ingest command

@pytest.mark.usefixtures("isolated_home")
def test_ingest_fails_closed_on_a_missing_env_var(capsys):
    """Invariant I6: a connector that cannot authenticate is skipped BEFORE it can reach the network."""
    from isidore.connectors.base import register
    from isidore.cli import main

    class NeedsKey:
        id, backend, required_env = "needs-key-x", "direct-api", ["ISIDORE_TEST_ABSENT_KEY"]

        def ingest(self, options):
            raise AssertionError("a connector missing its env must never run")

    register(NeedsKey())
    assert main(["ingest", "--connector", "needs-key-x"]) == 0
    out = capsys.readouterr().out
    assert "skipped" in out and "ISIDORE_TEST_ABSENT_KEY" in out


@pytest.mark.usefixtures("isolated_home")
def test_one_broken_connector_does_not_stop_the_others(tmp_path, capsys):
    from isidore.connectors.base import register
    from isidore.cli import main

    class Explodes:
        id, backend, required_env = "explodes", "direct-api", []

        def ingest(self, options):
            raise RuntimeError("boom")

    register(Explodes())
    repo = _make_repo(tmp_path / "r")
    save_config("git-repo", "", {"repos": [str(repo)]})

    rc = main(["ingest", "--connector", "explodes", "--connector", "git-repo"])
    out = capsys.readouterr().out
    assert rc == 1                       # the run reports failure...
    assert "boom" in out and "error" in out
    assert ",success,1," in out.replace(" ", "")   # ...and git-repo still ingested


@pytest.mark.usefixtures("isolated_home")
def test_an_unknown_connector_is_named_not_ignored(capsys):
    from isidore.cli import main
    assert main(["ingest", "--connector", "nope"]) == 2
    assert "nope" in capsys.readouterr().out


@pytest.mark.usefixtures("isolated_home")
def test_configure_then_ingest_end_to_end(tmp_path, capsys):
    """The gate F1 could never run: configure two repos, ingest, re-ingest for nothing."""
    from isidore.cli import main

    a, b = _make_repo(tmp_path / "one"), _make_repo(tmp_path / "two")
    assert main(["connect", "git-repo", "--configure",
                 "--set", f"repos={a}", "--set", f"repos={b}"]) == 0
    capsys.readouterr()

    assert main(["ingest", "--connector", "git-repo"]) == 0
    assert "2 new item(s)" in capsys.readouterr().out

    assert main(["ingest", "--connector", "git-repo"]) == 0
    assert "0 new item(s)" in capsys.readouterr().out      # idempotent

    _git(b, "commit", "-qm", "second", "--allow-empty")
    assert main(["ingest", "--connector", "git-repo"]) == 0
    assert "1 new item(s)" in capsys.readouterr().out      # only the repo that moved


@pytest.mark.usefixtures("isolated_home")
def test_a_corrupt_state_reingests_from_scratch_without_crashing(tmp_path, capsys):
    from isidore.cli import main
    from isidore.home import state_path

    repo = _make_repo(tmp_path / "r")
    save_config("git-repo", "", {"repos": [str(repo)]})
    main(["ingest", "--connector", "git-repo"])
    capsys.readouterr()

    state_path("git-repo", "").write_text('{"version": 1, "cursors": {"r": ', encoding="utf-8")
    assert main(["ingest", "--connector", "git-repo"]) == 0
    assert "1 new item(s)" in capsys.readouterr().out
