## Purpose
`tests/test_units.py` holds the unit‑tests that verify core Isidore utilities: the **toon table encoder**, the **graph scanning / serialization pipeline**, and the **findings‑block parser** used for QA and LLM interactions. By exercising these public APIs with concrete inputs, the file assures that encoding, path handling, repository scanning, round‑trip graph persistence, and markdown‑based findings extraction behave as documented.

## Architecture
The test file is divided into three logical sections, each introduced by a visual separator comment:

* **toon** – validates `isidore.toon.encode_table` output formatting【tests/test_units.py:22‑27】  
* **graph** – exercises `isidore.graph` helpers (`module_of`, `scan_repo`, `write_scan`, `find_graph`, `load_graph`) and checks for correct symbol extraction, import detection, error tolerance, and serialization【tests/test_units.py:29‑69】  
* **findings** – checks `isidore.findings.parse_findings_block` (and indirectly `filter_findings`) for proper markdown block stripping and finding‑kind extraction【tests/test_units.py:70‑84】

Each `def test_*` function is a standalone entry point for `pytest`. The suite imports the symbols under test from the Isidore package (see imports below) and supplies minimal temporary files via `tmp_path` fixtures to keep the tests deterministic and isolated.

## Key entry points
| Entry point | What it verifies | Relevant lines |
|-------------|------------------|----------------|
| `test_toon_encode_table_quoting_and_counts` | `encode_table` produces a quoted CSV‑style table with correct row count column | definition【tests/test_units.py:24】, assertion【tests/test_units.py:26】 |
| `test_module_of_normalizes_and_buckets` | `module_of` normalises POSIX paths, handles Windows separators, and returns “(concepts)” for a missing source | asserts【tests/test_units.py:32‑34】 |
| `test_scan_repo_extracts_symbols_imports_and_docs` | `scan_repo` discovers Python symbols, Markdown docs, respects `.venv` exclusion, and yields “contains” & “imports” relations | label check【tests/test_units.py:50】, exclusion check【tests/test_units.py:51】, relation check【tests/test_units.py:53】 |
| `test_scan_tolerates_syntax_errors` | `scan_repo` does not crash on syntactically invalid files and still registers the file label | assertion【tests/test_units.py:58】 |
| `test_write_scan_and_find_graph_roundtrip` | `write_scan` writes a scan file that `find_graph` can read back unchanged; `load_graph` returns node list and link list | round‑trip check【tests/test_units.py:65】, load check【tests/test_units.py:66‑67】 |
| `test_parse_findings_block_extracts_and_strips` | `parse_findings_block` removes the fenced block from the markdown and returns a list of findings with correct `kind` values | clean‑markdown check【tests/test_units.py:80】, kinds list check【tests/test_units.py:82】 |

## Dependencies
The module imports the following public APIs, all of which are external to the test file itself:

```python
from isidore.findings import (
    filter_findings,
    harvest_todos,
    orphan_file_candidates,
    parse_findings_block,
    render_findings,
    coverage_gap_candidates,
)
from isidore.graph import find_graph, load_graph, module_of, scan_repo, write_scan
from isidore.llm import build_request
from isidore.pipeline import PageSpec
from isidore.qa import ask, gather_evidence, question_terms
from isidore.render import render_toon_index
from isidore.toon import encode_table
```【tests/test_units.py:6‑19】

No other test files or runtime dependencies reference `tests/test_units.py`, and the module itself does not expose any symbols beyond the pytest functions.

## How to change safely
1. **Preserve the import list** – the tests rely on the exact symbols imported at lines 6‑19. Adding or removing imports without corresponding test updates will cause import errors.  
2. **Keep the fixture behavior** – many tests create temporary files under `tmp_path`. Do not alter the filenames or directory structure unless you also adjust the assertions that check for specific labels (e.g., `"alpha.py"`, `"beta.py"`).  
3. **Maintain assertion expectations** – the expected outputs (quoted strings, path normalisation, relation names) are hard‑coded. If you change implementation details, update the corresponding `assert` lines (e.g., line 26, 50‑53, 65‑67, 80‑82).  
4. **Run the full pytest suite** after any change to verify that no other test module relies on altered behaviour. Since this file has no downstream dependents, failures will be isolated to this suite.  
5. **Do not introduce external side‑effects** – the tests operate purely on in‑memory data and temporary files. Adding network calls, environment variable reads, or global state will break isolation and cause flaky results.  
6. **Document new test cases** – if new functionality is added to any of the imported modules, extend the corresponding section (toon, graph, or findings) with a new `def test_*` following the existing pattern, and cite the new lines accordingly.
