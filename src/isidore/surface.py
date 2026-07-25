"""API surface extraction from SOURCE TEXT — the zero-LLM substrate of `isidore whatsnew`.

The scanner in `graph.py` answers "what symbols exist in this working tree". This module answers a
different question: **what is the callable/declared surface of one file's text, with its signature**,
so two revisions of that text can be compared symbol by symbol. Two properties make it a separate
module rather than a scanner flag:

- **It takes text, never a path.** A changelog compares a file as it was at `<since>` against how it
  is at `<until>`; the old revision only exists as a git blob. Working on text means `whatsnew` never
  needs a worktree, a checkout, or a temp dir.
- **It descends into types and records signatures.** `graph.py::_scan_python_file` deliberately emits
  only top-level symbols, so a method added to an existing class is invisible to it — and a method is
  exactly what a new API usually is (verified on GICS 1.5.2: the new RPC surfaces as
  `GICSNodeClient.putManyConditional`, a class method with a multi-line signature). Signatures matter
  because "the parameter list changed" is news that no existence check can see.

Language coverage reuses `langspec` where it is strong — the per-language comment/string sanitizer and
the declaration keyword table — and adds the two things its node-oriented rules do not do:

1. **Multi-line headers.** langspec's rules match one physical line, so a signature whose parameters
   span lines (prettier's default for anything long) is missed. Here the sanitized text is folded into
   *logical* lines: a line with unbalanced `(` absorbs the following ones until the parens close. A
   run that never closes within `MAX_JOIN` lines is abandoned, so a `describe('x', () => {` block
   cannot swallow the symbols declared inside it.
2. **Brace-bearing parameter defaults.** langspec's method rule forbids `{}` between the parens, so
   `options: Opts = {}` defeats it. The header matcher here is paren-balanced instead.

False positives from the generic path are possible and tolerated — same honest tier as the native
scanner. A wrong *extra* symbol produces a changelog line that a reader can check against the cited
`path:line`; the failure mode this module refuses is the opposite one, silently missing a real
addition. Python never takes this path: it is parsed exactly, with `ast`.
"""
from __future__ import annotations

import ast
import re
from dataclasses import dataclass

from .langspec import LanguageSpec, sanitize, spec_for

# How many physical lines a single declaration header may span before the fold gives up. Six covers
# a formatted signature with several parameters; a longer unbalanced run is a call block, not a
# declaration, and must not be folded (it would hide every symbol inside it).
MAX_JOIN = 6

# A signature is a comparison key, not documentation: cap it so one generated 400-line literal cannot
# dominate a delta row.
MAX_SIG_CHARS = 200

KIND_FUNCTION = "function"
KIND_CLASS = "class"
KIND_METHOD = "method"
KIND_CONSTANT = "constant"

# Declaration modifiers to step over before the name. Deliberately cross-language (one table beats
# eight dialects of the same regex); a keyword that does not exist in a language simply never matches.
_MODIFIERS = (
    r"(?:export|default|public|private|protected|internal|static|async|get|set|readonly|override|"
    r"abstract|final|virtual|inline|constexpr|explicit|suspend|open|sealed|unsafe|extern|pub|"
    r"fn|func|function|def|proc|sub)\s+"
)

# `[modifiers] name[<generics>](` — the opening of a callable declaration. Matching this is not
# enough on its own: see `_declaration_tail`, which is what separates a definition from a call.
_HEADER = re.compile(r"^\s*(?:" + _MODIFIERS + r")*(?P<name>[A-Za-z_$][\w$]*)\s*(?:<[^()]*?>)?\s*\(")

# Control-flow words that read like a call header (`if (x) {`). langspec guards its own rules with the
# same idea; the header matcher needs its own copy because it accepts brace-bearing parameters.
_NOT_A_NAME = frozenset(
    "if for while switch catch return await typeof new delete throw do else yield with in of case "
    "default void try finally match loop unless elif except lambda and or not is".split()
)

