## Purpose

`src/isidore/revise.py` implements incremental page updates: change only what changed, keep the rest byte for byte (`src/isidore/revise.py:1`). Before this module, a page was "dirty" when the sha256 of its WHOLE prompt moved, and a dirty page was rewritten from nothing — the prompt did not even contain the previous version. The prompt carries things that say nothing about what the page should say (git log, link counts, symbol degrees, the prompt template itself), so a commit that fixed a comment or a new test that imported the module re-wrote whole pages. Measured on isidore's own wiki: 5 to 12 of 40 pages rewritten per commit, one page seven times in fifteen runs.

Two separate decisions, two separate fixes: WHETHER a page changed is decided by a semantic fingerprint; WHAT is rewritten is only the affected sections.

## Architecture

The module separates two concerns:

1. **Semantic fingerprinting** (`facts_record` at `src/isidore/revise.py:50`): what the module depends on, and a hash of each source excerpt's CODE (not its line numbers). No git log, no template. Counts, the modules that depend on this one (`deps_in`) and the test modules that exercise it (`tested_by`, `src/isidore/revise.py:62`) are recorded but never make a page dirty on their own (`src/isidore/revise.py:86`). A line shift, a new caller elsewhere, a new test, a new commit message: not a change.

2. **Section-level revision**: a dirty page that already exists gets a revision prompt — its current text plus the DELTA of facts (`facts_delta`) — and the model returns only the `##` sections that must change (or `NO-CHANGES`). `splice` replaces those and keeps every other section verbatim. Claims whose anchored line is still there are carried over at 0 LLM (`carry_claims`); the model adds claims only for what is new.

`--rewrite` (compile/handoff) restores full regeneration when that is what is wanted.

## Key entry points

- `facts_record(repo, spec, read_excerpt)` — the semantic facts a page's content depends on, in a comparable shape (`src/isidore/revise.py:50`).
- `facts_fingerprint(record)` — the identity of what a page describes: a sha256 over the record minus the keys in `_NOT_A_CHANGE` — the file and symbol counts, `deps_in` and `tested_by` (`src/isidore/revise.py:86`). A count that moved without any excerpt changing gives the model nothing to document; a new consumer of the module is documented on the consumer's own page, and `deps_in` is only the top few by link count, so one new consumer could push another off the list (`src/isidore/revise.py:82`); a new test of the module is news for the page's test list, not for its prose (`src/isidore/revise.py:85`). The filtering happens right before hashing (`src/isidore/revise.py:93`).
- `facts_delta(old, new, repo, spec, read_excerpt)` — what changed between two fact records, as FACTS the model can cite; counts, new consumers and new tests are still shown when something else made the page dirty (`src/isidore/revise.py:113-L114`).
- `_excerpt_code(excerpt)` — an excerpt's code without its header and line-number gutter (`src/isidore/revise.py:43`).
- `_h(text)` — sha256 truncated to 16 hex chars (`src/isidore/revise.py:39-L40`).

## Dependencies

The module depends on `src/isidore/claims.py` for claim-related operations. It is imported by `src/isidore/pipeline.py`, and its pure parts — `splice`, `strip_security_banner`, `carry_claims` — are tested directly by `tests/test_incremental.py`.

## How to change safely

1. Preserve the semantic fingerprint's invariance to non-semantic changes (line shifts, git log, counts).
2. Compare fingerprints by recomputing BOTH sides from the stored and the current record with the current rule (`src/isidore/revise.py:85-L87`). Comparing against a fingerprint stored under an older rule would turn any change to `_NOT_A_CHANGE` or to `facts_record` into every page going dirty at once — the stampede the module exists to end.
3. Keep `facts_delta` output citable by the model — it must be plain FACTS, not summaries.
4. Maintain the `NO-CHANGES` contract: the model returns it when nothing semantic changed, and the splicer leaves the page untouched.
5. The `read_excerpt` parameter is injected to keep this module independent of pipeline.py.
