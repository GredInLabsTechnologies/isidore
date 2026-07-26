## Purpose
The `src/isidore/verify.py` module implements verifiers for typed claims in the Isidore system, ensuring that predicates (e.g., "function X is called in file Y") are validated against the codebase. It acts as the decision engine for the system's Proof-Carrying Prose (PCP) framework, where claims are verified using multiple oracles (graph.json, AST parsing, and textual scans) to produce tamper-evident certificates. The module enforces a fail-closed policy: any claim that cannot be decided definitively is marked as `UNDECIDABLE`, never defaulting to `TRUE`.

## Architecture
The module is structured around verifiers that consult different oracles:
1. **Graph Oracle**: Uses `graph.json` to check structural claims (e.g., symbol definitions, imports).
2. **AST Oracle**: Parses source files to verify claims about function signatures, calls, or values.
3. **Grep Oracle**: Scans source files for environment variables or other textual patterns.
4. **Language-Specific Oracle**: Reserved for framework-specific rules (currently `UNDECIDABLE`).

Each verifier returns a `Verdict` (`TRUE`, `FALSE`, or `UNDECIDABLE`) and records its oracle. The module includes helper functions to normalize paths, extract symbols, and parse ASTs, which are used by the verifiers.

## Key entry points
- **`_symbol_nodes`**: Finds graph nodes matching a symbol name (e.g., `authenticate`).
- **`_file_nodes`**: Retrieves graph nodes associated with a file path.
- **`_ast_of`**: Parses a Python file into an AST for signature/value verification.
- **`_find_funcdef`**: Locates a function definition in an AST by name.

These helpers are used by verifiers to resolve claims against the oracles.

## Dependencies
- **`src/isidore/graph.py`**: Provides `load_graph` and `find_graph` for graph operations.
- **`src/isidore/pcp.py`**: Defines constants (`TRUE`, `FALSE`, `UNDECIDABLE`) and types (`Predicate`, `Verdict`).

## How to change safely
1. **Add a new verifier**: Use `register_verifier` to add a new claim type. Ensure it consults the appropriate oracle and returns a `Verdict`.
2. **Modify oracles**: Extend the AST or grep logic in `_ast_of` or `_read_source` if new claim types require additional parsing.
3. **Update helpers**: Add new helper functions (e.g., for class verification) but avoid breaking existing ones, as they are used by multiple verifiers.
