"""Compiling is a disclosure: where is this repository's source allowed to go?

Until this gate existed, `pipeline.py` asked only whether a provider was CONFIGURED, never where it
was. Measured 2026-07-26: a key pointing at a free tier whose training toggle is on by default took
87 prompts of private source out of five repositories, about 26,000 lines, before anyone read the
setting. Nothing in the pipeline objected, because nothing was looking.

The gate must be strict enough to have stopped that, and loose enough never to stand between anyone
and the two ways of working that send nothing at all — a model on this machine, and the handoff.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from isidore.llm import GenerationError
from isidore.pipeline import (
    DEST_CLI,
    DEST_DECLARED,
    DEST_LOCAL,
    DEST_TRUSTED,
    DEST_UNDECLARED,
    TRUST_ENV,
    assert_may_send_source,
    compile_wiki,
    source_destination,
)

PAGE = "## Purpose\nGenerated.\n"


def _make_repo(tmp_path: Path) -> Path:
    repo = tmp_path / "repo"
    nodes = []
    (repo / "mod0" / "core").mkdir(parents=True)
    for s in range(12):
        src = f"mod0/core/file{s}.py"
        (repo / src).write_text("\n".join(f"line {i}" for i in range(1, 11)), encoding="utf-8")
        nodes.append({"id": f"s{s}", "source_file": src, "file_type": "code",
                      "label": f"file{s}.py", "source_location": "L3"})
    (repo / "graphify-out").mkdir()
    (repo / "graphify-out" / "graph.json").write_text(
        json.dumps({"nodes": nodes, "links": [], "built_at_commit": "abc123"}), encoding="utf-8")
    return repo


@pytest.fixture()
def clean_env(monkeypatch):
    for var in ("ISIDORE_PROVIDER", "ISIDORE_BASE_URL", "ISIDORE_MODEL", TRUST_ENV):
        monkeypatch.delenv(var, raising=False)
    return monkeypatch


def _gp(repo: Path) -> Path:
    return repo / "graphify-out" / "graph.json"


# ------------------------------------------------------------------ classifying the destination

def test_the_default_destination_is_this_machine(clean_env):
    """Unconfigured means a local endpoint, so the out-of-the-box posture sends nothing anywhere."""
    kind, _detail = source_destination()
    assert kind == DEST_LOCAL


@pytest.mark.parametrize("url", ["http://localhost:11434/v1", "http://127.0.0.1:8080/v1",
                                 "http://[::1]:1234/v1", "http://0.0.0.0:5000/v1"])
def test_a_model_on_this_machine_is_local_however_it_is_addressed(clean_env, url):
    clean_env.setenv("ISIDORE_BASE_URL", url)
    assert source_destination()[0] == DEST_LOCAL


def test_the_operators_own_claude_session_is_not_a_third_party(clean_env):
    clean_env.setenv("ISIDORE_PROVIDER", "claude-cli")
    clean_env.setenv("ISIDORE_BASE_URL", "https://api.example-pool.com/v1")   # ignored: no HTTP path
    assert source_destination()[0] == DEST_CLI


def test_an_endpoint_under_an_agreement_is_trusted(clean_env):
    clean_env.setenv("ISIDORE_BASE_URL", "https://api.anthropic.com/v1")
    assert source_destination() == (DEST_TRUSTED, "api.anthropic.com")


def test_anything_else_is_undeclared_until_someone_says_otherwise(clean_env):
    clean_env.setenv("ISIDORE_BASE_URL", "https://api.some-free-tier.com/v1")
    assert source_destination() == (DEST_UNDECLARED, "api.some-free-tier.com")

    clean_env.setenv(TRUST_ENV, "yes")
    assert source_destination()[0] == DEST_DECLARED


@pytest.mark.parametrize("value", ["true", "1", "YES please", "y", " si ", ""])
def test_a_truthy_looking_value_is_not_a_decision(clean_env, value):
    """Same discipline as the classification gate: the word `yes`, exactly. Someone typing `1` into
    an environment variable has not weighed anything."""
    clean_env.setenv("ISIDORE_BASE_URL", "https://api.some-free-tier.com/v1")
    clean_env.setenv(TRUST_ENV, value)
    assert source_destination()[0] == DEST_UNDECLARED


# --------------------------------------------------------------------------- what the gate does

def test_the_refusal_names_the_host_and_every_way_out(clean_env):
    clean_env.setenv("ISIDORE_BASE_URL", "https://api.some-free-tier.com/v1")

    with pytest.raises(GenerationError) as exc:
        assert_may_send_source("source excerpts from 7 page(s)")

    message = str(exc.value)
    assert "api.some-free-tier.com" in message and "7 page(s)" in message
    assert "handoff emit" in message                 # the way that sends nothing at all
    assert "ISIDORE_PROVIDER=claude-cli" in message
    assert f"{TRUST_ENV}=yes" in message             # and how to say yes, if it really is fit


def test_a_declared_third_party_is_allowed_but_recorded(clean_env):
    """Consent is not the end of it. The incident was invisible for weeks because no run said where
    its prompts had gone — so a permitted disclosure still leaves a line behind."""
    clean_env.setenv("ISIDORE_BASE_URL", "https://api.some-free-tier.com/v1")
    clean_env.setenv(TRUST_ENV, "yes")

    warning = assert_may_send_source("source excerpts from 3 page(s)")

    assert warning and "DISCLOSURE" in warning
    assert "api.some-free-tier.com" in warning and "3 page(s)" in warning


@pytest.mark.parametrize("env", [{}, {"ISIDORE_PROVIDER": "claude-cli"},
                                 {"ISIDORE_BASE_URL": "https://api.anthropic.com/v1"}])
def test_the_ways_that_are_fit_pass_silently(clean_env, env):
    for k, v in env.items():
        clean_env.setenv(k, v)
    assert assert_may_send_source("anything") is None


# ------------------------------------------------------------------------- wired into compile

def test_a_compile_at_an_undeclared_host_writes_nothing(clean_env, tmp_path):
    repo = _make_repo(tmp_path)
    clean_env.setenv("ISIDORE_BASE_URL", "https://api.some-free-tier.com/v1")
    clean_env.setenv("ISIDORE_MODEL", "some-free-model")

    with pytest.raises(GenerationError, match="refusing to send source code"):
        compile_wiki(repo, graph_path=_gp(repo), execute=True)

    assert not list((repo / "wiki").glob("*.md")), "refused BEFORE anything was written"


def test_a_dry_run_is_never_gated(clean_env, tmp_path):
    """Planning reads the repository and sends nothing. Gating it would only teach people to set the
    variable for a command that never had a destination."""
    repo = _make_repo(tmp_path)
    clean_env.setenv("ISIDORE_BASE_URL", "https://api.some-free-tier.com/v1")

    result = compile_wiki(repo, graph_path=_gp(repo), execute=False)

    assert result.dirty == ["mod0-core.md"] and result.prompts


def test_the_handoff_still_works_when_the_gate_is_shut(clean_env, tmp_path):
    """The escape hatch has to be open exactly when the gate is closed, or the gate becomes a reason
    to declare a host trusted just to get work done."""
    from isidore.handoff import RESPONSE_SUFFIX, apply, emit, handoff_dir

    repo = _make_repo(tmp_path)
    clean_env.setenv("ISIDORE_BASE_URL", "https://api.some-free-tier.com/v1")

    class _Args:
        def __init__(self):
            self.repo, self.only, self.graph = repo, "", None

    count, names = emit(repo, {}, _Args())
    assert count == 1
    handoff_dir(repo).joinpath(f"{names[0]}{RESPONSE_SUFFIX}").write_text(PAGE, encoding="utf-8")

    result = apply(repo, {}, _Args())
    assert result.generated == ["mod0-core.md"] and (repo / "wiki" / "mod0-core.md").is_file()


def test_an_injected_generator_is_the_callers_own_business(clean_env, tmp_path):
    """The gate reads the environment, which is where a stray export puts a destination. A function
    passed in by the caller is not something it can see inside — say so, rather than pretend."""
    repo = _make_repo(tmp_path)
    clean_env.setenv("ISIDORE_BASE_URL", "https://api.some-free-tier.com/v1")

    result = compile_wiki(repo, graph_path=_gp(repo), execute=True, generator=lambda p: PAGE)

    assert result.generated == ["mod0-core.md"]


# ---------------------------------------------- the other doors into the same disclosure

def test_every_path_that_sends_repository_content_is_gated():
    """Gating `compile` alone would have been theatre: four call sites reach a provider with material
    read out of the repository, and a leak through any of them is the same leak. This pins the set —
    a fifth site added without a gate makes this test fail rather than silently open a door."""
    import ast
    from pathlib import Path as _P

    src = _P("src/isidore")
    ungated = []
    for path in sorted(src.rglob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if not (isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
                    and node.func.id == "default_generator"):
                continue
            # the gate is called in the same enclosing function, before this line
            enclosing = [f for f in ast.walk(tree)
                         if isinstance(f, (ast.FunctionDef, ast.AsyncFunctionDef))
                         and f.lineno <= node.lineno <= (f.end_lineno or node.lineno)]
            body = enclosing[-1] if enclosing else tree
            gated = any(isinstance(c, ast.Call) and isinstance(c.func, ast.Name)
                        and c.func.id == "assert_may_send_source" and c.lineno < node.lineno
                        for c in ast.walk(body))
            if not gated:
                ungated.append(f"{path.as_posix()}:{node.lineno}")

    # knowledge.py withholds by item classification instead — public material going to a free
    # endpoint is the legitimate use, and blocking it would push people to declare hosts trusted.
    assert ungated == ["src/isidore/knowledge.py:420"], ungated


def test_whatsnew_refuses_at_an_undeclared_host(clean_env, tmp_path):
    """Its prompts carry an excerpt of every added and changed symbol — a compile by another name."""
    import subprocess
    from isidore.whatsnew import WhatsnewError, run_whatsnew

    repo = tmp_path / "wn"
    (repo / "pkg").mkdir(parents=True)
    (repo / "pkg" / "m.py").write_text("def a():\n    return 1\n", encoding="utf-8")
    env = {"GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t",
           "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"}
    import os as _os
    env = {**_os.environ, **env}
    for args in (["init", "-q"], ["add", "-A"], ["commit", "-qm", "seed"]):
        subprocess.run(["git", *args], cwd=repo, check=True, capture_output=True, env=env)
    since = subprocess.run(["git", "rev-parse", "HEAD"], cwd=repo, capture_output=True,
                           text=True, env=env).stdout.strip()
    (repo / "pkg" / "m.py").write_text("def a():\n    return 1\n\n\ndef b():\n    return 2\n",
                                       encoding="utf-8")
    for args in (["add", "-A"], ["commit", "-qm", "add b"]):
        subprocess.run(["git", *args], cwd=repo, check=True, capture_output=True, env=env)

    clean_env.setenv("ISIDORE_BASE_URL", "https://api.some-free-tier.com/v1")
    clean_env.setenv("ISIDORE_MODEL", "some-free-model")

    with pytest.raises((GenerationError, WhatsnewError), match="refusing to send source code"):
        run_whatsnew(repo, since, execute=True)
