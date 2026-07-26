"""llms.txt: the wiki handed to an agent in the shape the ecosystem converged on. 0 LLM."""
from __future__ import annotations

from isidore.render import LLMS_FILENAME, render_llms_txt, write_llms_txt


def _wiki(tmp_path):
    root = tmp_path / "proj"
    wiki = root / "wiki"
    wiki.mkdir(parents=True)
    (wiki / "overview.md").write_text(
        "# proj\n\n## What this is\nIt keeps a project's guide honest and current.\n",
        encoding="utf-8")
    (wiki / "subsystem-core.md").write_text("## What this area is responsible for\nx\n",
                                            encoding="utf-8")
    (wiki / "src-core.md").write_text("## Purpose\ny\n", encoding="utf-8")
    (wiki / "quickstart.md").write_text("# Wiki\n", encoding="utf-8")
    (wiki / "index.toon").write_text("modules[0]{}:\n", encoding="utf-8")
    return root


def test_the_required_shape_of_the_format(tmp_path):
    text = render_llms_txt(_wiki(tmp_path))
    lines = [line for line in text.splitlines() if line.strip()]

    # The spec mandates the order: H1 project name, then a blockquote summary, then H2 file lists.
    assert lines[0] == "# proj"
    assert lines[1].startswith("> ")
    assert all(line.startswith("## ") or not line.startswith("#") for line in lines[2:])


def test_the_summary_is_the_plain_language_sentence_already_written(tmp_path):
    # Reuse, not regeneration: the product page's opening sentence was already gated for plain
    # language, so the agent-facing index inherits that instead of paying for a second one.
    assert "> It keeps a project's guide honest and current." in render_llms_txt(_wiki(tmp_path))


def test_pages_are_layered_and_areas_come_before_modules(tmp_path):
    text = render_llms_txt(_wiki(tmp_path))
    assert text.index("## Start here") < text.index("## Areas") < text.index("## Modules")
    assert "- [subsystem-core.md](wiki/subsystem-core.md)" in text
    assert "- [src-core.md](wiki/src-core.md)" in text
    # The overview leads the file; it must not be repeated in the module list.
    assert text.count("overview.md") == 2      # once as the link text, once as the target


def test_skippable_material_sits_under_the_reserved_optional_heading(tmp_path):
    text = render_llms_txt(_wiki(tmp_path))
    optional = text.split("## Optional")[1]
    # `## Optional` is reserved by the spec for content an agent may drop when context is short.
    assert "quickstart.md" in optional and "index.toon" in optional
    assert "subsystem-core.md" not in optional


def test_it_is_written_where_a_fetcher_looks_and_is_deterministic(tmp_path):
    root = _wiki(tmp_path)
    path = write_llms_txt(root)
    assert path == root / LLMS_FILENAME          # repo root, per the convention
    assert path.read_text(encoding="utf-8") == render_llms_txt(root)
    assert write_llms_txt(root).read_text(encoding="utf-8") == path.read_text(encoding="utf-8")


def test_a_repo_without_a_product_page_still_produces_a_valid_file(tmp_path):
    root = _wiki(tmp_path)
    (root / "wiki" / "overview.md").unlink()
    text = render_llms_txt(root)
    assert text.startswith("# proj")
    assert "## Start here" not in text          # nothing invented to fill the section
    assert "## Modules" in text
