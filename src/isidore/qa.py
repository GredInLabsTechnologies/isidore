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

# Common English function words are dropped from the query: without this a claim scores a false
# match on stopwords like "the"/"for" (e.g. every claim containing "the session") and the --offline
# path would answer an unrelated question instead of refusing. Domain words are never in this set.
_STOPWORDS = frozenset({
    "the", "and", "for", "are", "was", "were", "with", "that", "this", "from", "into", "your",
    "you", "how", "does", "did", "what", "why", "who", "whom", "where", "when", "which", "whose",
    "has", "have", "had", "not", "but", "its", "their", "there", "here", "then", "than", "them",
    "they", "our", "out", "get", "got", "can", "could", "would", "should", "will", "shall", "may",
    "might", "must", "about", "over", "under", "between", "using", "use", "used", "via", "per",
})


def question_terms(question: str) -> set[str]:
    return {w for w in (w.lower() for w in _WORD.findall(question)) if w not in _STOPWORDS}


def score_text(terms: set[str], text: str) -> int:
    lowered = text.lower()
    return sum(lowered.count(t) for t in terms)


def gather_claims(repo: Path, question: str) -> list[tuple[int, dict]]:
    """Score every anchored claim (verified atomic fact) against the question. Claims are the
    cheapest, highest-signal evidence there is — a checked statement with a `path:line` anchor."""
    from .claims import check_claims
    from .pipeline import load_state
    terms = question_terms(question)
    state = load_state(repo / WIKI_DIRNAME)
    scored: list[tuple[int, dict]] = []
    for row in check_claims(repo, state.get("pages", {})):
        score = score_text(terms, row["statement"]) * 3 + score_text(terms, row["evidence"])
        if score:
            scored.append((score, row))
    scored.sort(key=lambda t: -t[0])
    # de-dup identical statements (the same claim can ride several pages) keeping the best score
    seen: set[str] = set()
    deduped: list[tuple[int, dict]] = []
    for score, row in scored:
        key = f"{row['statement']}\x00{row['evidence']}"
        if key not in seen:
            seen.add(key)
            deduped.append((score, row))
    return deduped


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

    # Verified claims first — cheapest signal per token, each already anchored to a path:line.
    claims = gather_claims(repo, question)
    if claims:
        parts.append("--- verified claims (anchored, machine-checked facts) ---\n" + "\n".join(
            f"- {row['statement']} [{row['evidence']}] ({row['state']})" for _s, row in claims[:6]))
        sources.extend(f"claim [{row['evidence']}]" for _s, row in claims[:6])

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


OFFLINE_MIN_SCORE = 3      # >= one statement-term hit (statement matches are weighted x3)


def answer_offline(repo: Path, question: str) -> str:
    """Answer from verified claims with ZERO LLM calls, or refuse honestly. Never fabricates."""
    claims = gather_claims(repo, question)
    if not claims or claims[0][0] < OFFLINE_MIN_SCORE:
        return ("No confident offline answer: no verified claim matched strongly enough. "
                "Re-run without --offline for a full-evidence LLM answer, or rephrase with the "
                "exact symbol/module name.")
    lines = ["Offline answer from verified claims (0 LLM calls):"]
    for _score, row in claims[:5]:
        flag = "" if row["state"] == "ok" else f"  ⚠ {row['state']}"
        lines.append(f"- {row['statement']} [{row['evidence']}]{flag}")
    return "\n".join(lines)


def gather_knowledge_claims(question: str) -> list[tuple[int, dict]]:
    from .claims import check_claims
    from .knowledge import load_knowledge_state
    terms = question_terms(question)
    state = load_knowledge_state()
    scored: list[tuple[int, dict]] = []
    # repo is Path(".") because src:// resolver does not need physical repo path
    for row in check_claims(Path("."), state.get("pages", {})):
        score = score_text(terms, row["statement"]) * 3 + score_text(terms, row["evidence"])
        if score:
            scored.append((score, row))
    scored.sort(key=lambda t: -t[0])
    seen: set[str] = set()
    deduped: list[tuple[int, dict]] = []
    for score, row in scored:
        key = f"{row['statement']}\x00{row['evidence']}"
        if key not in seen:
            seen.add(key)
            deduped.append((score, row))
    return deduped


def answer_knowledge_offline(question: str) -> str:
    claims = gather_knowledge_claims(question)
    if not claims or claims[0][0] < OFFLINE_MIN_SCORE:
        return ("No confident offline answer: no verified knowledge claim matched strongly enough. "
                "Re-run without --offline for a full-evidence LLM answer.")
    lines = ["Offline answer from verified knowledge base claims (0 LLM calls):"]
    for _score, row in claims[:5]:
        flag = "" if row["state"] == "ok" else f"  ⚠ {row['state']}"
        lines.append(f"- {row['statement']} [{row['evidence']}]{flag}")
    return "\n".join(lines)


def ask_knowledge(question: str, generator, offline: bool = False) -> str:
    if offline:
        return answer_knowledge_offline(question)

    from .knowledge import knowledge_dir, load_knowledge_state
    wiki_dir = knowledge_dir()
    state = load_knowledge_state()
    pages_state = state.get("pages", {})

    parts: list[str] = []

    # 1. Claims
    claims = gather_knowledge_claims(question)
    if claims:
        parts.append("--- verified claims (anchored, machine-checked facts) ---\n" + "\n".join(
            f"- {row['statement']} [{row['evidence']}] ({row['state']})" for _s, row in claims[:6]))

    # 2. Topic Pages
    terms = question_terms(question)
    scored = []
    for page_name, entry in pages_state.items():
        page = wiki_dir / page_name
        body = page.read_text(encoding="utf-8", errors="replace") if page.is_file() else ""
        score = score_text(terms, page_name) * 5 + score_text(terms, body)
        if score:
            scored.append((score, page_name, body))
    scored.sort(key=lambda t: -t[0])

    for _score, page_name, body in scored[:2]:
        if body:
            parts.append(f"--- knowledge page {page_name} ---\n{body}")

    evidence = "\n\n".join(parts)
    if not evidence.strip():
        return ("No evidence found in knowledge base for this question. "
                "Run `isidore sync --execute` first.")

    if len(evidence) > DEFAULT_MAX_EVIDENCE_CHARS:
        evidence = evidence[:DEFAULT_MAX_EVIDENCE_CHARS]

    return generator(QA_PROMPT.format(question=question, evidence=evidence))


def ask(repo: Path, question: str, *, graph_path: Path, generator,
        module_depth: int = DEFAULT_MODULE_DEPTH, offline: bool = False,
        knowledge: bool = False) -> str:
    if knowledge:
        return ask_knowledge(question, generator, offline)
    if offline:
        return answer_offline(repo, question)
    evidence, _sources = gather_evidence(repo, question, graph_path=graph_path,
                                         module_depth=module_depth)
    if not evidence.strip():
        return ("No evidence found for this question (no compiled wiki and no graph matches). "
                "Run `isidore compile` first or rephrase with symbol/module names.")
    return generator(QA_PROMPT.format(question=question, evidence=evidence))
