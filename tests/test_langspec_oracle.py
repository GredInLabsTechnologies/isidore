"""`signature` and `value` decided outside Python, and — just as important — the cases where they
refuse to decide. A heuristic scanner may fail to confirm a claim; it may never invent a refutation.
"""
from __future__ import annotations

from pathlib import Path

from isidore.pcp import FALSE, ORACLE_AST, ORACLE_LANGSPEC, TRUE, UNDECIDABLE, Predicate, VerifyContext
from isidore.surface import literal_value, parameter_names
from isidore.verify import v_signature, v_value

TS = """\
export const GICS_VERSION = '1.5.2';
export const LIMIT = 5;
export const REGISTRY = new Set(['a', 'b']);

export class NodeClient {
    async putManyConditional(
        conditions: Condition[],
        records: Record[],
        options: Options = {},
    ): Promise<Result> {
        return null;
    }
}
"""

JAVA = """\
public class Client {
    public void save(String key, int count) {
    }
}
"""


def _ctx(tmp_path, name: str, text: str) -> VerifyContext:
    (tmp_path / name).write_text(text, encoding="utf-8")
    nodes = [{"id": name, "source_file": name, "file_type": "code", "label": name,
              "source_location": "L1"}]
    return VerifyContext(repo=tmp_path, nodes=nodes, links=[])


# ------------------------------------------------------------------ reading parameters

def test_parameter_names_are_read_where_the_name_comes_first():
    sig = "async putManyConditional( conditions: Condition[], records: Record[], options: Opts = {}, ): Promise<R>"
    assert parameter_names(sig, "TypeScript") == ["conditions", "records", "options"]
    assert parameter_names("fn f(ctx context.Context, n int)", "Go") == ["ctx", "n"]
    assert parameter_names("fn new(&self, size: usize)", "Rust") == ["self", "size"]
    assert parameter_names("function noArgs()", "TypeScript") == []


def test_a_language_whose_parameter_order_is_not_modelled_refuses_to_answer():
    # `String key` puts the type first: reading "the first word" would report the TYPE as the name.
    assert parameter_names("public void save(String key, int count)", "Java") is None
    assert parameter_names("void save(char *key)", "C") is None


def test_a_truncated_declaration_refuses_to_answer():
    # An unbalanced group means the extractor hit its own cap; comparing it would manufacture a
    # disagreement out of a limit rather than out of the code.
    assert parameter_names("fn f(a, b", "Rust") is None
    assert parameter_names("fn f(a, b, c…", "Rust") is None


def test_a_parameter_that_is_not_a_plain_name_refuses_to_answer():
    assert parameter_names("function C({ a, b }: Props)", "TypeScript") is None


def test_literal_value_reads_only_comparable_literals():
    assert literal_value("export const V = '1.5.2';") == "1.5.2"
    assert literal_value("const LIMIT = 5;") == "5"
    assert literal_value("const OK = true") == "true"
    # Built by a call: not comparable, exactly as the Python oracle already refuses to compare.
    assert literal_value("const R = new Set(['a'])") is None
    assert literal_value("class C") is None


# ------------------------------------------------------------------ the verifiers

def test_value_now_decides_for_a_typescript_constant(tmp_path):
    ctx = _ctx(tmp_path, "version.ts", TS)
    verdict = v_value(Predicate("value", ("GICS_VERSION", "1.5.2")), ctx)
    assert (verdict.value, verdict.oracle) == (TRUE, ORACLE_LANGSPEC)

    wrong = v_value(Predicate("value", ("GICS_VERSION", "9.9.9")), ctx)
    assert wrong.value == FALSE


def test_value_stays_undecidable_when_the_binding_is_not_a_literal(tmp_path):
    ctx = _ctx(tmp_path, "version.ts", TS)
    assert v_value(Predicate("value", ("REGISTRY", "a")), ctx).value == UNDECIDABLE


