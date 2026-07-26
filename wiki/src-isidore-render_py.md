## Purpose
`src/isidore/render.py` generates four deterministic outputs from the repository's structure graph: `quickstart.md`, `index.toon`, `llms.txt`, and an `AGENTS.md` reference block. These outputs serve as agent-oriented documentation, providing a machine-first catalog (`index.toon`) and a human-readable quickstart guide (`quickstart.md`). The `llms.txt` file adheres to a community convention for handing documentation to agents, while the `AGENTS.md` block is embedded in the repository's root to direct users to the compiled wiki. The module exists to bridge the gap between raw structural data and consumable documentation, ensuring agents and humans can access the repository's structure in formats optimized for their needs.

## Architecture
The module consists of four main functions:
1. `render_quickstart()` generates a human-readable Markdown catalog of modules and flows, with `path:line` citations to the repository's structure.
2. `render_toon_index()` produces a TOON-formatted table of the same catalog, optimized for agent consumption.
3. `agents_md_block()` creates a delimited block for embedding in `AGENTS.md`, pointing to the compiled wiki.
4. `upsert_agents_block()` handles the insertion or replacement of the `AGENTS.md` block in the repository's root.

The module also includes helper functions like `_first_sentence()` for extracting summaries and constants like `WIKI_DIRNAME` for configuring the output directory. The output directory is determined by the `ISIDORE_WIKI_DIR` environment variable, defaulting to `wiki` if not set.

## Key entry points
- `render_quickstart()`: Generates the human-readable `quickstart.md` from module and flow specifications.
- `render_toon_index()`: Produces the agent-optimized `index.toon` file.
- `agents_md_block()`: Creates the reference block for embedding in `AGENTS.md`.
- `upsert_agents_block()`: Manages the insertion of the `AGENTS.md` block in the repository's root.

## Dependencies
The module depends on `src/isidore/toon.py` for encoding data in TOON format, which is used in `render_toon_index()`.

## How to change safely
To modify `render.py`, focus on the following:
1. **Output formats**: Ensure changes to `render_quickstart()` or `render_toon_index()` maintain consistency between the human-readable and machine-readable outputs.
2. **Delimited blocks**: When updating `agents_md_block()` or `upsert_agents_block()`, preserve the `MARKER_START` and `MARKER_END` delimiters to maintain idempotency.
3. **Environment variables**: If changing `WIKI_DIRNAME`, ensure the new variable name is consistently used across the module and dependent modules.
4. **Citations**: When adding or modifying citations in `quickstart.md` or `index.toon`, verify they point to exact `path:line` references in the repository.
