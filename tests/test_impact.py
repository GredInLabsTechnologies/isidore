"""isidore impact — the 0-LLM emergent-interaction detector, over a real git repo + real scan."""
from __future__ import annotations

import shutil
import subprocess

import pytest

from isidore.graph import write_scan
from isidore.impact import build_impact, render_impact
from isidore.pipeline import compile_wiki

PAGE = "## Purpose\nok\n"


def _git(path, *args):
    subprocess.run(["git", *args], cwd=path, check=True, capture_output=True)


def _seed_repo(tmp_path):
    if shutil.which("git") is None:
        pytest.skip("git not available")
    repo = tmp_path / "repo"
    for pkg in ("aaa", "bbb"):
        (repo / pkg).mkdir(parents=True)
        (repo / pkg / "__init__.py").write_text("", encoding="utf-8")
    pad = "\n".join(f"# pad {i}" for i in range(15))
    (repo / "bbb" / "y.py").write_text(f"def helper():\n    return 1\n{pad}\n", encoding="utf-8")
    (repo / "aaa" / "x.py").write_text(f"def caller():\n    return 7\n{pad}\n", encoding="utf-8")
    _git(repo, "init", "-q")
    _git(repo, "config", "user.email", "t@t")
    _git(repo, "config", "user.name", "t")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-qm", "seed")
    gp = write_scan(repo)
    compile_wiki(repo, graph_path=gp, execute=True, min_symbols=1, generator=lambda p: PAGE)
    return repo, gp


def test_impact_reports_a_new_cross_module_edge_as_emergent(tmp_path):
    repo, gp = _seed_repo(tmp_path)
    # introduce a NEW dependency: aaa/x.py now imports bbb.y  (aaa -> bbb edge appears)
    x = repo / "aaa" / "x.py"
    x.write_text("import bbb.y\n" + x.read_text(encoding="utf-8").replace("return 7", "return bbb.y.helper()"),
                 encoding="utf-8")
    write_scan(repo)

    r = build_impact(repo, graph_path=gp, min_symbols=1)
    assert ("aaa/x.py", "bbb/y.py") in r.new_edges          # emergent interaction, detected with 0 LLM
    assert not r.removed_edges
    assert any("aaa" in p for p in r.dirty_pages)            # the changed page would regenerate
    assert "aaa/x.py" in r.affected_modules


def test_impact_reports_a_removed_edge(tmp_path):
    repo, gp = _seed_repo(tmp_path)
    # start FROM a state that has the edge, compile it into the fingerprint, then remove it
    x = repo / "aaa" / "x.py"
    x.write_text("import bbb.y\n" + x.read_text(encoding="utf-8").replace("return 7", "return bbb.y.helper()"),
                 encoding="utf-8")
    write_scan(repo)
    _git(repo, "add", "-A")
    _git(repo, "commit", "-qm", "add edge")
    compile_wiki(repo, graph_path=gp, execute=True, min_symbols=1, generator=lambda p: PAGE)  # fingerprint now HAS the edge
    # remove the dependency
    x.write_text("def caller():\n    return 7\n", encoding="utf-8")
    write_scan(repo)

    r = build_impact(repo, graph_path=gp, min_symbols=1)
    assert ("aaa/x.py", "bbb/y.py") in r.removed_edges
    assert not r.new_edges


def test_impact_check_exit_signal_and_clean(tmp_path):
    repo, gp = _seed_repo(tmp_path)
    # nothing changed since the baseline compile -> no signal
    clean = build_impact(repo, graph_path=gp, min_symbols=1)
    assert not clean.has_signal()
    # a real edit -> signal
    y = repo / "bbb" / "y.py"
    y.write_text(y.read_text(encoding="utf-8").replace("return 1", "return 42"), encoding="utf-8")
    write_scan(repo)
    dirty = build_impact(repo, graph_path=gp, min_symbols=1)
    assert dirty.has_signal() and dirty.dirty_pages
    # render both formats without error
    assert "isidore impact" in render_impact(dirty)
    assert "isidore impact" in render_impact(dirty, md=True)
