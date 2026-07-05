"""Structure graph: loading, module grouping, and a built-in Python AST scanner.

Isidore consumes a simple, tool-agnostic graph format (JSON):

    {
      "nodes": [{"id", "label", "file_type", "source_file", "source_location"}, ...],
      "links": [{"source", "target", "relation"}, ...],       # "edges" also accepted
      "built_at_commit": "<git sha, optional>"
    }

- `file_type`: "code" | "document" | anything else (ignored for planning).
- `source_file`: repo-relative path, forward slashes.
- `source_location`: "L<line>" (1-based) or null.
- Extra fields are ignored, so richer producers (e.g. Graphify) work as-is.

If no graph exists, `scan_repo()` builds one for Python codebases using only the stdlib
`ast` module: files and their top-level functions/classes become nodes; containment and
resolvable imports become links. It is intentionally simple — any external producer with
deeper analysis (calls, cross-language) will yield richer wikis through the same format.
"""
from __future__ import annotations

import ast
import json
import subprocess
from pathlib import Path, PurePosixPath

CONCEPTS_BUCKET = "(concepts)"
ISIDORE_DIR = ".isidore"
SKIP_DIRS = {
    ".git", ".hg", ".svn", "node_modules", "__pycache__", ".venv", "venv", "env",
    ".tox", ".mypy_cache", ".ruff_cache", ".pytest_cache", "dist", "build",
    ".idea", ".vscode", "target", ".isidore",
}


def load_graph(graph_path: Path) -> tuple[list[dict], list[dict], str | None]:
    data = json.loads(graph_path.read_text(encoding="utf-8"))
    nodes = data.get("nodes", [])
    links = data.get("links", data.get("edges", []))
    return nodes, links, data.get("built_at_commit")


def find_graph(repo: Path, explicit: Path | None = None) -> Path | None:
    """Resolve the graph source.

    Precedence: explicit --graph > this tool's own `.isidore/graph.json` (built by `scan`) >
    known third-party producers. The extra producers are a convenience so existing graphs work
    out of the box; the tool's own output always wins to avoid surprising a user who ran `scan`.
    """
    candidates = [explicit] if explicit else [
        repo / ISIDORE_DIR / "graph.json",
        repo / "graphify-out" / "graph.json",   # optional third-party producer, documented
    ]
    for candidate in candidates:
        if candidate and candidate.is_file():
            return candidate
    return None


def module_of(source_file: str | None, depth: int) -> str:
    if not source_file:
        return CONCEPTS_BUCKET
    parts = PurePosixPath(source_file.replace("\\", "/")).parts
    if not parts:
        return CONCEPTS_BUCKET
    return "/".join(parts[:depth])


# ------------------------------------------------------------------ scanner

def _node_id(rel_path: str, symbol: str | None = None) -> str:
    base = rel_path.replace("/", "_").replace(".", "_").replace("-", "_")
    return f"{base}_{symbol}" if symbol else base


def _iter_source_files(repo: Path) -> list[Path]:
    found: list[Path] = []
    stack = [repo]
    while stack:
        current = stack.pop()
        for entry in sorted(current.iterdir()):
            if entry.is_dir():
                if entry.name not in SKIP_DIRS and not entry.name.startswith("."):
                    stack.append(entry)
            elif entry.suffix in (".py", ".md"):
                found.append(entry)
    return found


def _scan_python_file(repo: Path, path: Path) -> tuple[list[dict], list[dict], list[str]]:
    """One file -> (nodes, containment links, imported module names)."""
    rel = path.relative_to(repo).as_posix()
    file_id = _node_id(rel)
    nodes = [{"id": file_id, "label": path.name, "file_type": "code",
              "source_file": rel, "source_location": "L1"}]
    links: list[dict] = []
    imports: list[str] = []
    try:
        tree = ast.parse(path.read_text(encoding="utf-8", errors="replace"))
    except SyntaxError:
        return nodes, links, imports

    for item in tree.body:
        if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            suffix = "()" if not isinstance(item, ast.ClassDef) else ""
            sym_id = _node_id(rel, item.name)
            nodes.append({"id": sym_id, "label": f"{item.name}{suffix}", "file_type": "code",
                          "source_file": rel, "source_location": f"L{item.lineno}"})
            links.append({"source": file_id, "target": sym_id, "relation": "contains"})
        elif isinstance(item, ast.Import):
            imports.extend(alias.name for alias in item.names)
        elif isinstance(item, ast.ImportFrom) and item.module:
            imports.append(("." * item.level) + item.module)
    return nodes, links, imports


def _resolve_import(importer_rel: str, module: str, known: dict[str, str]) -> str | None:
    """Map an import to a repo file id if the module resolves inside the repo."""
    if module.startswith("."):
        base = PurePosixPath(importer_rel).parent
        stripped = module.lstrip(".")
        hops = len(module) - len(stripped) - 1
        for _ in range(hops):
            base = base.parent
        candidate = (str(base) + "/" if str(base) != "." else "") + stripped.replace(".", "/")
    else:
        candidate = module.replace(".", "/")
    for rel in (f"{candidate}.py", f"{candidate}/__init__.py"):
        if rel in known:
            return known[rel]
    return None


def scan_repo(repo: Path) -> tuple[list[dict], list[dict]]:
    """Build a structure graph for a Python repo with stdlib ast only."""
    nodes: list[dict] = []
    links: list[dict] = []
    pending_imports: list[tuple[str, str]] = []  # (importer rel, module name)
    file_ids: dict[str, str] = {}

    for path in _iter_source_files(repo):
        rel = path.relative_to(repo).as_posix()
        if path.suffix == ".md":
            nodes.append({"id": _node_id(rel), "label": path.name, "file_type": "document",
                          "source_file": rel, "source_location": "L1"})
            continue
        file_nodes, file_links, imports = _scan_python_file(repo, path)
        nodes.extend(file_nodes)
        links.extend(file_links)
        file_ids[rel] = file_nodes[0]["id"]
        pending_imports.extend((rel, module) for module in imports)

    for importer_rel, module in pending_imports:
        target_id = _resolve_import(importer_rel, module, file_ids)
        if target_id and target_id != file_ids[importer_rel]:
            links.append({"source": file_ids[importer_rel], "target": target_id,
                          "relation": "imports"})
    return nodes, links


def git_head(repo: Path) -> str | None:
    try:
        out = subprocess.run(["git", "rev-parse", "HEAD"], cwd=repo, capture_output=True,
                             encoding="utf-8", errors="replace", timeout=15, check=False)
        return out.stdout.strip() or None if out.returncode == 0 else None
    except (OSError, subprocess.TimeoutExpired):
        return None


def write_scan(repo: Path) -> Path:
    """Run the scanner and persist the graph to .isidore/graph.json."""
    nodes, links = scan_repo(repo)
    out_dir = repo / ISIDORE_DIR
    out_dir.mkdir(exist_ok=True)
    out_path = out_dir / "graph.json"
    out_path.write_text(json.dumps(
        {"nodes": nodes, "links": links, "built_at_commit": git_head(repo)},
        indent=1,
    ) + "\n", encoding="utf-8")
    return out_path
