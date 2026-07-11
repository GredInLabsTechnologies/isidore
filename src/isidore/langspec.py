"""Language-agnostic symbol extraction: one engine, the language is *data*.

Isidore's native scanner used to understand a single language (Python, via stdlib `ast`).
Everything else was invisible. This module lifts that ceiling without betraying Isidore's
identity — **zero dependencies, stdlib only, runs on any architecture** (no tree-sitter, no
native wheels, no external binary).

The bet mirrors Isidore's own: for a *structure* wiki you do not need a perfect AST, you need
"what symbols exist and on which line". That is recoverable from a small, declarative table:

    LANGUAGES: {extension -> LanguageSpec}

A single engine (`extract`) interprets each `LanguageSpec`. Adding a language is adding a row,
never new control flow. Three honest tiers of degradation:

  1. Python                      -> exact stdlib `ast` (kept in graph.py, most precise).
  2. Known brace/decl languages  -> this engine: declarative symbol rules over a
                                    comment/string-sanitized, brace-depth-tracked scan.
  3. Any other text file         -> a bare file node (universal coverage, no symbols).

The engine is deliberately structural, not a compiler: it sanitizes comments and string
literals so braces/keywords inside them do not lie, tracks brace nesting so it only accepts
top-level and one-level-nested declarations (functions + methods + types), and recovers each
symbol's line span by matching its opening brace to its close. False positives are possible and
tolerated — exactly as the README already frames the native scanner ("intentionally simple; for
richer analysis bring your own graph"). Precision remains available via `--graph`.
"""
from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class SymbolRule:
    """One declarative way a symbol is declared. `pattern` must expose a named group `name`."""
    pattern: re.Pattern
    suffix: str = ""          # "()" for callables, "" for types — matches the Python scanner's style


@dataclass(frozen=True)
class LanguageSpec:
    name: str
    kind: str = "code"                                   # "code" | "document"
    line_comments: tuple[str, ...] = ()                  # e.g. ("//",) or ("#",)
    block_comments: tuple[tuple[str, str], ...] = ()     # e.g. (("/*", "*/"),)
    string_delims: tuple[str, ...] = ()                  # single-char delimiters, backslash-escaped
    symbol_rules: tuple[SymbolRule, ...] = ()
    import_rules: tuple[re.Pattern, ...] = ()            # each must expose a named group `mod`
    track_braces: bool = True                            # brace langs; False => flat (accept any depth)
    max_symbol_depth: int = 1                            # 0 = top-level only; 1 also captures methods


# --------------------------------------------------------------------- engine

def sanitize(text: str, spec: LanguageSpec, *, blank_strings: bool = True) -> str:
    """Blank out comment (and, by default, string) *contents*, preserving newlines and length.

    A char state machine so that braces, keywords and delimiters living inside a string or a
    comment can never be mistaken for code. Length preservation keeps line numbers exact.

    `blank_strings=False` keeps string contents intact (still skipping over them so a `//` inside a
    literal is not read as a comment) — used for import extraction, where the imported module path
    lives *inside* a string and must survive.
    """
    if not (spec.line_comments or spec.block_comments or spec.string_delims):
        return text
    out: list[str] = []
    i, n = 0, len(text)
    line_cs = spec.line_comments
    block_cs = spec.block_comments
    str_ds = spec.string_delims
    while i < n:
        ch = text[i]
        # line comment: blank to end of line (keep the newline)
        matched = False
        for lc in line_cs:
            if text.startswith(lc, i):
                j = text.find("\n", i)
                j = n if j == -1 else j
                out.append(" " * (j - i))
                i = j
                matched = True
                break
        if matched:
            continue
        # block comment: blank through the closer, preserving embedded newlines
        for opener, closer in block_cs:
            if text.startswith(opener, i):
                j = text.find(closer, i + len(opener))
                j = n if j == -1 else j + len(closer)
                for k in range(i, j):
                    out.append("\n" if text[k] == "\n" else " ")
                i = j
                matched = True
                break
        if matched:
            continue
        # string literal: skip to its close, honoring backslash escapes. Blank the contents (default)
        # or keep them verbatim (blank_strings=False, for import extraction).
        if ch in str_ds:
            out.append(ch)
            i += 1
            while i < n:
                c = text[i]
                if c == "\\" and i + 1 < n:            # escaped char: two positions
                    out.append(text[i:i + 2] if not blank_strings
                               else ("  " if text[i + 1] != "\n" else " \n"))
                    i += 2
                    continue
                if c == ch:
                    out.append(c)
                    i += 1
                    break
                out.append(c if (blank_strings is False or c == "\n") else " ")
                i += 1
            continue
        out.append(ch)
        i += 1
    return "".join(out)


