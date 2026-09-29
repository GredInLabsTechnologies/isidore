## Purpose

`src/isidore/citations.py` keeps the `path:line` references in a page's prose pointing at the code they cite as that code moves (`src/isidore/citations.py:1`). Claims were already anchored by the content of the line they cite, so a claim survives lines shifting above it; prose was not. Once incremental compiles stopped rewriting pages whose facts had not changed, a kept section's citations drifted a few lines with every edit above them (`src/isidore/citations.py:3-L8`). This module anchors a citation the way a claim is anchored and re-points it at 0 LLM.

## Architecture

Three operations over one fingerprint (`src/isidore/citations.py:10-L21`):

- **Anchoring.** `_fingerprint` identifies a cited line by its normalised text together with the next non-empty lines, up to `_CONTEXT` lines in all, and also records the line on its own (`src/isidore/citations.py:45-L58`). One line alone — a `return result`, a closing bracket — matches too many places to relocate safely, and a line shorter than `_MIN_CHARS` is not tracked at all (`src/isidore/citations.py:39`, `src/isidore/citations.py:50`). `anchors_for` maps every `path:line` of an existing file to its fingerprint, and a citation whose line identifies nothing to `UNANCHORED` (`src/isidore/citations.py:113`): it is remembered as unanchorable, so it never adopts whatever content an edit later slides onto that line (`src/isidore/citations.py:109-L112`).
- **Re-pointing.** `repoint` looks for each fingerprint again and rewrites the line number; a range keeps its length. `_relocate` searches for the whole window nearest first; if the lines below the cited one changed but the cited line did not, it falls back to that line alone — but only when it occurs exactly once in the file (`src/isidore/citations.py:67-L78`). A citation it cannot place is left as written and reported stale (`src/isidore/citations.py:15-L17`).
- **Migration.** `migrate_by_symbol` handles pages written before anchors existed. It moves a citation only when it can validate the move against the symbol the sentence names, and leaves anything else alone (`src/isidore/citations.py:18-L21`).

Every operation reads citations through `_matches`, which skips anything inside a code fence — a path in a fence is an example, not a citation (`src/isidore/citations.py:81-L86`, `src/isidore/citations.py:23`). Rewrites are applied from the end of the text backwards by `_rewrite`, so earlier match offsets stay valid (`src/isidore/citations.py:93-L96`), and `_render` rebuilds a citation in the form it was written, `path:a` or a range (`src/isidore/citations.py:89-L90`). `_Files` caches each cited file's lines for one pass (`src/isidore/citations.py:99-L106`).

## Key entry points

- `anchors_for(repo, markdown)` — `path:line` → fingerprint for a page, `UNANCHORED` where a line identifies nothing.
- `repoint` — re-points a page's citations from their stored fingerprints.
- `migrate_by_symbol` — the conservative one-time repair for pages with no stored fingerprints.
- `CITE` — the citation pattern: a path with an extension, a line, and an optional `-a` or `-La` end (`src/isidore/citations.py:32-L33`).

## Dependencies

It reuses the normalisation, hashing and file reading of `src/isidore/claims.py` (`src/isidore/citations.py:30`), so a citation and a claim anchored to the same line see it identically. It also depends on `src/isidore/pcp.py` and `src/isidore/verify.py`. It is used by `src/isidore/pipeline.py` and tested by `tests/test_citations.py`.

## How to change safely

1. Keep a fingerprint wider than one line (`_CONTEXT`, `src/isidore/citations.py:38`); a single-line fingerprint relocates a common line to the wrong copy.
2. Keep the search nearest-first within `RADIUS` (`src/isidore/citations.py:37`), so a duplicated block resolves to the copy that was cited.
3. Treat the migration's limits as safety rails, not tuning knobs: `_ADJACENT`, `_SYMBOL_REACH` and `_NEAR_REACH` bound when a symbol may be paired with a citation and how far its definition may have moved (`src/isidore/citations.py:40-L42`). Loosening them lets the migration "fix" citations that were correct.
4. Never re-point inside a code fence; keep every citation read through `_matches`.
