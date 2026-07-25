"""isidore whatsnew — a changelog you can re-verify, instead of one you have to trust.

A module page answers "what is this and how do I change it safely". It cannot answer "what is NEW
here", and regenerating it does not help: a new RPC is just one more symbol in a module that already
has dozens, so the page prompt has no reason to mention it. That gap is what sends a reader back to
a hand-written CHANGELOG — precisely the hand-written documentation this tool exists to retire.

The command works in two tiers, and the first one is free:

1. **The delta (0 LLM).** Two git revisions, the API surface of every changed file extracted from
   both blobs (`surface.py`), and a typed difference between them: symbols added, symbols removed,
   signatures changed, files added/removed/renamed. Nothing here is generated, so nothing here can
   be invented — every row is a coordinate into the repository. This tier alone is a usable
   changelog and it costs nothing.
2. **The prose (`--execute`, one call per changed module).** The model receives ONLY the structured
   delta — never a raw diff — plus commit subjects explicitly marked as non-evidence, and writes
   bullets under the SAME certificate discipline as a wiki page: each claim anchored to `path:line`
   by a content hash, verified against a deterministic oracle, and REFUTED claims kept in the
   certificate but never published. Measured hallucination rates in LLM-generated change summaries
   are 20-50% (arXiv 2508.08661); the refutation pass is what makes the difference between a
   changelog and a rumour.

Three decisions are load-bearing and are documented where they are enforced:

- **Removals are never written by the model** (`_llm_entries`). "X was removed" cannot be anchored to
  the new tree — there is nothing to cite — so it is reported by the deterministic tier only.
- **Commit messages are context, never evidence** (`WHATSNEW_PROMPT`). They are prose written by a
  human who may be wrong; the code delta is the ground truth. The model may read them to phrase a
  bullet, never to assert a fact.
- **Private symbols stay in the delta** (`build_delta`). A daemon RPC is dispatched by string and its
  handler is usually private, so a public-only filter would hide exactly the news that matters. The
  RENDER separates `api` from `internal`; the data keeps everything.

The artifact is a `wiki/whatsnew/<since>..<until>.md` page with a `.cert.json` sidecar. It is a
photograph of a range, not a living page: it never enters `state["pages"]`, so `claims --check` will
not slowly mark it stale as the code moves on past the range it describes. (`isidore verify` globs
`wiki/*.md` non-recursively, so these pages stay out of its loop by construction.)
"""
from __future__ import annotations

import re
import subprocess
from dataclasses import dataclass, field
from pathlib import Path

from .claims import (
    CLAIMS_PROMPT_ADDENDUM,
    anchor_claims,
    is_negative_existential,
    parse_claims_block,
)
from .graph import ISIDORE_DIR, module_of
from .langspec import BINARY_EXTS
from .pcp import CERT_SUFFIX, VerifyContext, write_certificate
from .pipeline import (
    DEFAULT_MODULE_DEPTH,
    LINT_REPAIR_ADDENDUM,
    annotate_unverified_paths,
    lint_cited_paths,
    read_excerpt,
)
from .render import WIKI_DIRNAME
from .surface import KIND_CLASS, SurfaceSymbol, extract_surface
from .toon import encode
from .verify import build_certificate

WHATSNEW_DIRNAME = "whatsnew"

# The typed vocabulary of novelty. Naming each kind (rather than emitting one undifferentiated "this
# changed") is what lets a reader — and a CI gate — treat an added symbol differently from a changed
# signature, and it is the same discipline API-diff tools use to stay auditable.
SYMBOL_ADDED = "symbol_added"
SYMBOL_REMOVED = "symbol_removed"
SIGNATURE_CHANGED = "signature_changed"
FILE_ADDED = "file_added"
FILE_REMOVED = "file_removed"
FILE_RENAMED = "file_renamed"
NOVELTY_KINDS = (SYMBOL_ADDED, SYMBOL_REMOVED, SIGNATURE_CHANGED,
                 FILE_ADDED, FILE_REMOVED, FILE_RENAMED)

# Kinds the model is allowed to write about: they can be cited in the tree that exists NOW.
_WRITABLE_KINDS = frozenset({SYMBOL_ADDED, SIGNATURE_CHANGED, FILE_ADDED, FILE_RENAMED})

