## Purpose
The `changeset.py` module bridges Git's diff output with Isidore's graph model, mapping file changes to the symbols they affect. It exists to enable incremental compilation and impact analysis by:
1. Identifying which lines in which files changed (via `git diff`)
2. Mapping those lines to the graph nodes (symbols) they belong to
3. Calculating the "fan-in" of modules (which modules depend on changed ones)

This is critical for the `--changed` compile mode, which only recompiles symbols that actually moved plus their dependents, and for `isidore impact` (T3), which reports emergent interactions from changes.

## Architecture
The module processes Git diffs in three stages:
1. `_git_diff()` runs `git diff` and returns the raw output
2. `changed_lines()` parses the diff to extract changed line numbers per file
3. `changed_symbols()` maps those lines to graph nodes using `symbol_spans()`

Key data structures:
- `WHOLE_FILE` sentinel marks pure renames (no content change)
- `_HUNK` regex parses diff hunk headers
- `_LOC` regex parses graph location strings

## Key entry points
- `changed_lines(repo, since)`: The primary interface, returning `{file: {changed_lines}}`
- `changed_symbols(nodes, changed)`: Maps changed lines to graph node IDs
- `_module_fan_in(nodes, links, module_depth)`: Calculates module dependencies

## Dependencies
- `src/isidore/graph.py`: Only imports `module_of` to determine a file's module path
- Used by:
  - `src/isidore/impact.py` (for impact analysis)
  - `src/isidore/pipeline.py` (for incremental compilation)

## How to change safely
1. **Git diff parsing**: Changes to `_git_diff()` or diff parsing logic must preserve the exact line number mapping
2. **Symbol mapping**: `symbol_spans()` and `changed_symbols()` assume graph nodes have `source_file` and `source_location` fields
3. **Module resolution**: Changes to module path calculation must maintain consistency with `graph.py`
