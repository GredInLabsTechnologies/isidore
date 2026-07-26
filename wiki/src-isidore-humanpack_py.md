## Purpose
The `humanpack.py` module generates a self-contained, deterministic HTML/PDF onboarding pack from pre-compiled artifacts. It serves as Lane E in the system, producing a human-readable document that includes:
- A cover page
- An SVG architecture map
- A reading path
- Per-sentence confidence indicators via a verified-mass bar (green/yellow/gray)
- Security banners
- A glossary
- Active contracts
- An Ágora task-board placeholder

The module ensures tamper-evident certificates by leveraging Proof-Carrying Prose (PCP) claims verified against the code (`ff902eb feat(pcp)`). It avoids LLM dependencies (`src/isidore/humanpack.py:10`) and produces identical output for the same input.

## Architecture
The module processes structured data (pages, claims, certificates, graph data, contracts) to generate HTML content. Key components include:
- `_esc()`: HTML-escapes untrusted content to prevent markup injection (`src/isidore/humanpack.py:35-L37`)
- `minimal_markdown_to_html()`: Converts a deterministic markdown subset to HTML (`src/isidore/humanpack.py:40-L78`)
- `_verdict_color()`: Maps claim verdicts to color codes (`src/isidore/humanpack.py:81-L86`)
- `generate_security_banner()`: Creates a security warning for "danger" severity marks (`src/isidore/humanpack.py:93-L99`)
- `generate_mass_bar()`: Renders a confidence bar based on verified mass metrics (`src/isidore/humanpack.py:102-L110`)

The module uses `load_graph` from `src/isidore/graph.py` and PCP-related types from `src/isidore/pcp.py`.

## Key entry points
The module does not expose a CLI directly but is invoked via the `isidore render` command (`src/isidore/humanpack.py:1`). The core functionality is driven by:
- `minimal_markdown_to_html()`: Converts markdown to HTML
- `generate_security_banner()`: Generates security warnings
- `generate_mass_bar()`: Creates confidence indicators

## Dependencies
The module depends on:
- `src/isidore/graph.py`: For loading graph data (`src/isidore/humanpack.py:20`)
- `src/isidore/pcp.py`: For PCP-related types and utilities (`src/isidore/humanpack.py:21-L32`)

## How to change safely
1. **HTML/Markdown rendering**: Modify `minimal_markdown_to_html()` to support additional markdown features, but ensure backward compatibility with existing artifacts.
2. **Security banners**: Update `generate_security_banner()` to handle new severity levels or formats, but preserve the existing "danger" severity behavior.
3. **Confidence indicators**: Adjust `generate_mass_bar()` to support additional confidence states, but maintain the existing green/yellow/gray mapping.
4. **PCP integration**: When adding new PCP-related features, ensure they align with the existing verified-mass and claim-verification logic.
