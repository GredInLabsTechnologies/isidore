> [!WARNING]
> **SECURITY — deterministic detectors flagged this code (0 LLM). Verify; never document as an intended feature.**
>
> - `src/isidore/detectors.py:29` — credential-shaped literal (-----BEGIN prefix)
> - `src/isidore/detectors.py:29` — credential-shaped literal (AIza prefix)
> - `src/isidore/detectors.py:29` — credential-shaped literal (AKIA prefix)
> - `src/isidore/detectors.py:29` — credential-shaped literal (gho_ prefix)
> - `src/isidore/detectors.py:29` — credential-shaped literal (ghp_ prefix)
> - `src/isidore/detectors.py:29` — credential-shaped literal (glpat- prefix)
> - `src/isidore/detectors.py:29` — credential-shaped literal (ya29. prefix)
> - `src/isidore/detectors.py:34` — eval()
> - `src/isidore/detectors.py:35` — exec()
> - `src/isidore/detectors.py:36` — os.system()
> - `src/isidore/detectors.py:38` — pickle.loads()
> - `src/isidore/detectors.py:39` — yaml.load() without Loader
> - `src/isidore/detectors.py:43` — eval()
## Purpose
The `detectors.py` module implements three security detection mechanisms for the Isidore system: entropy analysis, dangerous call-site detection, and import-based topology analysis. These detectors operate on codebases without relying on a vocabulary of words, instead using concrete facts about the code's structure and content. The entropy detector identifies high-Shannon strings shaped like credentials, the sink detector flags dangerous callsites per language, and the topology detector traces files reachable from authentication/secret/crypto roots via imports. Each detector is language-aware and fail-closed (a detector that cannot run for a language contributes nothing for it).

## Architecture
The module is organized around three core functions:
1. `shannon_entropy()` calculates the Shannon entropy of a string
2. `_looks_like_secret()` determines if a string literal resembles a credential
3. `_scan_file()` performs entropy and sink detection on individual files
4. `_topology_marks()` performs import-based reachability analysis

The detectors use a declarative `SINKS` table (a dictionary mapping file extensions to lists of dangerous patterns) and a set of `ROOTS` (file patterns indicating security-sensitive areas). The topology analysis uses a breadth-first search over the import graph with a configurable depth limit.

## Key entry points
The module is primarily used through its integration with the Isidore pipeline (via `src/isidore/pipeline.py`) and its dependency on the Proof-Carrying Prose system (`src/isidore/pcp.py`). The detectors are invoked as part of the security analysis pipeline, producing `Mark` objects that are verified and certified by the PCP system.

## Dependencies
The module depends on:
- `src/isidore/pcp.py` for the `Mark` and `VerifyContext` types
- Python's standard library modules (`math`, `re`, `collections`, `pathlib`)

## How to change safely
When modifying this module:
1. Maintain the fail-closed behavior for unsupported languages
2. Preserve the declarative nature of the `SINKS` table and `ROOTS` set
3. Ensure all detectors handle file read errors gracefully
4. Keep the topology analysis at the file level (no symbol-level mixing)
5. Verify that all changes maintain the security guarantees of the PCP integration
