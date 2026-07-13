"""The knowledge core: user-defined topics compile + 0-LLM suggest topics (ADR-0032 F2).

Presents a unified compilation path for external streams in the knowledge home (~/.isidore/knowledge).
Topics are defined in ~/.isidore/topics.json.
"""
from __future__ import annotations

import json
import os
import re
import time
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path

from .home import home, safe_chmod, safe_mkdir
from .llm import default_generator
from .claims import (
    CLAIMS_PROMPT_ADDENDUM,
    anchor_claims,
    is_negative_existential,
    parse_claims_block,
    stale_pages,
)
from .findings import (
    FINDINGS_PROMPT_ADDENDUM,
    filter_findings,
    parse_findings_block,
)

TOPIC_PROMPT = """You are writing ONE page of a knowledge base that coding agents read before touching a repository.

Write a Markdown page describing the topic `{name}` using ONLY the facts below. Every fact is an ingested item from our knowledge base — treat it as ground truth and do not invent details that are not evidenced below.

Structure (use these exact section headings):
## Overview
## Ingested Findings
## Synthesis & Key Takeaways

Rules:
- Cite sources inline as `src://<cid>[/<instance>]/<item-id>` using ONLY paths that appear in the facts.
- Describe only what IS evidenced.
- Max ~600 words. No preamble, no closing remarks — start directly with the first heading.

FACTS
=====
{facts}
"""


@dataclass
class TopicCompileResult:
    planned: int = 0
    dirty: list[str] = field(default_factory=list)
    generated: list[str] = field(default_factory=list)
    skipped_by_cap: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    claims_total: int = 0
    claims_dropped: int = 0
    claims_repaired: int = 0
    claims_dropped_negative: int = 0
    findings_kept: int = 0
    findings_dropped: int = 0
    findings_dropped_negative: int = 0
    claims_stale_pages: list[str] = field(default_factory=list)
    quarantined: list[str] = field(default_factory=list)
    retries: int = 0
    lint_findings: dict[str, list[str]] = field(default_factory=dict)
    security_flagged: list[str] = field(default_factory=list)
    pruned: list[str] = field(default_factory=list)


def knowledge_dir() -> Path:
    d = home() / "knowledge"
    safe_mkdir(d)
    return d


def state_path() -> Path:
    return knowledge_dir() / ".state.json"


def load_knowledge_state() -> dict:
    p = state_path()
    if not p.is_file():
        return {"version": 1, "pages": {}}
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {"version": 1, "pages": {}}
    if not isinstance(data, dict) or data.get("version") != 1:
        return {"version": 1, "pages": {}}
    data.setdefault("pages", {})
    return data


def write_knowledge_state(state: dict) -> None:
    p = state_path()
    safe_mkdir(p.parent)
    tmp = p.with_name(p.name + f".tmp{os.getpid()}")
    tmp.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
    safe_chmod(tmp, 0o600)
    os.replace(tmp, p)


def load_topics() -> list[dict]:
    p = home() / "topics.json"
    if not p.is_file():
        return []
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return []
    if isinstance(data, list):
        return [t for t in data if isinstance(t, dict) and t.get("name")]
    if isinstance(data, dict):
        topics = []
        for name, conf in data.items():
            if isinstance(conf, dict):
                topics.append({"name": name, **conf})
        return topics
    return []


def suggest_topics(top_n: int = 8) -> list[dict]:
    """Algorithmically suggest topics from ingested raw items (0-LLM, term frequency based)."""
    from .connectors.store import iter_items
    conn_root = home() / "connectors"
    connectors: list[tuple[str, str | None]] = []
    if conn_root.is_dir():
        for cdir in conn_root.iterdir():
            if not cdir.is_dir():
                continue
            cid = cdir.name
            if (cdir / "raw").is_dir():
                connectors.append((cid, None))
            for inst_dir in cdir.iterdir():
                if inst_dir.is_dir() and (inst_dir / "raw").is_dir():
                    connectors.append((cid, inst_dir.name))

    word_stream_freq = defaultdict(Counter)
    stopwords = {
        "this", "that", "with", "from", "have", "they", "will", "your", "what", "about",
        "their", "there", "would", "these", "code", "file", "line", "item", "stream",
        "date", "time", "user", "name", "type", "meta", "data", "status"
    }

    for cid, inst in connectors:
        for item in iter_items(cid, inst):
            stream = item.get("stream", "default")
            content = item.get("content", "")
            words = re.findall(r"\b[a-zA-Z]{4,15}\b", content.lower())
            for w in words:
                if w not in stopwords:
                    word_stream_freq[w][stream] += 1

    ranked = sorted(word_stream_freq.items(), key=lambda kv: -sum(kv[1].values()))[:top_n]
    suggestions = []
    for term, stream_counts in ranked:
        streams = [s for s, _count in stream_counts.most_common(2)]
        suggestions.append({
            "name": f"topic-{term}",
            "streams": streams,
            "filtros": [term],
            "top_k_items": 10
        })
    return suggestions


