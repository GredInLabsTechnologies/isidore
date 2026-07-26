## Purpose
The `src/isidore/findings.py` module harvests and manages "residue" — observations about the codebase that are generated during compilation but are not part of the main wiki prose. These findings come from two sources:

1. **LLM residue**: Structured observations from an LLM reading code excerpts, formatted in a fenced block with the marker `isidore-findings`. These are hypotheses about potential issues, mismatches, or unclear points, but are not verified conclusions.
2. **Deterministic residue**: Code-level observations like TODO comments, orphan files, and risk hotspots, extracted purely from the structure graph and git history without LLM involvement.

All findings are stored in `wiki/findings.toon` (a Toon table) and can be resolved by human audit. The module ensures findings are tied to real paths in the repository, filtering out hallucinations.

## Architecture
The module consists of a small set of functions that work together to parse, validate, and manage findings:

- `parse_findings_block()` extracts findings from a markdown block and splits them into clean prose and structured data.
- `finding_id()` generates a stable identifier for each finding using a hash of its kind, location, and note.
- `is_finding_resolved()` checks if a finding has been resolved by reading from `wiki/resolved_findings.json [⚠ isidore: path not found]`.
- `resolve_finding()` records a finding's resolution in `wiki/resolved_findings.json [⚠ isidore: path not found]`.
- `filter_findings()` validates that findings cite real paths in the repository and separates them into kept/dropped lists.

## Key entry points
- `parse_findings_block()` is the primary entry point for extracting findings from generated pages.
- `filter_findings()` is used to validate findings before they are stored or displayed.

## Dependencies
The module depends on `src/isidore/toon.py` for rendering findings in Toon tables. It is used by `src/isidore/knowledge.py` and `src/isidore/pipeline.py`.

## How to change safely
When modifying this module:
1. Ensure any changes to the findings format are backward-compatible with existing `isidore-findings` blocks.
2. Do not alter the resolution file path (`wiki/resolved_findings.json [⚠ isidore: path not found]`) or its schema, as it is a shared contract.
3. Preserve the deterministic ID generation (`finding_id()`) to avoid breaking resolution tracking.
4. Maintain the hallucination filter in `filter_findings()` to ensure only valid findings are stored.
