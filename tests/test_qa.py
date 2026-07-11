"""ask upgrade: claims as first-class evidence + the 0-LLM --offline path."""
from __future__ import annotations

from isidore.graph import write_scan
from isidore.pipeline import compile_wiki
from isidore.qa import answer_offline, ask, gather_claims, gather_evidence


def _repo(tmp_path):
    repo = tmp_path / "repo"
    (repo / "auth").mkdir(parents=True)
    (repo / "auth" / "__init__.py").write_text("", encoding="utf-8")
    pad = "\n".join(f"# pad {i}" for i in range(15))
    (repo / "auth" / "login.py").write_text(
        f"def verify_token():\n    return True\n{pad}\n", encoding="utf-8")
    gp = write_scan(repo)
    page = ("## Purpose\nHandles auth.\n\n```isidore-claims\n"
            "verify_token validates the session token | auth/login.py:1\n```\n")
    compile_wiki(repo, graph_path=gp, execute=True, min_symbols=1, generator=lambda p: page)
    return repo, gp


def test_gather_claims_scores_matching_claims(tmp_path):
    repo, _gp = _repo(tmp_path)
    scored = gather_claims(repo, "how is the session token validated?")
    assert scored and "validates the session token" in scored[0][1]["statement"]


def test_evidence_includes_verified_claims_block(tmp_path):
    repo, gp = _repo(tmp_path)
    evidence, sources = gather_evidence(repo, "session token", graph_path=gp)
    assert "verified claims" in evidence and "validates the session token" in evidence
    assert any(s.startswith("claim ") for s in sources)


def test_ask_offline_answers_from_claims_with_zero_calls(tmp_path):
    repo, gp = _repo(tmp_path)
    calls = []
    out = ask(repo, "how is the session token validated?", graph_path=gp,
              generator=lambda p: calls.append(p) or "SHOULD NOT BE CALLED", offline=True)
    assert calls == []                                   # zero LLM calls
    assert "0 LLM calls" in out and "validates the session token" in out


def test_ask_offline_refuses_honestly_when_no_claim_matches(tmp_path):
    repo, _gp = _repo(tmp_path)
    out = answer_offline(repo, "what is the deployment region for kubernetes ingress?")
    assert "No confident offline answer" in out
