"""`isidore recertify`: repair a certificate the code outgrew, and refuse to repair a page the code
now contradicts. 0 LLM either way — nothing in this file injects a generator, because nothing can.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from isidore.pcp import CERT_SUFFIX, FALSE, TRUE, UNDECIDABLE, Certificate, ClaimVerdict, VerifiedMass, prose_hash, read_certificate, write_certificate
from isidore.recertify import ACT_NO_CERT, ACT_RECERTIFY, ACT_REFUTED, ACT_TAMPERED, recertify
from isidore.verify import CERT_DRIFTED, CERT_OK, certificate_status, verify_page

PAGE = "# svc\n\nThe request limit is fixed and the handler reads it.\n"


def _repo(tmp_path, *, limit: int = 5) -> Path:
    root = tmp_path / "proj"
    (root / ".isidore").mkdir(parents=True)
    (root / "wiki").mkdir()
    (root / "svc.py").write_text(f"LIMIT = {limit}\n\n\ndef handler(request):\n    return LIMIT\n",
                                 encoding="utf-8")
    graph = {"nodes": [{"id": "n1", "source_file": "svc.py", "file_type": "code",
                        "label": "handler()", "source_location": "L4"}], "links": []}
    (root / ".isidore" / "graph.json").write_text(json.dumps(graph), encoding="utf-8")
    (root / "wiki" / "svc.md").write_text(PAGE, encoding="utf-8")
    return root


def _cert(root, claims: list[ClaimVerdict], *, page: str = "svc.md", prose: str = PAGE,
          mass: VerifiedMass | None = None, children: dict | None = None) -> None:
    write_certificate(
        Certificate(page=page, prose_sha256=prose_hash(prose), claims=claims,
                    mass=mass or VerifiedMass(), child_cert_hashes=dict(children or {})),
        root / "wiki" / f"{page}{CERT_SUFFIX}")


def _claim(cid="c-1", predicate="defines:svc.py;LIMIT", verdict=FALSE) -> ClaimVerdict:
    return ClaimVerdict(id=cid, statement="the module defines LIMIT", evidence="svc.py:1",
                        ehash="aa", predicate=predicate, verdict=verdict, oracle="graph")


# ------------------------------------------------------------------ the case that motivated this

def test_a_certificate_the_code_outgrew_is_repaired_without_a_model_call(tmp_path):
    """The GIMO case: a module-level constant an older extractor could not see. The page was MORE
    correct than its certificate, and `verify` punished it with no supported way out."""
    root = _repo(tmp_path)
    _cert(root, [_claim(verdict=FALSE)])          # recorded FALSE; the current oracle proves TRUE
    assert verify_page(root, root / "wiki" / "svc.md")[0] is False

    result = recertify(root, write=True)
    assert [p.action for p in result.pages] == [ACT_RECERTIFY]
    assert result.written == ["svc.md"]
    assert verify_page(root, root / "wiki" / "svc.md")[0] is True
    assert read_certificate(root / "wiki" / f"svc.md{CERT_SUFFIX}").claims[0].verdict == TRUE


def test_the_prose_is_not_touched(tmp_path):
    root = _repo(tmp_path)
    _cert(root, [_claim()])
    before = (root / "wiki" / "svc.md").read_bytes()
    recertify(root, write=True)
    assert (root / "wiki" / "svc.md").read_bytes() == before


def test_a_dry_run_reports_but_writes_nothing(tmp_path):
    root = _repo(tmp_path)
    _cert(root, [_claim()])
    stamp = (root / "wiki" / f"svc.md{CERT_SUFFIX}").read_bytes()

    result = recertify(root)
    assert [p.action for p in result.pages] == [ACT_RECERTIFY] and result.written == []
    assert (root / "wiki" / f"svc.md{CERT_SUFFIX}").read_bytes() == stamp


def test_the_verified_mass_is_recomputed_not_carried_over(tmp_path):
    # The verdicts moved, so which sentences count as proved moved with them. Copying the old mass
    # would leave the page's own honesty meter reporting the previous run.
    root = _repo(tmp_path)
    _cert(root, [_claim()], mass=VerifiedMass(green=0, yellow=1, gray=0))
    recertify(root, write=True)
    assert read_certificate(root / "wiki" / f"svc.md{CERT_SUFFIX}").mass.green == 1


# ------------------------------------------------------------------ what it refuses to do

def test_a_published_claim_the_code_now_denies_is_never_recertified(tmp_path):
    """TRUE -> FALSE is the one direction that means a sentence a reader sees is wrong. Rewriting
    the certificate would turn a wrong page green; the page needs new prose."""
    root = _repo(tmp_path, limit=9)                       # the code says 9, the certificate said 5
    _cert(root, [_claim(predicate="value:LIMIT;5", verdict=TRUE)])

    result = recertify(root, write=True)
    assert [p.action for p in result.pages] == [ACT_REFUTED]
    assert result.written == []
    assert read_certificate(root / "wiki" / f"svc.md{CERT_SUFFIX}").claims[0].verdict == TRUE


def test_a_page_edited_after_compile_is_refused(tmp_path):
    # Recertifying here would certify text no verifier ever looked at — laundering a hand edit.
    root = _repo(tmp_path)
    _cert(root, [_claim()])
    (root / "wiki" / "svc.md").write_text(PAGE + "\nAnd something a human added.\n", encoding="utf-8")

    result = recertify(root, write=True)
    assert [p.action for p in result.pages] == [ACT_TAMPERED] and result.written == []


def test_a_page_that_was_never_certified_is_left_to_compile(tmp_path):
    root = _repo(tmp_path)                                 # no certificate written at all
    result = recertify(root, write=True)
    assert [p.action for p in result.pages] == [ACT_NO_CERT] and result.written == []


def test_losing_the_ability_to_prove_a_claim_is_recorded_not_refused(tmp_path):
    # TRUE -> UNDECIDABLE is not a refutation: the sentence is not contradicted, the oracle just
    # cannot see it any more. Recording that honestly moves the sentence from green to yellow.
    root = _repo(tmp_path)
    _cert(root, [_claim(predicate="defines:gone.py;LIMIT", verdict=TRUE)])
    result = recertify(root, write=True)

    assert [p.action for p in result.pages] == [ACT_RECERTIFY]
    cert = read_certificate(root / "wiki" / f"svc.md{CERT_SUFFIX}")
    assert cert.claims[0].verdict == UNDECIDABLE
    assert cert.mass.green == 0 and cert.mass.yellow == 1


# ------------------------------------------------------------------ the chain (lane D)

def _chained(tmp_path):
    """A parent page resting on svc.md through a wiki:// chain, with the child hash recorded."""
    import hashlib
    root = _repo(tmp_path)
    _cert(root, [_claim(verdict=FALSE)])
    child_bytes = (root / "wiki" / f"svc.md{CERT_SUFFIX}").read_bytes()
    parent_prose = "# overview\n\nThe request limit is fixed.\n"
    (root / "wiki" / "overview.md").write_text(parent_prose, encoding="utf-8")
    _cert(root, [ClaimVerdict(id="p-1", statement="the limit is fixed",
                              evidence="wiki://svc.md#c-1",
                              ehash=hashlib.sha256(child_bytes).hexdigest()[:12],
                              predicate="wikichain:wiki://svc.md#c-1", verdict=FALSE,
                              oracle="wiki")],
          page="overview.md", prose=parent_prose,
          children={"svc.md": hashlib.sha256(child_bytes).hexdigest()})
    return root


