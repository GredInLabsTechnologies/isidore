from __future__ import annotations

import json
import os
from pathlib import Path
from unittest.mock import MagicMock


from isidore import contracts
from isidore.pcp import Contract, VerifyContext, TRUE, UNDECIDABLE, write_certificate, Certificate, ClaimVerdict


def test_verify_contracts_success():
    ctx = VerifyContext(repo=Path("."))
    
    # Mock verify_predicate
    from isidore import pcp
    old_verify = pcp.verify_predicate
    pcp.verify_predicate = MagicMock(return_value=pcp.Verdict(value=TRUE, oracle="ast"))
    
    try:
        cs = [Contract(id="c-1", predicate="calls:a;b", evidence="x.py:1", promoted_by="tester")]
        results = contracts.verify_contracts(cs, ctx)
        assert len(results) == 1
        assert results[0][0].id == "c-1"
        assert results[0][1].value == TRUE
    finally:
        pcp.verify_predicate = old_verify


def test_verify_contracts_malformed_predicate():
    ctx = VerifyContext(repo=Path("."))
    cs = [Contract(id="c-2", predicate="invalidpredicate", evidence="x.py:1", promoted_by="tester")]
    results = contracts.verify_contracts(cs, ctx)
    assert len(results) == 1
    assert results[0][1].value == UNDECIDABLE
    assert "malformed" in results[0][1].detail


def test_contracts_cli_promote_and_list(tmp_path, capsys):
    wiki_dir = tmp_path / "wiki"
    wiki_dir.mkdir()
    
    # Write a dummy cert
    cert = Certificate(
        page="svc.md",
        claims=[
            ClaimVerdict(
                id="c-d64d0c93",
                statement="authenticate verifies JWT",
                evidence="svc/auth.py:14",
                ehash="0f4f56be82b1",
                predicate="calls:authenticate;verify_jwt",
                verdict=TRUE
            )
        ]
    )
    write_certificate(cert, wiki_dir / "svc.md.cert.json")
    
    # 1. Promote a nonexistent claim -> exit 1
    args_fail = MagicMock(repo=tmp_path, promote="c-missing", list=False)
    rc = contracts._cmd_contracts(args_fail)
    assert rc == 1
    assert "not found" in capsys.readouterr().err
    
    # 2. Promote claim c-d64d0c93 -> success
    os.environ["AGORA_ACTOR"] = "tester-agent"
    args_ok = MagicMock(repo=tmp_path, promote="c-d64d0c93", list=False)
    rc = contracts._cmd_contracts(args_ok)
    assert rc == 0
    assert "ACCEPTED contract.promote" in capsys.readouterr().out
    
    # Check that contracts.json exists
    contracts_file = wiki_dir / "contracts.json"
    assert contracts_file.is_file()
    with open(contracts_file) as f:
        data = json.load(f)
    assert len(data["contracts"]) == 1
    c = data["contracts"][0]
    assert c["id"] == "c-d64d0c93"
    assert c["promoted_by"] == "tester-agent"
    
    # 3. List contracts -> success
    args_list = MagicMock(repo=tmp_path, promote=None, list=True)
    rc = contracts._cmd_contracts(args_list)
    assert rc == 0
    out = capsys.readouterr().out
    assert "c-d64d0c93" in out
    assert "tester-agent" in out


# ------------------------------------------------ the gate blocks when it cannot check (fail-closed)

FIX = Path(__file__).parent / "fixtures" / "pcp"


def _contract_repo(tmp_path: Path, predicate: str, *, graph: bool = True) -> Path:
    """The PCP fixture repo with one promoted contract and no pages: only the contract gate speaks."""
    import shutil
    repo = tmp_path / "repo"
    shutil.copytree(FIX / "repo" / "svc", repo / "svc")
    (repo / "wiki").mkdir()
    if graph:
        (repo / ".isidore").mkdir()
        shutil.copy(FIX / "graph.json", repo / ".isidore" / "graph.json")
    body = json.loads((FIX / "contracts.json").read_text(encoding="utf-8"))
    body["contracts"][0]["predicate"] = predicate
    (repo / "wiki" / "contracts.json").write_text(json.dumps(body), encoding="utf-8")
    return repo


def _verify(repo: Path) -> int:
    from argparse import Namespace
    from isidore.verify import _cmd_verify
    return _cmd_verify(Namespace(repo=repo, contracts=True, min_verified_mass=None,
                                 fail_on_marks=False))


def test_verify_contracts_passes_a_kept_invariant(tmp_path, capsys):
    assert _verify(_contract_repo(tmp_path, "calls:authenticate;verify_jwt")) == 0


def test_verify_contracts_blocks_when_it_cannot_check(tmp_path, capsys):
    # regression: each of these printed "certificates intact" and exited 0 over an unchecked invariant
    assert _verify(_contract_repo(tmp_path / "a", "calls:authenticate;verify_jwt", graph=False)) == 1
    assert "BLOCKED 1 contract(s)" in capsys.readouterr().out

    assert _verify(_contract_repo(tmp_path / "b", "not-a-predicate")) == 1
    assert "UNDECIDABLE contract" in capsys.readouterr().out

    repo = _contract_repo(tmp_path / "c", "calls:authenticate;verify_jwt")
    (repo / "wiki" / "contracts.json").write_text("{not json", encoding="utf-8")
    assert _verify(repo) == 1                      # a clean refusal, not a traceback
    assert "BLOCKED contracts" in capsys.readouterr().out


def test_contracts_promote_writes_where_verify_reads(tmp_path, capsys, monkeypatch):
    # regression: promote wrote a literal wiki/contracts.json while verify read the CONFIGURED wiki
    # directory, so with `wiki_dir` set a promoted invariant was never enforced.
    from isidore import render
    monkeypatch.setattr(render, "WIKI_DIRNAME", "doc/isidore")
    wiki_dir = tmp_path / "doc" / "isidore"
    wiki_dir.mkdir(parents=True)
    write_certificate(Certificate(page="svc.md", claims=[ClaimVerdict(
        id="c-d64d0c93", statement="s", evidence="svc/auth.py:14", ehash="0f4f56be82b1",
        predicate="calls:authenticate;verify_jwt", verdict=TRUE)]), wiki_dir / "svc.md.cert.json")
    assert contracts._cmd_contracts(MagicMock(repo=tmp_path, promote="c-d64d0c93", list=False)) == 0
    assert (wiki_dir / "contracts.json").is_file()
    assert not (tmp_path / "wiki").exists()