@dataclass
class _Pending:
    index: int          # position in the produced `symbols` list
    open_depth: int     # brace depth the declaration lived at
    active: bool = False  # its `{` has been seen (a real body opened)


def extract(text: str, spec: LanguageSpec) -> tuple[list[dict], list[str]]:
    """Extract (symbols, imported-module-names) from one file's source.

    symbols: [{"name", "suffix", "line", "end_line"}], line/end_line 1-based. The engine works on a
    sanitized copy for structure but reports lines relative to the original (they share line breaks).
    """
    clean = sanitize(text, spec)
    lines = clean.split("\n")
    symbols: list[dict] = []

    # imports: scanned on a comment-stripped-but-string-preserving copy, so a commented-out import
    # is ignored yet the module path (which lives inside a string) survives.
    imports: list[str] = []
    if spec.import_rules:
        imp_text = sanitize(text, spec, blank_strings=False)
        for rule in spec.import_rules:
            for m in rule.finditer(imp_text):
                mod = (m.group("mod") or "").strip()
                if mod:
                    imports.append(mod)

    depth = 0
    pending: list[_Pending] = []

    def _close_to(level: int, end_line: int) -> None:
        # a block just closed back to `level`: finalize any active pending opened at this level
        while pending and pending[-1].open_depth >= level and pending[-1].active:
            p = pending.pop()
            symbols[p.index]["end_line"] = end_line

    for lineno, line in enumerate(lines, start=1):
        if depth <= spec.max_symbol_depth:
            for rule in spec.symbol_rules:
                m = rule.pattern.search(line)
                if not m:
                    continue
                name = m.group("name")
                if not name:
                    continue
                # a new declaration at depth d retires any prior sibling that never opened a body
                while pending and pending[-1].open_depth >= depth and not pending[-1].active:
                    pending.pop()
                symbols.append({"name": name, "suffix": rule.suffix,
                                "line": lineno, "end_line": lineno})
                if spec.track_braces:
                    pending.append(_Pending(index=len(symbols) - 1, open_depth=depth))
                break  # one symbol per line
        if not spec.track_braces:
            continue
        for ch in line:
            if ch == "{":
                depth += 1
                if pending and not pending[-1].active and pending[-1].open_depth == depth - 1:
                    pending[-1].active = True
            elif ch == "}":
                depth = max(0, depth - 1)
                _close_to(depth, lineno)
            elif ch == ";":
                # a declaration that reaches its `;` at its own depth without ever opening a body is
                # bodiless (`using`, `typedef`, a forward decl, a trait-method prototype). Retire it
                # as start-only so it cannot adopt an unrelated block that opens later and inflate its
                # span — a stale span would make changeset.py mark it dirty on unrelated edits.
                if pending and not pending[-1].active and pending[-1].open_depth == depth:
                    pending.pop()

    return symbols, imports


# ------------------------------------------------------------------- helpers

def _kw_func(keywords: str) -> re.Pattern:
    """`<keyword> name` — Go `func`, Rust `fn`, JS `function`, PHP/Swift, etc."""
    return re.compile(rf"(?:^|\s)(?:{keywords})\s+(?P<name>[A-Za-z_]\w*)")


