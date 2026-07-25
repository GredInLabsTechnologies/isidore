"""The plain-language gate: named rules, one-sided verdicts, and the formula it deliberately lacks."""
from __future__ import annotations

from isidore.plain import RULES, check, explain, is_plain


def test_a_sentence_written_for_a_person_passes():
    assert is_plain(
        "Saving a group of records can now be made conditional, so two people editing at the same "
        "time no longer overwrite each other's work.")
    assert is_plain("Nothing was taken away, so anything already built on this keeps working.")


def test_each_rule_names_the_reason_it_fired():
    assert check("The method takes a new parameter.") == ["jargon-term"]
    assert check("Call put_many_conditional to save.") == ["snake-case"]
    assert check("Use putManyConditional instead.") == ["camel-case"]
    assert check("It lives in client.py now.") == ["file-name"]
    assert check("See the change at line client:295 for details.") == ["line-reference"]
    assert check("The handler now returns {} on failure.") == ["code-syntax"]


def test_a_rejection_can_be_explained_to_whoever_wrote_it():
    reason = explain(check("The daemon exposes a new endpoint."))
    assert "jargon-term" in reason
    assert "someone who builds software" in reason


def test_case_insensitivity_is_scoped_to_the_vocabulary_rule():
    # The bug this guards: `(?i)` across the whole rule set turns the camelCase pattern `[a-z][A-Z]`
    # into "any two letters", which rejected every sentence ever written — including good ones.
    assert check("Method calls are slow.") == ["jargon-term"]      # capitalised term still caught
    assert is_plain("Saving records is faster.")                    # ...and normal prose survives


def test_the_gate_is_one_sided_and_carries_no_readability_score():
    # ISO 24495-1 judges plain language by whether the reader can use the document, NOT by a
    # readability formula. A short jargon sentence must fail; a long plain one must pass.
    assert not is_plain("The API returns a payload.")               # short, scores "easy", fails
    assert is_plain(
        "When two people happen to save their changes at the very same moment, the second save is "
        "now refused instead of quietly replacing the first one, so no work is lost without anyone "
        "noticing it happened.")                                    # long, scores "hard", passes


def test_every_rule_declares_a_kind_and_a_reason():
    for rule in RULES:
        assert rule.kind in ("vocabulary", "structure")
        assert rule.why and not rule.why.endswith(".")
