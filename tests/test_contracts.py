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