def _kw_type(keywords: str) -> re.Pattern:
    """`<keyword> Name` — class/struct/interface/enum/trait/... across brace languages."""
    return re.compile(rf"(?:^|\s)(?:{keywords})\s+(?P<name>[A-Za-z_]\w*)")


# A generic C-family method/function definition: optional modifiers, a type, a name, a param list,
# then a brace (definition) rather than a semicolon (declaration/call). Restricted to lines that
# open a body so plain calls and prototypes are not captured.
_C_METHOD = re.compile(
    r"^\s*(?:(?:public|private|protected|internal|static|final|abstract|virtual|override|"
    r"inline|const|explicit|friend|async|suspend|open|sealed|unsafe|extern|noexcept|constexpr)\s+)*"
    r"[A-Za-z_][\w:<>,\*&\[\]\s\.]*?\s[\*&]?(?P<name>[A-Za-z_]\w*)\s*\([^;{}]*\)\s*"
    r"(?:const\s*)?(?:->[^{;]+)?(?:noexcept\s*)?\{"
)


# ------------------------------------------------------------------- the table

_C_LINE = ("//",)
_C_BLOCK = (("/*", "*/"),)
_C_STR = ('"', "'")

_TYPE_KWS = "class|struct|interface|enum|trait|protocol|record|union|object|actor|impl|namespace|module"

# Control-flow keywords that a "name(...) {" method-shorthand rule must never mistake for a symbol.
_JS_KEYWORDS = (r"(?!(?:if|for|while|switch|catch|return|function|await|typeof|new|delete|throw|"
                r"do|else|yield|with|in|of|case|default|void)\b)")

_JS_RULES = (
    SymbolRule(_kw_func("function|function\\*"), "()"),
    SymbolRule(_kw_type("class"), ""),
    # `const foo = (...) =>` / `let bar = function` / `const baz = async () =>`
    SymbolRule(re.compile(r"(?:^|\s)(?:const|let|var)\s+(?P<name>[A-Za-z_$][\w$]*)\s*=\s*"
                          r"(?:async\s*)?(?:function|\([^)]*\)\s*=>|[A-Za-z_$][\w$]*\s*=>)"), "()"),
    # method shorthand in classes/objects: `render() {`, `async load(): Promise<T> {`, `get x() {`
    SymbolRule(re.compile(
        r"^\s*(?:(?:public|private|protected|static|async|get|set|readonly|override|abstract)\s+)*"
        + _JS_KEYWORDS
        + r"(?P<name>[A-Za-z_$][\w$]*)\s*(?:<[^>]*>)?\s*\([^{}]*\)\s*(?::\s*[^={;]+?)?\{"), "()"),
)
_JS_IMPORTS = (
    re.compile(r"""(?:^|\s)import\s+(?:.+?\sfrom\s+)?['"](?P<mod>[^'"]+)['"]"""),
    re.compile(r"""require\(\s*['"](?P<mod>[^'"]+)['"]\s*\)"""),
    re.compile(r"""(?:^|\s)export\s+.*?\sfrom\s+['"](?P<mod>[^'"]+)['"]"""),
)


def _js(name: str) -> LanguageSpec:
    return LanguageSpec(name, line_comments=_C_LINE, block_comments=_C_BLOCK,
                        string_delims=_C_STR + ("`",), symbol_rules=_JS_RULES,
                        import_rules=_JS_IMPORTS)


def _brace(name: str, func_kws: str, *, extra_rules: tuple[SymbolRule, ...] = (),
           imports: tuple[re.Pattern, ...] = (), line=_C_LINE) -> LanguageSpec:
    rules = (
        SymbolRule(_kw_type(_TYPE_KWS), ""),
        *( (SymbolRule(_kw_func(func_kws), "()"),) if func_kws else () ),
        SymbolRule(_C_METHOD, "()"),
        *extra_rules,
    )
    return LanguageSpec(name, line_comments=line, block_comments=_C_BLOCK, string_delims=_C_STR,
                        symbol_rules=rules, import_rules=imports)


