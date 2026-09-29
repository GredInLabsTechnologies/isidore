> [!WARNING]
> **SECURITY — deterministic detectors flagged this code (0 LLM). Verify; never document as an intended feature.**
>
> - `tests/test_incremental.py:248` — high-entropy literal (>=24 chars, >=3.5 bits/char)
## Purpose

`tests/test_incremental.py` guards the incremental compile property: a page is rewritten only when what it describes changed, and then only the sections that must change. The docstring measures the problem it solved — before incremental, 5–12 of 40 pages were rewritten from nothing per commit, one page seven times in fifteen runs, because "dirty" was the hash of the whole prompt (git log, link counts, the template) and a dirty page was regenerated without even seeing its previous version (`tests/test_incremental.py:1-L6`).

The flow is real end-to-end: a git repository, the built-in scanner, `compile_wiki --execute`. Only the model is a stub, and it records every prompt it receives (`tests/test_incremental.py:8-L9`).

## Architecture

The module builds a controlled test environment around three helpers:

- `_source()` (`tests/test_incremental.py:47`) generates a Python module with twelve functions (`FUNCS`, `tests/test_incremental.py:23`) each returning a constant, plus 120 filler constants (`FILLER`, `tests/test_incremental.py:25`) — enough to keep the filler outside every excerpt window, so the excerpt content only changes when the function bodies change.

- `Model` (`tests/test_incremental.py:54`) is the stub generator. It records every prompt it receives (`self.prompts`) and answers either `FULL_PAGE` (for a fresh compile) or `self.revision` (for a revision prompt, which contains `CURRENT PAGE`). Setting `revision` to `NO-CHANGES` simulates the model saying "nothing to update"; setting it to a section simulates a real edit.

- `repo()` (`tests/test_incremental.py:67`) is the pytest fixture that creates a git repository with a seed commit holding a small `pkg` package: a core module with the twelve functions, a user module that imports from it, and the package's init file.

`_compile()` ties it together: `write_scan` builds the graph, then `compile_wiki` runs the pipeline with `execute=True`, `min_symbols=5`, and `max_calls=0` (no cap). `_commit()` wraps add-all + commit for the test cases that modify the source between compiles.

`FULL_PAGE` (`tests/test_incremental.py:27`) is the canned response for first-time generation. It includes two claims (`core defines alpha` and `beta returns 1`) so the test can verify that claims are carried across incremental revisions.

Beside the end-to-end cases, the module tests the pure parts of `src/isidore/revise.py` directly — `splice`, `strip_security_banner` and `carry_claims` — imported at `tests/test_incremental.py:21`.

## Key entry points

- `Model` — the stub generator that records prompts and controls revision behaviour (`tests/test_incremental.py:54`).
- `repo()` — the pytest fixture creating a git repo with a seed commit (`tests/test_incremental.py:67`).
- `_compile()` — runs `write_scan` + `compile_wiki` with `execute=True`.
- `test_the_first_compile_writes_full_pages` — verifies the first compile generates pages and records a facts fingerprint.
- `test_a_commit_that_changes_nothing_the_page_describes_rewrites_nothing` — the regression test: a commit changing only filler constants (outside every excerpt window) must not rewrite any page.

## Dependencies

- `src/isidore/pipeline.py` — for `compile_wiki` and `load_state` (`tests/test_incremental.py:20`).
- `src/isidore/revise.py` — for `carry_claims`, `splice` and `strip_security_banner`, tested directly (`tests/test_incremental.py:21`).
- `src/isidore/claims.py` — for `evidence_hash`, used to build an anchored claim for the carry-over test.
- `src/isidore/graph.py` — for `write_scan` (`tests/test_incremental.py:19`).
- `src/isidore/__init__.py` — imported as `from isidore import pipeline` (`tests/test_incremental.py:18`).

## How to change safely

1. Keep `Model` simple: it must record prompts verbatim so assertions can inspect what the compiler asked the model.
2. Keep `FILLER` high enough that filler constants stay outside every excerpt window — if the excerpt radius grows, increase it.
3. When adding a new test case, use `_commit()` to change the source and `_compile()` to re-run, then assert on `res.generated` vs `res.revised`.
