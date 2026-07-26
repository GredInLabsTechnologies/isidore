## Purpose
The `src/isidore/graph.py` module provides core functionality for loading, validating, and working with Isidore's structure graph. The graph is a tool-agnostic JSON format that represents code and document nodes along with their relationships. It serves as the foundation for Isidore's agent-oriented wiki generation, enabling tools to analyze and visualize repository structure without being tied to a specific architecture or language.

The module's primary responsibilities include:
- Loading and validating graph files from disk
- Resolving the source of a graph (either explicitly provided or from known locations)
- Grouping files into modules based on directory structure
- Scanning repositories to generate graphs when none exist, with built-in support for multiple languages

## Architecture
The module is organized into two main sections:
1. **Graph handling**: Functions for loading and validating graph files (`load_graph`, `find_graph`)
2. **Repository scanning**: Functions for generating graphs from repository contents (`git_listed_files`)

The graph format is intentionally simple, with nodes representing files or code symbols and links representing relationships like imports or containment. The module supports multiple language scanning through a declarative engine (via `langspec.py`) while providing exact parsing for Python via the standard library's `ast` module.

## Key entry points
- `load_graph()`: Loads and validates a graph file from disk
- `find_graph()`: Resolves the location of a graph file, with precedence rules
- `module_of()`: Groups files into modules based on directory structure
- `git_listed_files()`: Gets the set of files tracked by git in a repository

## Dependencies
The module depends on:
- `src/isidore/langspec.py`: For language-specific scanning rules
- Standard library modules: `ast`, `json`, `subprocess`, `pathlib`

## How to change safely
When modifying this module:
1. Maintain the existing graph format compatibility
2. Preserve the precedence rules in `find_graph()`
3. Ensure `git_listed_files()` continues to respect gitignore rules
4. Keep the module's zero-dependency scanning capability for Python
5. Update the docstring if you change the graph format or add new features
