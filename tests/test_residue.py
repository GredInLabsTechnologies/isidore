"""Residue-mining units: section diff, compile journal/stats, per-page history, claims/findings query."""
from __future__ import annotations

import shutil
import subprocess

import pytest

from isidore.claims import claims_for_file, claims_grep
from isidore.findings import findings_new
from isidore.graph import write_scan
from isidore.journal import render_stats, section_diff
from isidore.pipeline import WIKI_DIRNAME, compile_wiki, load_state

PAGE = "## Purpose\nok\n"


def _git(path, *args):
    subprocess.run(["git", *args], cwd=path, check=True, capture_output=True)


def _repo(tmp_path):
    if shutil.which("git") is None:
        pytest.skip("git not available")
    repo = tmp_path / "repo"
    (repo / "aaa").mkdir(parents=True)
    (repo / "aaa" / "__init__.py").write_text("", encoding="utf-8")
    pad = "\n".join(f"# pad {i}" for i in range(15))
    (repo / "aaa" / "x.py").write_text(f"def caller():\n    return 7\n{pad}\n", encoding="utf-8")
    _git(repo, "init", "-q")
    _git(repo, "config", "user.email", "t@t")
    _git(repo, "config", "user.name", "t")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-qm", "seed")
    return repo, write_scan(repo)


def test_section_diff_reports_changed_headings_and_line_delta():
    old = "## Purpose\nalpha\n## Architecture\nsame\n"
    new = "## Purpose\nBETA changed\n## Architecture\nsame\n## New\nextra\n"
    changed, delta = section_diff(old, new)
    assert "Purpose" in changed and "New" in changed and "Architecture" not in changed
    assert delta == 2


def test_journal_and_stats_track_calls_saved_and_unstable(tmp_path):
    repo, gp = _repo(tmp_path)
    compile_wiki(repo, graph_path=gp, execute=True, min_symbols=1, generator=lambda p: PAGE)
    # second run, nothing changed -> 0 generated, the page is a cache save
    compile_wiki(repo, graph_path=gp, execute=True, min_symbols=1, generator=lambda p: PAGE)
    state = load_state(repo / WIKI_DIRNAME)
    assert len(state["journal"]) == 2
    assert state["journal"][1]["generated"] == 0 and state["journal"][1]["calls_saved"] >= 1
    out = render_stats(state)
    assert "isidore stats" in out and "2 run(s)" in out


def test_page_history_records_section_changes(tmp_path):
    repo, gp = _repo(tmp_path)
    compile_wiki(repo, graph_path=gp, execute=True, min_symbols=1, generator=lambda p: PAGE)
    # force a regeneration with DIFFERENT prose by editing the source (dirties the page)
    x = repo / "aaa" / "x.py"
    x.write_text(x.read_text(encoding="utf-8").replace("return 7", "return 42"), encoding="utf-8")
    write_scan(repo)
    compile_wiki(repo, graph_path=gp, execute=True, min_symbols=1,
                 generator=lambda p: "## Purpose\nrewritten body\n## Extra\nnew section\n")
    state = load_state(repo / WIKI_DIRNAME)
    page = next(k for k in state["pages"] if k.startswith("aaa"))
    history = state["pages"][page]["history"]
    assert history and "Purpose" in history[-1]["sections_changed"]


def test_claims_for_file_and_grep(tmp_path):
    repo, gp = _repo(tmp_path)
    page = ("## Purpose\nText.\n\n```isidore-claims\n"
            "caller returns a constant integer | aaa/x.py:1\n```\n")
    compile_wiki(repo, graph_path=gp, execute=True, min_symbols=1, generator=lambda p: page)
    state = load_state(repo / WIKI_DIRNAME)
    by_file = claims_for_file(repo, state["pages"], "aaa/x.py")
    assert by_file and "constant integer" in by_file[0]["statement"]
    assert claims_grep(repo, state["pages"], "constant") == by_file
    assert claims_grep(repo, state["pages"], "nonexistent-term") == []


def test_findings_new_reports_todos_in_changed_files(tmp_path):
    repo, gp = _repo(tmp_path)
    compile_wiki(repo, graph_path=gp, execute=True, min_symbols=1, generator=lambda p: PAGE)
    baseline = load_state(repo / WIKI_DIRNAME)["commit"]
    x = repo / "aaa" / "x.py"
    x.write_text(x.read_text(encoding="utf-8") + "\n# TODO: wire the new path\n", encoding="utf-8")
    _llm, todos = findings_new(repo, {}, baseline)
    assert any("wire the new path" in t["note"] for t in todos)