# Where a change lives. A changelog that opens with "added `describe` in daemon-hardkill.test.ts" has
# buried its own headline: the reader wants the product's surface first. Test and documentation
# changes are still reported — they are real news — but in their own sections, and the LLM tier only
# ever writes about API and internal rows.
AREA_API = "api"
AREA_INTERNAL = "internal"
AREA_TESTS = "tests"
AREA_DOCS = "docs"

_TEST_MARKERS = ("/tests/", "/test/", "/__tests__/", "/spec/", ".test.", ".spec.", "_test.")
_DOC_SUFFIXES = frozenset({".md", ".markdown", ".rst", ".txt", ".adoc"})

DEFAULT_MAX_CALLS = 8
DEFAULT_MAX_PROMPT_CHARS = 20_000
_EXCERPT_RADIUS = 5
_MAX_EXCERPTS = 6
_MAX_HINTS = 30
_LARGE_RANGE = 500

_GIT_TIMEOUT = 120


class WhatsnewError(RuntimeError):
    """Git could not answer, or a ref does not resolve. Fail closed: never guess a range."""


@dataclass(frozen=True)
class DeltaEntry:
    """One typed novelty row. `file` is always the path as of `until` (renames map old -> new)."""
    kind: str
    file: str
    qualname: str = ""
    symbol_kind: str = ""
    public: bool = True
    line: int = 0
    sig: str = ""
    old_sig: str = ""
    old_file: str = ""
    detail: str = ""

    @property
    def evidence(self) -> str:
        return f"{self.file}:{self.line}" if self.line else self.file

    @property
    def area(self) -> str:
        posix = f"/{self.file.replace(chr(92), '/')}"
        name = posix.rsplit("/", 1)[-1]
        if any(marker in posix for marker in _TEST_MARKERS) or name.startswith("test_"):
            return AREA_TESTS
        if Path(posix).suffix.lower() in _DOC_SUFFIXES:
            return AREA_DOCS
        return AREA_API if self.public else AREA_INTERNAL


@dataclass
class SurfaceDelta:
    since_ref: str = ""
    until_ref: str = ""
    since_sha: str = ""
    until_sha: str = ""
    entries: list[DeltaEntry] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    changed_files: list[str] = field(default_factory=list)

    @property
    def short_range(self) -> str:
        return f"{self.since_sha[:7]}..{self.until_sha[:7]}"

    def by_area(self, area: str) -> list[DeltaEntry]:
        return [e for e in self.entries if e.area == area]

    def public_entries(self) -> list[DeltaEntry]:
        return self.by_area(AREA_API)


@dataclass
class WhatsnewResult:
    delta: SurfaceDelta
    page_path: Path | None = None
    cert_path: Path | None = None
    calls: int = 0
    retries: int = 0
    claims_published: int = 0
    claims_refuted: int = 0
    claims_dropped: int = 0
    quarantined: bool = False
    warnings: list[str] = field(default_factory=list)


# ------------------------------------------------------------------ git plumbing

