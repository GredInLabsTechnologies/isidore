from __future__ import annotations

from pathlib import Path

from isidore import reconcile
from isidore.pcp import Mark


def test_pure_reconcile_imports_constraint():
    """Ensure reconcile.py does not import pipeline, claims, or verify (frozen boundary constraint)."""
    with open(Path(reconcile.__file__), encoding="utf-8") as f:
        content = f.read()
    # Check for direct import patterns
    assert "import pipeline" not in content
    assert "from .pipeline" not in content
    assert "import claims" not in content
    assert "from .claims" not in content
    assert "import verify" not in content
    assert "from .verify" not in content


def test_reconcile_prose_omits_finding():
    findings = [{"kind": "bug", "where": "svc/auth.py:23", "note": "hardcoded secret"}]
    claims = []
    
    # 1. Omitted: prose does not contain the file path
    violations = reconcile.reconcile("This is unrelated documentation.", findings, claims)
    assert len(violations) == 1
    assert violations[0].kind == "prose-omits-finding"
    assert violations[0].where == "svc/auth.py:23"
    
    # 2. Included: prose contains the path
    violations = reconcile.reconcile("Check out svc/auth.py for details.", findings, claims)
    assert len(violations) == 0


def test_reconcile_prose_contradicts_finding_via_prose_denial():
    findings = [{"kind": "bug", "where": "svc/auth.py:23", "note": "hardcoded secret sk_live_"}]
    
    # 1. Contradicts: prose states secrets are never hard-coded
    violations = reconcile.reconcile(
        "svc/auth.py: secrets are read from the environment, never hardcoded.",
        findings, []
    )
    assert len(violations) == 1
    assert violations[0].kind == "prose-contradicts-finding"
    
    # 2. No contradiction: prose does not make safety claim
    violations = reconcile.reconcile(
        "svc/auth.py handles the configuration.",
        findings, []
    )
    assert len(violations) == 0


def test_reconcile_prose_contradicts_finding_via_positive_claim():
    findings = [{"kind": "bug", "where": "svc/auth.py:10", "note": "auth bypass risk"}]
    
    # 1. Contradicts: claim in the same region is positive
    claims = [{"statement": "authenticate verifies the JWT and is safe", "evidence": "svc/auth.py:12"}]
    violations = reconcile.reconcile("svc/auth.py", findings, claims)
    assert len(violations) == 1
    assert violations[0].kind == "prose-contradicts-finding"
    assert "verifies the JWT" in violations[0].detail

    # 2. No contradiction: claim is too far (offset > 5 lines)
    claims_far = [{"statement": "authenticate verifies the JWT and is safe", "evidence": "svc/auth.py:20"}]
    violations = reconcile.reconcile("svc/auth.py", findings, claims_far)
    assert len(violations) == 0


def test_reconcile_mark_uncovered():
    marks = [Mark(family="entropy", file="svc/auth.py", line=23, reason="sk_live_", severity="danger")]
    
    # 1. Uncovered
    violations = reconcile.reconcile("svc/auth.py", [], [], marks=marks)
    assert len(violations) == 1
    assert violations[0].kind == "mark-uncovered"
    assert violations[0].where == "svc/auth.py:23"
    
    # 2. Covered by claim within 5 lines
    claims = [{"statement": "credential handling", "evidence": "svc/auth.py:21"}]
    violations = reconcile.reconcile("svc/auth.py", [], claims, marks=marks)
    assert len(violations) == 0
    
    # 3. Mark with 'info' severity is ignored
    info_marks = [Mark(family="sink", file="svc/auth.py", line=23, reason="read", severity="info")]
    violations = reconcile.reconcile("svc/auth.py", [], [], marks=info_marks)
    assert len(violations) == 0


def test_reconcile_ignores_resolved_findings():
    findings = [{"kind": "bug", "where": "svc/auth.py:23", "note": "hardcoded sk_live_", "resolved": True}]
    violations = reconcile.reconcile("secrets are never hardcoded in svc/auth.py", findings, [])
    assert len(violations) == 0
