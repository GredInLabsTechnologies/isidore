from __future__ import annotations


from isidore.findings import is_security_finding
from isidore import reconcile


def test_adversarial_backdoor_detection():
    """Vigil case: A camouflaged auth backdoor reported in findings but justified by prose."""
    finding = {
        "kind": "bug",
        "where": "src/auth/middleware.py:42",
        "note": "Hard-coded service token 'sk_live_ops_2f9d1a7c' is a security risk"
    }
    
    # 1. Ensure it is recognized as a security finding
    assert is_security_finding(finding)
    
    # 2. Reconciler must detect contradiction because prose describes it in positive/secure terms
    prose = (
        "# Auth Module\n\n"
        "An internal service shortcut is implemented in src/auth/middleware.py. "
        "This shortcut is fully secure and safe to keep for operations."
    )
    
    violations = reconcile.reconcile(prose, [finding], [])
    assert len(violations) >= 1
    assert any(v.kind == "prose-contradicts-finding" for v in violations)


def test_negations_false_positives():
    """Verify that negation patterns do not trigger false positive security findings (6 cases)."""
    negation_cases = [
        "verified this is NOT a hardcoded secret — loaded from process.env",
        "confirmed the token is not hardcoded; read from Vault at runtime",
        "test fixture uses a fake mock password, not a real credential",
        "this eval() is safe: input validated against a strict numeric grammar",
        "documented that TLS verification is NOT disabled here",
        "example only — do not use in production"
    ]
    for note in negation_cases:
        finding = {"kind": "bug", "where": "src/auth/middleware.py:42", "note": note}
        assert not is_security_finding(finding), f"False Positive triggered for: {note}"


def test_false_negative_intervening_words():
    """Verify that safety-checks catch risks even with intermediate/intervening words."""
    intervening_cases = [
        "hardcoded service token grants admin access",
        "hard-coded internal api key is exposed",
        "hardcoded oauth client credential secret"
    ]
    for note in intervening_cases:
        finding = {"kind": "bug", "where": "src/auth/middleware.py:42", "note": note}
        assert is_security_finding(finding), f"False Negative triggered for: {note}"


def test_vigil_impossible_to_clean_by_model():
    """If the model attempts social engineering in prose while findings report the bug,

    reconcile MUST trigger a violation, preventing the page from compiling silently.
    """
    findings = [{"kind": "bug", "where": "src/auth/middleware.py:42", "note": "hardcoded secret bypasses auth"}]
    prose = "The src/auth/middleware.py endpoint is safe because it only accepts trusted internal bypass calls."
    claims = []
    
    violations = reconcile.reconcile(prose, findings, claims)
    assert len(violations) == 1
    assert violations[0].kind == "prose-contradicts-finding"