# A top-level value binding: `export const X =`, `static readonly Y =`, `val z =`. Captured only at
# depth 0, where it is module surface rather than a local variable.
_CONST = re.compile(
    r"^\s*(?:(?:export|default|public|private|protected|internal|static|readonly|pub|final)\s+)*"
    r"(?:const|let|var|val|static)\s+(?P<name>[A-Za-z_$][\w$]*)\s*(?::[^=]+)?=\s*(?P<value>.*)$"
)

# NOTE on signatures and TOON: they are stored VERBATIM. `toon.encode` already quotes a field that
# contains commas, so nothing downstream needs them pre-mangled. An earlier version replaced `,`
# with `;` here "for TOON safety", and the damage surfaced where it hurts most — in the page a
# person reads, as `(self; conditions; records)`.


@dataclass(frozen=True)
class SurfaceSymbol:
    """One declared symbol of a file, as of one revision of its text.

    `qualname` is what identity is matched on across revisions (`Class.method` when a callable is
    declared inside a type, bare otherwise), and `sig` is what CHANGE is detected on.
    """
    qualname: str
    kind: str
    public: bool
    line: int
    end_line: int
    sig: str

    @property
    def name(self) -> str:
        return self.qualname.rsplit(".", 1)[-1]


def clean_sig(text: str) -> str:
    """Collapse a declaration header into a stable one-line comparison key, readable as-is.

    Whitespace is normalised (so reformatting is never reported as an API change) and the trailing
    body brace is dropped for the same reason. Everything else — parameter names, defaults, types —
    survives VERBATIM, because this same string is what a person reads in the changelog.
    """
    flat = " ".join((text or "").replace("\t", " ").split())
    if flat.endswith("{"):
        flat = flat[:-1].rstrip()
    return flat[:MAX_SIG_CHARS - 1] + "…" if len(flat) > MAX_SIG_CHARS else flat


def _declaration_tail(line: str, open_paren: int) -> str | None:
    """What follows the parameter list, or None if the parens never close on this line.

    This is the test that tells a DEFINITION from a CALL, and it matters more than it looks:
    `describe('suite', () => {` also starts with `name(` and also ends in `{`, but that brace belongs
    to a callback still INSIDE the argument list — at that point the parenthesis is not closed. A
    real declaration closes its parameters first and only then opens a body. Requiring the close
    (and rejecting a `=>` in the tail) keeps every test-framework block out of the surface.
    """
    depth = 0
    for index in range(open_paren, len(line)):
        char = line[index]
        if char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth == 0:
                return line[index + 1:]
    return None


def _is_declaration(line: str, match: re.Match) -> bool:
    tail = _declaration_tail(line, match.end() - 1)
    return tail is not None and tail.strip().endswith("{") and "=>" not in tail


def _is_public(name: str) -> bool:
    """Underscore convention. Dunders (`__init__`, `__call__`) are surface: they are how callers use
    the type. A single leading underscore is the author saying "not yours"."""
    return not name.startswith("_") or (name.startswith("__") and name.endswith("__"))


# ------------------------------------------------------------------ Python (exact, via ast)

def _py_signature(node: ast.FunctionDef | ast.AsyncFunctionDef) -> str:
    """The parameter list and return annotation, rendered from the AST rather than the source text.

    Going through `ast.unparse` per parameter makes the key immune to formatting: a signature broken
    across lines, or re-indented, unparses identically, so only a REAL change moves it.
    """
    args = node.args
    parts: list[str] = []
    positional = list(getattr(args, "posonlyargs", [])) + list(args.args)
    defaults = list(args.defaults)
    pad = len(positional) - len(defaults)
    for i, arg in enumerate(positional):
        text = arg.arg
        if arg.annotation is not None:
            text += f": {ast.unparse(arg.annotation)}"
        if i >= pad:
            text += f"={ast.unparse(defaults[i - pad])}"
        parts.append(text)
        if getattr(args, "posonlyargs", None) and arg is args.posonlyargs[-1]:
            parts.append("/")
    if args.vararg is not None:
        parts.append(f"*{args.vararg.arg}")
    elif args.kwonlyargs:
        parts.append("*")
    for arg, default in zip(args.kwonlyargs, args.kw_defaults):
        text = arg.arg
        if arg.annotation is not None:
            text += f": {ast.unparse(arg.annotation)}"
        if default is not None:
            text += f"={ast.unparse(default)}"
        parts.append(text)
    if args.kwarg is not None:
        parts.append(f"**{args.kwarg.arg}")
    rendered = f"({', '.join(parts)})"
    returns = getattr(node, "returns", None)
    if returns is not None:
        rendered += f" -> {ast.unparse(returns)}"
    return clean_sig(rendered)


