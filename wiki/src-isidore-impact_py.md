## Purpose
`src/isidore/impact.py` is the zero-LLM emergent-interaction detector. Regenerating a neighbour's prose does NOT detect an emergent interaction; a NEW graph edge does, and it is free. The module diffs the current dependency graph against the fingerprint persisted at the last compile (`state["deps"]`) and cross-references the git change-set, reporting — with no LLM call — what a change touched, who depends on it, which cross-module edges appeared/vanished, which anchored claims are now at risk, and which pages a `--changed` compile would regenerate (`src/isidore/impact.py:1`).

## Architecture
The module has two layers:

**`ImpactReport`** (`src/isidore/impact.py:L31-L45`) is a dataclass that holds every dimension of the analysis: `changed_files`, `changed_symbols`, `affected_modules`, `new_edges`, `removed_edges`, `fan_in`, `claims_at_risk`, `dirty_pages`, and `todos_in_zone`. Its `has_signal()` method returns whether the report contains anything worth acting on (dirty pages, claims at risk, or edge changes).

**`build_impact()`** (`src/isidore/impact.py:L48-L111`) is the computation engine. It:
1. Loads the graph and restricts it to tracked files
2. Computes changed lines and symbols from the git diff
3. Propagates through the dependency graph to find affected modules (with configurable depth)
4. Compares current cross-module edges against the stored fingerprint to find emergent interactions
5. Checks anchored claims against changed files and stale/orphan states
6. Runs a dry-run `compile_wiki` to predict which pages would regenerate
7. Harvests TODO/FIXME markers from changed code files

**`render_impact()`** (`src/isidore/impact.py:L118-L143`) formats the report as either a human-readable Markdown summary or a machine-readable toon-encoded table.

## Key entry points
- `build_impact(repo, *, graph_path, since, module_depth, affected_depth, min_symbols, top_k)`: The primary interface. Returns an `ImpactReport` with all dimensions populated (`src/isidore/impact.py:L48-L111`).
- `render_impact(r, *, md)`: Formats the report. `md=True` for a compact summary; default produces toon-encoded tables (`src/isidore/impact.py:L118-L143`).
- `ImpactReport.has_signal()`: Quick check for whether the report contains actionable findings (`src/isidore/impact.py:L44-L45`).

## Dependencies
- `src/isidore/changeset.py`: Provides `changed_lines`, `changed_symbols`, and `affected_modules` for git-diff-to-symbol mapping.
- `src/isidore/claims.py`: Provides `check_claims` to identify anchored claims at risk.
- `src/isidore/graph.py`: Provides `load_graph`, `module_of`, and `restrict_to_tracked` for graph operations.
- `src/isidore/pipeline.py`: Provides `compile_wiki` (for dry-run dirty-page prediction), `load_state`, `module_dep_edges`, `WIKI_DIRNAME`, and the default constants.
- `src/isidore/toon.py`: Provides `encode` for table serialization.
- `src/isidore/findings.py`: Provides `harvest_todos` for TODO/FIXME detection in changed code.
- Used by:
  - `src/isidore/cli.py` (for the `isidore impact` subcommand)
- Tested by:
  - `tests/test_impact.py`

## How to change safely
1. **Graph fingerprint comparison**: The emergent-interaction detection (`src/isidore/impact.py:L72`) compares `module_dep_edges()` output against `state["deps"]`. Changes to `module_dep_edges` or the state schema must maintain compatibility.
2. **Affected-depth propagation**: `affected_modules` accepts a `depth` parameter. Increasing it widens the blast radius; decreasing it may miss transitive dependents.
3. **Dry-run compile**: `build_impact` calls `compile_wiki` with `execute=False` to predict dirty pages. This must remain a dry-run — changing it to execute would introduce LLM calls into a 0-LLM module.
4. **Rendering**: `render_impact` supports both Markdown and toon-encoded output. The toon format is consumed by downstream tools; table names and column orders are part of the contract.
