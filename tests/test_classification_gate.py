"""Ingesting a source does not authorise sending it to a third party.

Found by running it: a topic over the collective's own notebook put 25 Library cards marked
`classification: internal`, plus private messages and the whole task history, into a prompt bound for
a hosted API. Nothing in the pipeline objected, because nothing was looking. The invariant reads in
both directions — external content is data and never instruction (I8), and internal content is
evidence and never someone else's training input.
"""
from __future__ import annotations

import pytest

from isidore.connectors.store import (
    create_run_id,
    iso_now,
    read_state,
    record_run,
    write_items,
    write_state,
)
from isidore.knowledge import (
    _SENSITIVE_ENV,
    assemble_topic_context,
    compile_topics,
    item_classification,
    provider_is_trusted,
)


@pytest.fixture()
def home(tmp_path, monkeypatch):
    monkeypatch.setenv("ISIDORE_HOME", str(tmp_path / "home"))
    monkeypatch.delenv(_SENSITIVE_ENV, raising=False)
    return tmp_path


def _store(items: list[dict]) -> None:
    run_id = create_run_id()
    path = write_items("agora", "", run_id, items)
    state = read_state("agora", "")
    record_run(state, {"run_id": run_id, "at": iso_now(), "status": "success",
                       "raw_files": [path], "items": len(items)})
    write_state("agora", "", state)


def _item(ident: str, content: str, classification: str | None = None) -> dict:
    meta = {"classification": classification} if classification else {}
    return {"id": ident, "stream": "notes", "ts": "2026-07-26T00:00:00Z", "content": content,
            "meta": meta}


# ------------------------------------------------------------------ reading the label

def test_the_label_comes_from_meta_first_then_the_document_itself():
    assert item_classification(_item("a", "x", "internal")) == "internal"
    assert item_classification(_item("a", "x", "PUBLIC")) == "public"       # normalised

    # A Library card declares it in its own front matter, and no connector had to be taught about it.
    card = _item("b", "---\nid: c\nclassification: internal\ntitle: T\n---\n\nBody.\n")
    assert item_classification(card) == "internal"

    assert item_classification(_item("c", "no front matter here")) == "public"


def test_the_trust_declaration_takes_an_exact_word(monkeypatch):
    """A truthy-looking value is not a decision. This one deserves to be made deliberately."""
    for value in ("", "0", "no", "true", "1", "YES please"):
        monkeypatch.setenv(_SENSITIVE_ENV, value)
        assert provider_is_trusted() is False
    for value in ("yes", "YES", " yes "):
        monkeypatch.setenv(_SENSITIVE_ENV, value)
        assert provider_is_trusted() is True


# ------------------------------------------------------------------ the gate

@pytest.mark.usefixtures("home")
def test_restricted_items_never_reach_the_prompt_by_default():
    _store([_item("pub-1", "A public note."),
            _item("int-1", "A private one.", "internal"),
            _item("sec-1", "A secret one.", "secret")])

    ctx, warnings = assemble_topic_context({"name": "t", "streams": ["notes"], "top_k_items": 10})

    assert "A public note." in ctx
    assert "A private one." not in ctx and "A secret one." not in ctx
    note = next(w for w in warnings if "withheld" in w)
    assert "2 item(s)" in note and "1 internal" in note and "1 secret" in note
    assert _SENSITIVE_ENV in note                    # and it says exactly how to opt in


@pytest.mark.usefixtures("home")
def test_an_explicit_declaration_lets_them_through_and_is_recorded(monkeypatch):
    _store([_item("int-1", "A private one.", "internal")])
    monkeypatch.setenv(_SENSITIVE_ENV, "yes")

    ctx, warnings = assemble_topic_context({"name": "t", "streams": ["notes"], "top_k_items": 10})

    assert "A private one." in ctx
    # Consent is not silence: the run states that restricted material WAS sent, so it appears in the
    # log of whoever has to answer for it later.
    assert any("WERE sent to the configured provider" in w for w in warnings)


@pytest.mark.usefixtures("home")
def test_withholding_does_not_starve_a_topic_that_has_public_material():
    """The cap is per-item, not per-topic: one restricted item must not blank the whole page."""
    _store([_item(f"pub-{i}", f"Public note {i}.") for i in range(3)]
           + [_item("int-1", "Private.", "internal")])

    ctx, _warnings = assemble_topic_context({"name": "t", "streams": ["notes"], "top_k_items": 10})
    assert ctx.count("Public note") == 3


@pytest.mark.usefixtures("home")
def test_top_k_counts_what_survived_not_what_was_filtered():
    # Applying top_k before the filter would let restricted items eat the budget and leave a page
    # thinner than its own configuration asked for.
    _store([_item(f"int-{i}", f"Private {i}.", "internal") for i in range(5)]
           + [_item(f"pub-{i}", f"Public note {i}.") for i in range(3)])

    ctx, _warnings = assemble_topic_context({"name": "t", "streams": ["notes"], "top_k_items": 3})
    assert ctx.count("Public note") == 3


# ------------------------------------------------------------------ nothing to say, nothing to write

@pytest.mark.usefixtures("home")
def test_a_topic_with_no_facts_left_is_not_compiled_from_its_own_name():
    """Seen the moment the gate started withholding: three topics with nothing left to say still
    produced three confident pages. Prose invented from a topic NAME is the one thing this design
    exists to prevent."""
    from isidore.home import home as knowledge_home

    _store([_item("int-1", "Private.", "internal")])
    (knowledge_home() / "topics.json").write_text(
        '[{"name": "private-topic", "streams": ["notes"], "top_k_items": 5}]', encoding="utf-8")

    calls: list[str] = []

    def generator(prompt):
        calls.append(prompt)
        return "## Overview\nConfident prose about a topic I know nothing about.\n"

    result = compile_topics(execute=True, max_calls=5, generator=generator)

    assert calls == []                                   # no call was made...
    assert result.generated == []                        # ...and no page was written
    assert not (knowledge_home() / "knowledge" / "private-topic.md").is_file()
    assert any("no facts available" in w for w in result.warnings)
