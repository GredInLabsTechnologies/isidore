"""The wiki is OUTPUT. It must never round-trip into the input.

Reported from GIMO at isidore d5d1a1f, with numbers: `doc/isidore` was indexed as source, `plan_pages`
treated it as a module, and `compile` wrote a page documenting the documentation. Its certificate came
to **13 MB and 405,704 lines — 2 claims, 31,207 marks, 31,202 reconciler violations**, 26% of every
line in the repository, because prose about the wiki has no stable ground truth to be checked against.

isidore's own repo escaped the page by an accident of naming (`wiki/` splits per-file under its module
depth) while carrying 113 output nodes in its graph regardless — which is exactly why the name-based
`SKIP_DIRS` was not enough: `ISIDORE_WIKI_DIR` can be nested, and a name never matches `doc/isidore`.
"""
from __future__ import annotations

import json

import pytest

from isidore.graph import _is_wiki_output, scan_repo, wiki_output_prefix
from isidore.pipeline import (
    MAX_CERT_VIOLATIONS,
    degenerate_certificate,
    drop_wiki_output,
    plan_pages,
)


@pytest.fixture()
def nested_wiki_dir(monkeypatch):
    """Point the toolchain at GIMO's layout. WIKI_DIRNAME is resolved once at import so every module
    agrees on one directory; the constant is what has to move, not the environment."""
    import isidore.render
    monkeypatch.setattr(isidore.render, "WIKI_DIRNAME", "doc/isidore")
    return "doc/isidore"


@pytest.fixture()
def repo_with_nested_wiki(tmp_path, nested_wiki_dir):
    """GIMO's shape: the wiki lives several directories deep, at whatever the toolchain resolved."""
    root = tmp_path / "proj"
    wiki = root / nested_wiki_dir
    (root / "src" / "app").mkdir(parents=True)
    wiki.mkdir(parents=True)

    (root / "src" / "app" / "core.py").write_text(
        "def handle(request):\n    return 1\n\n\ndef helper():\n    return 2\n", encoding="utf-8")
    # ...and the output of a previous compile, sitting in the tree exactly as the org convention says
    for i in range(6):
        (wiki / f"page-{i}.md").write_text(
            f"# Page {i}\n\nProse about `src/app/core.py:1` and its helpers.\n", encoding="utf-8")
    (root / "doc" / "isidore" / "index.toon").write_text("pages[0]{file}:\n", encoding="utf-8")
    (root / "doc" / "isidore" / "page-0.md.cert.json").write_text('{"page": "page-0.md"}',
                                                                  encoding="utf-8")
    return root


@pytest.mark.usefixtures("nested_wiki_dir")
def test_the_prefix_is_a_path_not_a_name():
    assert wiki_output_prefix() == "doc/isidore"

    assert _is_wiki_output("doc/isidore", "doc/isidore")
    assert _is_wiki_output("doc/isidore/page-1.md", "doc/isidore")
    # a name-based skip would have matched neither of the first two, and wrongly matched the last
    assert not _is_wiki_output("doc/isidore-notes.md", "doc/isidore")
    assert not _is_wiki_output("src/isidore/render.py", "doc/isidore")
    assert not _is_wiki_output("anything", "")


def test_the_scanner_does_not_index_its_own_output(repo_with_nested_wiki):
    nodes, _links = scan_repo(repo_with_nested_wiki)
    sources = {str(n.get("source_file", "")) for n in nodes}

    assert any(s.endswith("src/app/core.py") for s in sources)          # real source is indexed
    assert not [s for s in sources if s.startswith("doc/isidore")]      # output is not


@pytest.mark.usefixtures("nested_wiki_dir")
def test_no_page_is_planned_for_the_wiki_itself():
    """The second barrier: a graph can arrive from `--graph` or Graphify, whose producers walk the
    filesystem and have no reason to know which directory is ours."""
    foreign = [
        {"id": "n1", "source_file": "src/app/core.py", "file_type": "code", "label": "handle()",
         "source_location": "L1"},
        {"id": "n2", "source_file": "src/app/core.py", "file_type": "code", "label": "helper()",
         "source_location": "L5"},
    ] + [
        {"id": f"w{i}", "source_file": f"doc/isidore/page-{i}.md", "file_type": "document",
         "label": f"page-{i}", "source_location": "L1"} for i in range(40)
    ]

    assert len(drop_wiki_output(foreign)) == 2
    specs = plan_pages(foreign, [], module_depth=2, top_k=None, min_symbols=1)
    assert specs and all(not s.name.startswith("doc/isidore") for s in specs)


def test_a_compile_of_a_repo_with_a_committed_wiki_stays_clean(repo_with_nested_wiki):
    """End to end: scan then plan, the way a caller runs it."""
    from isidore.graph import load_graph, write_scan

    graph_path = write_scan(repo_with_nested_wiki)
    nodes, links, _commit = load_graph(graph_path)
    specs = plan_pages(nodes, links, module_depth=2, top_k=None, min_symbols=1)

    assert not any("isidore" in s.filename for s in specs)
    assert json.loads(graph_path.read_text(encoding="utf-8"))["nodes"]


# ------------------------------------------------------------------ the loud failure

class _Cert:
    def __init__(self, claims=0, violations=0, marks=0):
        self.claims = [object()] * claims
        self.violations = [object()] * violations
        self.marks = [object()] * marks


def test_a_certificate_that_is_a_symptom_is_refused():
    """GIMO's actual numbers. Writing this silently is how it reached 13 MB before anyone looked."""
    reason = degenerate_certificate(_Cert(claims=2, violations=31_202, marks=31_207))
    assert reason and "31202 violations" in reason.replace(",", "")

    assert degenerate_certificate(_Cert(claims=2, marks=31_207)) is not None


def test_a_healthy_certificate_is_not_touched():
    # isidore's own busiest page: 20 claims, no violations. Nowhere near the cap.
    assert degenerate_certificate(_Cert(claims=20, violations=0, marks=3)) is None
    assert degenerate_certificate(_Cert(claims=5, violations=40, marks=10)) is None
    # A page with many claims is ALLOWED many findings — the cap is not a flat ceiling, it is a ratio
    # plus a floor, so a genuinely rich page is never punished for being rich.
    assert degenerate_certificate(_Cert(claims=100, violations=MAX_CERT_VIOLATIONS + 1)) is None
