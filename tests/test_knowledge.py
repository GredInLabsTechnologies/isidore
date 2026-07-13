import json
from pathlib import Path

from isidore.claims import _split_evidence, evidence_hash, evidence_state
from isidore.findings import filter_findings
from isidore.knowledge import (
    suggest_topics,
    compile_topics,
    knowledge_dir,
    load_knowledge_state,
)
import isidore.home
from isidore.connectors.store import write_items, create_run_id, resolve_uri


def test_split_evidence_src():
    # Simple URI
    uri, line = _split_evidence("src://git-repo/my-repo")
    assert uri == "src://git-repo/my-repo"
    assert line is None

    # URI with line number
    uri, line = _split_evidence("src://git-repo/my-repo:42")
    assert uri == "src://git-repo/my-repo"
    assert line == 42

    # URI with L prefixed line
    uri, line = _split_evidence("src://git-repo/my-repo:L100")
    assert uri == "src://git-repo/my-repo"
    assert line == 100


def test_evidence_hash_and_state_src(monkeypatch, tmp_path):
    # Set ISIDORE_HOME to tmp_path
    monkeypatch.setenv("ISIDORE_HOME", str(tmp_path))
    monkeypatch.setattr(isidore.home, "home", lambda: tmp_path)

    run_id = create_run_id()
    items = [
        {"id": "item1", "stream": "test-stream", "ts": "2026-07-12T10:00:00Z", "content": "Line 1\nLine 2\nLine 3"},
    ]
    # Write items to raw store
    write_items("git-repo", None, run_id, items)

    # Test resolve_uri works
    item = resolve_uri("src://git-repo/item1")
    assert item is not None
    assert item["chash"] is not None

    # 1. Test evidence_hash for whole file/item (no line number)
    h_whole = evidence_hash(Path("."), "src://git-repo/item1")
    assert h_whole == item["chash"]

    # 2. Test evidence_hash for specific line
    h_line = evidence_hash(Path("."), "src://git-repo/item1:2")
    assert h_line is not None

    # 3. Test evidence_state (ok)
    state = evidence_state(Path("."), "src://git-repo/item1:2", h_line)
    assert state == "ok"

    # 4. Test evidence_state (stale)
    state = evidence_state(Path("."), "src://git-repo/item1:2", "wronghash")
    assert state == "stale"

    # 5. Test evidence_state (orphan)
    state = evidence_state(Path("."), "src://git-repo/nonexistent", h_line)
    assert state == "orphan"

    # 6. Test evidence_state (superseded)
    # If compiled_at is older than the item ts
    state = evidence_state(Path("."), "src://git-repo/item1:2", h_line, compiled_at="2026-07-12T09:00:00Z")
    assert state == "superseded"

    # If compiled_at is newer than the item ts
    state = evidence_state(Path("."), "src://git-repo/item1:2", h_line, compiled_at="2026-07-12T11:00:00Z")
    assert state == "ok"


def test_suggest_topics(monkeypatch, tmp_path):
    monkeypatch.setenv("ISIDORE_HOME", str(tmp_path))
    monkeypatch.setattr(isidore.home, "home", lambda: tmp_path)

    run_id = create_run_id()
    items = [
        {"id": "item1", "stream": "tarot", "ts": "2026-07-12T10:00:00Z", "content": "tarot tarot login auth"},
        {"id": "item2", "stream": "tarot", "ts": "2026-07-12T10:00:00Z", "content": "tarot card card reading"},
    ]
    write_items("git-repo", None, run_id, items)

    suggestions = suggest_topics(top_n=3)
    assert len(suggestions) > 0
    # The most frequent word is "tarot"
    assert any(s["name"] == "topic-tarot" for s in suggestions)
    assert any("tarot" in s["streams"] for s in suggestions)


def test_compile_topics(monkeypatch, tmp_path):
    monkeypatch.setenv("ISIDORE_HOME", str(tmp_path))
    monkeypatch.setattr(isidore.home, "home", lambda: tmp_path)

    # 1. Write topics.json
    topics = [
        {
            "name": "my-topic",
            "streams": ["my-stream"],
            "filtros": ["python"],
            "top_k_items": 5
        }
    ]
    (tmp_path / "topics.json").write_text(json.dumps(topics), encoding="utf-8")

    # 2. Write raw items
    run_id = create_run_id()
    items = [
        {"id": "python-item", "stream": "my-stream", "ts": "2026-07-12T10:00:00Z", "content": "Python is a coding language."}
    ]
    write_items("git-repo", None, run_id, items)

    # 3. Compile topics (dry-run)
    res = compile_topics(execute=False)
    assert res.planned == 1
    assert "my-topic.md" in res.dirty

    # 4. Compile topics (execute)
    def dummy_generator(prompt):
        return (
            "## Overview\nThis is about Python.\n"
            "## Ingested Findings\n"
            "## Synthesis & Key Takeaways\n"
            "```isidore-claims\n"
            "Python is a coding language | src://git-repo/python-item:1\n"
            "```\n"
        )

    res2 = compile_topics(execute=True, generator=dummy_generator)
    assert "my-topic.md" in res2.generated

    # Check that file was written
    wiki_file = knowledge_dir() / "my-topic.md"
    assert wiki_file.is_file()
    assert "This is about Python" in wiki_file.read_text(encoding="utf-8")

    # Check state was written
    state = load_knowledge_state()
    assert "my-topic.md" in state["pages"]
    assert len(state["pages"]["my-topic.md"]["claims"]) == 1
    assert state["pages"]["my-topic.md"]["claims"][0]["statement"] == "Python is a coding language"


def test_filter_findings_with_src(monkeypatch, tmp_path):
    monkeypatch.setenv("ISIDORE_HOME", str(tmp_path))
    monkeypatch.setattr(isidore.home, "home", lambda: tmp_path)

    run_id = create_run_id()
    items = [
        {"id": "item-finding", "stream": "stream-finding", "ts": "2026-07-12T10:00:00Z", "content": "finding line"}
    ]
    write_items("git-repo", None, run_id, items)

    findings = [
        {"kind": "warning", "where": "src://git-repo/item-finding:1", "note": "Potential bug"},
        {"kind": "warning", "where": "src://git-repo/nonexistent:1", "note": "False bug"},
    ]

    kept, dropped = filter_findings(findings, Path("."))
    assert len(kept) == 1
    assert kept[0]["where"] == "src://git-repo/item-finding:1"
    assert len(dropped) == 1
    assert dropped[0]["where"] == "src://git-repo/nonexistent:1"