def assemble_topic_context(topic: dict) -> tuple[str, list[str]]:
    """Assemble items matching streams and filters into citable facts."""
    from .connectors.store import iter_items
    cid_inst_pairs = []
    conn_root = home() / "connectors"
    if conn_root.is_dir():
        for cdir in conn_root.iterdir():
            if not cdir.is_dir():
                continue
            cid = cdir.name
            if (cdir / "raw").is_dir():
                cid_inst_pairs.append((cid, None))
            for inst_dir in cdir.iterdir():
                if inst_dir.is_dir() and (inst_dir / "raw").is_dir():
                    cid_inst_pairs.append((cid, inst_dir.name))

    streams = topic.get("streams", [])
    filtros = [f.lower() for f in topic.get("filtros", []) if f.strip()]
    top_k = topic.get("top_k_items", 10)

    matched_items = []
    for cid, inst in cid_inst_pairs:
        for item in iter_items(cid, inst):
            if streams and item.get("stream") not in streams:
                continue
            content = item.get("content", "")
            if filtros:
                lowered_content = content.lower()
                lowered_id = str(item.get("id", "")).lower()
                lowered_stream = str(item.get("stream", "")).lower()
                if not any(f in lowered_content or f in lowered_id or f in lowered_stream for f in filtros):
                    continue
            matched_items.append((cid, inst, item))

    matched_items.sort(key=lambda x: x[2].get("ts", ""), reverse=True)

    facts = []
    warnings = []
    for cid, inst, item in matched_items[:top_k]:
        inst_part = f"/{inst}" if inst else ""
        uri = f"src://{cid}{inst_part}/{item.get('id')}"
        facts.append(
            f"--- excerpt {uri} ---\n"
            f"Stream: {item.get('stream')}\n"
            f"Timestamp: {item.get('ts')}\n"
            f"Content:\n"
            f"{item.get('content', '')}"
        )

    return "\n\n".join(facts), warnings


def compile_topics(
    execute: bool = False,
    max_calls: int = 10,
    generator=None,
) -> TopicCompileResult:
    """Compile dirty topic pages based on topics.json configurations."""
    result = TopicCompileResult()
    topics = load_topics()
    result.planned = len(topics)
    if not topics:
        return result

    state = load_knowledge_state()
    pages_state = state.setdefault("pages", {})

    claim_stale = stale_pages(Path("."), pages_state)
    result.claims_stale_pages = sorted(claim_stale)

    contexts = {}
    for t in topics:
        name = t["name"]
        filename = f"{name}.md"
        context, warns = assemble_topic_context(t)
        result.warnings.extend(warns)
        
        prompt = TOPIC_PROMPT.format(name=name, facts=context)
        prompt += CLAIMS_PROMPT_ADDENDUM + FINDINGS_PROMPT_ADDENDUM
        
        import hashlib
        digest = hashlib.md5(prompt.encode("utf-8")).hexdigest()
        contexts[filename] = (t, prompt, digest)

        prev = pages_state.get(filename, {})
        if (prev.get("context_hash") != digest
                or filename in claim_stale
                or not (knowledge_dir() / filename).is_file()):
            result.dirty.append(filename)

    def _dirty_key(fname: str) -> tuple:
        prev = pages_state.get(fname, {})
        return (0 if prev.get("pending") else 1, 0 if fname in claim_stale else 1, fname)
    result.dirty.sort(key=_dirty_key)

    if not execute:
        result.skipped_by_cap = result.dirty[max_calls:]
        for name in result.skipped_by_cap:
            result.warnings.append(f"{name}: dirty but over compile cap (pending)")
        return result

    generate = generator if generator is not None else default_generator()
    calls_made = 0

    for filename in result.dirty:
        if calls_made >= max_calls:
            result.skipped_by_cap.append(filename)
            pages_state.setdefault(filename, {})["pending"] = True
            result.warnings.append(f"{filename}: dirty but over compile cap (pending)")
            continue

        topic, prompt, digest = contexts[filename]
        try:
            raw = generate(prompt)
        except Exception as exc:
            result.warnings.append(f"LLM compilation failed for {filename}: {exc}")
            continue

        calls_made += 1
        markdown, raw_claims = parse_claims_block(raw)
        markdown, page_findings = parse_findings_block(markdown)

        clean_claims = [c for c in raw_claims if not is_negative_existential(c.get("statement", ""))]
        result.claims_dropped_negative += (len(raw_claims) - len(clean_claims))

        clean_findings = [f for f in page_findings if not is_negative_existential(f.get("note", ""))]
        result.findings_dropped_negative += (len(page_findings) - len(clean_findings))

        claims, claims_dropped, claims_repaired = anchor_claims(Path("."), clean_claims)
        result.claims_total += len(claims)
        result.claims_dropped += claims_dropped
        result.claims_repaired += claims_repaired

        kept, dropped = filter_findings(clean_findings, Path("."))
        result.findings_kept += len(kept)
        result.findings_dropped += len(dropped)

        wiki_file = knowledge_dir() / filename
        wiki_file.write_text(markdown, encoding="utf-8", newline="\n")

        iso_now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        pages_state[filename] = {
            "context_hash": digest,
            "compiled_at": iso_now,
            "claims": claims,
            "findings": kept,
        }
        result.generated.append(filename)

    eligible_files = {f"{t['name']}.md" for t in topics}
    for filename in list(pages_state.keys()):
        if filename not in eligible_files:
            del pages_state[filename]
            (knowledge_dir() / filename).unlink(missing_ok=True)
            result.pruned.append(filename)

    write_knowledge_state(state)
    return result
