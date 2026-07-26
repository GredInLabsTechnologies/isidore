## Purpose
The `src/isidore/knowledge.py` module implements the core knowledge compilation system for Isidore, handling the generation and management of topic pages in the knowledge home (`~/.isidore/knowledge`). It defines a unified compilation path for external knowledge streams, with topics sourced from `~/.isidore/topics.json [⚠ isidore: path not found]`. The module tracks compilation metrics, processes claims and findings, and manages persistent state to ensure consistent knowledge generation across runs.

## Architecture
The module uses a `TopicCompileResult` dataclass to track compilation metrics, including counts of generated, skipped, and quarantined topics, as well as statistics on claims and findings. Key functions include:
- `knowledge_dir()`: Returns the path to the knowledge directory (`~/.isidore/knowledge`), creating it if necessary.
- `state_path()`: Returns the path to the state file (`~/.isidore/knowledge/.state.json [⚠ isidore: path not found]`).
- `load_knowledge_state()`: Loads the state file, defaulting to a new state if the file is missing or invalid.
- `write_knowledge_state()`: Safely writes the state to disk using atomic file operations.
- `load_topics()`: Loads topics from `~/.isidore/topics.json [⚠ isidore: path not found]`, supporting both list and dictionary formats.

## Key entry points
- `TopicCompileResult`: The dataclass used to track compilation metrics and results.
- `knowledge_dir()`: The primary entry point for accessing the knowledge directory.
- `load_knowledge_state()`: Used to load the persistent state of the knowledge system.
- `write_knowledge_state()`: Used to persist the state of the knowledge system.

## Dependencies
The module depends on:
- `src/isidore/home.py`: For accessing the Isidore home directory and file operations.
- `src/isidore/llm.py`: For default LLM generation.
- `src/isidore/claims.py`: For claim processing and validation.
- `src/isidore/findings.py`: For findings processing and validation.

## How to change safely
When modifying this module, ensure:
1. The state file format remains compatible with the existing `load_knowledge_state()` and `write_knowledge_state()` functions.
2. The `TopicCompileResult` dataclass is updated carefully to avoid breaking existing code that relies on its structure.
3. Changes to the knowledge directory path or state file location are coordinated with other modules that may depend on them.