def test_signature_now_decides_for_a_typescript_method(tmp_path):
    ctx = _ctx(tmp_path, "node.ts", TS)
    ok = v_signature(
        Predicate("signature", ("putManyConditional", "conditions", "records", "options")), ctx)
    assert (ok.value, ok.oracle) == (TRUE, ORACLE_LANGSPEC)

    wrong = v_signature(Predicate("signature", ("putManyConditional", "conditions")), ctx)
    assert wrong.value == FALSE


def test_signature_refuses_rather_than_refutes_in_an_unmodelled_language(tmp_path):
    ctx = _ctx(tmp_path, "Client.java", JAVA)
    verdict = v_signature(Predicate("signature", ("save", "key", "count")), ctx)
    # The claim is TRUE in fact. The scanner cannot read Java parameter order, and saying FALSE here
    # would refute a true claim on the strength of its own blind spot.
    assert verdict.value == UNDECIDABLE
    assert "this oracle can read" in verdict.detail


def test_python_keeps_deciding_through_the_exact_parser(tmp_path):
    (tmp_path / "m.py").write_text("def handler(request, timeout=1):\n    pass\n", encoding="utf-8")
    ctx = VerifyContext(repo=tmp_path, links=[], nodes=[
        {"id": "h", "source_file": "m.py", "file_type": "code", "label": "handler()",
         "source_location": "L1"}])
    verdict = v_signature(Predicate("signature", ("handler", "request", "timeout")), ctx)
    # The fallback must not shadow the exact oracle: Python still answers, and says so.
    assert (verdict.value, verdict.oracle) == (TRUE, ORACLE_AST)


def test_an_ambiguous_name_is_not_refuted_against_whichever_match_came_first(tmp_path):
    # Measured on GICS: `signature:constructor;options` was refuted against a DIFFERENT class's
    # constructor, because a name is not unique across a repository and `constructor` least of all.
    two = """\
export class A {
    constructor(socketPath: string, token: string) {}
}
export class B {
    constructor(options: Options = {}) {}
}
"""
    ctx = _ctx(tmp_path, "two.ts", two)
    ok = v_signature(Predicate("signature", ("constructor", "options")), ctx)
    assert ok.value == TRUE                       # one of them does satisfy the claim

    neither = v_signature(Predicate("signature", ("constructor", "nope")), ctx)
    assert neither.value == UNDECIDABLE           # ...and with two candidates, no refutation
    assert "cannot tell which" in neither.detail


def test_a_unique_declaration_can_still_be_refuted(tmp_path):
    single = "export class A {\n    save(key: string) {}\n}\n"
    ctx = _ctx(tmp_path, "one.ts", single)
    assert v_signature(Predicate("signature", ("save", "wrong")), ctx).value == FALSE


def test_quoting_is_normalised_on_both_sides_of_a_literal(tmp_path):
    # Measured on GICS: the value IS '_insight/' and the claim said "'_insight/'". Refuting over the
    # quotes is a formatting complaint, not a verdict — and Python's oracle compares unquoted.
    ctx = _ctx(tmp_path, "p.ts", "const PREFIX = '_insight/';\n")
    assert v_value(Predicate("value", ("PREFIX", "'_insight/'")), ctx).value == TRUE
    assert v_value(Predicate("value", ("PREFIX", "_insight/")), ctx).value == TRUE
    assert v_value(Predicate("value", ("PREFIX", "other")), ctx).value == FALSE


def test_an_unknown_symbol_is_undecidable_not_false(tmp_path):
    ctx = _ctx(tmp_path, "node.ts", TS)
    assert v_signature(Predicate("signature", ("nowhere", "a")), ctx).value == UNDECIDABLE
    assert v_value(Predicate("value", ("NOWHERE", "1")), ctx).value == UNDECIDABLE


def test_the_oracle_never_walks_files_the_graph_does_not_know(tmp_path):
    # A file on disk but absent from the graph is outside the universe the wiki was built from.
    (tmp_path / "stray.ts").write_text("export const HIDDEN = 'x';", encoding="utf-8")
    ctx = VerifyContext(repo=Path(tmp_path), nodes=[], links=[])
    assert v_value(Predicate("value", ("HIDDEN", "x")), ctx).value == UNDECIDABLE
