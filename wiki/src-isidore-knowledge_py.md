## Purpose
The `src/isidore/knowledge.py` module manages the compilation and storage of user-defined topics in Isidore. It serves as the core for processing external knowledge streams, storing them in the knowledge home directory (`~/.isidore/knowledge`), and tracking their state. The module enforces strict rules for claim validation, ensuring that all knowledge claims are anchored to specific source excerpts and are never invented or summarized. This design supports a deterministic, auditable knowledge base where claims are tied to their original sources.

## Architecture
The module defines a `TopicCompileResult` dataclass to track the outcomes of topic compilation, including metrics for dropped claims, generated content, and warnings. It also provides utility functions to manage the knowledge directory and state file, ensuring atomic writes for state persistence. The core functionality depends on other Isidore modules for home directory management (`home.py`), LLM interactions (`llm.py`), claim processing (`claims.py`), and findings handling (`findings.py`).

## Key entry points
- `TopicCompileResult`: A dataclass that aggregates compilation metrics, such as the number of claims dropped or findings kept.
- `knowledge_dir()`: Returns the path to the knowledge directory (`~/.isidore/knowledge`), creating it if necessary.
- `state_path()`: Returns the path to the state file (`~/.isidore/knowledge/.state.json [⚠ isidore: path not found]`).
- `load_knowledge_state()`: Loads the knowledge state from the state file, defaulting to a new state if the file is missing or invalid.
- `write_knowledge_state()`: Writes the knowledge state to the state file atomically, using a temporary file and atomic replacement.

## Dependencies
The module depends on:
- `src/isidore/home.py`: For home directory management and file operations.
- `src/isidore/llm.py`: For LLM interactions, though the exact usage is not detailed in the excerpts.
- `src/isidore/claims.py`: For claim processing and validation.
- `src/isidore/findings.py`: For handling findings and warnings.

## How to change safely
When modifying `knowledge.py`, ensure that:
1. All state file operations use atomic writes via temporary files, as shown in `write_knowledge_state()`.
2. Claims and findings are strictly anchored to source excerpts, following the rules in the docstring.
3. The `TopicCompileResult` dataclass is updated only when new metrics are needed, as it is used by other modules.
4. File paths are constructed using the provided utility functions (`knowledge_dir()`, `state_path()`) to maintain consistency.
