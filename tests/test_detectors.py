"""Lane C gate — deterministic detectors flag by facts, are specific, and don't crash. Golden fixtures."""
from __future__ import annotations

from pathlib import Path

from isidore.detectors import scan, shannon_entropy
from isidore.graph import load_graph
from isidore.pcp import VerifyContext

FIX = Path(__file__).parent / "fixtures" / "pcp"
REPO = FIX / "repo"


def _ctx() -> VerifyContext:
    nodes, links, commit = load_graph(FIX / "graph.json")
    return VerifyContext(repo=REPO, nodes=nodes, links=links, commit=commit)


def test_entropy_flags_the_backdoor_token():
    marks = scan(REPO, _ctx())
    hit = [m for m in marks if m.family == "entropy" and m.file == "svc/auth.py" and m.line == 23]
    assert hit and hit[0].severity == "danger"


def test_specificity_no_false_positive_on_ordinary_strings():
    marks = scan(REPO, _ctx())
    # the docstring, "authorization", "sha256" etc. must NOT be flagged as secrets
    entropy_lines = {(m.file, m.line) for m in marks if m.family == "entropy"}
    assert entropy_lines == {("svc/auth.py", 23)}   # exactly the sk_live_ literal, nothing else


def test_topology_reaches_tokens_from_auth():
    marks = scan(REPO, _ctx())
    assert any(m.family == "topology" and m.file == "svc/tokens.py" for m in marks)


def test_determinism():
    assert scan(REPO, _ctx()) == scan(REPO, _ctx())


def test_unreadable_file_does_not_crash(tmp_path):
    # a graph pointing at a missing file must degrade to no marks for it, not raise
    ctx = VerifyContext(repo=tmp_path, nodes=[{"id": "x", "label": "gone.py",
                        "source_file": "gone.py", "source_location": "L1"}], links=[])
    assert scan(tmp_path, ctx) == []


def test_shannon_entropy_basic():
    assert shannon_entropy("") == 0.0
    assert shannon_entropy("aaaa") == 0.0
    assert shannon_entropy("ab") == 1.0