_GO_IMPORTS = (re.compile(r"""(?:^|\s)import\s+(?:[A-Za-z_.]+\s+)?"(?P<mod>[^"]+)\""""),)
_RUST_IMPORTS = (re.compile(r"(?:^|\s)use\s+(?P<mod>[A-Za-z_][\w:]*)"),)
_JVM_IMPORTS = (re.compile(r"(?:^|\s)import\s+(?:static\s+)?(?P<mod>[A-Za-z_][\w.]*)"),)
_PY_LIKE_IMPORTS = (
    re.compile(r"(?:^|\s)from\s+(?P<mod>[.\w]+)\s+import"),
    re.compile(r"(?:^|\s)import\s+(?P<mod>[.\w]+)"),
)

# Ruby uses `end` blocks, not braces — track_braces off, accept any depth (flat).
_RUBY = LanguageSpec(
    "Ruby", line_comments=("#",), string_delims=('"', "'"),
    symbol_rules=(
        SymbolRule(re.compile(r"(?:^|\s)def\s+(?P<name>[A-Za-z_][\w?!.]*)"), "()"),
        SymbolRule(re.compile(r"(?:^|\s)(?:class|module)\s+(?P<name>[A-Z]\w*)"), ""),
    ),
    import_rules=(re.compile(r"""(?:^|\s)require(?:_relative)?\s+['"](?P<mod>[^'"]+)['"]"""),),
    track_braces=False,
)

_SHELL = LanguageSpec(
    "Shell", line_comments=("#",), string_delims=('"', "'"),
    symbol_rules=(
        SymbolRule(re.compile(r"(?:^|\s)function\s+(?P<name>[A-Za-z_]\w*)"), "()"),
        SymbolRule(re.compile(r"^\s*(?P<name>[A-Za-z_]\w*)\s*\(\s*\)\s*\{"), "()"),
    ),
    track_braces=False,
)

_LUA = LanguageSpec(
    "Lua", line_comments=("--",), string_delims=('"', "'"),
    symbol_rules=(SymbolRule(
        re.compile(r"(?:^|\s)function\s+(?P<name>[A-Za-z_][\w.:]*)"), "()"),),
    track_braces=False,
)

_ELIXIR = LanguageSpec(
    "Elixir", line_comments=("#",), string_delims=('"',),
    symbol_rules=(
        SymbolRule(re.compile(r"(?:^|\s)def(?:p|module|macro)?\s+(?P<name>[A-Za-z_][\w?!.]*)"), "()"),
    ),
    track_braces=False,
)

# Documents: no symbols, just typed as documents so module pages can cite them.
def _doc(name: str) -> LanguageSpec:
    return LanguageSpec(name, kind="document")


