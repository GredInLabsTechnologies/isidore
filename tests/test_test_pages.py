"""Tests are evidence, not pages.

On isidore's own repo 23 of the 40 planned pages were test files, 13 product modules were pushed out of
the plan (handoff, recertify, changeset, detectors, llm, impact...) and 74 of 151 page generations went
to tests — because a test file counts every test function as a symbol. Tests now stay in the graph
(impact, coverage gaps, TODOs) and each product page lists the test modules exercising it; they get no
prose page of their own unless `document_tests` asks for it.
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest

from isidore.graph import is_test_path, load_graph, write_scan
from isidore.pipeline import compile_wiki, load_state, plan_pages
from isidore.pyramid import overview_facts

CORE = "".join(f"def f{i}():\n    return {i}\n\n\n" for i in range(8))
TESTS = "from pkg.core import f0\n\n\n" + "".join(
    f"def test_{i}():\n    assert f0() == 0\n\n\n" for i in range(30))


@pytest.mark.parametrize("path", [
    "tests/test_x.py", "tests/fixtures/pcp/repo/svc/auth.py", "pkg/test_mod.py", "pkg/mod_test.py",
    "conftest.py", "cmd/server_test.go", "web/app.test.tsx", "web/app.spec.js",
    "src/test/java/FooTest.java", "Foo.Tests/BarTests.cs", "spec/models/user_spec.rb",
    "app/__tests__/x.js", "e2e/login.ts"])
def test_test_files_are_recognised_across_languages(path):
    assert is_test_path(path)


@pytest.mark.parametrize("path", [
    "src/isidore/pipeline.py", "pkg/testing_utils_ok.py", "docs/testimonials.md", "src/contest.py",
    "lib/attest.py", "latest.go", "src/latest_version.ts", "app/Tester.java"])
def test_product_files_are_not(path):
    assert not is_test_path(path)


@pytest.fixture()
def repo(tmp_path: Path) -> Path:
    root = tmp_path / "repo"
    (root / "pkg").mkdir(parents=True)
    (root / "tests").mkdir()
    (root / "pkg" / "__init__.py").write_text("", encoding="utf-8")
    (root / "pkg" / "core.py").write_text(CORE, encoding="utf-8")
    (root / "tests" / "test_core.py").write_text(TESTS, encoding="utf-8")
    for args in (["init", "-q"], ["config", "user.email", "t@t.invalid"], ["config", "user.name", "t"],
                 ["add", "-A"], ["commit", "-qm", "seed"]):
        subprocess.run(["git", "-C", str(root), *args], check=True, capture_output=True)
    return root


def test_tests_get_no_page_and_the_module_they_test_lists_them(repo):
    nodes, links, _ = load_graph(write_scan(repo))
    specs = plan_pages(nodes, links, module_depth=2, min_symbols=5, top_k=None)
    assert [s.name for s in specs] == ["pkg/core.py"]           # the 30-test file outranked it before
    assert specs[0].tested_by == ["tests/test_core.py"]

    with_tests = plan_pages(nodes, links, module_depth=2, min_symbols=5, top_k=None,
                            include_tests=True)
    assert [s.name for s in with_tests] == ["tests/test_core.py", "pkg/core.py"]


def test_the_page_prompt_names_the_tests_that_exercise_the_module(repo):
    res = compile_wiki(repo, graph_path=write_scan(repo), min_symbols=5, module_depth=2)
    prompt = res.prompts["pkg-core_py.md"]
    assert "tested by (test modules that import it): tests/test_core.py" in prompt


def test_an_existing_test_page_is_pruned_with_its_certificate(repo):
    # A wiki compiled before this change has test pages; they leave together with their certificates.
    wiki = repo / "wiki"
    wiki.mkdir()
    (wiki / "tests-test_core_py.md").write_text("## Purpose\nold\n", encoding="utf-8")
    (wiki / "tests-test_core_py.md.cert.json").write_text("{}", encoding="utf-8")
    (wiki / ".isidore-state.json").write_text(json.dumps(
        {"pages": {"tests-test_core_py.md": {"context_hash": "x"}}}), encoding="utf-8")
    res = compile_wiki(repo, graph_path=write_scan(repo), execute=True, min_symbols=5,
                       module_depth=2, max_calls=0, generator=lambda p: "## Purpose\nCore.\n")
    assert res.pruned == ["tests-test_core_py.md"]
    assert not (wiki / "tests-test_core_py.md").exists()
    assert not (wiki / "tests-test_core_py.md.cert.json").exists()
    assert "tests-test_core_py.md" not in load_state(wiki)["pages"]


def test_document_tests_brings_the_test_pages_back(repo):
    res = compile_wiki(repo, graph_path=write_scan(repo), min_symbols=5, module_depth=2,
                       document_tests=True)
    assert "tests-test_core_py.md" in res.dirty


def test_the_product_overview_is_not_made_of_tests(repo):
    nodes, links, _ = load_graph(write_scan(repo))
    names = [m["name"] for m in overview_facts(repo, nodes, links, {})["modules"]]
    assert names and not any(n.startswith("tests") for n in names)


def test_files_without_code_are_not_parts_of_the_product(repo):
    # regression: once tests left the overview's module list, one-node files filled it —
    # ".gitignore (1 symbols)" was the product's second part.
    for name in ("LICENSE", ".gitignore", "pyproject.toml"):
        (repo / name).write_text("x\n", encoding="utf-8")
    subprocess.run(["git", "-C", str(repo), "add", "-A"], check=True, capture_output=True)
    nodes, links, _ = load_graph(write_scan(repo))
    assert [m["name"] for m in overview_facts(repo, nodes, links, {})["modules"]] == ["pkg/core.py"]
