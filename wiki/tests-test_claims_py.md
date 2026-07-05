## Purpose  
`tests/test_claims.py` validates the core *claims* subsystem of Isidore. It checks that claim blocks are parsed correctly, that evidence hashes are computed deterministically from cited source lines, and that the *staleness* logic (`evidence_state`) correctly classifies unchanged, whitespace‑only, or line‑shifted citations as “ok”, while detecting real content changes as “stale” and missing files as “orphan”. The module also contains a fixture for creating a synthetic repository used by the tests.

## Architecture  
The file is a pure‑Python pytest module. Its structure is:

1. **Imports** – pulls in the public API of `isidore.claims` and the compilation helper from `isidore.pipeline` (e.g. `anchor_claims`, `evidence_hash`, `parse_claims_block`, etc.)【tests/test_claims.py:8】.  
2. **Test data** – a multi‑line string `PAGE_WITH_CLAIMS` that contains an `isidore-claims` block and an `isidore-findings` block【tests/test_claims.py:19】.  
3. **Fixtures** – `_make_repo` builds a temporary repository with 12 dummy source files (each 10 lines) and a `graph.json` describing a simple call graph【tests/test_claims.py:33‑49】; `_gp` returns the path to that JSON file【tests/test_claims.py:52‑53】.  
4. **Test cases** – four explicit tests cover parsing (`test_parse_claims_block_extracts_and_stips`), evidence hashing (`test_evidence_hash_is_the_cited_line_content`), staleness detection (`test_evidence_state_ignores_neighbors_whitespace_and_line_shifts`), and a placeholder for quarantine behavior (`test_anchor_claims_quarantines_ghost_paths`). Each test calls the imported claim functions and asserts concrete, observable outcomes.

The module has no external dependencies beyond the standard library (`json`, `pathlib`) and the Isidore packages it imports. No other code imports this test file.

## Key entry points  

| Symbol | Role |
|--------|------|
| `_make_repo(tmp_path: Path) -> Path` | Builds a reproducible “repo” with synthetic source files and a `graph.json` used by the other tests【tests/test_claims.py:33‑49】 |
| `_gp(repo: Path) -> Path` | Helper that returns the path to the generated `graph.json`【tests/test_claims.py:52‑53】 |
| `test_parse_claims_block_extracts_and_stips()` | Ensures `parse_claims_block` strips the claim fence, preserves surrounding text, and extracts correct evidence rows【tests/test_claims.py:58‑62】 |
| `test_evidence_hash_is_the_cited_line_content()` | Verifies deterministic 12‑char hashes for valid citations, `None` for missing/out‑of‑range citations, and that modifying the cited line changes the hash【tests/test_claims.py:66‑77】 |
| `test_evidence_state_ignores_neighbors_whitespace_and_line_shifts()` | Checks that only the cited line’s content matters for staleness: neighbor edits, whitespace changes, and line insertions are ignored, while content changes mark “stale” and file deletion marks “orphan”【tests/test_claims.py:80‑103】 |
| `test_anchor_claims_quarantines_ghost_paths()` | Declared but body not shown; intended to test that ghost‑path citations are quarantined. |

## Dependencies  
* **Standard library** – `json`, `pathlib`.  
* **Isidore packages** – `isidore.claims` (functions listed above) and `isidore.pipeline.compile_wiki`【tests/test_claims.py:7‑18】.  
No other modules depend on this test file.

## How to change safely  
1. **Preserve the synthetic repo layout** – `_make_repo` is relied on for deterministic file contents; altering the number of files, their line counts, or the location of `graph.json` can break hash‑based expectations (e.g., `evidence_hash` length and determinism). If you need a different fixture, add a new helper rather than modifying the existing one.  
2. **Keep assertion expectations aligned with the claim API** – the tests encode the contract of `parse_claims_block`, `evidence_hash`, and `evidence_state`. When the underlying implementation changes (e.g., hash length or staleness policy), update the corresponding `assert` lines, not the fixture data.  
3. **Do not rename imported symbols** – the test imports a fixed set of symbols from `isidore.claims`; removing or renaming any of them will cause import errors.  
4. **When extending tests, add new `def test_…` functions** – avoid altering existing test bodies unless you have simultaneously updated the production code they verify.  
5. **Run the full test suite after changes** – the repository’s CI expects all tests, including these, to pass; a failing assertion indicates a contract regression.
