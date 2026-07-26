## What this area is responsible for
The `src` area implements Isidore's core functionality for compiling and verifying documentation from a codebase. It bridges Git's version control with Isidore's graph model, detects security patterns, and generates verifiable documentation artifacts. The area's responsibility is to transform raw code and changes into structured knowledge while ensuring the documentation remains tamper-evident and up-to-date.

## How the work is divided
The modules split responsibilities along logical boundaries:
- **Changeset handling** (`changeset.py`) bridges Git diffs to Isidore's graph model.
- **Staleness detection** (`claims.py`) tracks documentation freshness by hashing evidence.
- **Security analysis** (`detectors.py`) identifies sensitive patterns in code.
- **Documentation generation** (`knowledge.py`, `pipeline.py`, `render.py`) compiles structured content.
- **Verification** (`pcp.py`, `verify.py`) ensures claims hold true against the codebase.

The split reflects Isidore's architecture: changesets feed into security analysis and documentation, while verification operates on the compiled graph. This separation keeps concerns distinct while allowing cross-module dependencies where needed.

## What it depends on, and what depends on it
This area has no external dependencies but relies on Git for version control and Python's standard library for file operations. It promises to other areas a complete pipeline from code to verified documentation, with artifacts like `quickstart.md` and `AGENTS.md` serving as entry points for users.

## Where to start reading
- `changeset.py` for understanding how Git diffs map to Isidore's graph model.
- `claims.py` to see how staleness is detected in documentation.
- `detectors.py` for security pattern analysis in code.
- `knowledge.py` to understand how documentation is compiled from the graph.
