"""Claims: parsing, anchoring/quarantine, and the zero-LLM staleness property (ADR-0030)."""
from __future__ import annotations

import json
from pathlib import Path

from isidore.claims import (
    anchor_claims,
    check_claims,
    claim_id,
    evidence_hash,
    evidence_state,
    parse_claims_block,
    render_claims,
    stale_pages,
)
from isidore.pipeline import compile_wiki

PAGE_WITH_CLAIMS = """## Purpose
Fine page.

```isidore-claims
file0 defines exactly ten numbered lines | mod0/core/file0.py:3
this claim cites a ghost | ghost/nowhere.py:1
```

```isidore-findings
question | | none really
```
"""


def _make_repo(tmp_path: Path) -> Path:
    repo = tmp_path / "repo"
    mod = repo / "mod0" / "core"
    mod.mkdir(parents=True)
    nodes, links = [], []
    for s in range(12):
        src = f"mod0/core/file{s}.py"
        (repo / src).write_text("\n".join(f"line {i} of {src}" for i in range(1, 11)),
                                encoding="utf-8")
        nodes.append({"id": f"s{s}", "source_file": src, "file_type": "code",
                      "label": f"file{s}.py", "source_location": "L3"})
        links.append({"source": f"s{s}", "target": "s0", "relation": "calls"})
    out = repo / "graphify-out"
    out.mkdir()
    (out / "graph.json").write_text(json.dumps({"nodes": nodes, "links": links}),
                                    encoding="utf-8")
    return repo


def _gp(repo: Path) -> Path:
    return repo / "graphify-out" / "graph.json"


def test_parse_claims_block_extracts_and_strips():
    clean, rows = parse_claims_block(PAGE_WITH_CLAIMS)
    assert "isidore-claims" not in clean and "Fine page." in clean
    assert [r["evidence"] for r in rows] == ["mod0/core/file0.py:3", "ghost/nowhere.py:1"]
    # el bloque de findings sigue intacto para su propio parser
    assert "isidore-findings" in clean


def test_evidence_hash_is_the_cited_line_content(tmp_path):
    repo = _make_repo(tmp_path)
    h1 = evidence_hash(repo, "mod0/core/file0.py:3")
    assert h1 and len(h1) == 12
    assert evidence_hash(repo, "mod0/core/file0.py:3") == h1  # determinista
    assert evidence_hash(repo, "ghost/nope.py:1") is None
    assert evidence_hash(repo, "mod0/core/file0.py:999") is None  # línea fuera de rango
    assert evidence_hash(repo, "mod0/core/file0.py") is not None  # sin línea: hash del fichero

    # cambiar la LÍNEA CITADA (L3) cambia el hash
    target = repo / "mod0" / "core" / "file0.py"
    target.write_text(target.read_text(encoding="utf-8").replace("line 3 of", "CHANGED of"),
                      encoding="utf-8")
    assert evidence_hash(repo, "mod0/core/file0.py:3") != h1


def test_evidence_state_ignores_neighbors_whitespace_and_line_shifts(tmp_path):
    repo = _make_repo(tmp_path)
    anchor = evidence_hash(repo, "mod0/core/file0.py:3")
    target = repo / "mod0" / "core" / "file0.py"
    original = target.read_text(encoding="utf-8")

    # cambiar una línea VECINA (L2) NO marca stale (solo importa la línea citada)
    target.write_text(original.replace("line 2 of", "TOUCHED of"), encoding="utf-8")
    assert evidence_state(repo, "mod0/core/file0.py:3", anchor) == "ok"

    # re-indentar la línea citada (whitespace) NO marca stale
    target.write_text(original.replace("line 3 of", "    line 3 of"), encoding="utf-8")
    assert evidence_state(repo, "mod0/core/file0.py:3", anchor) == "ok"

    # insertar líneas ARRIBA desplaza el número pero NO marca stale (ancla por contenido)
    target.write_text("new top line\nanother\n" + original, encoding="utf-8")
    assert evidence_state(repo, "mod0/core/file0.py:3", anchor) == "ok"

    # cambiar la línea citada SÍ marca stale; borrar el fichero => orphan
    target.write_text(original.replace("line 3 of", "REAL CHANGE of"), encoding="utf-8")
    assert evidence_state(repo, "mod0/core/file0.py:3", anchor) == "stale"
    target.unlink()
    assert evidence_state(repo, "mod0/core/file0.py:3", anchor) == "orphan"


def test_anchor_claims_quarantines_ghost_paths(tmp_path):
    repo = _make_repo(tmp_path)
    _clean, raw = parse_claims_block(PAGE_WITH_CLAIMS)
    anchored, dropped, repaired = anchor_claims(repo, raw)
    assert len(anchored) == 1 and dropped == 1 and repaired == 0
    assert anchored[0]["id"].startswith("c-") and anchored[0]["ehash"]


