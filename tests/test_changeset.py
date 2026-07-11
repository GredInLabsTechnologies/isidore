"""Change-set detection units: symbol spans, changed symbols, affected modules, git line diff."""
from __future__ import annotations

import shutil
import subprocess

import pytest

from isidore.changeset import (
    affected_modules,
    changed_lines,
    changed_symbols,
    symbol_spans,
)

DEPTH = 2


def _code(nid, src, loc, label=None):
    return {"id": nid, "source_file": src, "file_type": "code",
            "label": label or nid, "source_location": loc}


def test_symbol_spans_accepts_span_and_start_only_forms():
    nodes = [
        _code("f", "a/core/x.py", "L3-L5"),
        _code("g", "a/core/x.py", "L10"),          # start-only -> spans to next start - 1
        _code("h", "a/core/x.py", "L20"),          # last start-only -> to EOF
        _code("doc", "a/core/x.py", "L1"),         # file node, start-only -> to first symbol - 1
    ]
    spans = {s[2]: (s[0], s[1]) for s in symbol_spans(nodes)["a/core/x.py"]}
    assert spans["f"] == (3, 5)
    assert spans["g"] == (10, 19)
    assert spans["h"][0] == 20 and spans["h"][1] > 1000
    assert spans["doc"] == (1, 2)


def test_changed_symbols_maps_lines_and_whole_file():
    nodes = [_code("f", "a/core/x.py", "L3-L5"), _code("g", "a/core/x.py", "L10-L12")]
    assert changed_symbols(nodes, {"a/core/x.py": {4}}) == {"f"}
    assert changed_symbols(nodes, {"a/core/x.py": {11}}) == {"g"}
    assert changed_symbols(nodes, {"a/core/x.py": {0}}) == {"f", "g"}      # whole-file sentinel
    assert changed_symbols(nodes, {"a/core/x.py": {99}}) == set()          # outside any span
    assert changed_symbols(nodes, {"other/z.py": {4}}) == set()            # unknown file


def test_affected_modules_is_changed_plus_fan_in_dependents():
    # A depends on B (edge A->B). A change in B affects B and, at depth>=1, A too.
    nodes = [_code("a", "aaa/core/x.py", "L1-L9"), _code("b", "bbb/core/y.py", "L1-L9")]
    links = [{"source": "a", "target": "b", "relation": "imports"}]
    changed = {"b"}
    assert affected_modules(nodes, links, changed, module_depth=DEPTH, depth=0) == {"bbb/core"}
    assert affected_modules(nodes, links, changed, module_depth=DEPTH, depth=1) == {"bbb/core", "aaa/core"}
    # a change in A does NOT drag in B (B does not depend on A)
    assert affected_modules(nodes, links, {"a"}, module_depth=DEPTH, depth=1) == {"aaa/core"}


def _git(path, *args):
    subprocess.run(["git", *args], cwd=path, check=True, capture_output=True)


def test_changed_lines_parses_new_side_hunks(tmp_path):
    if shutil.which("git") is None:
        pytest.skip("git not available")
    repo = tmp_path
    _git(repo, "init", "-q")
    _git(repo, "config", "user.email", "t@t")
    _git(repo, "config", "user.name", "t")
    f = repo / "m.py"
    f.write_text("\n".join(f"line{i}" for i in range(1, 11)) + "\n", encoding="utf-8")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-qm", "seed")
    # change lines 3 and 7 in the working tree
    lines = f.read_text(encoding="utf-8").splitlines()
    lines[2] = "CHANGED3"
    lines[6] = "CHANGED7"
    f.write_text("\n".join(lines) + "\n", encoding="utf-8")

    result = changed_lines(repo, "HEAD")
    assert "m.py" in result
    assert 3 in result["m.py"] and 7 in result["m.py"]
    assert 5 not in result["m.py"]
