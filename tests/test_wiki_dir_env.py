"""ISIDORE_WIKI_DIR redirects the compiled-wiki output directory.

WIKI_DIRNAME is resolved once at import from the environment, defaulting to
"wiki". Only render.py defines it (single source of truth); every other module,
including pipeline, imports it. These tests reload render.py under a patched
environment to prove the resolution, then restore the default for the suite.
"""
import importlib


def _reload_render():
    from isidore import render

    importlib.reload(render)
    return render


def test_wiki_dirname_defaults_to_wiki(monkeypatch):
    monkeypatch.delenv("ISIDORE_WIKI_DIR", raising=False)
    assert _reload_render().WIKI_DIRNAME == "wiki"


def test_wiki_dirname_honors_env(monkeypatch):
    monkeypatch.setenv("ISIDORE_WIKI_DIR", "doc/isidore")
    assert _reload_render().WIKI_DIRNAME == "doc/isidore"


def test_wiki_dirname_blank_env_falls_back(monkeypatch):
    monkeypatch.setenv("ISIDORE_WIKI_DIR", "   ")
    assert _reload_render().WIKI_DIRNAME == "wiki"


def test_save_state_creates_nested_wiki_dir(tmp_path):
    """A nested WIKI_DIRNAME (e.g. doc/isidore) must create its parents, not crash."""
    from isidore.pipeline import STATE_FILENAME, save_state

    nested = tmp_path / "doc" / "isidore"
    assert not nested.parent.exists()  # "doc/" does not exist yet
    save_state(nested, {"pages": {}})
    assert (nested / STATE_FILENAME).exists()


def teardown_module(_module):
    # Restore the default binding so the rest of the suite is unaffected.
    from isidore import render

    importlib.reload(render)
