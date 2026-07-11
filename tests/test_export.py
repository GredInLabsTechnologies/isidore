"""export-agora: verified claims -> Living-Library card DRAFTS, with the verify_cmd audit bridge."""
from __future__ import annotations

from isidore.export import build_cards, write_cards
from isidore.graph import write_scan
from isidore.pipeline import compile_wiki


def _repo(tmp_path):
    repo = tmp_path / "repo"
    (repo / "auth").mkdir(parents=True)
    (repo / "auth" / "__init__.py").write_text("", encoding="utf-8")
    pad = "\n".join(f"# pad {i}" for i in range(15))
    (repo / "auth" / "login.py").write_text(
        f"def verify_token():\n    return True\n{pad}\n", encoding="utf-8")
    gp = write_scan(repo)
    page = ("## Purpose\nAuth.\n\n```isidore-claims\n"
            "verify_token returns a boolean session decision | auth/login.py:1\n```\n")
    compile_wiki(repo, graph_path=gp, execute=True, min_symbols=1, generator=lambda p: page)
    return repo, gp


def test_export_builds_draft_cards_with_verify_cmd(tmp_path):
    repo, _gp = _repo(tmp_path)
    cards = build_cards(repo, domain="security")
    assert cards
    name, content = cards[0]
    assert name.startswith("isidore-") and name.endswith(".md")
    assert "verify_cmd: isidore claims --check" in content     # the audit bridge
    assert "domain: security" in content
    assert "verify_token returns a boolean session decision" in content
    assert "DRAFT" in content                                  # clearly a draft, never auto-posted


def test_export_writes_files_and_skips_when_no_claims(tmp_path):
    repo, _gp = _repo(tmp_path)
    out = tmp_path / "cards"
    written = write_cards(build_cards(repo), out)
    assert written and all(p.exists() for p in written)
    # a repo with no compiled claims yields nothing
    empty = tmp_path / "empty"
    (empty / "m").mkdir(parents=True)
    (empty / "m" / "__init__.py").write_text("", encoding="utf-8")
    (empty / "m" / "z.py").write_text("def f():\n    return 1\n", encoding="utf-8")
    gp2 = write_scan(empty)
    compile_wiki(empty, graph_path=gp2, execute=True, min_symbols=1, generator=lambda p: "## Purpose\nno claims\n")
    assert build_cards(empty) == []


def test_only_ok_claims_are_exported_by_default(tmp_path):
    # drift the cited code -> the claim goes stale -> it is excluded from cards by default (only
    # verified facts become library cards); the verify_cmd would fail an audit for a posted card.
    repo, _gp = _repo(tmp_path)
    from isidore.claims import check_claims
    from isidore.pipeline import WIKI_DIRNAME, load_state
    login = repo / "auth" / "login.py"
    # the claim is anchored to line 1 (the def). Change that exact line -> content anchor breaks.
    login.write_text(login.read_text(encoding="utf-8").replace(
        "def verify_token():", "def verify_token(session, *, strict=True):"), encoding="utf-8")
    state = load_state(repo / WIKI_DIRNAME)
    assert any(r["state"] != "ok" for r in check_claims(repo, state.get("pages", {})))  # now stale
    assert build_cards(repo) == []                              # stale claim not exported
    assert build_cards(repo, include_stale=True)                # unless explicitly asked
