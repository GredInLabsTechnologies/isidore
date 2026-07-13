"""Lane C — deterministic security detectors: entropy, sinks, topology. 0 LLM. (T-e11b)

Detection is by FACTS, not a vocabulary of words (that regex approach was rejected):
  entropy   high-Shannon string literals shaped like credentials (sk_/AKIA/ghp_/xox…)
  sinks     dangerous callsites per language, from the declarative SINKS table below
  topology  files reachable from auth/secret/crypto roots (BFS over the graph's imports)
A detector that cannot run for a language contributes nothing for it (never crashes) — fail-closed.

Drafted by the pool (groq llama-3.3-70b, T-e11b) against the frozen seam; the SINKS table and the
Shannon-entropy core are the pool's. claude-agora reviewed and rewrote scan(): file-level topology
(no symbol/file mix), StopIteration-safe BFS, single/double-quoted literals, no library-level prints,
dead-import cleanup, and a pytest that actually runs (the draft's used load_graph wrong).
"""
from __future__ import annotations

import math
import re
from collections import defaultdict, deque
from pathlib import Path

from .pcp import Mark, VerifyContext

# Topology roots: graph nodes whose source_file/label contains one of these (case-insensitive) seed
# the reachability BFS. Auditable and adjustable — not magic.
ROOTS = ("auth", "login", "session", "token", "secret", "crypto", "password", "credential")
TOPOLOGY_DEPTH = 2

# Credential-shaped prefixes: a literal starting with one of these is a secret regardless of entropy.
_CRED_PREFIXES = ("sk_", "sk-", "AKIA", "ghp_", "gho_", "xox", "glpat-", "AIza", "ya29.", "-----BEGIN")

# Declarative sink table: file extension -> [(regex, reason, severity)]. Append languages here.
SINKS: dict[str, list[tuple[str, str, str]]] = {
    ".py": [
        (r"\beval\s*\(", "eval()", "danger"),
        (r"\bexec\s*\(", "exec()", "danger"),
        (r"os\.system\s*\(", "os.system()", "danger"),
        (r"subprocess\.[A-Za-z_]+\([^)]*shell\s*=\s*True", "subprocess shell=True", "danger"),
        (r"pickle\.loads\s*\(", "pickle.loads()", "danger"),
        (r"yaml\.load\s*\((?![^)]*Loader)", "yaml.load() without Loader", "danger"),
    ],
}
_JS_SINKS = [
    (r"\beval\s*\(", "eval()", "danger"),
    (r"new\s+Function\s*\(", "new Function()", "danger"),
    (r"child_process", "child_process", "warn"),
    (r"\.innerHTML\s*=", "innerHTML assignment", "warn"),
    (r"dangerouslySetInnerHTML", "dangerouslySetInnerHTML", "warn"),
]
for _ext in (".js", ".ts", ".jsx", ".tsx"):
    SINKS[_ext] = _JS_SINKS

# String literals: single- or double-quoted, no escapes handling needed for a heuristic scan.
_STRING_RE = re.compile(r"""(['"])((?:(?!\1).){4,})\1""")
_HEX_COLOR = re.compile(r"^#(?:[0-9a-fA-F]{3,8})$")
_URL = re.compile(r"^[a-z][a-z0-9+.\-]*://")
_REPEATED = re.compile(r"^(.)\1*$")


def shannon_entropy(s: str) -> float:
    """Shannon entropy per character (bits). Stdlib only."""
    if not s:
        return 0.0
    counts: dict[str, int] = defaultdict(int)
    for ch in s:
        counts[ch] += 1
    n = len(s)
    return -sum((c / n) * math.log2(c / n) for c in counts.values())