LANGUAGES: dict[str, LanguageSpec] = {
    # JS / TS family
    ".js": _js("JavaScript"), ".jsx": _js("JavaScript"), ".mjs": _js("JavaScript"),
    ".cjs": _js("JavaScript"), ".ts": _js("TypeScript"), ".tsx": _js("TypeScript"),
    ".mts": _js("TypeScript"), ".cts": _js("TypeScript"),
    # C family
    ".c": _brace("C", "", imports=()), ".h": _brace("C", ""),
    ".cc": _brace("C++", ""), ".cpp": _brace("C++", ""), ".cxx": _brace("C++", ""),
    ".hpp": _brace("C++", ""), ".hh": _brace("C++", ""), ".hxx": _brace("C++", ""),
    ".m": _brace("Objective-C", ""), ".mm": _brace("Objective-C++", ""),
    # JVM
    ".java": _brace("Java", "", imports=_JVM_IMPORTS),
    ".kt": _brace("Kotlin", "fun", imports=_JVM_IMPORTS),
    ".kts": _brace("Kotlin", "fun", imports=_JVM_IMPORTS),
    ".scala": _brace("Scala", "def", imports=_JVM_IMPORTS),
    ".groovy": _brace("Groovy", "def", imports=_JVM_IMPORTS),
    ".cs": _brace("C#", "", imports=(re.compile(r"(?:^|\s)using\s+(?P<mod>[A-Za-z_][\w.]*)"),)),
    # systems
    ".go": _brace("Go", "func", imports=_GO_IMPORTS, extra_rules=(
        # Go declares types as `type Name struct/interface/...`, keyword first, name second.
        SymbolRule(re.compile(r"(?:^|\s)type\s+(?P<name>[A-Za-z_]\w*)"), ""),)),
    ".rs": _brace("Rust", "fn", imports=_RUST_IMPORTS),
    ".swift": _brace("Swift", "func"),
    ".zig": _brace("Zig", "fn"),
    ".dart": _brace("Dart", ""),
    ".php": LanguageSpec("PHP", line_comments=("//", "#"), block_comments=_C_BLOCK,
                         string_delims=_C_STR,
                         symbol_rules=(SymbolRule(_kw_type(_TYPE_KWS), ""),
                                       SymbolRule(_kw_func("function"), "()"),),
                         import_rules=(re.compile(r"(?:^|\s)(?:use|require|include)\s+(?P<mod>[A-Za-z_][\w\\]*)"),)),
    # brace-free / block languages
    ".rb": _RUBY,
    ".sh": _SHELL, ".bash": _SHELL, ".zsh": _SHELL,
    ".lua": _LUA,
    ".ex": _ELIXIR, ".exs": _ELIXIR,
    # documents
    ".md": _doc("Markdown"), ".markdown": _doc("Markdown"), ".rst": _doc("reStructuredText"),
    ".adoc": _doc("AsciiDoc"), ".txt": _doc("Text"), ".org": _doc("Org"),
}

# Text extensions that are real source/config but get no symbol extraction — still worth a file
# node so they appear in module pages. Kept separate from LANGUAGES to keep that table meaningful.
BARE_CODE_EXTS = frozenset({
    ".sql", ".r", ".jl", ".hs", ".ml", ".mli", ".fs", ".fsx", ".clj", ".cljs", ".edn",
    ".erl", ".vue", ".svelte", ".pl", ".pm", ".tcl", ".vim", ".el", ".nim", ".cr", ".v",
    ".sol", ".proto", ".graphql", ".gql", ".tf", ".hcl", ".gradle", ".cmake", ".make",
    ".dockerfile", ".ps1", ".psm1", ".bat", ".cmd", ".asm", ".s", ".vb", ".pas", ".d",
})

# Binary / non-source extensions we never open. NUL-byte sniffing (in graph.py) is the real guard;
# this is a cheap fast-path so we do not read a 4 GB video looking for a NUL.
BINARY_EXTS = frozenset({
    ".png", ".jpg", ".jpeg", ".gif", ".bmp", ".ico", ".webp", ".svg", ".pdf", ".zip", ".gz",
    ".tar", ".xz", ".bz2", ".7z", ".rar", ".jar", ".war", ".class", ".pyc", ".pyo", ".so",
    ".dylib", ".dll", ".exe", ".bin", ".o", ".a", ".lib", ".wasm", ".mp3", ".mp4", ".mov",
    ".avi", ".mkv", ".wav", ".flac", ".ogg", ".woff", ".woff2", ".ttf", ".otf", ".eot",
    ".db", ".sqlite", ".lock", ".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx",
})


def spec_for(suffix: str) -> LanguageSpec | None:
    """The LanguageSpec for a file extension (lowercased), or None if we do not extract it."""
    return LANGUAGES.get(suffix.lower())
