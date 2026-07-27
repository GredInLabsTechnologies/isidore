## Purpose

`src/isidore/render.py` holds the outputs that cost nothing: `quickstart.md`, `index.toon`,
`llms.txt` and the AGENTS.md reference block (`src/isidore/render.py:1`). None of them needs an LLM
call — they are projections of what the compiler already knows, so the expensive path stays reserved
for prose (`src/isidore/render.py:3`).

It also answers one question the whole toolchain depends on: **where this repository keeps its
living docs**. That answer has to be the same for `scan`, `compile`, the certificates, the state
file and the AGENTS.md block, or a run writes half of itself into one directory and reads the other
half from another.

## Architecture

`configured_wiki_dirname` resolves the directory with a stated precedence: the environment, then the
repository's own `isidore.json`, then `wiki` (`src/isidore/render.py:28`). The environment is read
first and returns immediately when set (`src/isidore/render.py:42`), so an existing export keeps
working and a one-off override stays possible.

The repository setting exists because the environment alone was a trap. A repo whose wiki is not at
the default path had to export the variable on every invocation; forget it once and the toolchain
guards a directory that does not exist while indexing the real one as if it were source — the
self-indexing bug this project already had to fix, measured in GIMO as a 13 MB certificate for a page
about the documentation (`src/isidore/render.py:30`). A setting that must be remembered is a setting
that will be forgotten, so this one travels with the repository
(`src/isidore/render.py:35`).

The config is located by walking up from the starting directory, the way a repo marker is normally
found (`src/isidore/render.py:38`), which makes running from `src/` behave like running from the
root. The names it depends on are declared once at the top rather than repeated: the variable
(`src/isidore/render.py:19`), the key (`src/isidore/render.py:20`), the filename
(`src/isidore/render.py:21`) and the fallback (`src/isidore/render.py:22`).

The rest of the module is rendering. `render_quickstart` (`src/isidore/render.py:66`) and
`render_toon_index` (`src/isidore/render.py:93`) are the human and machine faces of the same
catalog — `index.toon` exists because TOON tables are cheaper for an agent to load than prose.
`agents_md_block` (`src/isidore/render.py:118`) is the block written into a repo's AGENTS.md, and
`knowledge_summary` (`src/isidore/render.py:152`) covers the knowledge home.

## Key entry points

- `configured_wiki_dirname(start)` — where the docs live, by precedence
  (`src/isidore/render.py:25`).
- `render_quickstart(...)` — the catalog a human reads (`src/isidore/render.py:66`).
- `render_toon_index(...)` — the same catalog for an agent (`src/isidore/render.py:93`).
- `agents_md_block()` — the reference block for a repo's AGENTS.md (`src/isidore/render.py:118`).
- `knowledge_summary(...)` — the knowledge home's section (`src/isidore/render.py:152`).

## Dependencies

Only `src/isidore/toon.py`, for encoding the TOON tables (`src/isidore/render.py:14`). That thinness
is deliberate: `src/isidore/pipeline.py` and `src/isidore/whatsnew.py` both import from here, so a
dependency added to this module is a dependency added to the compiler.

## How to change safely

The resolved directory is bound once per process and every module reads the same constant. Keep it
that way: a second place that answers "where is the wiki" is a second answer, and the two will
disagree on the day it matters. When the resolution rules change, change them here and let the CLI's
mismatch check keep a run from starting in the wrong place. And keep the fallbacks boring — an
unreadable config resolves to the default, never to a guess.
