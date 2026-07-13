"""P-INT gate — the pipeline wiring ties all five PCP lanes together end to end: a real compile
produces a re-verifiable certificate (lane A) with typed verdicts, a deterministic danger mark
(lane C) forces the banner even though the prose never flags it, the reconciler runs (lane B), and
`verify_page` re-checks the result offline (tamper-evident). Uses the golden fixture repo."""
from __future__ import annotations

import shutil
from pathlib import Path

from isidore.pcp import CERT_SUFFIX, read_certificate
from isidore.pipeline import WIKI_DIRNAME, compile_wiki
from isidore.verify import verify_page

FIX = Path(__file__).parent / "fixtures" / "pcp"


def _fake_generator(_prompt: str) -> str:
    # a page whose prose deliberately NEVER mentions the hard-coded token (social engineering);
    # the deterministic detector must force the banner anyway (I10).
    return (
        "# svc\n\n"
        "The `svc` module authenticates callers. `authenticate` verifies the JWT by calling "
        "`verify_jwt`, and enforces the `MAX_ATTEMPTS` ceiling. Nothing unusual here.\n\n"
        "```isidore-claims\n"
        "authenticate calls verify_jwt | svc/auth.py:14 | calls:authenticate;verify_jwt\n"
        "the attempt ceiling MAX_ATTEMPTS is 5 | svc/auth.py:7 | value:MAX_ATTEMPTS;5\n"
        "```\n"
    )


def _compile(tmp_path: Path):
    repo = tmp_path / "repo"
    shutil.copytree(FIX / "repo", repo)
    graph = repo / ".isidore"
    graph.mkdir(exist_ok=True)
    shutil.copy(FIX / "graph.json", graph / "graph.json")
    result = compile_wiki(repo, graph_path=graph / "graph.json", execute=True,
                          generator=_fake_generator, max_calls=10,
                          module_depth=1, min_symbols=1)
    return repo, result


def test_compile_writes_a_certificate_with_typed_verdicts(tmp_path):
    repo, result = _compile(tmp_path)
    assert result.certificates, "no certificate written"
    page = result.certificates[0]
    cert_path = repo / WIKI_DIRNAME / (page + CERT_SUFFIX)
    assert cert_path.is_file()
    cert = read_certificate(cert_path)
    verdicts = {c.predicate: c.verdict for c in cert.claims if c.predicate}
    assert verdicts.get("calls:authenticate;verify_jwt") == "TRUE"
    assert verdicts.get("value:MAX_ATTEMPTS;5") == "TRUE"
    # verified mass counted at least the two proven sentences
    assert result.verified_mass["green"] >= 1


def test_deterministic_mark_forces_the_banner_despite_calm_prose(tmp_path):
    repo, result = _compile(tmp_path)
    page = result.certificates[0]
    # the prose never mentioned the token, yet the page must carry the SECURITY banner
    assert page in result.security_flagged
    assert result.marks_raised >= 1
    text = (repo / WIKI_DIRNAME / page).read_text(encoding="utf-8")
    assert "SECURITY" in text and "auth.py:23" in text
    # the certificate records the mark too
    cert = read_certificate(repo / WIKI_DIRNAME / (page + CERT_SUFFIX))
    assert any(m.family == "entropy" and m.line == 23 for m in cert.marks)


def _fake_generator_with_a_lie(_prompt: str) -> str:
    # the model asserts one TRUE predicate and one FALSE one (a hallucinated env var). The false
    # one must be quarantined: kept in the cert, never published in claims.toon.
    return (
        "# svc\n\nThe `svc` module authenticates callers via `authenticate`.\n\n"
        "```isidore-claims\n"
        "authenticate calls verify_jwt | svc/auth.py:14 | calls:authenticate;verify_jwt\n"
        "MAX_ATTEMPTS is read from the environment | svc/auth.py:7 | env:MAX_ATTEMPTS\n"
        "```\n"
    )


def test_refuted_claim_is_quarantined_not_published(tmp_path):
    import shutil
    from isidore.pcp import read_certificate
    repo = tmp_path / "repo"
    shutil.copytree(FIX / "repo", repo)
    (repo / ".isidore").mkdir(exist_ok=True)
    shutil.copy(FIX / "graph.json", repo / ".isidore" / "graph.json")
    result = compile_wiki(repo, graph_path=repo / ".isidore" / "graph.json", execute=True,
                          generator=_fake_generator_with_a_lie, max_calls=10,
                          module_depth=1, min_symbols=1)
    assert result.claims_refuted >= 1
    page = result.certificates[0]
    # the certificate KEEPS the refuted claim (audit trail)
    cert = read_certificate(repo / WIKI_DIRNAME / (page + CERT_SUFFIX))
    assert any(c.verdict == "FALSE" and c.predicate == "env:MAX_ATTEMPTS" for c in cert.claims)
    # but the published claims (claims.toon / pages_state) do NOT contain it
    from isidore.pipeline import load_state
    published = load_state(repo / WIKI_DIRNAME)["pages"][page]["claims"]
    assert all(c.get("verdict") != "FALSE" for c in published)
    assert not any(c["predicate"] == "env:MAX_ATTEMPTS" for c in published)
    # the TRUE one IS published
    assert any(c["predicate"] == "calls:authenticate;verify_jwt" for c in published)


def test_verify_ci_gates(tmp_path):
    from isidore.cli import main
    repo, _result = _compile(tmp_path)
    # baseline: intact certs -> 0
    assert main(["verify", "--repo", str(repo)]) == 0
    # the fixture page carries a danger mark (the hard-coded token) -> --fail-on-marks fails
    assert main(["verify", "--repo", str(repo), "--fail-on-marks"]) == 1
    # an impossibly high verified-mass bar fails; a floor of 0 passes
    assert main(["verify", "--repo", str(repo), "--min-verified-mass", "0.99"]) == 1
    assert main(["verify", "--repo", str(repo), "--min-verified-mass", "0.0"]) == 0


def test_verify_page_passes_then_breaks_on_tamper(tmp_path):
    repo, result = _compile(tmp_path)
    page_path = repo / WIKI_DIRNAME / result.certificates[0]
    ok, _cert = verify_page(repo, page_path)
    assert ok is True
    page_path.write_text(page_path.read_text(encoding="utf-8") + "\ninjected line\n", encoding="utf-8")
    ok2, _c2 = verify_page(repo, page_path)
    assert ok2 is False