def _git(repo: Path, *args: str, binary: bool = False) -> bytes | str:
    """Run one git command, argv-style. Any failure is an exception: a changelog built on a silently
    empty git answer would claim "nothing changed", which is the worst possible lie here."""
    try:
        out = subprocess.run(
            ["git", "-c", "core.quotepath=false", *args],
            cwd=repo, capture_output=True, timeout=_GIT_TIMEOUT, check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise WhatsnewError(f"git {' '.join(args)} failed: {exc}") from exc
    if out.returncode != 0:
        detail = out.stderr.decode("utf-8", errors="replace").strip().splitlines()
        raise WhatsnewError(f"git {' '.join(args)}: {detail[-1] if detail else 'failed'}")
    return out.stdout if binary else out.stdout.decode("utf-8", errors="replace")


def resolve_ref(repo: Path, ref: str) -> str:
    """A ref -> its full commit sha. Raises WhatsnewError if it does not resolve, so a typo in a ref
    never degrades into an empty (and therefore false) changelog.

    `rev-list -n 1` rather than `rev-parse --verify <ref>^{commit}`: both peel an annotated tag to
    its commit, but the brace form is mangled by the MSYS2 build of git on Windows (its argument
    conversion eats `^{...}`), which made the command fail in one shell and work in another on the
    same machine. This form is portable across both.
    """
    try:
        sha = str(_git(repo, "rev-list", "-n", "1", ref)).strip()
    except WhatsnewError as exc:
        raise WhatsnewError(f"cannot resolve ref '{ref}': {exc}") from exc
    if not sha:
        raise WhatsnewError(f"cannot resolve ref '{ref}': no commit found")
    return sha


def _blob(repo: Path, sha: str, path: str) -> str | None:
    """One file's text at one revision, or None when it is absent or binary."""
    try:
        raw = _git(repo, "cat-file", "blob", f"{sha}:{path}", binary=True)
    except WhatsnewError:
        return None
    if not isinstance(raw, bytes) or b"\0" in raw[:4096]:
        return None
    return raw.decode("utf-8", errors="replace")


def _is_comparable(path: str) -> bool:
    """Skip generated wiki output, the graph store, and anything not source code. Comparing the wiki
    against itself would report the tool's own writing as repository news."""
    posix = path.replace("\\", "/")
    if posix.startswith((f"{WIKI_DIRNAME}/", f"{ISIDORE_DIR}/")):
        return False
    suffix = Path(posix).suffix.lower()
    return bool(suffix) and suffix not in BINARY_EXTS


def commit_hints(repo: Path, since_sha: str, until_sha: str, n: int = _MAX_HINTS) -> list[str]:
    """Commit subjects in the range. CONTEXT ONLY — see WHATSNEW_PROMPT. Never fatal."""
    try:
        raw = str(_git(repo, "log", "--no-merges", f"-{n}", "--pretty=%s",
                       f"{since_sha}..{until_sha}"))
    except WhatsnewError:
        return []
    return [line.strip() for line in raw.splitlines() if line.strip()]


def _name_status(repo: Path, since_sha: str, until_sha: str) -> list[tuple[str, str, str]]:
    """[(status, old_path, new_path)] between two revisions, NUL-parsed.

    Two-dot (`a b`) compares the two end states, which is what a changelog describes; `-z` keeps
    paths with spaces or non-ASCII intact, which `--name-status` alone would quote and mangle.
    """
    raw = str(_git(repo, "diff", "--name-status", "--find-renames", "-z", since_sha, until_sha))
    fields = [f for f in raw.split("\0") if f != ""]
    out: list[tuple[str, str, str]] = []
    i = 0
    while i < len(fields):
        status = fields[i]
        code = status[0]
        if code in ("R", "C"):                       # rename/copy: two paths follow
            if i + 2 >= len(fields):
                break
            out.append((code, fields[i + 1], fields[i + 2]))
            i += 3
        else:
            if i + 1 >= len(fields):
                break
            out.append((code, fields[i + 1], fields[i + 1]))
            i += 2
    return out


# ------------------------------------------------------------------ the delta

def _surface_of(repo: Path, sha: str, path: str) -> list[SurfaceSymbol] | None:
    text = _blob(repo, sha, path)
    if text is None:
        return None
    return extract_surface(text, Path(path).suffix)


def _file_summary(symbols: list[SurfaceSymbol] | None, limit: int = 8) -> str:
    """A compact roll-up of what a whole added/removed file declares."""
    if not symbols:
        return ""
    public = [s.qualname for s in symbols if s.public] or [s.qualname for s in symbols]
    head = ", ".join(public[:limit])
    return f"{head}, +{len(public) - limit} more" if len(public) > limit else head


def _diff_surfaces(old: list[SurfaceSymbol], new: list[SurfaceSymbol], path: str) -> list[DeltaEntry]:
    """Typed difference between two surfaces of the same file.

    Identity is the qualified name; change is the signature. Overloads (one name declared more than
    once) are compared as multisets of signatures, so a genuinely added overload shows up while a
    reordering does not.
    """
    entries: list[DeltaEntry] = []
    old_by_name: dict[str, list[SurfaceSymbol]] = {}
    new_by_name: dict[str, list[SurfaceSymbol]] = {}
    for symbol in old:
        old_by_name.setdefault(symbol.qualname, []).append(symbol)
    for symbol in new:
        new_by_name.setdefault(symbol.qualname, []).append(symbol)

    for name, news in new_by_name.items():
        olds = old_by_name.get(name)
        if not olds:
            for symbol in news:
                entries.append(DeltaEntry(kind=SYMBOL_ADDED, file=path, qualname=name,
                                          symbol_kind=symbol.kind, public=symbol.public,
                                          line=symbol.line, sig=symbol.sig))
            continue
        old_sigs = sorted(s.sig for s in olds)
        new_sigs = sorted(s.sig for s in news)
        if old_sigs == new_sigs:
            continue
        if len(news) > len(olds):                    # a new overload of an existing name
            for symbol in news:
                if symbol.sig not in old_sigs:
                    entries.append(DeltaEntry(kind=SYMBOL_ADDED, file=path, qualname=name,
                                              symbol_kind=symbol.kind, public=symbol.public,
                                              line=symbol.line, sig=symbol.sig))
            continue
        # A class carries no signature of its own, so a difference here is body churn, not surface.
        symbol = news[0]
        if symbol.kind == KIND_CLASS and not symbol.sig:
            continue
        entries.append(DeltaEntry(kind=SIGNATURE_CHANGED, file=path, qualname=name,
                                  symbol_kind=symbol.kind, public=symbol.public,
                                  line=symbol.line, sig=symbol.sig, old_sig=olds[0].sig))

    for name, olds in old_by_name.items():
        if name not in new_by_name:
            symbol = olds[0]
            entries.append(DeltaEntry(kind=SYMBOL_REMOVED, file=path, qualname=name,
                                      symbol_kind=symbol.kind, public=symbol.public,
                                      line=0, old_sig=symbol.sig))
    return entries


def build_delta(repo: Path, since: str, until: str = "HEAD") -> SurfaceDelta:
    """The zero-LLM core: a typed API-surface difference between two revisions.

    Private symbols are KEPT. A daemon RPC is dispatched by string and handled by a private method,
    so filtering them out here would drop the very rows that document a new endpoint; `public` rides
    along on each entry and the renderer decides what to foreground.
    """
    since_sha, until_sha = resolve_ref(repo, since), resolve_ref(repo, until)
    delta = SurfaceDelta(since_ref=since, until_ref=until, since_sha=since_sha, until_sha=until_sha)
    if since_sha == until_sha:
        return delta

    changes = _name_status(repo, since_sha, until_sha)
    comparable = [c for c in changes if _is_comparable(c[2]) or _is_comparable(c[1])]
    if len(comparable) > _LARGE_RANGE:
        delta.warnings.append(
            f"{len(comparable)} changed source files in this range — the delta covers all of them, "
            "but consider a narrower range for a readable changelog")

    for status, old_path, new_path in comparable:
        path = new_path if status != "D" else old_path
        if not _is_comparable(path):
            continue
        delta.changed_files.append(path)

        if status == "T":                            # symlink <-> file, submodule: no surface to read
            delta.warnings.append(f"{path}: type change skipped")
            continue

        if status == "A":
            new_surface = _surface_of(repo, until_sha, new_path)
            delta.entries.append(DeltaEntry(kind=FILE_ADDED, file=new_path, line=1,
                                            detail=_file_summary(new_surface)))
            for symbol in new_surface or []:
                delta.entries.append(DeltaEntry(kind=SYMBOL_ADDED, file=new_path,
                                                qualname=symbol.qualname, symbol_kind=symbol.kind,
                                                public=symbol.public, line=symbol.line,
                                                sig=symbol.sig))
            continue

        if status == "D":
            old_surface = _surface_of(repo, since_sha, old_path)
            delta.entries.append(DeltaEntry(kind=FILE_REMOVED, file=old_path,
                                            detail=_file_summary(old_surface)))
            continue

        if status in ("R", "C"):
            delta.entries.append(DeltaEntry(kind=FILE_RENAMED, file=new_path, old_file=old_path,
                                            line=1))

        old_surface = _surface_of(repo, since_sha, old_path)
        new_surface = _surface_of(repo, until_sha, new_path)
        if old_surface is None or new_surface is None:
            # One side does not parse (or is not code we read): comparing would fabricate a wholesale
            # addition or deletion. Say so instead.
            if Path(path).suffix.lower() in (".py",) or old_surface != new_surface:
                delta.warnings.append(f"{path}: surface not comparable at both revisions")
            continue
        delta.entries.extend(_diff_surfaces(old_surface, new_surface, new_path))

    delta.entries.sort(key=lambda e: (e.file, e.line, e.kind, e.qualname))
    delta.changed_files = sorted(set(delta.changed_files))
    return delta


def surface_verify_ctx(repo: Path, delta: SurfaceDelta) -> VerifyContext:
    """A verification context built from the delta's own post-state surface.

    The repository graph only carries top-level symbols, so `defines(file, Class.method)` would be
    judged FALSE for a method — refuting a claim that is true. Synthesising nodes from the surface
    extractor fixes the oracle where it is blind AND bounds it usefully: a claim about a file outside
    this range finds no node and comes back UNDECIDABLE (honest), never FALSE (a false accusation).
    """
    nodes: list[dict] = []
    for path in delta.changed_files:
        symbols = _surface_of(repo, delta.until_sha, path)
        if symbols is None:
            continue
        nodes.append({"id": path, "label": Path(path).name, "file_type": "code",
                      "source_file": path, "source_location": "L1"})
        for symbol in symbols:
            suffix = "" if symbol.kind == KIND_CLASS else "()"
            nodes.append({
                "id": f"{path}::{symbol.qualname}",
                "label": f"{symbol.name}{suffix}",
                "file_type": "code", "source_file": path,
                "source_location": f"L{symbol.line}-L{symbol.end_line}",
            })
    return VerifyContext(repo=repo, nodes=nodes, links=[], commit=delta.until_sha)


# ------------------------------------------------------------------ rendering

_KIND_LABEL = {
    SYMBOL_ADDED: "added", SYMBOL_REMOVED: "removed", SIGNATURE_CHANGED: "signature",
    FILE_ADDED: "new file", FILE_REMOVED: "deleted file", FILE_RENAMED: "renamed",
}


def _rows(entries: list[DeltaEntry]) -> list[dict]:
    return [{"kind": _KIND_LABEL.get(e.kind, e.kind), "symbol": e.qualname or Path(e.file).name,
             "where": e.evidence, "signature": e.sig or e.detail or e.old_file} for e in entries]


def render_whatsnew_toon(delta: SurfaceDelta, *, public_only: bool = False) -> str:
    """The machine/agent view: one table per area, product surface first."""
    header = (f"# isidore whatsnew · {delta.since_ref}..{delta.until_ref} "
              f"({delta.short_range}) · {len(delta.entries)} change(s) in "
              f"{len(delta.changed_files)} file(s) · 0 LLM\n")
    for warning in delta.warnings:
        header += f"# warning: {warning}\n"
    areas = [AREA_API] if public_only else [AREA_API, AREA_INTERNAL, AREA_TESTS, AREA_DOCS]
    fields = ["kind", "symbol", "where", "signature"]
    return header + encode(
        *((area, fields, _rows(delta.by_area(area))) for area in areas)) + "\n"


def _md_section(title: str, entries: list[DeltaEntry]) -> list[str]:
    if not entries:
        return []
    out = [f"## {title}", ""]
    for entry in entries:
        label = _KIND_LABEL.get(entry.kind, entry.kind)
        name = entry.qualname or entry.file
        line = f"- **{label}** `{name}` — `{entry.evidence}`"
        if entry.kind == SIGNATURE_CHANGED:
            line += f"\n  - was: `{entry.old_sig}`\n  - now: `{entry.sig}`"
        elif entry.kind == FILE_RENAMED:
            line += f" (was `{entry.old_file}`)"
        elif entry.detail:
            line += f" — declares {entry.detail}"
        elif entry.sig:
            line += f" `{entry.sig}`"
        out.append(line)
    out.append("")
    return out


def render_whatsnew_md(delta: SurfaceDelta, prose_by_module: dict[str, str] | None = None) -> str:
    """The page. Deterministic: no wall-clock, so re-running an unchanged range rewrites the same
    bytes and the certificate's prose hash stays meaningful."""
    out = [
        f"# What's new — `{delta.since_ref}..{delta.until_ref}`",
        "",
        f"Range `{delta.since_sha[:12]}..{delta.until_sha[:12]}` · "
        f"{len(delta.entries)} surface change(s) across {len(delta.changed_files)} file(s).",
        "",
    ]
    if not delta.entries:
        out += ["No API surface changes in this range.", ""]
    for warning in delta.warnings:
        out.append(f"> ⚠ {warning}")
    if delta.warnings:
        out.append("")

    if prose_by_module:
        out += ["## Summary", ""]
        for module in sorted(prose_by_module):
            out += [f"### {module}", "", prose_by_module[module].strip(), ""]

    out += _md_section("Public API", delta.by_area(AREA_API))
    out += _md_section("Internal surface", delta.by_area(AREA_INTERNAL))
    out += _md_section("Tests", delta.by_area(AREA_TESTS))
    out += _md_section("Docs", delta.by_area(AREA_DOCS))
    return "\n".join(out).rstrip() + "\n"


# ------------------------------------------------------------------ prose (--execute)

WHATSNEW_PROMPT = """You are writing the "what's new" notes for ONE module of a codebase, from a
VERIFIED list of API surface changes between two revisions.

MODULE: {module}

SURFACE CHANGES (this is the ground truth — every row was computed from the two revisions):
{rows}

{excerpts}
COMMIT HINTS (context only — these are humans' prose, NOT evidence. You may use them to phrase a
bullet or to group related changes. You must NEVER cite them, quote them as fact, or state anything
that rests on them alone. If a hint contradicts the surface rows, the rows win):
{hints}

Write 3-8 bullets, in Markdown, describing what changed for someone who USES this module. Rules:
- Cite `path:line` from the SURFACE CHANGES rows or the excerpts. Never invent a path.
- Say what the change means for a caller, not just that it happened.
- Write ONLY about what was added or changed. Do NOT write about removals or absences.
- No preamble, no headings, no conclusion. Bullets only.
"""

WHATSNEW_CLAIMS_ADDENDUM = """
For this changelog, each claim's evidence MUST be a path:line that appears in the SURFACE CHANGES
rows or the excerpts above. Do not write claims about anything being removed, missing or absent.

Choosing the predicate (a claim whose predicate cannot be proved is NOT published, so pick one that
can be checked):
- `defines:<file>;<symbol>` — works for EVERY language. This is the right choice by default. For a
  method, name it as `Class.method`.
- `signature:<function>;<param1>;<param2>;...` — Python files ONLY, and it must list EVERY
  parameter in order, INCLUDING `self` for a method. Omitting `self` makes the claim false.
- `value:<name>;<literal>` — Python files only.
Never use `signature:` or `value:` for a non-Python file; use `defines:` there instead.
"""


# A bullet that ends in `... | path:line | predicate` is the model echoing the claims block inline
# instead of (or as well as) fencing it. The claims themselves are parsed and verified from the
# fenced block; what is left here is raw syntax leaking into the page a human reads.
# The middle field is matched loosely (`path:line` anywhere in it) because a model wraps it in
# backticks or quotes as often as not — the first version of this pattern anchored on the digits and
# was defeated by a single trailing backtick.
_INLINE_CLAIM_ROW = re.compile(r"^(?P<text>.*?)\s*\|[^|]*?[^|\s]:\d+[^|]*\|.*$")


def strip_inline_claim_rows(markdown: str) -> str:
    """Drop the trailing `| evidence | predicate` a model sometimes appends to its own bullets.

    Observed against a real provider: the prose stayed correct but every daemon bullet carried the
    machine syntax after it. Removing it is presentation only — the claim keeps its verdict in the
    certificate either way.
    """
    out = []
    for line in markdown.splitlines():
        match = _INLINE_CLAIM_ROW.match(line)
        out.append(match.group("text").rstrip() if match and match.group("text").strip() else line)
    return "\n".join(out)


def _llm_entries(delta: SurfaceDelta) -> list[DeltaEntry]:
    """What the model is allowed to write about: product surface, and only what can be cited in the
    tree as it exists at `until`. Removals are the deterministic tier's job (there is no line to
    point at, so a sentence about one is unverifiable by construction), and test/doc churn is not
    worth a paid call."""
    return [e for e in delta.entries
            if e.kind in _WRITABLE_KINDS and e.area in (AREA_API, AREA_INTERNAL)]


def _group_by_module(entries: list[DeltaEntry], depth: int) -> dict[str, list[DeltaEntry]]:
    groups: dict[str, list[DeltaEntry]] = {}
    for entry in entries:
        groups.setdefault(module_of(entry.file, depth), []).append(entry)
    return groups


def _prompt_for_module(repo: Path, module: str, entries: list[DeltaEntry], hints: list[str],
                       max_chars: int) -> str:
    rows = "\n".join(
        f"- [{_KIND_LABEL.get(e.kind, e.kind)}] {e.qualname or e.file} — {e.evidence}"
        + (f" — signature: {e.sig}" if e.sig else "")
        + (f" (was: {e.old_sig})" if e.old_sig else "")
        for e in entries)
    excerpts = ""
    for entry in entries[:_MAX_EXCERPTS]:
        if entry.line:
            excerpts += read_excerpt(repo, entry.file, f"L{entry.line}", _EXCERPT_RADIUS)
    if excerpts:
        excerpts = f"EXCERPTS FROM THE CURRENT CODE:\n{excerpts}\n"
    prompt = WHATSNEW_PROMPT.format(
        module=module, rows=rows, excerpts=excerpts,
        hints="\n".join(f"- {h}" for h in hints) or "- (none)",
    ) + CLAIMS_PROMPT_ADDENDUM + WHATSNEW_CLAIMS_ADDENDUM
    return prompt[:max_chars]


def generate_prose(repo: Path, delta: SurfaceDelta, hints: list[str], generator,
                   *, max_calls: int = DEFAULT_MAX_CALLS,
                   max_prompt_chars: int = DEFAULT_MAX_PROMPT_CHARS,
                   module_depth: int = DEFAULT_MODULE_DEPTH) -> tuple[dict[str, str], list[dict], dict]:
    """One bounded call per changed module -> (prose by module, anchored claims, stats).

    The post-processing order mirrors the page compiler exactly, because every step of it exists to
    catch a different way a model goes wrong: absence claims are unanchorable, off-range citations
    are outside what this range can prove, phantom paths get one bounded repair attempt and then a
    visible quarantine mark rather than a silent deletion.
    """
    stats = {"calls": 0, "retries": 0, "dropped": 0, "quarantined": False}
    prose: dict[str, str] = {}
    claims: list[dict] = []
    in_range = set(delta.changed_files)

    groups = _group_by_module(_llm_entries(delta), module_depth)
    ordered = sorted(groups.items(), key=lambda kv: (-len(kv[1]), kv[0]))
    for module, entries in ordered:
        if max_calls and stats["calls"] >= max_calls:
            break
        prompt = _prompt_for_module(repo, module, entries, hints, max_prompt_chars)
        raw = generator(prompt)
        stats["calls"] += 1

        markdown, raw_claims = parse_claims_block(raw)
        kept_claims = []
        for claim in raw_claims:
            if is_negative_existential(claim.get("statement", "")):
                stats["dropped"] += 1
                continue
            cited = (claim.get("evidence") or "").replace("\\", "/").rsplit(":", 1)[0]
            if cited not in in_range:
                # Outside the range this artifact describes: nothing here can prove it.
                stats["dropped"] += 1
                continue
            kept_claims.append(claim)

        missing = lint_cited_paths(markdown, repo)
        if missing and (not max_calls or stats["calls"] < max_calls):
            repair = prompt + LINT_REPAIR_ADDENDUM.format(paths=", ".join(sorted(missing)))
            raw = generator(repair)
            stats["calls"] += 1
            stats["retries"] += 1
            markdown, raw_claims = parse_claims_block(raw)
            kept_claims = [c for c in raw_claims
                           if not is_negative_existential(c.get("statement", ""))
                           and (c.get("evidence") or "").replace("\\", "/").rsplit(":", 1)[0] in in_range]
            missing = lint_cited_paths(markdown, repo)
        if missing:
            markdown = annotate_unverified_paths(markdown, set(missing))
            stats["quarantined"] = True

        anchored, dropped, _repaired = anchor_claims(repo, kept_claims, in_range)
        stats["dropped"] += dropped
        claims.extend(anchored)
        prose[module] = strip_inline_claim_rows(markdown).strip()
    return prose, claims, stats


# ------------------------------------------------------------------ the command

def run_whatsnew(repo: Path, since: str, until: str = "HEAD", *, execute: bool = False,
                 generator=None, max_calls: int = DEFAULT_MAX_CALLS,
                 module_depth: int = DEFAULT_MODULE_DEPTH) -> WhatsnewResult:
    """Build the delta, optionally write the prose, and persist page + certificate."""
    delta = build_delta(repo, since, until)
    result = WhatsnewResult(delta=delta, warnings=list(delta.warnings))

    prose: dict[str, str] = {}
    claims: list[dict] = []
    if execute and delta.until_sha != resolve_ref(repo, "HEAD"):
        # Checked before anything is written, and regardless of whether the range turned out empty:
        # the request itself is impossible to honour. Claims are anchored and verified against the
        # working tree, so prose about any other revision could never be checked.
        raise WhatsnewError(
            "--execute requires --until to be HEAD: claims are anchored and verified against the "
            "working tree, so prose about any other revision could not be checked")
    if execute and delta.entries:
        dirty = str(_git(repo, "status", "--porcelain")).strip()
        if dirty:
            result.warnings.append(
                "working tree is dirty — claims anchor to the files on disk, not to HEAD")
        if generator is None:
            from .llm import default_generator
            generator = default_generator()
        prose, claims, stats = generate_prose(
            repo, delta, commit_hints(repo, delta.since_sha, delta.until_sha), generator,
            max_calls=max_calls, module_depth=module_depth)
        result.calls = stats["calls"]
        result.retries = stats["retries"]
        result.claims_dropped = stats["dropped"]
        result.quarantined = bool(stats["quarantined"])

    markdown = render_whatsnew_md(delta, prose or None)
    page_name = f"{WHATSNEW_DIRNAME}/{delta.short_range}"
    out_dir = repo / WIKI_DIRNAME / WHATSNEW_DIRNAME
    out_dir.mkdir(parents=True, exist_ok=True)
    page_path = out_dir / f"{delta.short_range}.md"
    page_path.write_text(markdown, encoding="utf-8")

    ctx = surface_verify_ctx(repo, delta)
    cert = build_certificate(page_name, markdown, claims, ctx)
    cert.graph_commit = delta.until_sha
    cert_path = out_dir / f"{delta.short_range}.md{CERT_SUFFIX}"
    write_certificate(cert, cert_path)

    result.page_path = page_path
    result.cert_path = cert_path
    result.claims_refuted = sum(1 for c in cert.claims if c.verdict == "FALSE")
    result.claims_published = len(cert.claims) - result.claims_refuted
    return result


def _cmd_whatsnew(args) -> int:
    repo = args.repo.resolve()
    try:
        result = run_whatsnew(repo, args.since, args.until, execute=args.execute,
                              max_calls=args.max_calls)
    except WhatsnewError as exc:
        print(f"[isidore] {exc}")
        return 2
    delta = result.delta

    if args.md:
        print(render_whatsnew_md(delta, None))
    else:
        print(render_whatsnew_toon(delta, public_only=args.public_only))
    for warning in result.warnings:
        print(f"[isidore] warning: {warning}")
    print(f"[isidore] wrote {result.page_path} (+ certificate)")
    if args.execute:
        print(f"[isidore] {result.calls} call(s), {result.retries} retry(ies) · claims: "
              f"{result.claims_published} published, {result.claims_refuted} refuted, "
              f"{result.claims_dropped} dropped"
              + (" · QUARANTINED" if result.quarantined else ""))
    return 0


def register_cli(sub) -> None:
    parser = sub.add_parser("whatsnew", help="verifiable changelog of an API-surface delta (0 LLM by default)")
    parser.add_argument("--repo", type=Path, default=Path("."))
    parser.add_argument("--since", required=True, help="git ref to compare FROM")
    parser.add_argument("--until", default="HEAD", help="git ref to compare TO (default HEAD)")
    parser.add_argument("--execute", action="store_true",
                        help="also write prose (one LLM call per changed module; requires --until HEAD)")
    parser.add_argument("--public-only", action="store_true", help="print only public surface")
    parser.add_argument("--max-calls", type=int, default=DEFAULT_MAX_CALLS)
    parser.add_argument("--md", action="store_true", help="print Markdown instead of TOON")
    parser.set_defaults(func=_cmd_whatsnew)
