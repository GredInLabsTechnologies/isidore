"""Prose citations that follow the code (citations.py) — the pure parts, over a real file on disk.

The end-to-end behaviour (compile re-points, certificates follow, revisions see corrected pages) lives
in test_incremental.py. Here: what counts as the same line, what is never touched, and every way the
legacy migration must refuse to move a citation — each negative case is a real miss of its first
version on isidore's own wiki, where 9 of 14 proposed moves would have broken a correct citation.
"""
from __future__ import annotations

from pathlib import Path

import pytest

from isidore.citations import anchors_for, migrate_by_symbol, repoint

SRC = """import os


def helper():
    value = os.getcwd()
    return value


def other():
    return helper()
"""


@pytest.fixture()
def repo(tmp_path: Path) -> Path:
    (tmp_path / "m.py").write_text(SRC, encoding="utf-8")
    return tmp_path


def _shift(repo: Path, n: int) -> None:
    (repo / "m.py").write_text("# pad\n" * n + SRC, encoding="utf-8")


def test_a_citation_and_its_range_follow_their_lines(repo):
    page = "`helper` (`m.py:4`) returns the cwd (`m.py:5-L6`).\n"
    anchors = anchors_for(repo, page)
    _shift(repo, 3)
    new, _anchors, moved, stale = repoint(repo, page, anchors)
    assert new == "`helper` (`m.py:7`) returns the cwd (`m.py:8-L9`).\n"
    assert (moved, stale) == (2, [])


def test_the_same_code_twice_resolves_to_the_nearest_copy(repo):
    doubled = SRC + "\n\n" + SRC.replace("import os\n", "")
    (repo / "m.py").write_text(doubled, encoding="utf-8")
    assert doubled.splitlines()[14] == "def helper():"   # line 15: the second copy
    page = "second copy (`m.py:15`)\n"
    anchors = anchors_for(repo, page)
    (repo / "m.py").write_text("# pad\n" + doubled, encoding="utf-8")
    assert repoint(repo, page, anchors)[0] == "second copy (`m.py:16`)\n"   # not the first copy


def test_changed_content_is_reported_and_left_as_written(repo):
    page = "reads the cwd (`m.py:5`)\n"
    anchors = anchors_for(repo, page)
    (repo / "m.py").write_text(SRC.replace("os.getcwd()", "os.environ['HOME']"), encoding="utf-8")
    new, _anchors, moved, stale = repoint(repo, page, anchors)
    assert (new, moved, stale) == (page, 0, ["m.py:5"])


def test_code_fences_blank_lines_and_missing_files_are_never_touched(repo):
    page = "```\nexample m.py:4\n```\nblank (`m.py:2`) and gone (`nope.py:4`) and real (`m.py:4`)\n"
    anchors = anchors_for(repo, page)
    assert anchors["m.py:4"] and anchors["m.py:2"] == ""   # the blank line: remembered, unanchored
    assert set(anchors) == {"m.py:2", "m.py:4"}         # the fence and the missing file: not at all
    _shift(repo, 1)
    new = repoint(repo, page, anchors)[0]
    assert new.startswith("```\nexample m.py:4\n```") and "(`m.py:5`)" in new
    assert "(`m.py:2`)" in new and "(`nope.py:4`)" in new


# --------------------------------------------------------------- legacy migration (conservative)

def test_migration_moves_a_citation_that_names_its_symbol_and_missed_it(repo):
    _shift(repo, 2)                                    # helper is at 6 now; page still says 4
    page = "- `helper` (`m.py:4`) — reads the cwd\n"
    assert migrate_by_symbol(repo, page) == ("- `helper` (`m.py:6`) — reads the cwd\n", 1)


def test_migration_fixes_a_citation_that_lands_on_a_blank_line(repo):
    _shift(repo, 2)                                    # line 4 is now blank
    page = "- `helper()` — the one that reads the working directory from os (`m.py:4`)\n"
    assert migrate_by_symbol(repo, page)[0].endswith("(`m.py:6`)\n")


@pytest.mark.parametrize("page", [
    # a line inside the named symbol's own body is cited on purpose
    "`helper` computes it (`m.py:5`)\n",
    # the cited line holds another symbol the sentence names
    "`other` delegates to `helper` (`m.py:10`)\n",
    # the cited line is some other definition
    "`helper` is used by (`m.py:9`)\n",
    # named further back in the clause, with its definition more than a few lines away
    "`other` is a function that exists, and a long clause follows before its cite (`m.py:1`)\n",
])
def test_migration_leaves_every_citation_it_cannot_validate(repo, page):
    assert migrate_by_symbol(repo, page) == (page, 0)


def test_migration_does_not_reach_for_a_far_away_definition(repo):
    (repo / "m.py").write_text("# pad\n" * 60 + SRC, encoding="utf-8")   # helper moved by 60
    page = "`helper` (`m.py:4`)\n"
    assert migrate_by_symbol(repo, page) == (page, 0)


def test_migration_pairs_a_symbol_further_back_only_with_a_nearby_definition(repo):
    # The real case: "`source_destination()` — classify where a compile would send the source
    # (`pipeline.py:168`)" after the function had moved 3 lines down.
    _shift(repo, 3)                                    # helper at 7; line 4 is now a comment
    page = "- `helper()` — reads the working directory, then hands it back (`m.py:4`)\n"
    assert migrate_by_symbol(repo, page)[0].endswith("(`m.py:7`)\n")


def test_a_citation_of_a_blank_line_never_adopts_what_slides_onto_it(repo):
    # regression, from a live round trip on isidore's own wiki: the blank line cited got code shifted
    # onto it, the citation was anchored to that code, and then travelled with it.
    page = "blank (`m.py:3`)\n"
    anchors = anchors_for(repo, page)
    _shift(repo, 1)                                    # line 3 now holds what was on line 2 — blank
    _shift(repo, 2)                                    # ...and now `import os`'s neighbour
    new, anchors, moved, stale = repoint(repo, page, anchors)
    (repo / "m.py").write_text(SRC, encoding="utf-8")
    new, anchors, moved, stale = repoint(repo, new, anchors)
    assert (new, moved, stale) == (page, 0, [])


def test_a_definition_whose_body_changed_is_still_followed_when_its_line_is_unique(repo):
    # Found on isidore's own page for citations.py: `anchors_for` got a new docstring and moved down;
    # its three-line window no longer existed, so the citation was reported stale although the line
    # it cites — the `def` — was unchanged and unique in the file.
    page = "`helper` (`m.py:4`)\n"
    anchors = anchors_for(repo, page)
    (repo / "m.py").write_text("# pad\n" * 2 + SRC.replace("value = os.getcwd()", "value = 1"),
                               encoding="utf-8")
    new, _anchors, moved, stale = repoint(repo, page, anchors)
    assert (new, moved, stale) == ("`helper` (`m.py:6`)\n", 1, [])


def test_a_changed_body_with_a_repeated_line_is_stale_not_guessed(repo):
    # `return value` appears twice after the edit: the line alone cannot say which one was cited.
    page = "returns it (`m.py:6`)\n"
    anchors = anchors_for(repo, page)
    (repo / "m.py").write_text(SRC.replace("def other():\n    return helper()",
                                           "def other():\n    value = 2\n    return value"),
                               encoding="utf-8")
    (repo / "m.py").write_text("# pad\n" + (repo / "m.py").read_text(encoding="utf-8")
                               .replace("value = os.getcwd()", "value = 3"), encoding="utf-8")
    new, _anchors, moved, stale = repoint(repo, page, anchors)
    assert (new, moved, stale) == (page, 0, ["m.py:6"])