def test_children_are_recertified_before_the_pages_that_cite_them(tmp_path):
    # A wikichain claim reads the child's certificate live off disk: recertify the parent first and
    # it composes the child's OLD verdict, then goes stale the moment the child is rewritten.
    root = _chained(tmp_path)
    result = recertify(root, write=True)
    assert result.written == ["svc.md", "overview.md"]

    parent = read_certificate(root / "wiki" / f"overview.md{CERT_SUFFIX}")
    assert parent.claims[0].verdict == TRUE          # the child now proves what the parent cites
    assert verify_page(root, root / "wiki" / "overview.md")[0] is True


def test_a_child_certificate_that_moved_is_visible_in_the_parent(tmp_path):
    """The property the pyramid advertises: edit a page below and it shows up above with no model
    call. It only holds if something checks the recorded hash — nothing did."""
    root = _chained(tmp_path)
    recertify(root, write=True)                      # everything current
    assert certificate_status(root, root / "wiki" / "overview.md").status == CERT_OK

    # Touch only the child's certificate. The parent's claims still verify; its provenance does not.
    child_path = root / "wiki" / f"svc.md{CERT_SUFFIX}"
    cert = read_certificate(child_path)
    cert.claims.append(_claim(cid="c-2", predicate="defines:svc.py;handler", verdict=TRUE))
    write_certificate(cert, child_path)

    st = certificate_status(root, root / "wiki" / "overview.md")
    assert st.status == CERT_DRIFTED and st.children_moved == ("svc.md",)
    assert recertify(root, write=True).written == ["overview.md"]
    assert certificate_status(root, root / "wiki" / "overview.md").status == CERT_OK