def _looks_like_secret(literal: str) -> str | None:
    """Return a reason if the literal is credential-shaped, else None."""
    for prefix in _CRED_PREFIXES:
        if literal.startswith(prefix):
            return f"credential-shaped literal ({prefix} prefix)"
    if (len(literal) >= 24 and shannon_entropy(literal) >= 3.5
            and re.fullmatch(r"[A-Za-z0-9_\-+/=]+", literal)
            and not _HEX_COLOR.match(literal) and not _URL.match(literal)
            and not _REPEATED.match(literal)):
        return "high-entropy literal (>=24 chars, >=3.5 bits/char)"
    return None


def _source_files(root: Path, ctx: VerifyContext) -> list[str]:
    """Repo-relative source files to scan: the graph's, or a bounded walk if the graph is empty."""
    files = {n["source_file"] for n in ctx.nodes if n.get("source_file")}
    if files:
        return sorted(files)
    exts = {".py", ".js", ".ts", ".jsx", ".tsx"}
    return sorted(p.relative_to(root).as_posix()
                  for p in root.rglob("*") if p.is_file() and p.suffix in exts)


def _scan_file(root: Path, rel: str) -> list[Mark]:
    """Entropy + sink marks for one file. Never raises (unreadable file -> no marks)."""
    path = root / rel
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return []
    marks: list[Mark] = []
    ext = path.suffix.lower()
    sinks = SINKS.get(ext, [])
    for i, line in enumerate(lines, start=1):
        for m in _STRING_RE.finditer(line):
            reason = _looks_like_secret(m.group(2))
            if reason:
                marks.append(Mark("entropy", rel, i, reason, "danger"))
        for pattern, reason, severity in sinks:
            if re.search(pattern, line):
                marks.append(Mark("sink", rel, i, reason, severity))
    return marks


def _topology_marks(ctx: VerifyContext) -> list[Mark]:
    """Files reachable from an auth/secret/crypto root via imports (BFS, file-level). 0-LLM."""
    id_to_file = {n["id"]: n["source_file"] for n in ctx.nodes if n.get("source_file")}
    # file-level import adjacency (both directions: importer <-> imported)
    adj: dict[str, set[str]] = defaultdict(set)
    for link in ctx.links:
        if link.get("relation") != "imports":
            continue
        a, b = id_to_file.get(link.get("source")), id_to_file.get(link.get("target"))
        if a and b and a != b:
            adj[a].add(b)
            adj[b].add(a)
    # root files: any node whose source_file or label hits a ROOT substring
    root_files = sorted({
        n["source_file"] for n in ctx.nodes if n.get("source_file")
        and any(r in n["source_file"].lower() or r in (n.get("label") or "").lower() for r in ROOTS)
    })
    # The security surface = the roots themselves (directly sensitive) PLUS everything reachable from
    # them within TOPOLOGY_DEPTH imports. Both get a mark; the reason distinguishes provenance so a
    # file that is a root AND reachable (e.g. tokens.py: matches "token" and is imported by auth) is
    # still surfaced. reason for a root wins over a reachable reason.
    surface: dict[str, str] = {rf: "auth/secret/crypto surface (direct)" for rf in root_files}
    for rf in root_files:
        seen = {rf}
        queue = deque([(rf, 0)])
        while queue:
            cur, depth = queue.popleft()
            if depth >= TOPOLOGY_DEPTH:
                continue
            for nxt in sorted(adj[cur]):
                if nxt not in seen:
                    seen.add(nxt)
                    queue.append((nxt, depth + 1))
                    surface.setdefault(nxt, f"reachable from auth/secret surface: {rf}")
    return [Mark("topology", f, 1, reason, "info") for f, reason in sorted(surface.items())]


def scan(root: Path, ctx: VerifyContext) -> list[Mark]:
    """Run all three detector families over the repo -> deterministic marks. Pure, 0-LLM."""
    marks: list[Mark] = []
    for rel in _source_files(root, ctx):
        marks.extend(_scan_file(root, rel))
    marks.extend(_topology_marks(ctx))
    marks.sort(key=lambda m: (m.file, m.line, m.family, m.reason))
    return marks
