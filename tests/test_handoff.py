"""`isidore handoff` — the caller is the model, so the source never leaves the machine.

Everything here runs with NO provider configured (`ISIDORE_MODEL` is deleted in the fixture): that is
the property under test, not a convenience. The loop exists because on 2026-07-26 a `compile --execute`
against a free tier that trains by default carried 87 prompts of private source out of five repos.

The other half of the contract is that the prose gets no more trust for being yours: it goes through
the same claim anchoring, the same lint gate and the same quarantine as any provider's reply.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from isidore.handoff import (
    MANIFEST,
    PROMPT_SUFFIX,
    REPAIR_MARKER,
    RESPONSE_SUFFIX,
    apply,
    emit,
    handoff_dir,
    prompt_id,
    response_generator,
)
from isidore.llm import GenerationError

PAGE = "## Purpose\nWritten by whoever was already reading the repository.\n"


class _Args:
    """What the CLI hands the functions — deliberately duck-typed, as `getattr(args, ...)` expects."""

    def __init__(self, repo: Path, only: str = "", graph: Path | None = None):
        self.repo = repo
        self.only = only
        self.graph = graph


def _make_repo(tmp_path: Path, n_modules: int = 3) -> Path:
    """Three modules of twelve symbols each — over `min_symbols`, so each earns its own page."""
    repo = tmp_path / "repo"
    nodes, links = [], []
    for m in range(n_modules):
        (repo / f"mod{m}" / "core").mkdir(parents=True)
        for s in range(12):
            src = f"mod{m}/core/file{s}.py"
            (repo / src).write_text(
                "\n".join(f"line {i} of {src}" for i in range(1, 11)), encoding="utf-8")
            nodes.append({"id": f"m{m}_s{s}", "source_file": src, "file_type": "code",
                          "label": f"file{s}.py", "source_location": "L3"})
            links.append({"source": f"m{m}_s{s}", "target": f"m{(m + 1) % n_modules}_s0",
                          "relation": "calls"})
    (repo / "graphify-out").mkdir()
    (repo / "graphify-out" / "graph.json").write_text(
        json.dumps({"nodes": nodes, "links": links, "built_at_commit": "abc123"}), encoding="utf-8")
    return repo


@pytest.fixture()
def repo(tmp_path, monkeypatch):
    """No provider, no key, no network — the loop must work with nothing configured."""
    monkeypatch.delenv("ISIDORE_MODEL", raising=False)
    monkeypatch.delenv("ISIDORE_API_KEY", raising=False)
    return _make_repo(tmp_path)


def _answer_all(repo: Path, body: str = PAGE) -> list[str]:
    """Play the model: write one response beside each prompt. Returns the page names answered."""
    out = handoff_dir(repo)
    names = []
    for prompt_file in sorted(out.glob(f"*{PROMPT_SUFFIX}")):
        name = prompt_file.name[: -len(PROMPT_SUFFIX)]
        (out / f"{name}{RESPONSE_SUFFIX}").write_text(body, encoding="utf-8")
        names.append(name)
    return names


# ------------------------------------------------------------------------------- emit

def test_emit_writes_one_prompt_per_dirty_page_and_calls_nothing(repo):
    count, names = emit(repo, {}, _Args(repo))

    out = handoff_dir(repo)
    assert count == 3 and names == ["mod0-core.md", "mod1-core.md", "mod2-core.md"]
    assert len(list(out.glob(f"*{PROMPT_SUFFIX}"))) == 3
    # emit is a PLAN: not a single page, index or state file exists yet
    assert not list((repo / "wiki").glob("*.md"))
    for name in names:
        assert (out / f"{name}{PROMPT_SUFFIX}").read_text(encoding="utf-8").strip()


def test_the_manifest_keys_prompts_by_their_content(repo):
    emit(repo, {}, _Args(repo))
    out = handoff_dir(repo)
    manifest = json.loads((out / MANIFEST).read_text(encoding="utf-8"))

    assert len(manifest) == 3
    for key, name in manifest.items():
        prompt = (out / f"{name}{PROMPT_SUFFIX}").read_text(encoding="utf-8")
        assert prompt_id(prompt) == key


def test_prompt_id_is_content_identity():
    assert prompt_id("same") == prompt_id("same")
    assert prompt_id("same") != prompt_id("same ")
    assert len(prompt_id("x")) == 16
    assert int(prompt_id("x"), 16) >= 0            # hex, so it survives a JSON round-trip as a key


def test_the_call_cap_belongs_to_whoever_answers(repo):
    """A provider's budget bounds spend. There is no spend here, so a cap would only hide work: the
    emitted set is every dirty page, whatever `max_calls` the config carries for compiles."""
    count, _names = emit(repo, {"max_calls": 1}, _Args(repo))
    assert count == 3


def test_only_scopes_the_prompts(repo):
    count, names = emit(repo, {}, _Args(repo, only="mod1/core"))
    assert count == 1 and names == ["mod1-core.md"]


def test_nothing_dirty_emits_nothing(repo):
    emit(repo, {}, _Args(repo))
    _answer_all(repo)
    apply(repo, {}, _Args(repo))

    count, names = emit(repo, {}, _Args(repo))
    assert count == 0 and names == []


def test_a_page_that_is_no_longer_dirty_leaves_no_answerable_prompt(repo):
    """Otherwise the next `apply` certifies a page nobody asked about, from an answer written against
    an older repository — the stale-answer refusal below would never even get a chance to fire."""
    emit(repo, {}, _Args(repo))
    _answer_all(repo)
    apply(repo, {}, _Args(repo))

    emit(repo, {}, _Args(repo))                      # second round: clean tree, nothing dirty
    out = handoff_dir(repo)
    assert list(out.glob(f"*{PROMPT_SUFFIX}")) == []
    assert list(out.glob(f"*{RESPONSE_SUFFIX}")) == []


# ------------------------------------------------------------------------------ apply

def test_apply_writes_the_pages_through_the_ordinary_pipeline(repo):
    emit(repo, {}, _Args(repo))
    answered = _answer_all(repo)

    result = apply(repo, {}, _Args(repo))

    assert sorted(result.generated) == sorted(answered)
    wiki = repo / "wiki"
    for name in answered:
        assert (wiki / name).is_file()
    # the rest of the pipeline ran too — this is not a special-cased write path
    for name in ("quickstart.md", "index.toon", ".isidore-state.json"):
        assert (wiki / name).is_file(), name


def test_claims_written_by_hand_are_anchored_like_anyone_elses(repo):
    emit(repo, {}, _Args(repo))
    body = (
        "## Purpose\nText.\n\n"
        "```isidore-claims\n"
        "file0 is not thread-safe | mod0/core/file0.py:3\n"           # behavioural -> anchored
        "There is no retry logic here | mod0/core/file0.py:3\n"       # absence -> dropped by construction
        "```\n"
    )
    _answer_all(repo, body)

    result = apply(repo, {}, _Args(repo))

    assert result.claims_total == 3                       # one kept per page, three pages
    assert result.claims_dropped_negative == 3            # and one dropped per page
    cert = json.loads((repo / "wiki" / "mod0-core.md.cert.json").read_text(encoding="utf-8"))
    assert cert["claims"], "the hand-written claim carries a certificate like any other"


def test_a_phantom_citation_is_quarantined_not_aborted(repo):
    """The lint gate asks a provider for one repair round. There is nobody to ask here — the answer is
    already written — so the round must resolve into the ORDINARY outcome (annotated inline, page
    quarantined) instead of blowing up the whole apply and losing every other page with it."""
    emit(repo, {}, _Args(repo))
    _answer_all(repo, "## Purpose\nUses `fake/dir/ghost.py`.\n")

    result = apply(repo, {}, _Args(repo))

    assert sorted(result.quarantined) == ["mod0-core.md", "mod1-core.md", "mod2-core.md"]
    page = (repo / "wiki" / "mod0-core.md").read_text(encoding="utf-8")
    assert "[⚠ isidore: path not found]" in page
    state = json.loads((repo / "wiki" / ".isidore-state.json").read_text(encoding="utf-8"))
    assert state["pages"]["mod0-core.md"]["quarantined"] is True


# ------------------------------------------------------------- refusing what cannot be trusted

def test_a_stale_answer_is_refused_not_certified(repo):
    """The facts moved under the answer. Certifying it would publish prose about a repository that no
    longer looks like this — and the certificate would say it verified."""
    emit(repo, {}, _Args(repo, only="mod1/core"))
    _answer_all(repo)

    target = repo / "mod1" / "core" / "file0.py"
    target.write_text(target.read_text(encoding="utf-8").replace("line 3", "CHANGED 3"),
                      encoding="utf-8")

    with pytest.raises(GenerationError, match="repository changed"):
        apply(repo, {}, _Args(repo, only="mod1/core"))
    assert not (repo / "wiki" / "mod1-core.md").exists()


def test_a_longer_prompt_that_merely_starts_the_same_is_still_refused(repo):
    """The repair round is recognised by a prefix match, and a prefix match alone would be a hole:
    facts appended to a page's context make a prompt that STARTS with the answered one. Only the
    gate's own addendum may follow — anything else is a repository that moved."""
    emit(repo, {}, _Args(repo, only="mod0/core"))
    _answer_all(repo)
    answered = handoff_dir(repo).joinpath(f"mod0-core.md{PROMPT_SUFFIX}").read_text(encoding="utf-8")
    generate = response_generator(repo)

    assert generate(answered) == PAGE.strip()                           # the answered prompt
    assert generate(answered + REPAIR_MARKER + "\n  - ghost.py\n") == PAGE.strip()   # its repair round
    with pytest.raises(GenerationError, match="repository changed"):
        generate(answered + "\n\n--- excerpt mod0/core/file12.py ---\n1: brand new\n")


