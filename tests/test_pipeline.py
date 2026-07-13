"""Compiler pipeline tests — no network: the LLM generator is always injected and counted."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from isidore.llm import GenerationError
from isidore.pipeline import (
    assemble_context,
    compile_wiki,
    context_hash,
    lint_cited_paths,
    plan_flows,
    plan_pages,
    prompt_for,
    read_excerpt,
    suggest_flows,
)
from isidore.render import MARKER_END, MARKER_START, agents_md_block, upsert_agents_block

PAGE = "## Purpose\nGenerated.\n"


def _node(id_, source_file, file_type="code", label=None, loc="L2"):
    return {"id": id_, "source_file": source_file, "file_type": file_type,
            "label": label or id_, "source_location": loc}


def _link(source, target, relation="calls"):
    return {"source": source, "target": target, "relation": relation}


def _make_repo(tmp_path: Path, n_modules: int = 3, symbols_per_module: int = 12) -> Path:
    repo = tmp_path / "repo"
    nodes, links = [], []
    for m in range(n_modules):
        mod_dir = repo / f"mod{m}" / "core"
        mod_dir.mkdir(parents=True)
        for s in range(symbols_per_module):
            src = f"mod{m}/core/file{s}.py"
            (repo / src).write_text(
                "\n".join(f"line {i} of {src}" for i in range(1, 11)), encoding="utf-8")
            node_id = f"m{m}_s{s}"
            nodes.append(_node(node_id, src, label=f"file{s}.py", loc="L3"))
            links.append(_link(node_id, f"m{(m + 1) % n_modules}_s0"))
        readme = f"mod{m}/core/README.md"
        (repo / readme).write_text(f"# Module {m}\nDoes things.", encoding="utf-8")
        nodes.append(_node(f"m{m}_doc", readme, file_type="document", loc="L1"))
    out = repo / "graphify-out"
    out.mkdir()
    (out / "graph.json").write_text(
        json.dumps({"nodes": nodes, "links": links, "built_at_commit": "abc123"}),
        encoding="utf-8")
    return repo


def _graph(repo: Path):
    data = json.loads((repo / "graphify-out" / "graph.json").read_text(encoding="utf-8"))
    return data["nodes"], data["links"]


def _gp(repo: Path) -> Path:
    return repo / "graphify-out" / "graph.json"


# ---------------------------------------------------------------------- plan

def test_plan_pages_selects_top_modules_excluding_small_and_concepts(tmp_path):
    repo = _make_repo(tmp_path)
    nodes, links = _graph(repo)
    nodes.append({"id": "c1", "source_file": None, "file_type": "concept", "label": "idea"})
    nodes.append(_node("tiny", "tiny/mod/x.py"))

    specs = plan_pages(nodes, links, min_symbols=10)

    assert sorted(s.name for s in specs) == ["mod0/core", "mod1/core", "mod2/core"]


def test_plan_pages_top_k_and_none_means_all(tmp_path):
    repo = _make_repo(tmp_path)
    nodes, links = _graph(repo)
    assert len(plan_pages(nodes, links, top_k=2)) == 2
    assert len(plan_pages(nodes, links, top_k=None)) == 3


def test_plan_pages_records_cross_module_deps(tmp_path):
    repo = _make_repo(tmp_path, n_modules=2)
    nodes, links = _graph(repo)
    spec0 = next(s for s in plan_pages(nodes, links) if s.name == "mod0/core")
    assert any(m == "mod1/core" for m, _ in spec0.deps_out)
    assert any(m == "mod1/core" for m, _ in spec0.deps_in)


# --------------------------------------------------------------------- flows

def test_plan_flows_bfs_collects_modules_and_edges(tmp_path):
    repo = _make_repo(tmp_path, n_modules=2)
    nodes, links = _graph(repo)

    flows = plan_flows(nodes, links, [{"name": "cross call", "seeds": ["m0_s0"]}])

    assert len(flows) == 1
    flow = flows[0]
    assert flow.kind == "flow"
    assert flow.filename == "flow-cross-call.md"
    assert "mod0/core" in flow.modules and "mod1/core" in flow.modules
    assert flow.flow_edges, "BFS debe recoger aristas reales del grafo"


def test_plan_flows_ignores_malformed_entries(tmp_path):
    repo = _make_repo(tmp_path, n_modules=1)
    nodes, links = _graph(repo)
    assert plan_flows(nodes, links, [{"name": "x"}, {"seeds": ["y"]}, {}]) == []


def test_suggest_flows_ranks_heaviest_bridges(tmp_path):
    repo = _make_repo(tmp_path, n_modules=2)
    nodes, links = _graph(repo)
    candidates = suggest_flows(nodes, links)
    assert candidates
    assert candidates[0]["links"] >= candidates[-1]["links"]
    assert candidates[0]["seeds"], "cada candidato trae el símbolo puente como semilla"


# ------------------------------------------------------------------- context

def test_read_excerpt_exact_lines_and_tolerance(tmp_path):
    repo = _make_repo(tmp_path, n_modules=1)
    excerpt = read_excerpt(repo, "mod0/core/file0.py", "L3", radius=1)
    assert "2: line 2 of mod0/core/file0.py" in excerpt
    assert "4: line 4 of mod0/core/file0.py" in excerpt
    assert "5: line 5" not in excerpt
    assert read_excerpt(repo, "no/such.py", "L3") == ""
    assert read_excerpt(repo, "mod0/core/file0.py", "garbage") == ""


def test_assemble_context_includes_docs_excerpts_deps_and_budget_warning(tmp_path):
    repo = _make_repo(tmp_path, n_modules=2)
    nodes, links = _graph(repo)
    spec = next(s for s in plan_pages(nodes, links) if s.name == "mod0/core")

    context, warnings = assemble_context(repo, spec)
    assert "# Module 0" in context and "--- excerpt mod0/core/" in context
    assert "mod1/core" in context and not warnings

    truncated, warns = assemble_context(repo, spec, max_chars=200)
    assert len(truncated) == 200 and warns


def test_prompt_carries_findings_addendum_and_hash_is_stable(tmp_path):
    repo = _make_repo(tmp_path, n_modules=1)
    nodes, links = _graph(repo)
    spec = plan_pages(nodes, links)[0]
    context, _ = assemble_context(repo, spec)
    prompt = prompt_for(spec, context)
    assert "isidore-findings" in prompt
    assert context_hash(prompt) == context_hash(prompt)


# ---------------------------------------------------------------------- lint

def test_lint_flags_only_nonexistent_paths_with_directories(tmp_path):
    repo = _make_repo(tmp_path, n_modules=1)
    md = "See `mod0/core/file0.py:3` and `invented/ghost.py`; also config.json alone."
    findings = lint_cited_paths(md, repo)
    assert findings == ["invented/ghost.py"]


def test_lint_ignores_placeholders_and_code_blocks(tmp_path):
    repo = _make_repo(tmp_path, n_modules=1)
    
    # 1. Test system placeholders are ignored
    md_placeholders = "Do not turn `src/pkg/x.py` into `pkg/x.py` or use `src/x.py`."
    assert lint_cited_paths(md_placeholders, repo) == []
    
    # 2. Test paths inside code blocks are ignored
    md_code_block = (
        "Here is an example:\n"
        "```python\n"
        "import invented/ghost.py\n"
        "```\n"
        "But check out `mod0/core/file0.py` in prose."
    )
    assert lint_cited_paths(md_code_block, repo) == []



# ----------------------------------------------------------------- agents.md

def test_upsert_agents_block_is_idempotent_and_preserves_content():
    original = "# My rules\n\nDo not break prod.\n"
    once = upsert_agents_block(original, agents_md_block())
    twice = upsert_agents_block(once, agents_md_block())
    assert once == twice
    assert once.startswith("# My rules") and "Do not break prod." in twice
    assert twice.count(MARKER_START) == 1 and twice.count(MARKER_END) == 1


# ------------------------------------------------------------------ pipeline

def test_dry_run_reports_dirty_and_never_calls_generator(tmp_path):
    repo = _make_repo(tmp_path)
    calls = []
    result = compile_wiki(repo, graph_path=_gp(repo), execute=False,
                          generator=lambda p: calls.append(p) or PAGE)
    assert result.planned == 3 and len(result.dirty) == 3
    assert calls == [] and not (repo / "wiki").exists()


def test_execute_writes_pages_quickstart_toon_index_findings_state_agents(tmp_path):
    repo = _make_repo(tmp_path)
    result = compile_wiki(repo, graph_path=_gp(repo), execute=True, generator=lambda p: PAGE)

    wiki = repo / "wiki"
    assert len(result.generated) == 3
    for name in ("quickstart.md", "index.toon", "findings.toon", ".isidore-state.json"):
        assert (wiki / name).is_file(), name
    quickstart = (wiki / "quickstart.md").read_text(encoding="utf-8")
    assert "abc123" in quickstart and "mod0-core.md" in quickstart
    index = (wiki / "index.toon").read_text(encoding="utf-8")
    assert "modules[3]" in index
    assert MARKER_START in (repo / "AGENTS.md").read_text(encoding="utf-8")


def test_incremental_zero_calls_when_nothing_changed(tmp_path):
    repo = _make_repo(tmp_path)
    compile_wiki(repo, graph_path=_gp(repo), execute=True, generator=lambda p: PAGE)
    calls = []
    result = compile_wiki(repo, graph_path=_gp(repo), execute=True,
                          generator=lambda p: calls.append(p) or PAGE)
    assert result.dirty == [] and calls == []


def test_incremental_regenerates_only_touched_module(tmp_path):
    repo = _make_repo(tmp_path)
    compile_wiki(repo, graph_path=_gp(repo), execute=True, generator=lambda p: PAGE)
    target = repo / "mod1" / "core" / "file0.py"
    target.write_text(target.read_text(encoding="utf-8").replace("line 3", "CHANGED 3"),
                      encoding="utf-8")
    calls = []
    result = compile_wiki(repo, graph_path=_gp(repo), execute=True,
                          generator=lambda p: calls.append(p) or PAGE)
    assert result.dirty == ["mod1-core.md"] and len(calls) == 1


def test_max_calls_cap_warns_loudly(tmp_path):
    repo = _make_repo(tmp_path)
    result = compile_wiki(repo, graph_path=_gp(repo), execute=True, max_calls=1,
                          generator=lambda p: PAGE)
    assert len(result.generated) == 1 and len(result.skipped_by_cap) == 2
    assert any("cap" in w for w in result.warnings)


def test_max_calls_zero_is_unlimited(tmp_path):
    repo = _make_repo(tmp_path)
    result = compile_wiki(repo, graph_path=_gp(repo), execute=True, max_calls=0,
                          generator=lambda p: PAGE)
    assert len(result.generated) == 3 and result.skipped_by_cap == []


def test_pending_pages_drain_first_across_runs(tmp_path):
    # A page skipped by the cap is marked pending and generated FIRST next run — the backlog drains
    # instead of the same page being re-skipped forever.
    repo = _make_repo(tmp_path)
    def n_pages() -> int:
        return len(list((repo / "wiki").glob("mod*-core.md")))
    compile_wiki(repo, graph_path=_gp(repo), execute=True, max_calls=1, generator=lambda p: PAGE)
    assert n_pages() == 1
    r2 = compile_wiki(repo, graph_path=_gp(repo), execute=True, max_calls=1, generator=lambda p: PAGE)
    assert n_pages() == 2 and len(r2.generated) == 1        # a previously-pending page, not a re-skip
    compile_wiki(repo, graph_path=_gp(repo), execute=True, max_calls=1, generator=lambda p: PAGE)
    assert n_pages() == 3                                   # backlog fully drained


def test_only_scopes_to_matching_pages_and_disables_prune(tmp_path):
    repo = _make_repo(tmp_path)
    compile_wiki(repo, graph_path=_gp(repo), execute=True, generator=lambda p: PAGE)
    before = {p.name: p.read_bytes() for p in (repo / "wiki").glob("mod*-core.md")}
    # touch every module's source so ALL pages would be dirty without scope
    for m in range(3):
        f = repo / f"mod{m}" / "core" / "file0.py"
        f.write_text(f.read_text(encoding="utf-8").replace("line 3", "EDIT 3"), encoding="utf-8")
    calls = []
    result = compile_wiki(repo, graph_path=_gp(repo), execute=True, only=["mod1/core"],
                          generator=lambda p: calls.append(p) or PAGE)
    assert result.dirty == ["mod1-core.md"] and len(calls) == 1
    # out-of-scope pages untouched on disk
    assert (repo / "wiki" / "mod0-core.md").read_bytes() == before["mod0-core.md"]
    assert (repo / "wiki" / "mod2-core.md").read_bytes() == before["mod2-core.md"]
    # prune disabled under scope even if a module vanished from the graph
    data = json.loads(_gp(repo).read_text(encoding="utf-8"))
    data["nodes"] = [n for n in data["nodes"] if not str(n.get("source_file", "")).startswith("mod2/")]
    data["links"] = [ln for ln in data["links"]
                     if not (str(ln["source"]).startswith("m2_") or str(ln["target"]).startswith("m2_"))]
    _gp(repo).write_text(json.dumps(data), encoding="utf-8")
    r2 = compile_wiki(repo, graph_path=_gp(repo), execute=True, only=["mod1/core"],
                      generator=lambda p: PAGE)
    assert r2.pruned == [] and (repo / "wiki" / "mod2-core.md").is_file()


def test_changed_scopes_to_blast_radius_over_a_real_git_repo(tmp_path):
    import shutil
    import subprocess
    if shutil.which("git") is None:
        import pytest
        pytest.skip("git not available")
    from isidore.graph import write_scan

    repo = tmp_path / "repo"
    (repo / "aaa").mkdir(parents=True)
    (repo / "bbb").mkdir(parents=True)
    # aaa/x.py imports bbb/y.py  => module aaa depends on module bbb (fan-in: bbb -> aaa)
    (repo / "bbb" / "__init__.py").write_text("", encoding="utf-8")
    (repo / "aaa" / "__init__.py").write_text("", encoding="utf-8")
    (repo / "bbb" / "y.py").write_text(
        "\n".join(["def helper():", "    return 1"] + [f"# pad {i}" for i in range(15)]),
        encoding="utf-8")
    (repo / "aaa" / "x.py").write_text(
        "\n".join(["import bbb.y", "def caller():", "    return bbb.y.helper()"]
                  + [f"# pad {i}" for i in range(15)]), encoding="utf-8")
    (repo / "ccc").mkdir()
    (repo / "ccc" / "__init__.py").write_text("", encoding="utf-8")
    (repo / "ccc" / "z.py").write_text(
        "\n".join(["def unrelated():", "    return 2"] + [f"# pad {i}" for i in range(15)]),
        encoding="utf-8")

    for args in (["init", "-q"], ["config", "user.email", "t@t"], ["config", "user.name", "t"],
                 ["add", "-A"], ["commit", "-qm", "seed"]):
        subprocess.run(["git", *args], cwd=repo, check=True, capture_output=True)

    gp = write_scan(repo)
    compile_wiki(repo, graph_path=gp, execute=True, min_symbols=1, generator=lambda p: PAGE)
    # edit ONLY bbb/y.py's helper body
    y = repo / "bbb" / "y.py"
    y.write_text(y.read_text(encoding="utf-8").replace("return 1", "return 42"), encoding="utf-8")
    write_scan(repo)  # refresh graph locations (still pre-commit; --changed diffs against last commit)

    calls = []
    result = compile_wiki(repo, graph_path=gp, execute=True, changed=True, min_symbols=1,
                          generator=lambda p: calls.append(p) or PAGE)
    # Only the truly-changed page regenerates (the hash gate skips the hash-clean fan-in page) —
    # this is the whole point: scope narrows what is CONSIDERED, the context hash decides what is
    # rewritten. ccc (unrelated) is never even considered.
    assert result.dirty == ["bbb-y_py.md"] and len(calls) == 1
    scope_msg = next(w for w in result.warnings if "scoped by --changed" in w)
    assert "2 affected module(s)" in scope_msg          # bbb (changed) + aaa (fan-in dependent)
    assert not any("ccc" in d for d in result.dirty)     # unrelated module excluded from scope


def test_prune_only_when_module_leaves_graph_not_on_smaller_top_k(tmp_path):
    repo = _make_repo(tmp_path)
    compile_wiki(repo, graph_path=_gp(repo), execute=True, generator=lambda p: PAGE)

    result = compile_wiki(repo, graph_path=_gp(repo), execute=True, top_k=1,
                          generator=lambda p: PAGE)
    assert result.pruned == [] and (repo / "wiki" / "mod2-core.md").is_file()

    data = json.loads(_gp(repo).read_text(encoding="utf-8"))
    data["nodes"] = [n for n in data["nodes"]
                     if not str(n.get("source_file", "")).startswith("mod1/")]
    data["links"] = [ln for ln in data["links"]
                     if not (str(ln["source"]).startswith("m1_")
                             or str(ln["target"]).startswith("m1_"))]
    _gp(repo).write_text(json.dumps(data), encoding="utf-8")

    result = compile_wiki(repo, graph_path=_gp(repo), execute=True, generator=lambda p: PAGE)
    assert "mod1-core.md" in result.pruned
    assert not (repo / "wiki" / "mod1-core.md").exists()


def test_flow_pages_compile_alongside_module_pages(tmp_path):
    repo = _make_repo(tmp_path, n_modules=2)
    result = compile_wiki(repo, graph_path=_gp(repo), execute=True,
                          flows_config=[{"name": "hop", "seeds": ["m0_s0"]}],
                          generator=lambda p: PAGE)
    assert "flow-hop.md" in result.generated
    assert "flow-hop.md" in (repo / "wiki" / "quickstart.md").read_text(encoding="utf-8")


def test_lint_gate_retries_then_quarantines_when_phantom_path_persists(tmp_path):
    # Bug A fix: a page citing a nonexistent path must NOT ship silently. It gets ONE bounded retry
    # (the phantom path named back), and if still bad it ships with the citation annotated inline
    # AND is marked quarantined — never emitted with a dead citation and no signal.
    repo = _make_repo(tmp_path, n_modules=1)
    calls = []
    result = compile_wiki(
        repo, graph_path=_gp(repo), execute=True,
        generator=lambda p: calls.append(p) or "## Purpose\nUses `fake/dir/x.py`.\n")
    page = (repo / "wiki" / "mod0-core.md").read_text(encoding="utf-8")
    assert "[⚠ isidore: path not found]" in page          # annotated inline, not silently shipped
    assert "mod0-core.md" in result.quarantined and result.retries == 1
    assert len(calls) == 2                                 # original + one repair retry
    assert "CORRECTION REQUIRED" in calls[1] and "fake/dir/x.py" in calls[1]
    import json
    state = json.loads((repo / "wiki" / ".isidore-state.json").read_text(encoding="utf-8"))
    assert state["pages"]["mod0-core.md"]["quarantined"] is True


def test_lint_gate_retry_repairs_and_clears_quarantine(tmp_path):
    # If the retry fixes the citation, the page is NOT quarantined and ships clean.
    repo = _make_repo(tmp_path, n_modules=1)
    good = "## Purpose\nUses `mod0/core/file0.py`.\n"
    seq = iter(["## Purpose\nUses `fake/ghost.py`.\n", good])
    result = compile_wiki(repo, graph_path=_gp(repo), execute=True, generator=lambda p: next(seq))
    page = (repo / "wiki" / "mod0-core.md").read_text(encoding="utf-8")
    assert "[⚠ isidore: path not found]" not in page
    assert result.quarantined == [] and result.retries == 1


def test_absence_claims_and_findings_dropped_but_behavioral_kept(tmp_path):
    repo = _make_repo(tmp_path, n_modules=1)
    real = "mod0/core/file0.py"
    page = (
        "## Purpose\nText.\n\n"
        "```isidore-claims\n"
        f"There is no retry logic in this module | {real}:3\n"          # absence -> dropped
        f"file0 is not thread-safe | {real}:3\n"                        # behavioral -> kept
        "```\n\n"
        "```isidore-findings\n"
        f"bug | {real}:3 | no error handling exists for the parse path\n"  # absence -> dropped
        f"bug | {real}:3 | the lock is not released on the error path\n"   # behavioral -> kept
        "```\n"
    )
    result = compile_wiki(repo, graph_path=_gp(repo), execute=True, generator=lambda p: page)
    assert result.claims_dropped_negative == 1 and result.claims_total == 1
    assert result.findings_dropped_negative == 1 and result.findings_kept == 1


def test_compile_preserves_crlf_line_endings_in_agents_md(tmp_path):
    # regression (scale, found on GIMO): a CRLF AGENTS.md must NOT be rewritten to LF — that turned
    # a 6-line insert into an all-985-lines diff. Only the appended block is new; the rest is byte-stable.
    repo = _make_repo(tmp_path, n_modules=1)
    agents = repo / "AGENTS.md"
    agents.write_bytes("# Rules\r\n\r\nLine one.\r\nLine two.\r\n".encode("utf-8"))

    compile_wiki(repo, graph_path=_gp(repo), execute=True, generator=lambda p: PAGE)

    out = agents.read_bytes()
    assert b"\r\n" in out, "CRLF preservado"
    assert b"\n\n" not in out.replace(b"\r\n", b""), "no se coló ningún LF suelto"
    assert out.startswith("# Rules\r\n\r\nLine one.\r\nLine two.\r\n".encode("utf-8"))
    assert MARKER_START.encode("utf-8") in out


def test_git_log_survives_non_ascii_commit_messages(tmp_path):
    # regression: git output with accents (UTF-8) must not crash on Windows (cp1252 default)
    import subprocess as sp

    from isidore.pipeline import git_log_for
    repo = _make_repo(tmp_path, n_modules=1)
    env = {**__import__("os").environ, "GIT_AUTHOR_NAME": "T", "GIT_AUTHOR_EMAIL": "t@t",
           "GIT_COMMITTER_NAME": "T", "GIT_COMMITTER_EMAIL": "t@t"}
    sp.run(["git", "init", "-q"], cwd=repo, check=False, env=env)
    sp.run(["git", "add", "-A"], cwd=repo, check=False, env=env)
    sp.run(["git", "commit", "-qm", "refactor módulo: cañón, ñoño, €uro, 日本語"],
           cwd=repo, check=False, env=env)
    out = git_log_for(repo, "mod0/core")     # must return a string, never raise
    assert isinstance(out, str)


def test_missing_graph_raises_and_missing_model_fails_closed(tmp_path, monkeypatch):
    repo = tmp_path / "empty"
    repo.mkdir()
    with pytest.raises(FileNotFoundError):
        compile_wiki(repo, graph_path=None)

    repo2 = _make_repo(tmp_path, n_modules=1)
    monkeypatch.delenv("ISIDORE_MODEL", raising=False)
    with pytest.raises(GenerationError):
        compile_wiki(repo2, graph_path=_gp(repo2), execute=True)
