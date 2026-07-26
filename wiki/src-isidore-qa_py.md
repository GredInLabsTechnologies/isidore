## Purpose
The `src/isidore/qa.py` module provides a deterministic, LLM-free Q&A system over a compiled wiki and repository structure graph. It retrieves evidence by scoring verified claims (machine-checked facts with `path:line` anchors) and other repository artifacts against a question, then formats the results for direct consumption by coding agents. The design avoids embeddings, vector stores, or iterative agent loops by relying on the existing graph and wiki structure, ensuring answers are always grounded in verifiable repository data.

## Architecture
The module consists of three main components:
1. **Term extraction and scoring**: `question_terms()` filters out stopwords and `score_text()` counts term matches in text.
2. **Evidence gathering**: `gather_claims()` retrieves and scores verified claims, while `gather_evidence()` assembles a comprehensive response from claims, wiki pages, and code excerpts.
3. **Offline answering**: `answer_offline()` provides answers using only verified claims, with no LLM calls, or refuses if no confident match is found.

## Key entry points
- `answer_offline()`: The primary interface for offline Q&A, returning answers from verified claims.
- `gather_evidence()`: Assembles evidence for LLM-based answers, combining claims, wiki pages, and code excerpts.
- `question_terms()` and `score_text()`: Core utilities for term extraction and relevance scoring.

## Dependencies
- `src/isidore/graph.py`: For loading the repository structure graph.
- `src/isidore/pipeline.py`: For accessing compiled wiki pages and utilities like `read_excerpt()`.
- `src/isidore/claims.py`: For checking verified claims.
- `src/isidore/knowledge.py`: For loading knowledge claims.

## How to change safely
1. **Add new evidence sources**: Extend `gather_evidence()` to include additional repository artifacts (e.g., tests, documentation) while preserving the existing structure.
2. **Modify scoring logic**: Adjust `score_text()` or `question_terms()` to improve relevance, but ensure backward compatibility with existing evidence formats.
3. **Add offline answer rules**: Extend `answer_offline()` to handle new claim types or scoring thresholds, but maintain the deterministic refusal behavior when no confident match is found.
