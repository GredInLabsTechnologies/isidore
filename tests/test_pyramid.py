"""Lane D gate — the pyramid plans from the real graph, uses imports for cohesion, and the wiki://
chain verifier resolves against certificates fail-closed. Golden fixtures. (regression for T-5726)"""
from __future__ import annotations

import json
from pathlib import Path

from isidore.graph import load_graph
from isidore.pcp import (
    Certificate,
    ClaimVerdict,
    Predicate,
    VerifyContext,
    parse_wiki_uri,
    write_certificate,
)
from isidore.pyramid import _wikichain_verifier, plan_pyramid

FIX = Path(__file__).parent / "fixtures" / "pcp"


def _graph():
    return load_graph(FIX / "graph.json")


def test_autoseed_groups_by_source_file_on_the_real_graph():
    """BUG 1 regression: auto-seed used node['path'/'file'/'name'] (absent) -> []. Must group by
    source_file's top dir."""
    nodes, links, _c = _graph()
    specs = plan_pyramid(nodes, links, {})
    assert specs, "auto-seed produced no subsystems on the real graph"
    subs = {s["name"] for s in specs if s["level"] == 2}
    assert "svc" in subs
    svc = next(s for s in specs if s["name"] == "svc")
    assert "svc/auth.py" in svc["modules"] and "svc/tokens.py" in svc["modules"]


def test_explicit_config_still_works():
    nodes, links, _c = _graph()
    cfg = json.loads((FIX / "pyramid_config.json").read_text())
    specs = plan_pyramid(nodes, links, cfg)
    assert any(s["level"] == 2 and s["name"] == "authentication" for s in specs)
    assert any(s["level"] == 3 and s["name"] == "overview" for s in specs)


def test_links_used_for_inter_subsystem_deps():
    """BUG 2 regression: `links` was ignored. imports edges must yield depends_on."""
    nodes = [
        {"id": "a", "label": "a.py", "source_file": "aa/a.py", "source_location": "L1"},
        {"id": "b", "label": "b.py", "source_file": "bb/b.py", "source_location": "L1"},
    ]
    links = [{"source": "a", "target": "b", "relation": "imports"}]
    specs = plan_pyramid(nodes, links, {})
    aa = next(s for s in specs if s["name"] == "aa")
    assert "bb" in aa["depends_on"]      # aa imports bb -> recorded from links


def test_wikichain_none_does_not_crash(tmp_path):
    """BUG 3 regression: a None predicate crashed with AttributeError."""
    ctx = VerifyContext(repo=tmp_path)
    assert _wikichain_verifier(None, ctx).value == "UNDECIDABLE"
    assert _wikichain_verifier(Predicate("wikichain", ("not-a-uri",)), ctx).value == "FALSE"


def test_wikichain_resolves_verdict_from_certificate(tmp_path):
    """The chain's truth comes from the cited page's certificate (verdict lives there)."""
    from isidore.pipeline import WIKI_DIRNAME
    wiki = tmp_path / WIKI_DIRNAME
    wiki.mkdir()
    cert = Certificate(page="svc.md", claims=[
        ClaimVerdict("c-true", "s", "svc/auth.py:1", "h", "calls:a;b", "TRUE", "ast"),
        ClaimVerdict("c-false", "s", "svc/auth.py:2", "h", "calls:a;c", "FALSE", "ast"),
    ])
    write_certificate(cert, wiki / "svc.md.cert.json")
    ctx = VerifyContext(repo=tmp_path)
    assert parse_wiki_uri("wiki://svc.md#c-true") == ("svc.md", "c-true")
    assert _wikichain_verifier(Predicate("wikichain", ("wiki://svc.md#c-true",)), ctx).value == "TRUE"
    assert _wikichain_verifier(Predicate("wikichain", ("wiki://svc.md#c-false",)), ctx).value == "FALSE"
    # a claim id that isn't in the cert -> quarantine (FALSE), not a crash
    assert _wikichain_verifier(Predicate("wikichain", ("wiki://svc.md#c-missing",)), ctx).value == "FALSE"
