## What this area is responsible for
The `src` area implements Isidore's core functionality for compiling and managing a codebase wiki. It bridges code analysis with documentation generation, handling everything from raw evidence ingestion to verified knowledge synthesis. Its responsibility is to transform a codebase's structure and changes into a maintainable, verifiable knowledge base.

## How the work is divided
The modules split responsibilities along the pipeline from raw data to final output:
- **Connectors** (`connectors`) ingest and store evidence from the codebase.
- **Graph** (`graph.py`) models the codebase's structure and relationships.
- **Detectors** (`detectors.py`) identify security and quality issues.
- **Claims** (`claims.py`) track staleness and verify assertions about the code.
- **Pipeline** (`pipeline.py`) orchestrates the compilation of wiki pages.
- **PCP** (`pcp.py` and `verify.py`) ensures claims are cryptographically verifiable.
- **Surface** (`surface.py`) extracts API surfaces for change detection.
- **Humanpack** (`humanpack.py`) generates onboarding materials.

The split reflects the linear flow of data: from ingestion to analysis, then to documentation, with verification as a cross-cutting concern. This separation keeps concerns modular while enabling end-to-end verification.

## What it depends on, and what depends on it
This area has no recorded dependencies, making it self-contained. It promises to the rest of the system a complete pipeline from code to verified documentation, enabling tools like `humanpack.py` to generate onboarding materials. Other areas depend on its graph model and verified claims for their own functionality.

## Where to start reading
- `src-isidore-graph_py.md` for understanding the codebase model.
- `src-isidore-pipeline_py.md` to see how documentation is generated.
- `src-isidore-claims_py.md` for how staleness is tracked.
- `src-isidore-verify_py.md` for the verification mechanism.