def test_a_child_certificate_that_vanished_drops_out_instead_of_surviving_forever(tmp_path):
    # Carrying the recorded hash over when the child is gone leaves the page drifted after every
    # repair — a loop that never converges.
    root = _chained(tmp_path)
    (root / "wiki" / f"svc.md{CERT_SUFFIX}").unlink()
    (root / "wiki" / "svc.md").unlink()

    recertify(root, write=True)
    assert read_certificate(root / "wiki" / f"overview.md{CERT_SUFFIX}").child_cert_hashes == {}
    assert recertify(root).of(ACT_RECERTIFY) == []


# ------------------------------------------------------------------ the disagreement with compile

def test_compile_now_owns_only_the_drift_that_needs_prose(tmp_path):
    """The bug in one assertion: `compile` reported dirty: 0 for a page `verify` reported FAIL.

    It splits in two now. A page whose published claim is refuted is dirty (it needs a new page). A
    page whose certificate merely fell behind the oracles is NOT dirty — it is recertify's, free.
    """
    from isidore.pipeline import compile_wiki

    root = _repo(tmp_path, limit=9)
    (root / "svc2.py").write_text("OTHER = 1\n\n\ndef helper():\n    return OTHER\n",
                                  encoding="utf-8")
    graph = json.loads((root / ".isidore" / "graph.json").read_text(encoding="utf-8"))
    graph["nodes"].append({"id": "n2", "source_file": "svc2.py", "file_type": "code",
                           "label": "helper()", "source_location": "L4"})
    (root / ".isidore" / "graph.json").write_text(json.dumps(graph), encoding="utf-8")

    refuted_page, free_page = "svc_py.md", "svc2_py.md"
    (root / "wiki" / "svc.md").unlink()
    for name in (refuted_page, free_page):
        (root / "wiki" / name).write_text(PAGE, encoding="utf-8")
    _cert(root, [_claim(predicate="value:LIMIT;5", verdict=TRUE)], page=refuted_page)
    _cert(root, [_claim(verdict=FALSE)], page=free_page)

    # Both pages are otherwise clean: their stored context hash is the one compile computes now, so
    # the ONLY thing that can make either dirty is its certificate.
    state = {"pages": {n: {"context_hash": _context_hash_for(root, n)} for n in
                       (refuted_page, free_page)}}
    (root / "wiki" / ".isidore-state.json").write_text(json.dumps(state), encoding="utf-8")

    result = compile_wiki(root, graph_path=root / ".isidore" / "graph.json", execute=False,
                          min_symbols=1)
    assert result.certs_refuted == [refuted_page]
    assert result.certs_repairable == [free_page]
    assert result.dirty == [refuted_page]
    assert any("isidore recertify" in w for w in result.warnings)


def _context_hash_for(root, name):
    """Recompute the context hash compile would store for a page, so the test can pin it as 'clean'."""
    from isidore.graph import load_graph
    from isidore.pipeline import assemble_context, context_hash, plan_pages, prompt_for
    nodes, links, _commit = load_graph(root / ".isidore" / "graph.json")
    for spec in plan_pages(nodes, links, module_depth=3, top_k=None, min_symbols=1):
        if spec.filename == name:
            context, _w = assemble_context(root, spec)
            return context_hash(prompt_for(spec, context))
    raise AssertionError(f"no spec planned for {name}")


@pytest.mark.parametrize("kind", ["missing", "unreadable"])
def test_a_page_with_no_usable_certificate_never_stampedes_a_recompile(tmp_path, kind):
    # Wikis compiled before certificates existed have none. Treating that as drift would send every
    # page back through the model on the next run.
    from isidore.pipeline import compile_wiki

    root = _repo(tmp_path)
    if kind == "unreadable":
        (root / "wiki" / f"svc.md{CERT_SUFFIX}").write_text("{not json", encoding="utf-8")
    result = compile_wiki(root, graph_path=root / ".isidore" / "graph.json", execute=False,
                          min_symbols=1)
    assert result.certs_refuted == [] and result.certs_repairable == []
