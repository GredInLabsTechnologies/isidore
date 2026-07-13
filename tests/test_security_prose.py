"""Security escalation: a security suspect forces a loud, deterministic prose banner.

Motivated by a live adversarial test — a camouflaged auth backdoor ("internal service shortcut")
was caught in findings as a bug but the prose recommended KEEPING it. The banner is mechanical, so
the prose can no longer soften a security suspect into a feature.
"""
from __future__ import annotations

from isidore.findings import (
    insert_security_banner,
    is_security_finding,
    render_findings,
    security_banner,
    security_suspects,
)

BACKDOOR = {"kind": "bug", "where": "modules/auth/auth.middleware.ts:70",
            "note": 'Hard-coded service token "sk_live_ops_2f9d1a7c" may be a security risk'}


def test_detects_the_camouflaged_backdoor():
    assert is_security_finding(BACKDOOR)


def test_detects_common_security_vocabulary():
    for note in [
        "auth bypass when header is missing",
        "SQL injection in the search query builder",
        "uses eval( on request input",
        "os.system called with unsanitized filename",
        "TLS certificate verification disabled (verify=false)",
        "credential leak: secret written to logs",
        "hardcoded password in the config loader",
    ]:
        assert is_security_finding({"kind": "bug", "where": "x.py:1", "note": note}), note


def test_ignores_non_security_and_wrong_kinds():
    assert not is_security_finding({"kind": "bug", "where": "x.py:1", "note": "lock not released"})
    assert not is_security_finding({"kind": "drift", "where": "r.md:1", "note": "docs say 3, code 1"})
    # security wording but a question/term never escalates (only bug/drift are suspects)
    assert not is_security_finding({"kind": "question", "where": "", "note": "is this a security risk?"})


def test_negation_guard_does_not_escalate_safety_affirming_notes():
    """False-positive regression: a note that CLEARS the code must not raise the banner."""
    for note in [
        "verified this is NOT a hardcoded secret — loaded from process.env",
        "confirmed the token is not hardcoded; read from Vault at runtime",
        "test fixture uses a fake mock password, not a real credential",
        "this eval() is safe: input validated against a strict numeric grammar",
        "documented that TLS verification is NOT disabled here",
        "example only — do not use in production",
    ]:
        assert not is_security_finding({"kind": "bug", "where": "x.ts:1", "note": note}), note


def test_hardcoded_with_intervening_word_is_caught():
    """False-negative regression: 'hardcoded SERVICE token' has a word between hardcoded and token."""
    assert is_security_finding(
        {"kind": "bug", "where": "x.ts:1", "note": "hardcoded service token grants admin without check"})
    assert is_security_finding(
        {"kind": "bug", "where": "x.ts:1", "note": "hard-coded internal api key in the client bundle"})


def test_banner_is_loud_and_lists_evidence():
    banner = security_banner([BACKDOOR])
    assert "[!WARNING]" in banner
    assert "SECURITY" in banner
    assert "auth.middleware.ts:70" in banner
    assert "never as intended features" in banner or "never as intended" in banner.lower() \
        or "VERIFY" in banner


def test_no_banner_without_security_suspects():
    assert security_banner([{"kind": "bug", "where": "x.py:1", "note": "off-by-one"}]) == ""


def test_banner_goes_under_the_h1():
    md = "# modules/auth\n\nThis module authenticates requests.\n"
    out = insert_security_banner(md, security_banner([BACKDOOR]))
    lines = out.splitlines()
    assert lines[0] == "# modules/auth"          # title stays first
    assert any("[!WARNING]" in ln for ln in lines[:6])  # banner right under it
    assert "sk_live_ops_2f9d1a7c" in out


def test_findings_toon_lists_security_first_and_in_summary():
    toon = render_findings([BACKDOOR], [], [], [], [], commit="abc")
    assert "1 SECURITY" in toon
    assert "security[1]" in toon              # a dedicated table
    assert toon.index("security[") < toon.index("suspects[")  # listed first (loud)


def test_security_suspects_filters():
    findings = [BACKDOOR, {"kind": "bug", "where": "x.py:1", "note": "typo"}]
    assert security_suspects(findings) == [BACKDOOR]
