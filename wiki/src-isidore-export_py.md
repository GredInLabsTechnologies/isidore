## Purpose
The `export.py` module bridges Isidore's verified claims into Living-Library card drafts. Each anchored claim is a machine-checked fact with a `path:line` anchor; a page's OK claims become a draft card whose `verify_cmd` is `isidore claims --check`, so `agora lib audit` degrades the card automatically when the code drifts. These are DRAFTS written to an output directory for human review — nothing is ever posted into a notebook. The entire pipeline is 0 LLM (`src/isidore/export.py:1`).

## Architecture
The module has three layers:
1. **Rendering** — `render_card()` takes a module name and its verified claims, produces a YAML-frontmatter Markdown document with `id`, `title`, `domain`, `verify_cmd`, and a claims list. Each claim carries its `statement` and `evidence` (the `path:line` anchor).
2. **Aggregation** — `build_cards()` reads the wiki state, runs `check_claims()` to get current claim statuses, groups OK claims by page, and calls `render_card()` for each page that meets a minimum claim count.
3. **Output** — `write_cards()` writes the rendered cards to a directory, one file per card.

Helper functions handle slug generation (`_slug()` normalizes module paths to filesystem-safe identifiers) and YAML string escaping (`_yaml_str()`).

## Key entry points
- `build_cards(repo, *, domain, min_claims, include_stale)`: The primary interface. Returns `[(filename, content)]` draft cards — one per wiki page with enough OK claims (`src/isidore/export.py:L62-L80`).
- `render_card(module, claims, *, domain, commit)`: Renders a single card as a YAML-frontmatter Markdown string (`src/isidore/export.py:L28-L59`).
- `write_cards(cards, out_dir)`: Writes card tuples to disk, returning the list of written paths (`src/isidore/export.py:L83-L90`).

## Dependencies
- `src/isidore/claims.py`: Provides `check_claims()` to verify claim statuses against the codebase.
- `src/isidore/pipeline.py`: Provides `WIKI_DIRNAME` (the wiki output directory name) and `load_state()` to read the compiled wiki state.
- Used by:
  - `src/isidore/cli.py` (for the export CLI subcommand)
- Tested by:
  - `tests/test_export.py`

## How to change safely
1. **Card format**: `render_card()` produces YAML frontmatter consumed by `agora lib audit`. Changes to the frontmatter keys (especially `verify_cmd`, `claims`, `confidence`) must preserve compatibility with the Agora Living-Library audit tool.
2. **Claim filtering**: `build_cards()` defaults to including only `state == "ok"` claims. The `include_stale` flag relaxes this — ensure stale claims are still clearly marked in the card body.
3. **Slug generation**: `_slug()` normalizes module paths to a flat identifier. Changing the slug algorithm invalidates existing card filenames; treat it as a breaking change.
4. **Output encoding**: `write_cards()` uses UTF-8 with explicit `newline="\n"`. Preserve this for cross-platform consistency.
