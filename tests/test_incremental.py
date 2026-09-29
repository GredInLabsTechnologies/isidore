"""Incremental compile: a page is rewritten only when what it describes changed, and then only the
sections that must change.

Measured before this on isidore's own wiki: 5-12 of 40 pages rewritten from nothing per commit, one
page seven times in fifteen runs — because "dirty" was the hash of the whole prompt (git log, link
counts, the template) and a dirty page was regenerated without even seeing its previous version.

Real flow throughout: a git repository, the built-in scanner, `compile_wiki --execute`. Only the model
is a stub, and it records every prompt it receives.
"""
from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from isidore import pipeline
from isidore.graph import write_scan
from isidore.pipeline import compile_wiki, load_state
from isidore.revise import carry_claims, splice, strip_security_banner

FUNCS = ["alpha", "beta", "gamma", "delta", "epsilon", "zeta", "eta", "theta", "iota", "kappa",
         "lambda_", "mu"]
FILLER = 120        # module-level constants below the functions, far outside every excerpt window

FULL_PAGE = """## Purpose
Core holds the arithmetic helpers `pkg/core.py:1`.

## Architecture
Twelve small functions, each returning a constant.

## How to change safely
Keep the return values stable; the constants end at `X_100` (`pkg/core.py:149`).

```isidore-claims
core defines alpha | pkg/core.py:1 | defines:pkg/core.py;alpha
beta returns 1 | pkg/core.py:6
```
"""


def _git(repo: Path, *args: str) -> None:
    subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True)


def _source(returns: dict[str, object] | None = None, tail: str = "") -> str:
    returns = returns or {}
    body = "".join(f"def {f}():\n    return {returns.get(f, i)}\n\n\n" for i, f in enumerate(FUNCS))
    consts = "".join(f"X_{i} = {i}\n" for i in range(FILLER))
    return body + consts + tail


class Model:
    """Records prompts; answers a full page, or — for a revision — whatever `revision` says."""

    def __init__(self):
        self.prompts: list[str] = []
        self.revision = "NO-CHANGES"

    def __call__(self, prompt: str) -> str:
        self.prompts.append(prompt)
        return self.revision if "CURRENT PAGE" in prompt else FULL_PAGE


@pytest.fixture()
def repo(tmp_path):
    root = tmp_path / "repo"
    (root / "pkg").mkdir(parents=True)
    _git(root, "init", "-q")
    _git(root, "config", "user.email", "t@t.invalid")
    _git(root, "config", "user.name", "t")
    (root / "pkg" / "__init__.py").write_text("", encoding="utf-8")
    (root / "pkg" / "core.py").write_text(_source(), encoding="utf-8")
    (root / "pkg" / "user.py").write_text("from pkg.core import alpha\n", encoding="utf-8")
    _git(root, "add", "-A")
    _git(root, "commit", "-qm", "seed")
    return root


def _compile(root: Path, model: Model, **kw):
    graph = write_scan(root)
    return compile_wiki(root, graph_path=graph, execute=True, generator=model, min_symbols=5,
                        max_calls=0, **kw)


def _commit(root: Path, msg: str) -> None:
    _git(root, "add", "-A")
    _git(root, "commit", "-qm", msg)


PAGE = "pkg-core_py.md"


def test_the_first_compile_writes_full_pages(repo):
    model = Model()
    res = _compile(repo, model)
    assert PAGE in res.generated and res.revised == []
    assert "CURRENT PAGE" not in model.prompts[0]
    assert load_state(repo / "wiki")["pages"][PAGE]["facts_fp"]


def test_a_commit_that_changes_nothing_the_page_describes_rewrites_nothing(repo):
    # regression: the module's git log was part of the page's identity, so this commit — a value far
    # below every excerpt — re-generated the whole page.
    model = Model()
    _compile(repo, model)
    (repo / "pkg" / "core.py").write_text(_source(tail="X_LAST = 1\n"), encoding="utf-8")
    _commit(repo, "touch a constant nobody documents")
    model.prompts.clear()
    res = _compile(repo, model)
    assert res.dirty == [] and model.prompts == []


def test_an_isidore_upgrade_that_rewords_the_prompt_rewrites_nothing(repo, monkeypatch):
    # regression: the template was hashed with the facts, so upgrading isidore dirtied every page
    # of every repository.
    model = Model()
    _compile(repo, model)
    monkeypatch.setattr(pipeline, "MODULE_PROMPT", pipeline.MODULE_PROMPT + "\nBe concise.\n")
    model.prompts.clear()
    assert _compile(repo, model).dirty == [] and model.prompts == []


