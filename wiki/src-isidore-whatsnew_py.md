## Purpose
The `whatsnew.py` module generates verifiable changelogs by comparing the API surface of a codebase at two git revisions. It operates in two tiers: a deterministic delta tier (free, zero-LLM) that extracts typed changes (symbols added/removed, signatures changed, files added/removed/renamed), and an optional LLM tier that produces human-readable summaries anchored to the delta. The module ensures changelogs are trustworthy by requiring every claim to be citable to a specific `path:line` in the code, with refuted claims kept in a certificate but never published. This addresses the gap between machine-readable diffs and human-readable changelogs, which are often unreliable due to hallucinations in LLM-generated summaries.

## Architecture
The module defines three core data structures:
1. `DeltaEntry` — a typed novelty row with fields like `kind` (added/removed/changed), `file`, `qualname`, and `line`, plus methods to determine the change's evidence (`evidence`) and area (`area` — API, internal, tests, or docs).
2. `SurfaceDelta` — a container for all changes between two revisions, including the refs, SHAs, and lists of `DeltaEntry` objects, with methods to filter entries by area.
3. `WhatsnewResult` — the final output, combining the delta with paths to generated artifacts (wiki page, certificate, TOON diagram) and metrics (LLM calls, refuted claims, etc.).

The module also includes git plumbing functions (`_git`, `resolve_ref`) to safely interact with the repository, failing closed on errors to avoid false claims.

## Key entry points
- `DeltaEntry` — the atomic unit of change, with properties to classify and cite changes.
- `SurfaceDelta` — the structured delta between two revisions, with methods to filter and summarize changes.
- `WhatsnewResult` — the final output, combining the delta with generated artifacts and metrics.

## Dependencies
The module depends on:
- `src/isidore/plain.py` (2) — for plain-language summaries.
- `src/isidore/claims.py` (1) — for certificate generation.
- `src/isidore/graph.py` (1) — for TOON diagram generation.
- `src/isidore/langspec.py` (1) — for language-specific parsing.
- `src/isidore/pcp.py` (1) — for plain-language rules.
- `src/isidore/pipeline.py` (1) — for LLM pipeline execution.
- `src/isidore/render.py` (1) — for wiki page rendering.
- `src/isidore/surface.py` (1) — for API surface extraction.

## How to change safely
1. **Add a new change kind**: Extend `_WRITABLE_KINDS` in `src/isidore/whatsnew.py:83` to include the new kind, ensuring it is citable to the current tree.
2. **Modify area classification**: Adjust `_TEST_MARKERS` or `_DOC_SUFFIXES` in `src/isidore/whatsnew.py:95` to update how files are categorized.
3. **Update git commands**: Modify `_git` in `src/isidore/whatsnew.py:180` to handle new git operations, ensuring failures are raised as `WhatsnewError`.
4. **Add a new output format**: Extend `WhatsnewResult` in `src/isidore/whatsnew.py:163` to include paths for new artifact types.
