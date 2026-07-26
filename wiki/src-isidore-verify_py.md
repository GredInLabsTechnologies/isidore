## Purpose
`src/isidore/verify.py` implements Lane A of the Proof-Carrying Prose (PCP) system, which verifies typed claims against code and generates tamper-evident certificates. The module's verifiers decide a `Predicate`'s truth by consulting two oracles: the `graph.json` (for defines/exports/imports) and a reparse of the cited file's AST (for calls/value/signature). It ensures fail-closed behavior, where `UNDECIDABLE` never masquerades as `TRUE`, and certificates can be re-verified offline without LLM (`isidore verify`). The verifiers return `TRUE`, `FALSE`, or `UNDECIDABLE` and record their oracle usage. | `src/isidore/verify.py:1`

## Architecture
The module consists of oracle helper functions and verifiers that work with `VerifyContext` to evaluate claims. The key components are:
- Path normalization (`_norm`) and symbol extraction (`_symbol_base`, `_symbol_nodes`).
- File and source handling (`_file_nodes`, `_read_source`, `_ast_of`).
- AST traversal (`_find_funcdef`) to locate function definitions. | `src/isidore/verify.py:43`

## Key entry points
The module is not directly called but is used by `src/isidore/pipeline.py` and `src/isidore/whatsnew.py` to verify claims. The verifiers are registered via `register_verifier` from `src/isidore/pcp.py`. | `src/isidore/verify.py:36`

## Dependencies
The module depends on `src/isidore/graph.py` (for `find_graph`, `load_graph`) and `src/isidore/pcp.py` (for `Predicate`, `Verdict`, `Certificate`, and other PCP-related types). | `src/isidore/verify.py:18`

## How to change safely
When modifying `verify.py`, ensure that:
1. All verifiers remain fail-closed (no `UNDECIDABLE` masquerading as `TRUE`).
2. Oracle usage is accurately recorded for each verdict.
3. Changes to AST parsing or file handling do not introduce false positives or negatives.
4. The module's interface with `pcp.py` remains stable. | `src/isidore/verify.py:9`