def test_changed_code_is_revised_section_by_section(repo):
    model = Model()
    _compile(repo, model)
    before = (repo / "wiki" / PAGE).read_text(encoding="utf-8")

    (repo / "pkg" / "core.py").write_text(_source(returns={"gamma": 99}), encoding="utf-8")
    _commit(repo, "gamma returns 99")
    model.revision = ("## Architecture\nTwelve small functions; gamma now returns 99 "
                      "`pkg/core.py:10`.\n\n```isidore-claims\ngamma returns 99 | pkg/core.py:10\n```\n")
    model.prompts.clear()
    res = _compile(repo, model)

    assert res.revised == [PAGE] and res.sections_rewritten == 1
    prompt = model.prompts[0]
    assert "CURRENT PAGE" in prompt and "CHANGED code" in prompt and "return 99" in prompt
    assert "Twelve small functions, each returning a constant." in prompt   # the old text it revises
    after = (repo / "wiki" / PAGE).read_text(encoding="utf-8")
    # the sections the reply did not return are byte-identical; the returned one replaced
    for kept in ("## Purpose\nCore holds the arithmetic helpers `pkg/core.py:1`.",
                 "## How to change safely\nKeep the return values stable; the constants end at"):
        assert kept in before and kept in after
    assert "gamma now returns 99" in after and "each returning a constant" not in after
    # both old claims still anchor (their lines did not change) and ride along at 0 LLM
    claims = {c["statement"] for c in load_state(repo / "wiki")["pages"][PAGE]["claims"]}
    assert claims == {"core defines alpha", "beta returns 1", "gamma returns 99"}
    assert res.claims_carried == 2


def test_a_claim_about_code_that_changed_is_not_carried(repo):
    model = Model()
    _compile(repo, model)
    (repo / "pkg" / "core.py").write_text(_source(returns={"beta": 42}), encoding="utf-8")
    _commit(repo, "beta returns 42")
    res = _compile(repo, model)                      # NO-CHANGES reply
    claims = {c["statement"] for c in load_state(repo / "wiki")["pages"][PAGE]["claims"]}
    assert "beta returns 1" not in claims and "core defines alpha" in claims
    assert res.claims_carried == 1


def test_no_changes_keeps_the_page_and_records_the_new_facts(repo):
    model = Model()
    _compile(repo, model)
    before = (repo / "wiki" / PAGE).read_text(encoding="utf-8")
    (repo / "pkg" / "core.py").write_text(_source(returns={"gamma": 99}), encoding="utf-8")
    _commit(repo, "gamma returns 99")
    res = _compile(repo, model)
    assert res.revised == [PAGE] and res.sections_rewritten == 0
    assert (repo / "wiki" / PAGE).read_text(encoding="utf-8") == before
    model.prompts.clear()
    assert _compile(repo, model).dirty == []         # the new facts were recorded: converged


def test_an_unusable_revision_keeps_the_page_and_leaves_it_pending(repo):
    model = Model()
    _compile(repo, model)
    before = (repo / "wiki" / PAGE).read_text(encoding="utf-8")
    (repo / "pkg" / "core.py").write_text(_source(returns={"gamma": 99}), encoding="utf-8")
    _commit(repo, "gamma returns 99")
    model.revision = "Sure! Here is the updated page, with gamma changed."
    res = _compile(repo, model)
    assert res.revised == [] and PAGE in res.skipped_by_cap
    assert (repo / "wiki" / PAGE).read_text(encoding="utf-8") == before
    assert load_state(repo / "wiki")["pages"][PAGE]["pending"] is True
    assert PAGE in _compile(repo, Model()).dirty     # still owed, not forgotten


def test_rewrite_regenerates_from_scratch_on_request(repo):
    model = Model()
    _compile(repo, model)
    (repo / "pkg" / "core.py").write_text(_source(returns={"gamma": 99}), encoding="utf-8")
    _commit(repo, "gamma returns 99")
    model.prompts.clear()
    res = _compile(repo, model, rewrite=True)
    assert res.revised == [] and PAGE in res.generated
    assert "CURRENT PAGE" not in model.prompts[0]


def test_a_page_from_before_fingerprints_adopts_one_without_a_call(repo):
    model = Model()
    _compile(repo, model)
    import json
    state_path = repo / "wiki" / ".isidore-state.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    for entry in state["pages"].values():           # what every existing wiki looks like today
        entry.pop("facts", None)
        entry.pop("facts_fp", None)
    state_path.write_text(json.dumps(state), encoding="utf-8")
    model.prompts.clear()
    assert _compile(repo, model).dirty == [] and model.prompts == []
    assert load_state(repo / "wiki")["pages"][PAGE]["facts_fp"]


