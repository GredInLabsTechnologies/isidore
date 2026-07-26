## What this area is responsible for
The `src` area implements Isidore's core documentation pipeline, transforming a codebase into a verified, agent-oriented wiki. It bridges the gap between raw source code and human-readable documentation by extracting structure, detecting security patterns, and compiling verifiable knowledge artifacts. The area's responsibility is to ensure that documentation is always up-to-date, tamper-evident, and aligned with the codebase's actual state.

## How the work is divided
The area splits responsibilities along the pipeline's logical stages:
- **Changeset analysis** (`changeset.py`) maps Git diffs to code symbols, enabling incremental updates.
- **Security detection** (`detectors.py`) identifies sensitive patterns (entropy, sinks, topology) before they reach the wiki.
- **Knowledge compilation** (`knowledge.py`, `pipeline.py`) generates the wiki's prose and verifiable claims.
- **Verification** (`pcp.py`, `verify.py`) ensures claims are cryptographically tied to the code.
- **Output generation** (`render.py`, `humanpack.py`) produces deterministic artifacts (HTML, PDF, changelogs).

The split reflects the pipeline's stages: from raw diffs to verified documentation. Modules are grouped by function, with dependencies flowing linearly through the pipeline.

## What it depends on, and what depends on it
This area has no external dependencies but provides the foundation for Isidore's user-facing features. It depends on Git for diffs and Python's standard library for parsing. Other areas (e.g., connectors) rely on its verified documentation outputs, while the CLI (`cli.py`) exposes its functionality to users.

## Where to start reading
- For understanding how changes propagate to the wiki, start with `changeset.py`.
- To see how claims are verified, read `pcp.py` and `verify.py`.
- For the core compilation logic, begin with `pipeline.py` and `knowledge.py`.
- To explore the security detectors, open `detectors.py`.
