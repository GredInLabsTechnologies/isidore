> [!WARNING]
> **SECURITY — deterministic detectors flagged this code (0 LLM). Verify; never document as an intended feature.**
>
> - `src/isidore/detectors.py:29` — credential-shaped literal (-----BEGIN prefix)
> - `src/isidore/detectors.py:29` — credential-shaped literal (AIza prefix)
> - `src/isidore/detectors.py:29` — credential-shaped literal (AKIA prefix)
> - `src/isidore/detectors.py:29` — credential-shaped literal (gho_ prefix)
> - `src/isidore/detectors.py:29` — credential-shaped literal (ghp_ prefix)
> - `src/isidore/detectors.py:29` — credential-shaped literal (glpat- prefix)
> - `src/isidore/detectors.py:29` — credential-shaped literal (ya29. prefix)
> - `src/isidore/detectors.py:34` — eval()
> - `src/isidore/detectors.py:35` — exec()
> - `src/isidore/detectors.py:36` — os.system()
> - `src/isidore/detectors.py:38` — pickle.loads()
> - `src/isidore/detectors.py:39` — yaml.load() without Loader
> - `src/isidore/detectors.py:43` — eval()
> - `src/isidore/pcp.py:207` — high-entropy literal (>=24 chars, >=3.5 bits/char)
> - `src/isidore/reconcile.py:76` — high-entropy literal (>=24 chars, >=3.5 bits/char)
> - `src/isidore/reconcile.py:93` — high-entropy literal (>=24 chars, >=3.5 bits/char)
> - `src/isidore/reconcile.py:110` — high-entropy literal (>=24 chars, >=3.5 bits/char)
> - `src/isidore/reconcile.py:119` — high-entropy literal (>=24 chars, >=3.5 bits/char)
## Purpose
The `src/isidore` module is a compiler pipeline for generating and verifying structured documentation from code. It treats documentation as a derived artifact, not a primary source, and focuses on **deterministic, evidence-anchored claims** that can be automatically verified. The pipeline ensures that documentation remains accurate by tracking changes in code and flagging stale claims, reducing the need for manual review.

## Architecture
The module follows a **frozen seam** design (ADR-0033), where the core types and predicate grammar are defined in `pcp.py` and shared across five lanes (A–E). The pipeline consists of four stages:
1. **Plan**: Determine which pages need updating based on code changes.
2. **Assemble**: Gather context for each page from the codebase.
3. **Generate**: Use an LLM to produce prose and structured claims.
4. **Cache**: Store the results and track staleness.

Key invariants:
- **Fail-closed**: A claim is never marked as true if its verifier returns `UNDECIDABLE`.
- **Monotonic escalation**: Once a mark (e.g., a claim or finding) is created, it is never removed by the model.
- **Zero-LLM verification**: Certificates can be re-verified offline with no LLM calls.

## Key entry points
- `pipeline.py`: Orchestrates the compilation pipeline (`plan`, `assemble`, `generate`, `cache`).
- `verify.py`: Implements verifiers for typed claims (e.g., `defines`, `calls`, `imports`).
- `pcp.py`: Defines the core types, predicate grammar, and verifier registry.
- `graph.py`: Loads and scans the codebase into a structure graph.
- `claims.py`: Manages evidence-anchored claims with content hashing.
- `findings.py`: Harvests side observations (e.g., bugs, drift) during compilation.

## Dependencies
The module has **no cross-module dependencies** and relies only on the Python standard library (`ast`, `hashlib`, `subprocess`, etc.). It uses `git` as the source of truth for file changes and `graph.json` as the structure graph.

## How to change safely
- **Claims and verifiers**: New claim types must be added to `pcp.py` and implemented in `verify.py`. Ensure verifiers are fail-closed (return `UNDECIDABLE` for undecidable cases).
- **Pipeline stages**: Changes to `pipeline.py` must preserve the deterministic nature of the pipeline. LLM calls are bounded by `--max-calls` and a per-prompt character budget.
- **Graph and scanning**: Modifications to `graph.py` or `langspec.py` must ensure the graph remains tool-agnostic and compatible with external producers.
- **Staleness detection**: Changes to `claims.py` must maintain the content-hash anchor for claim-level staleness detection.
