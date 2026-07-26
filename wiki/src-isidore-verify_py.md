## Purpose
`src/isidore/verify.py` implements the "Lane A" verifiers for the Proof-Carrying Prose (PCP) system, which checks typed claims against the codebase. The module's core function is to validate `Predicate` objects by consulting two oracles: the `graph.json` (for structural facts like imports/exports) and the re-parsed AST of the cited file (for runtime behavior like calls/values/signatures). The verifiers are fail-closed: they return `TRUE`, `FALSE`, or `UNDECIDABLE`, with `UNDECIDABLE` never masquerading as `TRUE`. This ensures certificates can be re-verified offline without LLM dependency (`isidore verify`).

## Architecture
The module is organized around oracle helpers and verifiers. The oracle helpers (`_norm`, `_symbol_base`, `_symbol_nodes`, `_file_nodes`, `_read_source`, `_ast_of`, `_find_funcdef`) provide low-level access to the codebase and its graph representation. These helpers are used by the verifiers to gather evidence for deciding predicate truth. The verifiers themselves are registered via `register_verifier` and operate on a `VerifyContext` containing the repository path and graph nodes.

## Key entry points
The most connected symbol is the module itself (`verify.py`), which is imported by `src/isidore/pipeline.py`, `src/isidore/recertify.py`, and `src/isidore/whatsnew.py`. The module exposes the `register_verifier` decorator and `undecidable` function for verifier registration and handling undecidable verdicts, respectively.

## Dependencies
The module depends on `src/isidore/graph.py` (for graph loading) and `src/isidore/pcp.py` (for PCP constants and types). It imports `ast`, `re`, and `dataclasses` from the standard library, and `Path` from `pathlib`.

## How to change safely
When modifying `verify.py`, focus on the oracle helpers and verifiers. The oracle helpers should be updated carefully, as they are used by all verifiers. New verifiers should be registered using `register_verifier`. When adding or modifying verifiers, ensure they follow the fail-closed principle and handle `UNDECIDABLE` cases appropriately. The module's design allows for adding new verifiers without changing existing ones, as long as they adhere to the `VerifyContext` interface.
