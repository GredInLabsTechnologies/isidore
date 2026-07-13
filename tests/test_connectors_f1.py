"""F1 (ADR-0032): knowledge home + raw store + git-repo connector.

The load-bearing test is idempotency — a re-ingest with no git changes must yield ZERO items. That
is exactly what the first draft broke (it never persisted the cursor), so it is asserted head-on.
"""
from __future__ import annotations

import json
import subprocess

import pytest

from isidore.connectors.base import IngestOptions
from isidore.connectors.git_repo import GitRepoConnector
from isidore.connectors import store


def _git(repo, *args):
    subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True, text=True)


def _make_repo(path):
    path.mkdir(parents=True)
    _git(path, "init", "-q")
    _git(path, "config", "user.email", "t@example.com")
    _git(path, "config", "user.name", "tester")
    (path / "a.txt").write_text("hi")
    _git(path, "add", "-A")
    _git(path, "commit", "-qm", "first")
    return path


def _head(repo):
    return subprocess.run(["git", "-C", str(repo), "rev-parse", "HEAD"],
                          capture_output=True, text=True).stdout.strip()


# ------------------------------------------------------------------ home + store

def test_home_env_override(tmp_path, monkeypatch):
    monkeypatch.setenv("ISIDORE_HOME", str(tmp_path / "kh"))
    from isidore.home import home, knowledge_dir
    assert home() == (tmp_path / "kh").resolve()
    assert knowledge_dir() == (tmp_path / "kh").resolve() / "knowledge"


def test_write_items_stamps_chash_and_does_not_mutate(tmp_path, monkeypatch):
    monkeypatch.setenv("ISIDORE_HOME", str(tmp_path))
    item = {"id": "1", "stream": "s", "ts": "t", "content": "  hello   world ", "meta": {}}
    store.write_items("c", "", "run1", [item])
    assert "chash" not in item  # caller's dict untouched
    got = list(store.iter_items("c", ""))
    assert len(got) == 1
    assert got[0]["chash"] == store.chash("hello world")  # normalized fingerprint


def test_read_state_missing_and_corrupt_return_default(tmp_path, monkeypatch):
    monkeypatch.setenv("ISIDORE_HOME", str(tmp_path))
    from isidore.home import state_path
    assert store.read_state("x", "") == {"version": 1, "cursors": {}, "runs": []}
    p = state_path("x", "")
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text("{ this is not json ][")
    assert store.read_state("x", "") == {"version": 1, "cursors": {}, "runs": []}


def test_record_run_keeps_last_20(tmp_path, monkeypatch):
    monkeypatch.setenv("ISIDORE_HOME", str(tmp_path))
    st = store.read_state("c", "")
    for i in range(25):
        store.record_run(st, {"run_id": f"r{i}", "at": "t"})
    assert len(st["runs"]) == 20
    assert st["runs"][0]["run_id"] == "r24"  # newest first


def test_resolve_uri_forms_and_malformed(tmp_path, monkeypatch):
    monkeypatch.setenv("ISIDORE_HOME", str(tmp_path))
    store.write_items("git-repo", "", "run1",
                      [{"id": "repo@abc", "stream": "repo", "ts": "t", "content": "x", "meta": {}}])
    assert store.resolve_uri("src://git-repo/repo@abc")["stream"] == "repo"
    assert store.resolve_uri("src://git-repo/nope") is None
    assert store.resolve_uri("not-a-uri") is None
    assert store.resolve_uri("src://a/b/c/d") is None


# ------------------------------------------------------------------ git-repo: the gate

def test_git_repo_ingest_persists_and_is_idempotent(tmp_path, monkeypatch):
    monkeypatch.setenv("ISIDORE_HOME", str(tmp_path / "home"))
    repo = _make_repo(tmp_path / "r1")
    conn = GitRepoConnector()

    r1 = conn.ingest(IngestOptions(config={"repos": [str(repo)]}))
    assert r1.status == "success"
    assert r1.counts["items"] == 1
    assert r1.raw_files and json.loads  # a raw file was actually written
    assert store.read_state("git-repo", "")["cursors"]["r1"] == _head(repo)

    # re-ingest, no changes -> ZERO new items (the F1 gate)
    r2 = conn.ingest(IngestOptions(config={"repos": [str(repo)]}))
    assert r2.status == "success"
    assert r2.counts["items"] == 0
    assert r2.raw_files == []

    # a new commit -> emits again
    (repo / "b.txt").write_text("more")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-qm", "second")
    r3 = conn.ingest(IngestOptions(config={"repos": [str(repo)]}))
    assert r3.counts["items"] == 1
    assert store.resolve_uri(f"src://git-repo/r1@{_head(repo)}")["stream"] == "r1"


def test_git_repo_handles_non_ascii_commit_messages(tmp_path, monkeypatch):
    """Regression: a real repo's commit messages carry UTF-8 (accents, emoji). On Windows,
    subprocess text-mode defaults to cp1252 and crashes on those bytes — the ingest must not."""
    monkeypatch.setenv("ISIDORE_HOME", str(tmp_path / "home"))
    repo = tmp_path / "uni"
    repo.mkdir(parents=True)
    _git(repo, "init", "-q")
    _git(repo, "config", "user.email", "t@example.com")
    _git(repo, "config", "user.name", "tester")
    (repo / "a.txt").write_text("x")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-qm", "café résumé 日本語 🚀 co-authored")
    r = GitRepoConnector().ingest(IngestOptions(config={"repos": [str(repo)]}))
    assert r.status == "success"
    assert r.counts["items"] == 1


def test_git_repo_bad_path_warns_not_crashes(tmp_path, monkeypatch):
    monkeypatch.setenv("ISIDORE_HOME", str(tmp_path / "home"))
    notgit = tmp_path / "notgit"
    notgit.mkdir()
    r = GitRepoConnector().ingest(IngestOptions(config={"repos": [str(notgit)]}))
    assert r.status == "error"  # all repos failed
    assert r.warnings and r.counts["items"] == 0


def test_git_repo_no_repos_skips(tmp_path, monkeypatch):
    monkeypatch.setenv("ISIDORE_HOME", str(tmp_path / "home"))
    r = GitRepoConnector().ingest(IngestOptions(config={"repos": []}))
    assert r.status == "skipped"


def test_one_bad_repo_does_not_abort_the_good_one(tmp_path, monkeypatch):
    monkeypatch.setenv("ISIDORE_HOME", str(tmp_path / "home"))
    good = _make_repo(tmp_path / "good")
    bad = tmp_path / "bad"
    bad.mkdir()
    r = GitRepoConnector().ingest(IngestOptions(config={"repos": [str(bad), str(good)]}))
    assert r.status == "success"  # the good one worked
    assert r.counts["items"] == 1
    assert any("bad" in w for w in r.warnings)


def test_registry_discovers_git_repo():
    import isidore.connectors  # noqa: F401  (registers built-ins on import)
    from isidore.connectors import base
    assert base.get("git-repo") is not None
    assert base.get("git-repo").backend == "local-git"


@pytest.mark.parametrize("limit,expected", [(1, 1), (2, 2)])
def test_limit_caps_repos(tmp_path, monkeypatch, limit, expected):
    monkeypatch.setenv("ISIDORE_HOME", str(tmp_path / "home"))
    repos = [str(_make_repo(tmp_path / f"r{i}")) for i in range(2)]
    r = GitRepoConnector().ingest(IngestOptions(config={"repos": repos}, limit=limit))
    assert r.counts["repos"] == expected
