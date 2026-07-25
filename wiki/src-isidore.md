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
`src/isidore` is a tool for generating and verifying documentation that is anchored to the codebase's structure and content. It addresses the gap between hand-written changelogs and the need for machine-verifiable documentation. The module provides a two-tier approach: a deterministic delta analysis (0 LLM) and a prose generation tier (one LLM call per changed module). The core property is claim-level staleness detection, where each claim is anchored to a content hash of the cited lines, enabling zero-LLM verification of documentation freshness (`src/isidore/whatsnew.py:L1`).

## Architecture
The module follows a pipeline architecture (`src/isidore/pipeline.py:L1`) where the graph of the codebase is first analyzed (`src/isidore/graph.py:L1`), then used to plan and generate documentation. The pipeline is deterministic except for the single bounded LLM call per dirty page. The graph is loaded from a JSON file (`src/isidore/graph.py:L5`) and can be generated automatically with zero dependencies for any language (`src/isidore/graph.py:L17`). The documentation is generated in a Proof-Carrying Prose (PCP) format (`src/isidore/pcp.py:L1`), where each claim is verified against the code (`src/isidore/verify.py:L1`).

## Key entry points
- `whatsnew.py`: Generates changelogs with a focus on the delta between git revisions (`src/isidore/whatsnew.py:L1`).
- `pipeline.py`: Orchestrates the documentation generation pipeline (`src/isidore/pipeline.py:L1`).
- `verify.py`: Verifies claims against the codebase (`src/isidore/verify.py:L1`).
- `pcp.py`: Defines the Proof-Carrying Prose framework and predicate grammar (`src/isidore/pcp.py:L1`).
- `graph.py`: Handles the structure graph and multi-language scanning (`src/isidore/graph.py:L1`).
- `claims.py`: Manages the atomic, evidence-anchored claims (`src/isidore/claims.py:L1`).

## Dependencies
The module has no cross-module dependencies (`depends on (cross-module, link count): (none)`). It relies on the Python standard library (`src/isidore/graph.py:L26`) and git for source of truth (`src/isidore/pipeline.py:L23`).

## How to change safely
1. **Deterministic changes**: For changes that do not involve the LLM, ensure they are anchored to specific lines of code and do not introduce new behavior without evidence.
2. **LLM changes**: When modifying the LLM prompts or behavior, ensure the changes are bounded and do not increase the number of LLM calls per page.
3. **Claim verification**: When adding or modifying claims, ensure they are anchored to specific lines of code and can be verified against the codebase (`src/isidore/claims.py:L1`).
4. **Graph updates**: If the graph format is changed, ensure backward compatibility with existing graph producers (`src/isidore/graph.py:L11`).
