"""The wiki directory travels with the repository, not with whoever remembers to export a variable.

Before this, `ISIDORE_WIKI_DIR` was the only way to say a repo keeps its docs somewhere other than
`wiki/`. Forget it once and the toolchain guards a directory that does not exist while indexing the
real one as source — the self-indexing bug all over again (GIMO, wiki at `doc/isidore`: a 13 MB
certificate for a page about the documentation). A setting that must be remembered gets forgotten.
"""
from __future__ import annotations

import json

import pytest

from isidore.render import (
    CONFIG_FILENAME,
    DEFAULT_WIKI_DIRNAME,
    WIKI_DIR_ENV,
    configured_wiki_dirname,
)


@pytest.fixture()
def no_env(monkeypatch):
    monkeypatch.delenv(WIKI_DIR_ENV, raising=False)
    return monkeypatch


def _config(root, value):
    payload = {} if value is None else {"wiki_dir": value}
    (root / CONFIG_FILENAME).write_text(json.dumps(payload), encoding="utf-8")


@pytest.mark.usefixtures("no_env")
def test_a_repo_without_a_setting_gets_the_default(tmp_path):
    assert configured_wiki_dirname(tmp_path) == DEFAULT_WIKI_DIRNAME


@pytest.mark.usefixtures("no_env")
def test_a_repo_says_where_its_docs_live(tmp_path):
    _config(tmp_path, "doc/isidore")
    assert configured_wiki_dirname(tmp_path) == "doc/isidore"


@pytest.mark.usefixtures("no_env")
def test_the_setting_is_found_from_a_subdirectory(tmp_path):
    """Found by walking up, so running from `src/` behaves like running from the root — the case
    where forgetting the variable used to change the answer."""
    _config(tmp_path, "docs/isidore")
    deep = tmp_path / "src" / "pkg" / "inner"
    deep.mkdir(parents=True)
    assert configured_wiki_dirname(deep) == "docs/isidore"


def test_the_environment_still_wins(tmp_path, monkeypatch):
    """An existing export keeps working, and a one-off override stays possible."""
    _config(tmp_path, "doc/isidore")
    monkeypatch.setenv(WIKI_DIR_ENV, "somewhere/else")
    assert configured_wiki_dirname(tmp_path) == "somewhere/else"


@pytest.mark.parametrize("value", ["", "   ", None, 42])
@pytest.mark.usefixtures("no_env")
def test_a_config_without_a_usable_value_settles_on_the_default(tmp_path, value):
    """And it STOPS there: a parent repo's setting must not leak into a nested one that declined
    to declare its own."""
    _config(tmp_path.parent, "parent/wiki")
    _config(tmp_path, value)
    assert configured_wiki_dirname(tmp_path) == DEFAULT_WIKI_DIRNAME


@pytest.mark.usefixtures("no_env")
def test_an_unreadable_config_is_the_default_never_a_guess(tmp_path):
    (tmp_path / CONFIG_FILENAME).write_text("{ not json", encoding="utf-8")
    assert configured_wiki_dirname(tmp_path) == DEFAULT_WIKI_DIRNAME


@pytest.mark.parametrize("written,expected", [("doc\\isidore", "doc/isidore"),
                                              ("/docs/isidore/", "docs/isidore"),
                                              ("  wiki  ", "wiki")])
@pytest.mark.usefixtures("no_env")
def test_the_value_is_normalised(tmp_path, written, expected):
    """A Windows separator or a stray slash must not make two spellings of one directory."""
    _config(tmp_path, written)
    assert configured_wiki_dirname(tmp_path) == expected


@pytest.mark.usefixtures("no_env")
def test_the_cli_refuses_a_repo_whose_wiki_is_somewhere_else(tmp_path, capsys):
    """Half a run in the right place and half in the wrong one is the failure this prevents. The
    process bound its directory at import; if the repo disagrees, stop and say how to fix it."""
    from isidore.cli import main

    repo = tmp_path / "proj"
    repo.mkdir()
    _config(repo, "doc/isidore")

    assert main(["scan", "--repo", str(repo)]) == 2
    err = capsys.readouterr().err
    assert "doc/isidore" in err and "ISIDORE_WIKI_DIR=doc/isidore" in err
    assert not (repo / ".isidore").exists(), "refused before writing anything"
