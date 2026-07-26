## Purpose
The `src/isidore/knowledge.py` module implements Isidore's knowledge compilation system, which manages user-defined topics and their compilation into a structured knowledge base. It enforces strict rules for claim validation and state management, ensuring that knowledge is derived from verifiable sources. The module's core functionality includes compiling topics, tracking compilation results, and persisting state to disk.

## Architecture
The module defines a `TopicCompileResult` dataclass to track compilation metrics, such as the number of claims processed, dropped, or repaired. It also provides utility functions for managing the knowledge directory, loading and writing state, and loading topic configurations. The state is stored in a JSON file (`~/.isidore/knowledge/.state.json [⚠ isidore: path not found]`) and topics are defined in `~/.isidore/topics.json [⚠ isidore: path not found]`.

## Key entry points
- `TopicCompileResult`: A dataclass that aggregates compilation statistics, including counts of claims, findings, and warnings.
- `knowledge_dir()`: Returns the path to the knowledge directory (`~/.isidore/knowledge`), creating it if necessary.
- `state_path()`: Returns the path to the state file (`~/.isidore/knowledge/.state.json [⚠ isidore: path not found]`).
- `load_knowledge_state()`: Loads the knowledge state from disk, defaulting to an empty state if the file is missing or invalid.
- `write_knowledge_state()`: Writes the knowledge state to disk atomically, using a temporary file and atomic replacement.
- `load_topics()`: Loads topic configurations from `~/.isidore/topics.json [⚠ isidore: path not found]`, supporting both list and dictionary formats.

## Dependencies
The module depends on:
- `src/isidore/home.py`: For accessing the user's home directory and file operations.
- `src/isidore/llm.py`: For default LLM interactions (though not directly used in the excerpted code).
- `src/isidore/claims.py`: For claim parsing and validation.
- `src/isidore/findings.py`: For handling findings (though not directly used in the excerpted code).

## How to change safely
When modifying this module:
1. Ensure all state changes are written atomically using `write_knowledge_state()` to avoid corruption.
2. Validate all claims and findings strictly according to the rules in the docstring (`src/isidore/knowledge.py:92-L110`).
3. Maintain backward compatibility with the state file format (`version: 1`).
4. Test changes with both list and dictionary formats in `topics.json`.
