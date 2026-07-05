"""Unit tests: toon encoder, graph scanner, findings residue, QA retrieval, LLM request."""
from __future__ import annotations

import json

import pytest

from isidore.findings import (
    filter_findings,
    harvest_todos,
    orphan_file_candidates,
    parse_findings_block,
    render_findings,
    coverage_gap_candidates,
)
from isidore.graph import GraphError, find_graph, load_graph, module_of, scan_repo, write_scan
from isidore.llm import build_request
from isidore.pipeline import PageSpec
from isidore.qa import ask, gather_evidence, question_terms
from isidore.render import render_toon_index
from isidore.toon import encode_table


# ----------------------------------------------------------------------- toon

def test_toon_encode_table_quoting_and_counts():
    out = encode_table("t", ["a", "b"], [{"a": "x,y", "b": None}, {"a": "", "b": True}])
    assert out.splitlines() == ['t[2]{a,b}:', '  "x,y",', '  ,1']


# ---------------------------------------------------------------------- graph

def test_module_of_normalizes_and_buckets():
    assert module_of("a/b/c.py", 2) == "a/b"
    assert module_of("a\\b\\c.py", 2) == "a/b"
    assert module_of(None, 2) == "(concepts)"


def test_scan_repo_extracts_symbols_imports_and_docs(tmp_path):
    pkg = tmp_path / "pkg"
    pkg.mkdir()
    (pkg / "alpha.py").write_text(
        "import pkg.beta\n\ndef top():\n    pass\n\nclass Thing:\n    pass\n", encoding="utf-8")
    (pkg / "beta.py").write_text("def helper():\n    pass\n", encoding="utf-8")
    (pkg / "notes.md").write_text("# notes\n", encoding="utf-8")
    (tmp_path / ".venv").mkdir()
    (tmp_path / ".venv" / "junk.py").write_text("x=1", encoding="utf-8")

    nodes, links = scan_repo(tmp_path)

    labels = {n["label"] for n in nodes}
    assert {"alpha.py", "beta.py", "top()", "Thing", "helper()", "notes.md"} <= labels
    assert all(".venv" not in str(n.get("source_file")) for n in nodes)
    rels = {(link["relation"]) for link in links}
    assert "contains" in rels and "imports" in rels


def test_scan_tolerates_syntax_errors(tmp_path):
    (tmp_path / "bad.py").write_text("def broken(:\n", encoding="utf-8")
    nodes, _links = scan_repo(tmp_path)
    assert any(n["label"] == "bad.py" for n in nodes)


def test_write_scan_and_find_graph_roundtrip(tmp_path):
    (tmp_path / "m.py").write_text("def f():\n    pass\n", encoding="utf-8")
    out = write_scan(tmp_path)
    assert find_graph(tmp_path) == out
    nodes, links, _commit = load_graph(out)
    assert nodes and isinstance(links, list)


# ------------------------------------------------------------------- findings

def test_parse_findings_block_extracts_and_strips():
    md = ("## Purpose\nGood page.\n\n```isidore-findings\n"
          "bug | src/x.py:42 | lock never released\n"
          "drift | README.md:1 | says 3 retries, code has 1\n"
          "question | | why disabled?\n"
          "garbage line without pipes\n"
          "notakind | a | b\n"
          "```\n")
    clean, findings = parse_findings_block(md)
    assert "isidore-findings" not in clean and "Good page." in clean
    assert [f["kind"] for f in findings] == ["bug", "drift", "question"]


def test_filter_findings_drops_hallucinated_paths(tmp_path):
    (tmp_path / "real.py").write_text("x=1", encoding="utf-8")
    kept, dropped = filter_findings([
        {"kind": "bug", "where": "real.py:1", "note": "ok"},
        {"kind": "bug", "where": "ghost/fake.py:9", "note": "invented"},
        {"kind": "question", "where": "", "note": "no path needed"},
    ], tmp_path)
    assert [f["note"] for f in kept] == ["ok", "no path needed"]
    assert len(dropped) == 1


def test_harvest_todos_finds_markers_with_lines(tmp_path):
    (tmp_path / "a.py").write_text("x=1\n# TODO: fix this later\ny=2  # FIXME broken\n",
                                   encoding="utf-8")
    rows = harvest_todos(tmp_path, {"a.py"})
    assert [(r["marker"], r["line"]) for r in rows] == [("TODO", 2), ("FIXME", 3)]