def test_a_carried_claim_keeps_its_id_when_its_line_moves(repo):
    # regression, found on the first real run: a carried claim was re-anchored at its new line and
    # got a NEW id (the id hashes the evidence), which broke the `wiki://page#<id>` chain of the area
    # page above it — subsystem-src.md came back refuted over a two-line shift.
    model = Model()
    _compile(repo, model)
    ids = {c["statement"]: c["id"] for c in load_state(repo / "wiki")["pages"][PAGE]["claims"]}

    shifted = "# a header comment\n# pushed everything down\n\n" + _source(returns={"gamma": 99})
    (repo / "pkg" / "core.py").write_text(shifted, encoding="utf-8")
    _commit(repo, "shift lines and change gamma")
    res = _compile(repo, model)                      # a revision: NO-CHANGES
    assert res.revised == [PAGE]
    after = {c["statement"]: c for c in load_state(repo / "wiki")["pages"][PAGE]["claims"]}
    assert after["core defines alpha"]["evidence"] == "pkg/core.py:4"      # followed the code...
    assert after["core defines alpha"]["id"] == ids["core defines alpha"]  # ...under the same id


def test_a_count_alone_is_not_a_change_and_a_new_rule_never_stampedes(repo):
    # regression, from the first real incremental run: a new test function outside the page's
    # excerpts moved `symbols` 16 -> 17 and bought a call whose only honest answer was NO-CHANGES.
    # And the fingerprint is recomputed on BOTH sides with the current rule, so changing what counts
    # as a change (as this very fix did) does not dirty every stored page.
    import json
    model = Model()
    _compile(repo, model)
    state_path = repo / "wiki" / ".isidore-state.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    entry = state["pages"][PAGE]
    entry["facts"]["symbols"] += 1                   # a count moved
    entry["facts"]["deps_in"] = ["someone/new_caller.py"]   # a new consumer elsewhere
    entry["facts_fp"] = "fingerprint-from-an-older-rule"
    state_path.write_text(json.dumps(state), encoding="utf-8")
    model.prompts.clear()
    assert _compile(repo, model).dirty == [] and model.prompts == []


# ------------------------------------------------------------- splice, banner, carry: the pure parts

OLD = "# svc\n\n## Purpose\nOld purpose.\n\n## Architecture\nOld arch.\n\n## How to change safely\nCare.\n"


def test_splice_replaces_only_the_returned_sections_and_keeps_the_title():
    page, changed = splice(OLD, "## Architecture\nNew arch.\n")
    assert changed == ["Architecture"]
    assert page == "# svc\n\n## Purpose\nOld purpose.\n\n## Architecture\nNew arch.\n\n" \
                   "## How to change safely\nCare.\n"


def test_splice_appends_a_section_the_page_did_not_have():
    page, changed = splice(OLD, "## Gotchas\nWatch the cache.\n")
    assert changed == ["Gotchas"] and page.endswith("## Gotchas\nWatch the cache.\n")
    assert "## Purpose\nOld purpose." in page


def test_splice_treats_no_changes_as_the_old_page_even_with_text_after_it():
    assert splice(OLD, "NO-CHANGES") == (OLD, [])
    assert splice(OLD, "NO-CHANGES\n\nnothing else to add") == (OLD, [])


def test_splice_refuses_a_reply_it_cannot_place():
    assert splice(OLD, "Sure! I updated the architecture section.") is None
    assert splice(OLD, "### Architecture\nWrong heading level.\n") is None


def test_the_old_security_banner_is_removed_before_it_is_rebuilt():
    banner = "> [!WARNING]\n> **SECURITY — flagged.**\n> - `a.py:1` — hardcoded secret\n\n"
    page = "# svc\n\n" + banner + "## Purpose\nText.\n"
    assert strip_security_banner(page) == "# svc\n\n## Purpose\nText.\n"
    assert strip_security_banner(OLD) == OLD                     # no banner: untouched


def test_carry_claims_skips_refuted_and_unanchored_claims(tmp_path):
    from isidore.claims import evidence_hash
    (tmp_path / "m.py").write_text("x = 1\ny = 2\n", encoding="utf-8")
    good = {"id": "c-1", "statement": "x is one", "evidence": "m.py:1",
            "ehash": evidence_hash(tmp_path, "m.py:1"), "verdict": "TRUE", "predicate": "value:x;1"}
    rows = carry_claims(tmp_path, [good, dict(good, id="c-2", verdict="FALSE"),
                                   dict(good, id="c-3", ehash="000000000000"),
                                   dict(good, id="c-4", ehash="")])
    assert rows == [{"statement": "x is one", "evidence": "m.py:1", "id": "c-1",
                     "predicate": "value:x;1"}]


