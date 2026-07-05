"""Q&A over the compiled wiki + graph: one bounded LLM call, deterministic retrieval.

No embeddings, no vector store, no agent loop: relevance is plain keyword scoring against
module names, symbol labels and page contents — all of which the graph and the compiled wiki
already provide. The single call answers with `path:line` citations or says the evidence is
not there.
"""
from __future__ import annotations

import re
from pathlib import Path

from .graph import load_graph
from .pipeline import (
    DEFAULT_MODULE_DEPTH,
    WIKI_DIRNAME,
    assemble_context,
    plan_pages,
    read_excerpt,
)

QA_PROMPT = """You answer ONE question about a repository for a coding agent, using ONLY the evidence below
(wiki pages compiled from the repository's structure graph, plus exact source excerpts).

Question: {question}

Rules:
- Cite sources inline as `path:line` or as wiki page names, using ONLY what appears in the evidence.
- If the evidence does not answer the question, say exactly what is missing — do not guess.
- Be direct and short. No preamble.

EVIDENCE
========
{evidence}
"""

DEFAULT_MAX_EVIDENCE_CHARS = 24_000
_WORD = re.compile(r"[a-zA-Z_][a-zA-Z0-9_]{2,}")


def question_terms(question: str) -> set[str]:
    return {w.lower() for w in _WORD.findall(question)}


def score_text(terms: set[str], text: str) -> int:
    lowered = text.lower()
    return sum(lowered.count(t) for t in terms)


def gather_evidence(
    repo: Path,
    question: str,
    *,
    graph_path: Path,
    module_depth: int = DEFAULT_MODULE_DEPTH,
    max_chars: int = DEFAULT_MAX_EVIDENCE_CHARS,
) -> tuple[str, list[str]]:
    """Deterministic retrieval. Returns (evidence, list of sources used)."""
    terms = question_terms(question)
    nodes, links, _commit = load_graph(graph_path)
    wiki_dir = repo / WIKI_DIRNAME
    sources: list[str] = []
    parts: list[str] = []

    quickstart = wiki_dir / "quickstart.md"
    if quickstart.is_file():
        parts.append("--- wiki quickstart ---\n" + quickstart.read_text(encoding="utf-8",
                                                                        errors="replace"))
        sources.append("quickstart.md")

    # rank compiled pages (or assembled module contexts as fallback) by term overlap
    specs = plan_pages(nodes, links, module_depth=module_depth, top_k=None)
    scored = []
    for spec in specs:
        page = wiki_dir / spec.filename
        body = page.read_text(encoding="utf-8", errors="replace") if page.is_file() else ""
        score = score_text(terms, spec.name) * 5 + score_text(
            terms, " ".join(lbl for lbl, _f, _loc, _d in spec.hot_symbols)) * 3 + score_text(terms, body)
        if score:
            scored.append((score, spec, body))
    scored.sort(key=lambda t: -t[0])

    for _score, spec, body in scored[:2]:
        if body:
            parts.append(f"--- wiki page {spec.filename} ---\n{body}")
            sources.append(spec.filename)
        else:
            context, _warns = assemble_context(repo, spec, max_chars=max_chars // 3)
            parts.append(f"--- assembled facts for {spec.name} (page not compiled yet) ---\n{context}")
            sources.append(f"(facts) {spec.name}")

    # exact-symbol excerpts: nodes whose label matches a question term
    hits = 0
    for n in nodes:
        if hits >= 4 or n.get("file_type") != "code" or not n.get("source_file"):
            continue
        label = str(n.get("label", "")).lower().rstrip("()")
        if label and label in terms:
            excerpt = read_excerpt(repo, n["source_file"], n.get("source_location") or "")
            if excerpt:
                parts.append(excerpt)
                sources.append(f"{n['source_file']}:{(n.get('source_location') or '?').lstrip('L')}")
                hits += 1

    evidence = "\n\n".join(parts)
    if len(evidence) > max_chars:
        evidence = evidence[:max_chars]
    return evidence, sources


def ask(repo: Path, question: str, *, graph_path: Path, generator,
        module_depth: int = DEFAULT_MODULE_DEPTH) -> str:
    evidence, _sources = gather_evidence(repo, question, graph_path=graph_path,
                                         module_depth=module_depth)
    if not evidence.strip():
        return ("No evidence found for this question (no compiled wiki and no graph matches). "
                "Run `isidore compile` first or rephrase with symbol/module names.")
    return generator(QA_PROMPT.format(question=question, evidence=evidence))
