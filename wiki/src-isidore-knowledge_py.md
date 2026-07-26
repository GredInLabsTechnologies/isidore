## Purpose
The `src/isidore/knowledge.py` module implements the core knowledge compilation system for Isidore, handling user-defined topics and their compilation into a unified knowledge base stored in `~/.isidore/knowledge`. It enforces strict rules for claim validation, ensuring that all knowledge assertions are anchored to specific source excerpts and are never invented or summarized. The module tracks compilation metrics, state management, and topic configurations, serving as the foundation for Isidore's knowledge processing pipeline.

## Architecture
The module defines a `TopicCompileResult` dataclass to track compilation metrics, including counts of generated, dropped, and repaired claims, as well as warnings and security flags. It provides utility functions to manage the knowledge directory (`knowledge_dir()`), state file path (`state_path()`), and state persistence (`load_knowledge_state()`/`write_knowledge_state()`). The core functionality revolves around validating and processing claims, with strict rules to ensure claims are supported by exact source excerpts.

## Key entry points
- `TopicCompileResult`: A dataclass tracking compilation metrics and outcomes.
- `knowledge_dir()`: Returns the path to the knowledge directory, creating it if necessary.
- `state_path()`: Returns the path to the state file.
- `load_knowledge_state()`: Loads the knowledge state from disk, with fallback defaults.
- `write_knowledge_state()`: Safely writes the knowledge state to disk using atomic file operations.

## Dependencies
The module depends on:
- `src/isidore/home.py`: For home directory and file system utilities.
- `src/isidore/llm.py`: For default LLM generators.
- `src/isidore/claims.py`: For claim parsing and validation.
- `src/isidore/findings.py`: For findings-related constants.

## How to change safely
When modifying this module:
1. Ensure all claims adhere to the strict citation rules, copying URIs verbatim from source excerpts.
2. Maintain the atomic file operations in `write_knowledge_state()` to prevent corruption.
3. Preserve the `TopicCompileResult` structure, as it is used by other components.
4. Do not alter the state file format or version without migration support.
