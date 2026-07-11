"""Structure graph: loading, module grouping, and a built-in multi-language scanner.

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

If no graph exists, `scan_repo()` builds one with **zero dependencies, any architecture**:
Python goes through the stdlib `ast` for an exact parse; every other language goes through the
declarative engine in `langspec.py` (comment/string-sanitized, brace-depth-tracked symbol rules);
and any remaining text file still becomes a bare file node, so coverage is universal. Files and
their top-level functions/classes/methods become nodes; containment and resolvable imports become
links. It is intentionally simple — any external producer with deeper analysis (calls, precise
cross-language) will yield richer wikis through the same format.
"""
from __future__ import annotations

import ast
import json
import subprocess
from pathlib import Path, PurePosixPath

from .langspec import BARE_CODE_EXTS, BINARY_EXTS, LANGUAGES, extract, spec_for

CONCEPTS_BUCKET = "(concepts)"
ISIDORE_DIR = ".isidore"
SKIP_DIRS = {
    ".git", ".hg", ".svn", "node_modules", "__pycache__", ".venv", "venv", "env",
    ".tox", ".mypy_cache", ".ruff_cache", ".pytest_cache", "dist", "build",
    ".idea", ".vscode", "target", ".isidore",
}


class GraphError(ValueError):
    """The graph file exists but is not valid (malformed JSON or wrong shape)."""


def load_graph(graph_path: Path) -> tuple[list[dict], list[dict], str | None]:
    raw = graph_path.read_text(encoding="utf-8", errors="replace")
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise GraphError(f"malformed graph JSON at {graph_path}: {exc}") from exc
    if not isinstance(data, dict):
        raise GraphError(f"graph at {graph_path} must be a JSON object, got {type(data).__name__}")
    nodes = data.get("nodes", [])
    links = data.get("links", data.get("edges", []))
    if not isinstance(nodes, list) or not isinstance(links, list):
        raise GraphError(f"graph at {graph_path}: 'nodes'/'links' must be lists")
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