# ------------------------------------------------------------ prose citations follow the code

def _with_line_inserted(at: int, text: str = "X_EXTRA = 0\n", **kw) -> str:
    lines = _source(**kw).splitlines(keepends=True)
    lines.insert(at, text)
    return "".join(lines)


def test_a_citation_follows_its_line_without_touching_the_page(repo):
    # The known limit this closes: a section an incremental compile rightly kept used to keep its
    # old line numbers. A line inserted among the constants — outside every excerpt, so the page's
    # facts do not move and no call is made — shifts the cited `X_100` from :149 to :150.
    model = Model()
    _compile(repo, model)
    (repo / "pkg" / "core.py").write_text(_with_line_inserted(100), encoding="utf-8")
    _commit(repo, "one constant more, above the cited one")
    model.prompts.clear()
    res = _compile(repo, model)
    assert res.dirty == [] and model.prompts == []
    assert res.citations_moved == 1 and res.citations_stale == []
    page = (repo / "wiki" / PAGE).read_text(encoding="utf-8")
    assert "`X_100` (`pkg/core.py:150`)" in page and "pkg/core.py:149" not in page
    from isidore.verify import verify_page
    assert verify_page(repo, repo / "wiki" / PAGE)[0] is True     # the certificate followed too


def test_a_citation_whose_line_changed_is_reported_not_guessed(repo):
    model = Model()
    _compile(repo, model)
    src = _source().replace("X_100 = 100\n", "X_100 = 999\n")
    (repo / "pkg" / "core.py").write_text(src, encoding="utf-8")
    _commit(repo, "the cited constant changed")
    res = _compile(repo, model)
    assert res.citations_moved == 0
    assert res.citations_stale == [f"{PAGE}: pkg/core.py:149"]
    assert "pkg/core.py:149" in (repo / "wiki" / PAGE).read_text(encoding="utf-8")


def test_a_revision_prompt_shows_the_page_with_its_citations_already_repointed(repo):
    # Order matters: re-point first, then revise. Otherwise a NO-CHANGES reply keeps — and re-anchors
    # — citations that drifted.
    model = Model()
    _compile(repo, model)
    (repo / "pkg" / "core.py").write_text(_with_line_inserted(100, returns={"gamma": 99}),
                                          encoding="utf-8")
    _commit(repo, "gamma changes and a constant shifts the cited one")
    model.prompts.clear()
    res = _compile(repo, model)
    assert res.revised == [PAGE]
    assert "`pkg/core.py:150`" in model.prompts[0] and "pkg/core.py:149" not in model.prompts[0]
    assert "`pkg/core.py:150`" in (repo / "wiki" / PAGE).read_text(encoding="utf-8")


def test_a_graph_older_than_the_code_is_said_out_loud(repo):
    # regression: a page recorded against a stale graph came back "changed" the next run with nothing
    # changed — every excerpt window had been placed on old line numbers. Now the run says so.
    import os
    import time
    graph = write_scan(repo)
    old = time.time() - 60
    os.utime(graph, (old, old))
    res = compile_wiki(repo, graph_path=graph, min_symbols=5)
    assert any("older than" in w and "pkg/core.py" in w for w in res.warnings)
    assert not any("older than" in w for w in compile_wiki(
        repo, graph_path=write_scan(repo), min_symbols=5).warnings)


def test_a_run_stopped_at_the_provider_gate_writes_no_citation_either(repo, monkeypatch):
    # regression, from a live round trip: citations were re-pointed on disk BEFORE the provider gate,
    # so a run that then stopped for a missing model left pages moved and their anchors unsaved.
    from isidore.llm import GenerationError
    model = Model()
    _compile(repo, model)
    before = (repo / "wiki" / PAGE).read_text(encoding="utf-8")
    state_before = (repo / "wiki" / ".isidore-state.json").read_text(encoding="utf-8")
    (repo / "pkg" / "core.py").write_text(_with_line_inserted(100, returns={"gamma": 99}),
                                          encoding="utf-8")       # a citation moves AND a page is dirty
    _commit(repo, "shift and change")

    def no_provider():
        raise GenerationError("ISIDORE_MODEL is not set")
    monkeypatch.setattr(pipeline, "default_generator", no_provider)
    with pytest.raises(GenerationError):
        compile_wiki(repo, graph_path=write_scan(repo), execute=True, min_symbols=5, max_calls=0)
    assert (repo / "wiki" / PAGE).read_text(encoding="utf-8") == before
    assert (repo / "wiki" / ".isidore-state.json").read_text(encoding="utf-8") == state_before
