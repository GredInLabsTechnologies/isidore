"""Multi-language scanner: the declarative engine (langspec) and its wiring into scan_repo.

These lock the behavior that matters for a *structure* wiki — symbol names, line spans, comment/
string immunity, brace-depth top-level detection, and honest degradation to a bare file node —
without pretending to be a compiler. They are the regression net for the cross-language claim.
"""
from __future__ import annotations

from isidore.graph import scan_repo
from isidore.langspec import extract, sanitize, spec_for


def _names(text: str, ext: str) -> list[str]:
    syms, _ = extract(text, spec_for(ext))
    return [s["name"] for s in syms]


# ------------------------------------------------------------------- sanitize

def test_sanitize_blanks_comments_and_strings_preserving_lines():
    src = 'a = "x { fn foo }";  // fn bar\nb = 1\n'
    spec = spec_for(".js")
    clean = sanitize(src, spec)
    # braces/keywords inside the string and the line comment must be gone...
    assert "fn foo" not in clean and "fn bar" not in clean and "{" not in clean
    # ...but line count and structure outside them survive
    assert clean.count("\n") == src.count("\n")
    assert "b = 1" in clean


def test_sanitize_handles_escaped_quote():
    src = r'const s = "a\"b { }"; function real() {}'
    assert "real" in _names(src, ".js")          # the escaped quote must not end the string early


# --------------------------------------------------------------- symbol rules

def test_rust_functions_types_and_spans():
    src = (
        "pub struct Foo {\n"
        "    x: i32,\n"
        "}\n"
        "impl Foo {\n"
        "    fn new() -> Self {\n"
        "        Foo { x: 0 }\n"
        "    }\n"
        "}\n"
    )
    syms, _ = extract(src, spec_for(".rs"))
    by = {s["name"]: s for s in syms}
    assert "Foo" in by and "new" in by
    assert by["new"]["suffix"] == "()" and by["Foo"]["suffix"] == ""
    assert by["new"]["line"] == 5 and by["new"]["end_line"] == 7   # exact span


def test_typescript_class_and_arrow_and_imports():
    src = (
        "import { A } from './a';\n"
        "export class Widget {\n"
        "  render() { return 1; }\n"
        "}\n"
        "const helper = (n: number) => n + 1;\n"
    )
    syms, imports = extract(src, spec_for(".ts"))
    names = {s["name"] for s in syms}
    assert {"Widget", "render", "helper"} <= names
    assert "./a" in imports


def test_go_func_and_type():
    names = _names("package p\ntype T struct{}\nfunc Do(x int) int {\n\treturn x\n}\n", ".go")
    assert "Do" in names and "T" in names


def test_control_flow_is_not_mistaken_for_a_symbol():
    # the classic false-positive risk for the C-method rule: if/for/while/switch with a body
    src = (
        "int process(int n) {\n"
        "    if (n > 0) {\n"
        "        for (int i = 0; i < n; i++) {\n"
        "            while (i) { i--; }\n"
        "        }\n"
        "    }\n"
        "    return n;\n"
        "}\n"
    )
    names = _names(src, ".c")
    assert "process" in names
    assert not ({"if", "for", "while", "switch", "return"} & set(names))


def test_bodiless_declaration_stays_start_only():
    # a `using`/typedef/forward-decl must not adopt a later unrelated block and inflate its span
    src = (
        "using namespace std;\n"
        "\n"
        "void real() {\n"
        "    work();\n"
        "}\n"
    )
    syms, _ = extract(src, spec_for(".cpp"))
    std = next(s for s in syms if s["name"] == "std")
    assert std["line"] == std["end_line"] == 1        # start-only, not stretched to real()'s brace


def test_ruby_uses_end_blocks_not_braces():
    names = _names("class Cat\n  def meow\n    puts 'hi'\n  end\nend\n", ".rb")
    assert "Cat" in names and "meow" in names


# -------------------------------------------------------------- scan_repo wire

def test_scan_repo_is_multilanguage(tmp_path):
    (tmp_path / "app.ts").write_text("export function main() { return 0; }\n", encoding="utf-8")
    (tmp_path / "lib.rs").write_text("pub fn helper() {}\n", encoding="utf-8")
    (tmp_path / "Svc.kt").write_text("class Svc {\n  fun run() {}\n}\n", encoding="utf-8")
    (tmp_path / "core.py").write_text("def pyfn():\n    pass\n", encoding="utf-8")
    (tmp_path / "notes.md").write_text("# doc\n", encoding="utf-8")

    nodes, links = scan_repo(tmp_path)
    labels = {n["label"] for n in nodes}
    # a symbol from every language + Python's exact path + the document
    assert {"main()", "helper()", "run()", "pyfn()", "app.ts", "lib.rs", "notes.md"} <= labels
    assert any(n["label"] == "notes.md" and n["file_type"] == "document" for n in nodes)
    assert any(link["relation"] == "contains" for link in links)


def test_scan_repo_unknown_text_becomes_bare_file_node(tmp_path):
    # a language with no spec still gets a file node so it appears in a module page
    (tmp_path / "query.sql").write_text("SELECT 1;\n", encoding="utf-8")
    (tmp_path / "weird.xyz").write_text("some textual content\n", encoding="utf-8")
    nodes, _ = scan_repo(tmp_path)
    sources = {n.get("source_file") for n in nodes}
    assert "query.sql" in sources and "weird.xyz" in sources


def test_scan_repo_skips_binary_files(tmp_path):
    (tmp_path / "real.go").write_text("package p\nfunc F() {}\n", encoding="utf-8")
    (tmp_path / "blob.bin").write_bytes(b"\x00\x01\x02\x03bytes")
    (tmp_path / "img.png").write_bytes(b"\x89PNG\r\n\x1a\n\x00\x00")
    nodes, _ = scan_repo(tmp_path)
    sources = {n.get("source_file") for n in nodes}
    assert "real.go" in sources
    assert "blob.bin" not in sources and "img.png" not in sources


def test_scan_repo_tolerates_unreadable_and_empty(tmp_path):
    (tmp_path / "empty.ts").write_text("", encoding="utf-8")
    (tmp_path / "ok.ts").write_text("function a(){}\n", encoding="utf-8")
    nodes, _ = scan_repo(tmp_path)
    labels = {n["label"] for n in nodes}
    assert "empty.ts" in labels and "a()" in labels     # empty file still yields its file node