def test_a_missing_answer_names_the_page(repo):
    emit(repo, {}, _Args(repo, only="mod0/core"))

    with pytest.raises(GenerationError, match="mod0-core.md"):
        apply(repo, {}, _Args(repo, only="mod0/core"))


def test_an_empty_answer_is_refused(repo):
    emit(repo, {}, _Args(repo, only="mod0/core"))
    handoff_dir(repo).joinpath(f"mod0-core.md{RESPONSE_SUFFIX}").write_text("   \n", encoding="utf-8")

    with pytest.raises(GenerationError, match="empty"):
        apply(repo, {}, _Args(repo, only="mod0/core"))


def test_apply_before_emit_says_to_emit_first(repo):
    with pytest.raises(GenerationError, match="handoff emit"):
        response_generator(repo)


# ---------------------------------------------------------------------------------- CLI

def test_the_cli_round_trip_needs_no_provider(repo, capsys, monkeypatch):
    from isidore.cli import main

    monkeypatch.chdir(repo)
    assert main(["handoff", "emit", "--repo", str(repo)]) == 0
    assert "0 LLM, 0 network" in capsys.readouterr().out

    _answer_all(repo)
    assert main(["handoff", "apply", "--repo", str(repo)]) == 0
    out = capsys.readouterr().out
    assert "applied 3 page(s)" in out
    assert (repo / "wiki" / "mod0-core.md").is_file()


def test_the_cli_reports_nothing_dirty_instead_of_inventing_work(repo, capsys):
    from isidore.cli import main

    main(["handoff", "emit", "--repo", str(repo)])
    _answer_all(repo)
    main(["handoff", "apply", "--repo", str(repo)])
    capsys.readouterr()

    assert main(["handoff", "emit", "--repo", str(repo)]) == 0
    assert "nothing dirty" in capsys.readouterr().out


def test_the_cli_fails_closed_on_a_missing_answer(repo, capsys):
    from isidore.cli import main

    main(["handoff", "emit", "--repo", str(repo)])
    capsys.readouterr()

    assert main(["handoff", "apply", "--repo", str(repo)]) == 2
    assert "ERROR" in capsys.readouterr().out
