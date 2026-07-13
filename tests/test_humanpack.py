"""Lane E gate — the human pack renders from golden artifacts, is deterministic, and is 0-LLM."""
from __future__ import annotations

import re
from pathlib import Path

from isidore.humanpack import render_pack

WIKI = Path(__file__).parent / "fixtures" / "pcp" / "repo" / "wiki"


def test_render_pack_content(tmp_path):
    index = render_pack(WIKI, tmp_path / "pack")
    assert index.is_file()
    html = index.read_text(encoding="utf-8")
    # the page and the reading path
    assert "svc.md" in html
    # the legend, in all three confidence classes
    assert "proved against the code" in html
    assert "anchored (existence)" in html
    assert "narrative, not load-bearing" in html
    # the security banner text for the entropy mark (real reason from the golden cert)
    assert "high-entropy credential literal" in html
    # a claim statement made it into the claims table
    assert "authenticate verifies the JWT" in html
    # the promoted contract shows up
    assert "calls:authenticate;verify_jwt" in html


def test_render_pack_is_deterministic(tmp_path):
    a = render_pack(WIKI, tmp_path / "a").read_bytes()
    b = render_pack(WIKI, tmp_path / "b").read_bytes()
    assert a == b


def test_pdf_flag_writes_print_html(tmp_path):
    out = tmp_path / "pack"
    render_pack(WIKI, out, pdf=True)
    assert (out / "print.html").is_file()
    assert "@page" in (out / "index.html").read_text(encoding="utf-8")


def test_humanpack_does_not_import_llm():
    """I12: the renderer must be 0-LLM. Guard it at the source level."""
    src = Path(__file__).parent.parent / "src" / "isidore" / "humanpack.py"
    text = src.read_text(encoding="utf-8")
    assert not re.search(r"^\s*(from|import)\s+.*\bllm\b", text, re.MULTILINE)
