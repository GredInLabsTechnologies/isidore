## Purpose
`src/isidore/render.py` generates deterministic, LLM-free documentation for agents. It produces four outputs:
1. `quickstart.md`: A human-readable catalog of modules and flows, with `path:line` citations.
2. `index.toon`: A machine-friendly TOON table version of the same catalog, cheaper for agents to load.
3. `llms.txt`: A standardized format for agent documentation, emitted as `f3399f1`.
4. An `AGENTS.md` block: A self-reference for agents before they modify the repo, inserted between `<!-- ISIDORE:START -->` and `<!-- ISIDORE:END -->` markers.

The module exists to provide a consistent, low-cost documentation layer for agents, ensuring they have reliable access to repository structure and purpose without requiring LLM calls.

## Architecture
The module is structured around four key functions:
- `render_quickstart()`: Generates the human-readable `quickstart.md` with tables of modules and flows.
- `render_toon_index()`: Creates the TOON-formatted `index.toon` for agent consumption.
- `agents_md_block()`: Produces the `AGENTS.md` block with a self-reference and optional knowledge home summary.
- `knowledge_summary()`: Collects metadata about the local knowledge home (if it exists).

The module uses `src/isidore/toon.py` for TOON encoding (`src/isidore/render.py:L13`) and defines markers for delimiting the `AGENTS.md` block (`src/isidore/render.py:L15-L16`). The output directory is configurable via `ISIDORE_WIKI_DIR` (`src/isidore/render.py:L22`).

## Key entry points
- `render_quickstart()`: Entry point for generating `quickstart.md`.
- `render_toon_index()`: Entry point for generating `index.toon`.
- `agents_md_block()`: Entry point for generating the `AGENTS.md` block.
- `knowledge_summary()`: Entry point for collecting knowledge home metadata.

## Dependencies
- `src/isidore/toon.py`: Used for TOON encoding (`src/isidore/render.py:L13`).

## How to change safely
1. To modify the `quickstart.md` format, edit `render_quickstart()` (`src/isidore/render.py:L25-L49`).
2. To change the `index.toon` structure, modify `render_toon_index()` (`src/isidore/render.py:L52-L74`).
3. To update the `AGENTS.md` block, adjust `agents_md_block()` (`src/isidore/render.py:L77-L108`).
4. To alter knowledge home handling, edit `knowledge_summary()` (`src/isidore/render.py:L111-L127`).
5. To change the output directory, modify `WIKI_DIRNAME` (`src/isidore/render.py:L22`).
