"""The N3 product overview: plain language for anyone, resting on claims already proven below it."""
from __future__ import annotations

import json

import pytest

from isidore.pcp import CERT_SUFFIX, Certificate, ClaimVerdict, write_certificate
from isidore.pyramid import compile_overview, verified_claims

PAGE = """## What this is
This tool writes and keeps up to date the guide to a software project.

## What you can do with it
- **Trust what you read** – Every statement is checked against the project itself.

## How the pieces fit together
It reads the project, works out which parts matter, and writes the guide.

```isidore-claims
Every statement is checked against the project itself. | wiki://mod.md#c-1111 |
```
"""


@pytest.fixture()
def repo(tmp_path):
    """A repo whose module page already PROVED one claim and failed another."""
    root = tmp_path / "proj"
    (root / "wiki").mkdir(parents=True)
    (root / "README.md").write_text("# proj\n\nKeeps a project's guide honest.\n", encoding="utf-8")
    (root / "wiki" / "mod.md").write_text("# mod\n", encoding="utf-8")
    write_certificate(
        Certificate(page="mod.md", claims=[
            ClaimVerdict(id="c-1111", statement="the checker runs on every build",
                         evidence="mod.py:1", ehash="aaaa", predicate="defines:mod.py;check",
                         verdict="TRUE", oracle="graph"),
            ClaimVerdict(id="c-2222", statement="something the code did not support",
                         evidence="mod.py:9", ehash="bbbb", predicate="defines:mod.py;nope",
                         verdict="FALSE", oracle="graph"),
        ]),
        root / "wiki" / f"mod.md{CERT_SUFFIX}")
    return root


def test_only_proven_claims_become_citable_facts(repo):
    facts = verified_claims(repo)
    assert [c["id"] for c in facts] == ["c-1111"]          # the FALSE one is not offered
    assert facts[0]["uri"] == "wiki://mod.md#c-1111"


def test_dry_run_makes_no_call_and_reports_the_material(repo):
    result = compile_overview(repo, [], [], {},
                              generator=lambda p: pytest.fail("must not call the LLM"))
    assert result["calls"] == 0
    assert len(result["facts"]["claims"]) == 1


def test_a_wiki_claim_is_chained_and_verified_instead_of_being_dropped(repo):
    # The bug this pins: `anchor_claims` treats evidence as a file path, so a wiki:// URI was
    # hashed, failed, and dropped — leaving lane D's verifier registered but never once consulted.
    result = compile_overview(repo, [], [], {}, execute=True, generator=lambda p: PAGE)
    assert result["proved"] == 1

    cert = json.loads((repo / "wiki" / f"overview.md{CERT_SUFFIX}").read_text(encoding="utf-8"))
    claim = cert["claims"][0]
    assert claim["verdict"] == "TRUE"
    assert claim["oracle"] == "wiki"
    assert claim["evidence"] == "wiki://mod.md#c-1111"
    # Composed integrity: the child certificate is hashed in, so editing the module page shows up
    # here with no model call at all.
    assert cert["child_cert_hashes"]["mod.md"]


def test_a_page_that_can_prove_nothing_is_refused(repo):
    naked = "## What this is\nIt does many wonderful things for everyone.\n"
    result = compile_overview(repo, [], [], {}, execute=True, generator=lambda p: naked)

    assert result["written"] is False
    page = (repo / "wiki" / "overview.md").read_text(encoding="utf-8")
    assert "not published" in page
    assert "wonderful things" not in page      # fluent and unverifiable is exactly what is refused


def test_a_claim_citing_a_refuted_fact_does_not_count_as_proof(repo):
    lying = PAGE.replace("#c-1111", "#c-2222")          # the child claim that came back FALSE
    result = compile_overview(repo, [], [], {}, execute=True, generator=lambda p: lying)
    assert result["proved"] == 0
    assert result["written"] is False


def test_jargon_earns_one_rewrite_and_then_the_page_is_refused(repo):
    jargon = "## What this is\nThe module exposes a method for each endpoint.\n"
    prompts: list[str] = []

    def generator(prompt):
        prompts.append(prompt)
        return jargon

    result = compile_overview(repo, [], [], {}, execute=True, generator=generator)
    assert len(prompts) == 2
    assert "jargon-term" in prompts[1]                  # the repair names the rule that was broken
    assert result["plain_broken"]
    assert "could not be written in plain language" in \
        (repo / "wiki" / "overview.md").read_text(encoding="utf-8")


def test_the_fenced_block_is_not_judged_as_prose(repo):
    # The claims block carries URIs and identifiers by construction; judging it as prose would make
    # every well-formed page fail the plain-language gate.
    result = compile_overview(repo, [], [], {}, execute=True, generator=lambda p: PAGE)
    assert result["plain_broken"] == []