def test_resolve_citation_unique_suffix_only():
    from isidore.claims import resolve_citation
    known = {"apps/web/src/App.tsx", "apps/mobile/src/Main.tsx", "pkg/util.py"}
    # shortened path resolves to the unique real file
    assert resolve_citation("src/App.tsx", known) == "apps/web/src/App.tsx"
    assert resolve_citation("App.tsx", known) == "apps/web/src/App.tsx"
    # ambiguous suffix (src/ matches two) -> None (never guess)
    assert resolve_citation("src", known) is None
    # unknown -> None
    assert resolve_citation("ghost/x.py", known) is None
    assert resolve_citation("util.py", known) == "pkg/util.py"


def test_anchor_claims_repairs_shortened_path(tmp_path):
    # a claim citing a shortened path is REPAIRED (not dropped) when it uniquely matches a real file
    real = tmp_path / "apps" / "web" / "src"
    real.mkdir(parents=True)
    (real / "App.tsx").write_text("export const App = () => null\n", encoding="utf-8")
    raw = [{"statement": "App is defined", "evidence": "src/App.tsx:1"}]
    anchored, dropped, repaired = anchor_claims(
        tmp_path, raw, known_files={"apps/web/src/App.tsx"})
    assert dropped == 0 and repaired == 1
    assert anchored[0]["evidence"] == "apps/web/src/App.tsx:1"


def test_claim_id_stable_and_distinct():
    assert claim_id("a", "b:1") == claim_id("a", "b:1")
    assert claim_id("a", "b:1") != claim_id("a", "b:2")


def test_check_claims_states_ok_stale_orphan(tmp_path):
    repo = _make_repo(tmp_path)
    _clean, raw = parse_claims_block(PAGE_WITH_CLAIMS)
    anchored, _, _ = anchor_claims(repo, raw)
    pages_state = {"mod0-core.md": {"claims": anchored}}

    assert [r["state"] for r in check_claims(repo, pages_state)] == ["ok"]

    target = repo / "mod0" / "core" / "file0.py"
    target.write_text(target.read_text(encoding="utf-8").replace("line 3", "EDITED"),
                      encoding="utf-8")
    assert [r["state"] for r in check_claims(repo, pages_state)] == ["stale"]
    assert stale_pages(repo, pages_state) == {"mod0-core.md"}

    target.unlink()
    assert [r["state"] for r in check_claims(repo, pages_state)] == ["orphan"]


def test_render_claims_reports_summary(tmp_path):
    repo = _make_repo(tmp_path)
    _clean, raw = parse_claims_block(PAGE_WITH_CLAIMS)
    anchored, _, _ = anchor_claims(repo, raw)
    out = render_claims(repo, {"p.md": {"claims": anchored}}, "beef")
    assert "claims[1]" in out and "0 stale/orphan" in out and "beef" in out


# ------------------------------------------------- integración con el compile

def test_compile_stores_claims_and_writes_claims_toon(tmp_path):
    repo = _make_repo(tmp_path)
    result = compile_wiki(repo, graph_path=_gp(repo), execute=True,
                          generator=lambda p: PAGE_WITH_CLAIMS)
    assert result.claims_total == 1 and result.claims_dropped == 1
    claims_toon = (repo / "wiki" / "claims.toon").read_text(encoding="utf-8")
    assert "claims[1]" in claims_toon
    page = (repo / "wiki" / "mod0-core.md").read_text(encoding="utf-8")
    assert "isidore-claims" not in page


def test_stale_claim_forces_page_regeneration_without_llm_detection(tmp_path):
    repo = _make_repo(tmp_path)
    compile_wiki(repo, graph_path=_gp(repo), execute=True,
                 generator=lambda p: PAGE_WITH_CLAIMS)

    # cambio FUERA de las ventanas de extracto del contexto (línea 9; extractos centran L3±25...
    # el claim está anclado a la LÍNEA CITADA (file0.py:3); mutarla la marca stale y fuerza
    # regenerar SOLO esa página (aunque el contexto ensamblado no se moviera).
    prev_state = json.loads((repo / "wiki" / ".isidore-state.json").read_text(encoding="utf-8"))
    target = repo / "mod0" / "core" / "file0.py"
    target.write_text(target.read_text(encoding="utf-8").replace("line 3 of", "MUTATED of"),
                      encoding="utf-8")

    calls = []
    result = compile_wiki(repo, graph_path=_gp(repo), execute=True,
                          generator=lambda p: calls.append(p) or PAGE_WITH_CLAIMS)
    assert "mod0-core.md" in result.claims_stale_pages
    assert result.dirty == ["mod0-core.md"] and len(calls) == 1
    assert prev_state["pages"]["mod0-core.md"]["claims"], "el estado previo tenía el claim anclado"


def test_dry_run_still_detects_stale_claims_for_free(tmp_path):
    repo = _make_repo(tmp_path)
    compile_wiki(repo, graph_path=_gp(repo), execute=True,
                 generator=lambda p: PAGE_WITH_CLAIMS)
    target = repo / "mod0" / "core" / "file0.py"
    target.write_text(target.read_text(encoding="utf-8").replace("line 3 of", "MUTATED of"),
                      encoding="utf-8")

    calls = []
    result = compile_wiki(repo, graph_path=_gp(repo), execute=False,
                          generator=lambda p: calls.append(p) or "x")
    assert result.claims_stale_pages == ["mod0-core.md"]
    assert calls == [], "la detección de staleness jamás cuesta una llamada"
