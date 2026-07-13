"""Lane A gate — the typed-claim verifiers decide truth against the two oracles, build a certificate
that matches the golden expectations, and re-verify offline (tamper-evident). Golden fixtures."""
from __future__ import annotations

from pathlib import Path

from isidore.claims import anchor_claims, parse_claims_block, parse_predicate_field
from isidore.graph import load_graph
from isidore.pcp import FALSE, TRUE, UNDECIDABLE, VerifyContext, prose_hash, verify_predicate
from isidore.verify import build_certificate, classify_mass, ground_symbols, verify_page

FIX = Path(__file__).parent / "fixtures" / "pcp"
REPO = FIX / "repo"


def _ctx() -> VerifyContext:
    nodes, links, commit = load_graph(FIX / "graph.json")
    return VerifyContext(repo=REPO, nodes=nodes, links=links, commit=commit)


def _anchored():
    md = (REPO / "wiki" / "svc.md").read_text(encoding="utf-8")
    _clean, rows = parse_claims_block(md)
    anchored, _d, _r = anchor_claims(REPO, rows)
    return anchored


def test_three_field_parser_captures_predicate():
    _clean, rows = parse_claims_block(
        "```isidore-claims\nx does y | a.py:1 | calls:x;y\nz | b.py:2\n```\n")
    assert rows[0]["predicate"] == "calls:x;y"
    assert "predicate" not in rows[1]          # two-field stays existence-anchored


def test_each_predicate_kind_decides_correctly():
    ctx = _ctx()
    cases = {
        "calls:authenticate;verify_jwt": TRUE,
        "value:MAX_ATTEMPTS;5": TRUE,
        "imports:svc/auth.py;svc/tokens.py": TRUE,
        "env:AUTH_SIGNING_KEY": TRUE,
        "defines:svc/auth.py;authenticate": TRUE,
        "calls:authenticate;nonexistent_fn": FALSE,
        "value:MAX_ATTEMPTS;999": FALSE,
        "imports:svc/auth.py;svc/nowhere.py": UNDECIDABLE,  # partial graph -> can't assert absence
        "signature:authenticate;request": TRUE,
        "route:GET /x;handler": UNDECIDABLE,     # honest: no framework extractor
    }
    for raw, expected in cases.items():
        v = verify_predicate(parse_predicate_field(raw), ctx)
        assert v.value == expected, f"{raw}: got {v.value} ({v.detail})"


def test_certificate_matches_golden_verdicts():
    cert = build_certificate("svc.md", (REPO / "wiki" / "svc.md").read_text(encoding="utf-8"),
                             _anchored(), _ctx())
    by_pred = {c.predicate: c.verdict for c in cert.claims if c.predicate}
    assert by_pred["calls:authenticate;verify_jwt"] == TRUE
    assert by_pred["value:MAX_ATTEMPTS;5"] == TRUE
    assert by_pred["imports:svc/auth.py;svc/tokens.py"] == TRUE
    assert by_pred["env:AUTH_SIGNING_KEY"] == TRUE
    assert by_pred["defines:svc/auth.py;authenticate"] == TRUE
    # the existence-anchored claim (no predicate) stays UNDECIDABLE
    assert any(c.predicate == "" and c.verdict == UNDECIDABLE for c in cert.claims)
    assert len(cert.prose_sha256) == 64


def test_imports_and_value_fail_closed_to_undecidable_not_false():
    """Dogfood regression: the graph's import edges are partial and `value` can't compare non-literals,
    so neither may assert absence (FALSE would discredit a real fact). They degrade to UNDECIDABLE."""
    ctx = _ctx()
    # an import the (partial) graph doesn't carry -> UNDECIDABLE, not FALSE
    v = verify_predicate(parse_predicate_field("imports:svc/auth.py;os"), ctx)
    assert v.value == UNDECIDABLE
    # a real import the graph DOES carry still proves TRUE
    assert verify_predicate(parse_predicate_field(
        "imports:svc/auth.py;svc/tokens.py"), ctx).value == TRUE
    # value against a symbol assigned a non-literal cannot be refuted -> UNDECIDABLE
    v2 = verify_predicate(parse_predicate_field("value:authenticate;5"), ctx)
    assert v2.value == UNDECIDABLE
    # but a real literal mismatch is still FALSE (the oracle is complete for a literal)
    assert verify_predicate(parse_predicate_field("value:MAX_ATTEMPTS;999"), ctx).value == FALSE


def test_symbol_grounding_catches_a_hallucinated_identifier():
    ctx = _ctx()
    # requirePlanOrRole is a plausible mash-up that resolves to nothing in the graph
    unresolved = ground_symbols("The `requirePlanOrRole` guard wraps `authenticate`.", ctx)
    assert "requirePlanOrRole" in unresolved
    assert "authenticate" not in unresolved     # this one is real


def test_verified_mass_classifies_sentences():
    from isidore.pcp import ClaimVerdict
    claims = [ClaimVerdict("c1", "authenticate verifies the JWT", "svc/auth.py:14", "h",
                           "calls:authenticate;verify_jwt", TRUE, "ast")]
    mass = classify_mass("authenticate verifies the JWT here. This is unrelated prose.", claims)
    assert mass.green == 1 and mass.gray == 1


def test_verify_page_tamper_evidence(tmp_path):
    # a compiled page + its certificate: verify_page is True; editing the prose breaks it
    wiki = tmp_path / "wiki"
    wiki.mkdir()
    page = wiki / "svc.md"
    md = (REPO / "wiki" / "svc.md").read_text(encoding="utf-8")
    page.write_text(md, encoding="utf-8")
    # build + persist a cert against a graph copied where find_graph will see it
    isidore_dir = tmp_path / ".isidore"
    isidore_dir.mkdir()
    (isidore_dir / "graph.json").write_text((FIX / "graph.json").read_text(), encoding="utf-8")
    # source files must exist relative to repo=tmp_path for the AST oracles
    (tmp_path / "svc").mkdir()
    for f in ("auth.py", "tokens.py"):
        (tmp_path / "svc" / f).write_text((REPO / "svc" / f).read_text(encoding="utf-8"),
                                          encoding="utf-8")
    from isidore.pcp import write_certificate
    nodes, links, commit = load_graph(isidore_dir / "graph.json")
    ctx = VerifyContext(repo=tmp_path, nodes=nodes, links=links, commit=commit)
    clean, rows = parse_claims_block(md)
    anchored, _d, _r = anchor_claims(tmp_path, rows)
    cert = build_certificate("svc.md", md, anchored, ctx)
    cert.prose_sha256 = prose_hash(clean)      # cert anchors the CLEAN prose (claims block stripped)
    write_certificate(cert, wiki / "svc.md.cert.json")

    ok, _c = verify_page(tmp_path, page)
    assert ok is True
    # tamper: append a lie to the prose
    page.write_text(md + "\n\nThis line was injected after compile.\n", encoding="utf-8")
    ok2, _c2 = verify_page(tmp_path, page)
    assert ok2 is False