def test_harvest_todos_skips_oversized_files(tmp_path):
    # regression (scale): a pathologically large file must not stall the compile
    from isidore.findings import MAX_TODO_FILE_BYTES
    huge = tmp_path / "huge.py"
    huge.write_text("# TODO ignored\n" + ("x = 1\n" * (MAX_TODO_FILE_BYTES // 5)), encoding="utf-8")
    (tmp_path / "small.py").write_text("# TODO real\n", encoding="utf-8")
    rows = harvest_todos(tmp_path, {"huge.py", "small.py"})
    assert [r["file"] for r in rows] == ["small.py"], "el fichero gigante se salta"


def test_load_graph_raises_graph_error_on_malformed_and_wrong_shape(tmp_path):
    # regression (robustness): a corrupt graph must fail clean, not crash with a raw traceback
    bad = tmp_path / "bad.json"
    bad.write_text('{"nodes":[{"id":', encoding="utf-8")
    with pytest.raises(GraphError):
        load_graph(bad)

    not_obj = tmp_path / "arr.json"
    not_obj.write_text("[1,2,3]", encoding="utf-8")
    with pytest.raises(GraphError):
        load_graph(not_obj)

    wrong = tmp_path / "wrong.json"
    wrong.write_text('{"nodes":"oops","links":[]}', encoding="utf-8")
    with pytest.raises(GraphError):
        load_graph(wrong)


def test_orphan_and_coverage_gap_candidates():
    nodes = [
        {"id": "f1", "file_type": "code", "source_file": "pkg/orphan.py", "source_location": "L1"},
        {"id": "f2", "file_type": "code", "source_file": "pkg/used.py", "source_location": "L1"},
        {"id": "f3", "file_type": "code", "source_file": "pkg/main.py", "source_location": "L1"},
    ]
    links = [{"source": "f1", "target": "f2", "relation": "imports"}]
    orphans = orphan_file_candidates(nodes, links)
    assert [o["file"] for o in orphans] == ["pkg/orphan.py"]

    spec_no_tests = PageSpec("module", "pkg/core", symbols=20, deps_in=[("pkg/other", 3)])
    spec_tested = PageSpec("module", "pkg/api", symbols=15, deps_in=[("tests/unit", 9)])
    gaps = coverage_gap_candidates([spec_no_tests, spec_tested])
    assert [g["module"] for g in gaps] == ["pkg/core"]


def test_render_findings_tables_and_summary(tmp_path):
    out = render_findings(
        [{"kind": "bug", "where": "a/b.py:1", "note": "n"}],
        [{"marker": "TODO", "file": "a/b.py", "line": 2, "note": "x"}],
        [], [], [], "beef")
    assert "suspects[1]" in out and "todos[1]" in out and "1 bug suspects" in out


# ------------------------------------------------------------------------- qa

def _qa_repo(tmp_path):
    repo = tmp_path / "repo"
    (repo / "auth").mkdir(parents=True)
    for i in range(12):
        (repo / "auth" / f"f{i}.py").write_text(f"def login_{i}():\n    pass\n", encoding="utf-8")
    nodes = [{"id": f"n{i}", "label": f"login_{i}()", "file_type": "code",
              "source_file": f"auth/f{i}.py", "source_location": "L1"} for i in range(12)]
    graph = repo / "graphify-out"
    graph.mkdir()
    (graph / "graph.json").write_text(json.dumps({"nodes": nodes, "links": []}), encoding="utf-8")
    return repo, graph / "graph.json"


def test_question_terms_tokenizes():
    assert "login" in question_terms("how does login_3 relate to auth login?")


def test_gather_evidence_prefers_matching_pages_and_excerpts(tmp_path):
    repo, graph_path = _qa_repo(tmp_path)
    evidence, sources = gather_evidence(repo, "how does login_3 work in auth?",
                                        graph_path=graph_path)
    assert "auth" in evidence
    assert any("auth/f3.py" in s for s in sources), "el símbolo exacto de la pregunta trae extracto"


def test_ask_uses_single_injected_generator_call(tmp_path):
    repo, graph_path = _qa_repo(tmp_path)
    calls = []
    answer = ask(repo, "what is auth login_3?", graph_path=graph_path,
                 generator=lambda p: calls.append(p) or "grounded answer")
    assert answer == "grounded answer" and len(calls) == 1
    assert "EVIDENCE" in calls[0]


def test_ask_without_evidence_refuses_instead_of_calling(tmp_path):
    repo, graph_path = _qa_repo(tmp_path)
    answer = ask(repo, "zzz qqq vvv", graph_path=graph_path,
                 generator=lambda p: (_ for _ in ()).throw(AssertionError("no debe llamarse")))
    assert "No evidence" in answer


# ----------------------------------------------------------------------- llm

def test_build_request_openai_compat_temperature_zero_and_bearer():
    req = build_request("http://localhost:11434/v1", "m1", "hi", None)
    body = json.loads(req.data.decode("utf-8"))
    assert req.full_url.endswith("/v1/chat/completions")
    assert body["temperature"] == 0 and body["model"] == "m1"
    assert "Authorization" not in req.headers
    req2 = build_request("https://x/v1/", "m", "p", "sk-1")
    assert req2.get_header("Authorization") == "Bearer sk-1"


# -------------------------------------------------------------------- render

def test_render_toon_index_contains_all_tables():
    mod = PageSpec("module", "a/b", files=2, symbols=12,
                   hot_symbols=[("f()", "a/b/f.py", "L3", 7)], deps_out=[("c/d", 4)])
    flow = PageSpec("flow", "hop", modules=["a/b", "c/d"])
    out = render_toon_index([mod], [flow], "beef")
    for fragment in ("modules[1]", "flows[1]", "hot_symbols[1]", "module_deps[1]", "beef"):
        assert fragment in out
