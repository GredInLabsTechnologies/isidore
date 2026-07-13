"""P0 gate (ADR-0033) — the frozen PCP seam parses its golden fixtures and exposes every lane's
public surface. This test does NOT check verification LOGIC (that is each lane's gate); it checks
that lanes A–E can start against a stable, self-consistent surface: types round-trip, the registry
is wired fail-closed, and the CLI subcommands are registered.
"""
from __future__ import annotations

from pathlib import Path

import pytest

from isidore import contracts, detectors, humanpack, pyramid, reconcile, verify
from isidore.cli import main
from isidore.graph import load_graph
from isidore.pcp import (
    ORACLE_NONE,
    UNDECIDABLE,
    Certificate,
    Mark,
    Predicate,
    VerifyContext,
    parse_predicate,
    parse_wiki_uri,
    read_certificate,
    read_contracts,
    verify_predicate,
    write_certificate,
)

FIX = Path(__file__).parent / "fixtures" / "pcp"
REPO = FIX / "repo"


# ---------------------------------------------------------------- fixtures parse

def test_golden_graph_loads():
    nodes, links, commit = load_graph(FIX / "graph.json")
    assert len(nodes) == 5 and len(links) == 4
    assert commit and commit.startswith("0f1e5ba")


def test_golden_certificate_round_trips(tmp_path):
    cert = read_certificate(REPO / "wiki" / "svc.md.cert.json")
    assert cert.page == "svc.md"
    assert len(cert.prose_sha256) == 64
    assert len(cert.claims) == 6
    # five typed claims carry a predicate; the sixth is existence-anchored (yellow)
    typed = [c for c in cert.claims if c.predicate]
    assert len(typed) == 5
    assert cert.marks and cert.marks[0].family == "entropy"
    # write -> read is identity (byte-deterministic persistence)
    out = tmp_path / "rt.cert.json"
    write_certificate(cert, out)
    assert read_certificate(out) == cert


def test_golden_contracts_load():
    cs = read_contracts(FIX / "contracts.json")
    assert len(cs) == 1 and cs[0].predicate == "calls:authenticate;verify_jwt"


def test_golden_marks_and_pyramid_config_parse():
    import json
    marks = [Mark(**m) for m in json.loads((FIX / "marks.json").read_text())["marks"]]
    assert {m.family for m in marks} == {"entropy", "sink", "topology"}
    cfg = json.loads((FIX / "pyramid_config.json").read_text())
    assert cfg["pyramid"]["subsystems"][0]["name"] == "authentication"


# ---------------------------------------------------------------- predicate grammar

@pytest.mark.parametrize("raw,kind,args", [
    ("calls:authenticate;verify_jwt", "calls", ("authenticate", "verify_jwt")),
    ("value:MAX_ATTEMPTS;5", "value", ("MAX_ATTEMPTS", "5")),
    ("env:AUTH_SIGNING_KEY", "env", ("AUTH_SIGNING_KEY",)),
])
def test_predicate_parse_and_serialize_round_trip(raw, kind, args):
    p = parse_predicate(raw)
    assert p == Predicate(kind=kind, args=args)
    assert p.serialize() == raw


@pytest.mark.parametrize("raw", ["", None, "no-colon", "bogus:x", "calls:"])
def test_predicate_rejects_absent_or_unknown(raw):
    assert parse_predicate(raw) is None


def test_wiki_uri_parsing():
    assert parse_wiki_uri("wiki://svc.md#c-d64d0c93") == ("svc.md", "c-d64d0c93")
    assert parse_wiki_uri("svc/auth.py:14") is None


# ---------------------------------------------------------------- registry is fail-closed

def test_registry_has_every_kind_and_is_fail_closed():
    ctx = VerifyContext(repo=REPO)
    # lane A's eight kinds + lane D's wiki chain kind are all registered (import side effects)
    for raw in ("calls:a;b", "defines:f;s", "value:c;1", "env:X"):
        v = verify_predicate(parse_predicate(raw), ctx)
        assert v.value == UNDECIDABLE and v.oracle == ORACLE_NONE  # stubs decide nothing (yet)
    # a predicate with no registered verifier also degrades to UNDECIDABLE, never TRUE
    assert verify_predicate(Predicate("neverregistered", ("x",)), ctx).value == UNDECIDABLE


# ---------------------------------------------------------------- lane public surfaces exist

def test_lane_public_surfaces_return_frozen_types(tmp_path):
    """The frozen signatures exist and return the seam's types (whether stub or implemented)."""
    ctx = VerifyContext(repo=REPO)
    assert isinstance(reconcile.reconcile("prose", [], []), list)
    assert isinstance(detectors.scan(REPO, ctx), list)
    assert isinstance(pyramid.plan_pyramid([], [], {}), list)
    assert isinstance(humanpack.render_pack(REPO / "wiki", tmp_path / "out"), Path)
    verdicts = contracts.verify_contracts(read_contracts(FIX / "contracts.json"), ctx)
    assert verdicts and verdicts[0][0].predicate == "calls:authenticate;verify_jwt"
    cert = verify.build_certificate("svc.md", "# svc\n", [], ctx, marks=[], violations=[])
    assert isinstance(cert, Certificate) and len(cert.prose_sha256) == 64


# ---------------------------------------------------------------- CLI subcommands registered

@pytest.mark.parametrize("cmd", ["verify", "contracts", "pyramid", "render"])
def test_pcp_subcommands_are_registered(cmd, tmp_path):
    # each subcommand is registered and dispatches to an int-returning handler (argparse would
    # SystemExit on an unknown choice); we assert registration, not a particular exit code.
    rc = main([cmd, "--repo", str(tmp_path)])
    assert isinstance(rc, int)