def git_listed_files(repo: Path) -> set[str] | None:
    """Repo files git tracks or would track: `git ls-files` cached + untracked-not-ignored.

    Returns POSIX-relative paths, or None when `repo` is not a git working tree (or git is
    unavailable) — callers MUST treat None as "cannot tell, do not filter". This is the source
    of truth for "is this real source?": `--exclude-standard` honors .gitignore / .git/info/exclude
    / global excludes, so gitignored build artifacts (a Gradle/Chaquopy copy of a source tree,
    a vendored subtree) are excluded; `--others` keeps brand-new files not yet `git add`ed, so
    writing a file and indexing before committing still works. `-z` = NUL-separated, unquoted
    paths (robust to spaces/unicode).
    """
    try:
        out = subprocess.run(
            ["git", "ls-files", "-z", "--cached", "--others", "--exclude-standard"],
            cwd=repo, capture_output=True, timeout=30, check=False,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    if out.returncode != 0:
        return None
    return {p for p in out.stdout.decode("utf-8", errors="replace").split("\0") if p}


def _norm_source_file(source_file: str) -> str:
    rel = source_file.replace("\\", "/")
    return rel[2:] if rel.startswith("./") else rel


def restrict_to_tracked(
    nodes: list[dict], links: list[dict], repo: Path,
) -> tuple[list[dict], list[dict], set[str]]:
    """Drop graph nodes whose source_file is gitignored/untracked, from ANY producer.

    The internal scanner already skips them, but Isidore also consumes third-party graphs
    (Graphify, --graph) whose producers walk the raw filesystem and so can index build
    artifacts. Filtering here, at the point of consumption, protects every code path: a node
    whose source_file is not git-listed is not maintained source and is removed, along with any
    link touching it. Nodes without a source_file (concepts) are always kept. Returns
    (nodes, links, dropped_source_files); dropped is empty when `repo` is not a git tree
    (cannot tell what's ignored -> index everything, unchanged behavior).
    """
    listed = git_listed_files(repo)
    if listed is None:
        return nodes, links, set()
    kept_nodes: list[dict] = []
    dropped: set[str] = set()
    for n in nodes:
        src = n.get("source_file")
        if not src or _norm_source_file(src) in listed:
            kept_nodes.append(n)
        else:
            dropped.add(_norm_source_file(src))
    if not dropped:
        return kept_nodes, links, dropped
    kept_ids = {n["id"] for n in kept_nodes if "id" in n}
    kept_links = [
        link for link in links
        if link.get("source") in kept_ids and link.get("target") in kept_ids
    ]
    return kept_nodes, kept_links, dropped


def _node_id(rel_path: str, symbol: str | None = None) -> str:
    base = rel_path.replace("/", "_").replace(".", "_").replace("-", "_")
    return f"{base}_{symbol}" if symbol else base


def _is_binary(path: Path, sniff: int = 4096) -> bool:
    """Cheap binary guard: a NUL byte in the first few KB. Extension fast-paths run before this."""
    try:
        with path.open("rb") as fh:
            return b"\0" in fh.read(sniff)
    except OSError:
        return True


# Extensions the scanner will open: symbol-extracted languages/documents, bare-but-textual source,
# plus Python (handled by the exact ast path). Anything else is only opened if it has no suffix or
# an unknown one and passes the NUL-byte sniff — so brand-new languages still get a file node.
_KNOWN_TEXT_EXTS = frozenset(LANGUAGES) | BARE_CODE_EXTS | {".py"}


def _iter_source_files(repo: Path) -> list[Path]:
    listed = git_listed_files(repo)
    found: list[Path] = []
    stack = [repo]
    while stack:
        current = stack.pop()
        for entry in sorted(current.iterdir()):
            if entry.is_dir():
                if entry.name not in SKIP_DIRS and not entry.name.startswith("."):
                    stack.append(entry)
                continue
            suffix = entry.suffix.lower()
            if suffix in BINARY_EXTS:
                continue
            # Known text/source extension -> index it. Unknown-or-no extension -> index it too, but
            # only after a NUL-byte sniff, so a new language gets at least a file node while random
            # binaries are skipped. Universal coverage without indexing blobs.
            if suffix and suffix not in _KNOWN_TEXT_EXTS and _is_binary(entry):
                continue
            if not suffix and _is_binary(entry):
                continue
            # In a git tree, index only what git tracks/would-track: a raw walk otherwise picks up
            # gitignored build artifacts (e.g. a Gradle/Chaquopy copy of a source tree) as if they
            # were maintained source. `listed is None` => not a git tree, so fall back to the plain
            # walk (unchanged behavior for non-git dirs).
            if listed is None or entry.relative_to(repo).as_posix() in listed:
                found.append(entry)
    return found


def _scan_python_file(repo: Path, path: Path) -> tuple[list[dict], list[dict], list[str]]:
    """One Python file -> (nodes, containment links, imported module names). Exact, via stdlib ast."""
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
            # Record the FULL line span (L<start>-L<end>), not just the start. The change-set
            # detector (changeset.py) needs a symbol's extent to decide whether a git hunk touched
            # it. read_excerpt still reads the leading L<start> (its regex is L(\d+)), so this is
            # backwards compatible with older start-only graphs.
            end = getattr(item, "end_lineno", None) or item.lineno
            nodes.append({"id": sym_id, "label": f"{item.name}{suffix}", "file_type": "code",
                          "source_file": rel, "source_location": f"L{item.lineno}-L{end}"})
            links.append({"source": file_id, "target": sym_id, "relation": "contains"})
        elif isinstance(item, ast.Import):
            imports.extend(alias.name for alias in item.names)
        elif isinstance(item, ast.ImportFrom) and item.module:
            imports.append(("." * item.level) + item.module)
    return nodes, links, imports


def _scan_generic_file(repo: Path, path: Path, spec) -> tuple[list[dict], list[dict], list[str]]:
    """One non-Python file -> (nodes, containment links, imports) via the declarative engine.

    A `document`-kind spec yields just the file node (no symbols). A `code` spec runs the symbol
    engine. The node shape is identical to the Python scanner's, so downstream code is unaware of
    the language. Symbol node ids are salted with the start line to stay unique when a language
    legitimately repeats a name (overloads, a method and a same-named free function).
    """
    rel = path.relative_to(repo).as_posix()
    file_id = _node_id(rel)
    nodes = [{"id": file_id, "label": path.name, "file_type": spec.kind,
              "source_file": rel, "source_location": "L1"}]
    links: list[dict] = []
    if spec.kind != "code":
        return nodes, links, []
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return nodes, links, []
    symbols, imports = extract(text, spec)
    seen: set[str] = {file_id}
    for sym in symbols:
        sym_id = _node_id(rel, f"{sym['name']}_L{sym['line']}")
        if sym_id in seen:
            continue
        seen.add(sym_id)
        nodes.append({"id": sym_id, "label": f"{sym['name']}{sym['suffix']}", "file_type": "code",
                      "source_file": rel, "source_location": f"L{sym['line']}-L{sym['end_line']}"})
        links.append({"source": file_id, "target": sym_id, "relation": "contains"})
    return nodes, links, imports


def _scan_bare_file(repo: Path, path: Path, kind: str = "code") -> tuple[list[dict], list[dict], list[str]]:
    """A textual file we do not symbol-parse -> a single file node, so it still shows up in a module."""
    rel = path.relative_to(repo).as_posix()
    nodes = [{"id": _node_id(rel), "label": path.name, "file_type": kind,
              "source_file": rel, "source_location": "L1"}]
    return nodes, [], []


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


def _scan_one_file(repo: Path, path: Path) -> tuple[list[dict], list[dict], list[str]]:
    """Route a file to the right scanner: exact ast for Python, the declarative engine for known
    languages/documents, a bare file node for anything else textual."""
    suffix = path.suffix.lower()
    if suffix == ".py":
        return _scan_python_file(repo, path)
    spec = spec_for(suffix)
    if spec is not None:
        return _scan_generic_file(repo, path, spec)
    return _scan_bare_file(repo, path)


def scan_repo(repo: Path) -> tuple[list[dict], list[dict]]:
    """Build a structure graph for a repo in ANY language, zero dependencies (see module docstring)."""
    nodes: list[dict] = []
    links: list[dict] = []
    pending_imports: list[tuple[str, str]] = []  # (importer rel, module name)
    file_ids: dict[str, str] = {}

    for path in _iter_source_files(repo):
        rel = path.relative_to(repo).as_posix()
        file_nodes, file_links, imports = _scan_one_file(repo, path)
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