def _py_constant(node: ast.stmt) -> tuple[str, str] | None:
    """A module-level binding -> (name, `= value`). Config constants are API: a consumer reads them,
    and a changed default is exactly the kind of news a changelog exists to carry."""
    if isinstance(node, ast.AnnAssign):
        target, value = node.target, node.value
    elif isinstance(node, ast.Assign) and len(node.targets) == 1:
        target, value = node.targets[0], node.value
    else:
        return None
    if not isinstance(target, ast.Name):
        return None
    try:
        rendered = ast.unparse(value) if value is not None else ""
    except Exception:                                  # unparse is total in practice; stay total anyway
        rendered = ""
    return target.id, clean_sig(f"= {rendered}" if rendered else "")


def python_surface(text: str) -> list[SurfaceSymbol] | None:
    """Exact surface of one Python source text, or None if it does not parse.

    None is not an error to swallow: it means this revision of the file cannot be compared, and the
    caller reports that as a warning instead of inventing an empty surface (which would read as
    "everything was deleted").
    """
    try:
        tree = ast.parse(text)
    except (SyntaxError, ValueError):
        return None

    out: list[SurfaceSymbol] = []

    def _end(node: ast.AST) -> int:
        return getattr(node, "end_lineno", None) or node.lineno

    def _callable(node: ast.FunctionDef | ast.AsyncFunctionDef,
                  container: str | None) -> SurfaceSymbol:
        qual = f"{container}.{node.name}" if container else node.name
        public = _is_public(node.name) and (container is None or _is_public(container))
        return SurfaceSymbol(qualname=qual, kind=KIND_METHOD if container else KIND_FUNCTION,
                             public=public, line=node.lineno, end_line=_end(node),
                             sig=_py_signature(node))

    def _walk_class(cls: ast.ClassDef, prefix: str) -> None:
        for item in cls.body:
            if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                out.append(_callable(item, prefix))
            elif isinstance(item, ast.ClassDef):
                # One more level (a nested type IS surface); deeper nesting is implementation detail.
                nested = f"{prefix}.{item.name}"
                out.append(SurfaceSymbol(qualname=nested, kind=KIND_CLASS,
                                         public=_is_public(item.name) and _is_public(prefix),
                                         line=item.lineno, end_line=_end(item), sig=""))
                for sub in item.body:
                    if isinstance(sub, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        out.append(_callable(sub, nested))

    for item in tree.body:
        if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
            out.append(_callable(item, None))
        elif isinstance(item, ast.ClassDef):
            out.append(SurfaceSymbol(qualname=item.name, kind=KIND_CLASS, public=_is_public(item.name),
                                     line=item.lineno, end_line=_end(item), sig=""))
            _walk_class(item, item.name)
        else:
            const = _py_constant(item)
            if const is not None:
                name, sig = const
                out.append(SurfaceSymbol(qualname=name, kind=KIND_CONSTANT, public=_is_public(name),
                                         line=item.lineno, end_line=_end(item), sig=sig))
    return out


# ------------------------------------------------------------------ everything else (langspec)

def logical_lines(clean: str) -> list[tuple[int, int, str]]:
    """Fold a sanitized text into (start_line, end_line, text) logical lines.

    A line whose parentheses do not close absorbs the following ones until they do, which is what
    turns a wrapped signature back into something a one-line rule can match. If they never close
    within MAX_JOIN lines the fold is ABANDONED and the line is emitted alone — the run is a call
    block (`describe('x', () => {`), and folding it would hide every declaration nested inside.
    """
    lines = clean.split("\n")
    out: list[tuple[int, int, str]] = []
    i, total = 0, len(lines)
    while i < total:
        balance = lines[i].count("(") - lines[i].count(")")
        if balance <= 0:
            out.append((i + 1, i + 1, lines[i]))
            i += 1
            continue
        buffer, j = [lines[i]], i + 1
        while j < total and balance > 0 and (j - i) <= MAX_JOIN:
            balance += lines[j].count("(") - lines[j].count(")")
            buffer.append(lines[j])
            j += 1
        if balance > 0:
            out.append((i + 1, i + 1, lines[i]))
            i += 1
            continue
        out.append((i + 1, j, " ".join(part.strip() for part in buffer)))
        i = j
    return out


def generic_surface(text: str, spec: LanguageSpec) -> list[SurfaceSymbol]:
    """Surface of a non-Python source text, via the langspec table plus the folding above.

    Type declarations and language-specific callable forms come from `spec.symbol_rules` (so every
    language the scanner knows is covered without restating its keywords); the paren-balanced header
    matcher is the fallback that catches what those rules structurally cannot.
    """
    clean = sanitize(text, spec)
    raw_lines = text.split("\n")
    type_rules = [rule for rule in spec.symbol_rules if rule.suffix == ""]
    call_rules = [rule for rule in spec.symbol_rules if rule.suffix == "()"]

    out: list[SurfaceSymbol] = []
    depth = 0
    open_types: list[tuple[str, int]] = []          # (type name, brace depth it opened at)

    for start, end, line in logical_lines(clean):
        stripped = line.strip()
        opens_body = stripped.endswith("{")
        name: str | None = None
        kind = KIND_FUNCTION

        for rule in type_rules:
            match = rule.pattern.search(line)
            if match and match.group("name"):
                name, kind = match.group("name"), KIND_CLASS
                break
        if name is None:
            for rule in call_rules:
                match = rule.pattern.search(line)
                if match and match.group("name"):
                    name = match.group("name")
                    break
        if name is None and opens_body:
            match = _HEADER.match(line)
            if match and match.group("name").lower() not in _NOT_A_NAME and _is_declaration(line, match):
                name = match.group("name")
        if name is None and depth == 0:
            match = _CONST.match(line)
            if match and match.group("name") not in _NOT_A_NAME:
                name, kind = match.group("name"), KIND_CONSTANT

        if name is not None and depth <= 1:
            container = open_types[-1][0] if open_types else None
            if kind == KIND_FUNCTION and container:
                kind = KIND_METHOD
            qual = f"{container}.{name}" if container and kind == KIND_METHOD else name
            # The signature comes from the ORIGINAL lines: sanitize blanks string contents, and a
            # default value like `sep = ','` is part of what changed.
            source = " ".join(part.strip() for part in raw_lines[start - 1:end])
            sig = clean_sig(source if kind != KIND_CLASS else "")
            public = _is_public(name) and not re.search(r"\bprivate\b", source)
            if container:
                public = public and _is_public(container)
            out.append(SurfaceSymbol(qualname=qual, kind=kind, public=public,
                                     line=start, end_line=end, sig=sig))
            if kind == KIND_CLASS and opens_body:
                open_types.append((name, depth))

        if not spec.track_braces:
            continue
        for char in line:
            if char == "{":
                depth += 1
            elif char == "}":
                depth = max(0, depth - 1)
                while open_types and depth <= open_types[-1][1]:
                    open_types.pop()
    return out


def extract_surface(text: str, suffix: str) -> list[SurfaceSymbol] | None:
    """Surface of one file's text, routed by extension. None = not comparable source.

    None means either "not code we can parse" (a document, an unknown extension) or "this revision
    does not parse", and both must reach the caller as a warning rather than as an empty surface —
    an empty surface would read as a wholesale deletion.
    """
    if suffix.lower() == ".py":
        return python_surface(text)
    spec = spec_for(suffix.lower())
    if spec is None or spec.kind != "code":
        return None
    return generic_surface(text, spec)


__all__ = ["KIND_CLASS", "KIND_CONSTANT", "KIND_FUNCTION", "KIND_METHOD", "MAX_JOIN",
           "MAX_SIG_CHARS", "SurfaceSymbol", "clean_sig", "extract_surface", "generic_surface",
           "logical_lines", "python_surface"]
