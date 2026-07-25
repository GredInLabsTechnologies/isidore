"""API surface extraction: qualified names, signatures as change keys, and the folding of
multi-line declaration headers. Pure text in, symbols out — no git, no disk, no LLM."""
from __future__ import annotations

from isidore.surface import (
    KIND_CLASS,
    KIND_CONSTANT,
    KIND_FUNCTION,
    KIND_METHOD,
    MAX_SIG_CHARS,
    clean_sig,
    extract_surface,
    logical_lines,
    python_surface,
)


def _by_name(symbols):
    return {s.qualname: s for s in symbols}


# ------------------------------------------------------------------ Python (exact)

PY_SOURCE = '''\
DEFAULT_TOP_K = 24
_PRIVATE_CONST = 3


def top_level(a, b=2):
    return a + b


async def fetch(url: str, *, timeout: float = 1.0) -> bytes:
    return b""


def _helper():
    pass


class Client:
    """Doc."""

    def __init__(self, host):
        self.host = host

    async def put_many_conditional(self, conditions, records, verify=False):
        return None

    def _internal(self):
        pass

    class Nested:
        def inner(self):
            pass


class _Hidden:
    def method(self):
        pass
'''


def test_python_surface_covers_functions_methods_nested_and_constants():
    found = _by_name(python_surface(PY_SOURCE))

    assert found["top_level"].kind == KIND_FUNCTION
    assert found["fetch"].kind == KIND_FUNCTION
    assert found["Client"].kind == KIND_CLASS
    # A method of an existing class is the case graph.py's top-level-only scanner cannot see.
    assert found["Client.put_many_conditional"].kind == KIND_METHOD
    assert found["Client.__init__"].kind == KIND_METHOD
    # One level of nesting is still surface.
    assert found["Client.Nested"].kind == KIND_CLASS
    assert found["Client.Nested.inner"].kind == KIND_METHOD
    assert found["DEFAULT_TOP_K"].kind == KIND_CONSTANT


def test_python_surface_marks_visibility_including_inheritance_from_the_container():
    found = _by_name(python_surface(PY_SOURCE))

    assert found["top_level"].public is True
    assert found["_helper"].public is False
    assert found["_PRIVATE_CONST"].public is False
    assert found["Client._internal"].public is False
    # Dunders are how callers use the type -> surface.
    assert found["Client.__init__"].public is True
    # A public-looking method of a private class is not public surface.
    assert found["_Hidden.method"].public is False


def test_python_signature_is_exact_and_survives_reformatting():
    found = _by_name(python_surface(PY_SOURCE))
    # Verbatim, commas included: this exact string is what a person reads in the changelog.
    assert found["fetch"].sig == "(url: str, *, timeout: float=1.0) -> bytes"

    reflowed = python_surface(
        "async def fetch(\n    url: str,\n    *,\n    timeout: float = 1.0,\n) -> bytes:\n    return b''\n"
    )
    # Same signature written across lines must NOT read as an API change.
    assert _by_name(reflowed)["fetch"].sig == found["fetch"].sig


def test_python_signature_moves_when_a_default_or_parameter_changes():
    base = _by_name(python_surface("def f(a, b=2):\n    pass\n"))["f"].sig
    assert _by_name(python_surface("def f(a, b=3):\n    pass\n"))["f"].sig != base
    assert _by_name(python_surface("def f(a, b=2, c=None):\n    pass\n"))["f"].sig != base
    # Reindenting is not a change.
    assert _by_name(python_surface("def f(a,   b = 2):\n        pass\n"))["f"].sig == base


def test_python_constant_value_change_is_visible():
    before = _by_name(python_surface("VERSION = '1.5.1'\n"))["VERSION"]
    after = _by_name(python_surface("VERSION = '1.5.2'\n"))["VERSION"]
    assert before.sig != after.sig
    assert "1.5.2" in after.sig


def test_python_surface_returns_none_on_syntax_error():
    # None means "not comparable"; an empty list would read as "everything was deleted".
    assert python_surface("def broken(:\n") is None


def test_python_line_spans_point_at_the_declaration():
    found = _by_name(python_surface(PY_SOURCE))
    line = found["Client.put_many_conditional"].line
    assert PY_SOURCE.splitlines()[line - 1].strip().startswith("async def put_many_conditional")


# ------------------------------------------------------------------ generic (langspec-backed)

TS_SOURCE = """\
import { Foo } from './foo';

export const GICS_VERSION = '1.5.2';

export class NodeClient {
    private token: string;

    async putManyConditional(
        conditions: Condition[],
        records: Record[],
        options: BatchOptions = {},
    ): Promise<BatchResult> {
        return this.rpc('putManyConditional', { conditions, records });
    }

    private async resolveEntry(key: string): Promise<Entry | null> {
        return null;
    }

    get ready(): boolean {
        return true;
    }
}

export class OtherClient {
    async putManyConditional(a: string): Promise<void> {}
}

export function standalone(x: number): number {
    return x;
}
"""


def test_generic_surface_folds_a_multiline_signature_and_qualifies_the_method():
    found = _by_name(extract_surface(TS_SOURCE, ".ts"))

    symbol = found["NodeClient.putManyConditional"]
    assert symbol.kind == KIND_METHOD
    # The declaration starts where the name is, not where the body brace lands three lines later.
    assert TS_SOURCE.splitlines()[symbol.line - 1].strip() == "async putManyConditional("
    # A parameter default containing braces must not defeat the header matcher.
    assert "BatchOptions = {}" in symbol.sig
    assert "Promise<BatchResult>" in symbol.sig


def test_generic_surface_disambiguates_same_named_methods_of_different_classes():
    found = _by_name(extract_surface(TS_SOURCE, ".ts"))
    assert "NodeClient.putManyConditional" in found
    assert "OtherClient.putManyConditional" in found
    assert found["NodeClient.putManyConditional"].sig != found["OtherClient.putManyConditional"].sig


def test_generic_surface_reads_types_constants_and_visibility():
    found = _by_name(extract_surface(TS_SOURCE, ".ts"))
    assert found["NodeClient"].kind == KIND_CLASS
    assert found["GICS_VERSION"].kind == KIND_CONSTANT
    assert "1.5.2" in found["GICS_VERSION"].sig
    assert found["standalone"].kind == KIND_FUNCTION
    assert found["NodeClient.resolveEntry"].public is False
    assert found["NodeClient.putManyConditional"].public is True


def test_generic_surface_does_not_capture_control_flow_or_locals():
    source = """\
export function run(items: string[]): void {
    const local = 5;
    if (items.length > 0) {
        for (const item of items) {
            while (item) {}
        }
    }
}
"""
    names = set(_by_name(extract_surface(source, ".ts")))
    assert names == {"run"}


def test_logical_lines_abandons_a_run_that_never_balances():
    # A test-suite block never closes its parens on the header line. Folding it would hide every
    # symbol declared inside, so the fold must give up and leave the lines alone.
    source = """\
describe('suite', () => {
    it('a', () => {});
    it('b', () => {});
    it('c', () => {});
    it('d', () => {});
    it('e', () => {});
    it('f', () => {});
    function helperInside(x: number): number { return x; }
});
"""
    folded = logical_lines(source)
    assert folded[0] == (1, 1, "describe('suite', () => {")
    assert any("helperInside" in text for _s, _e, text in folded)
    assert "helperInside" in _by_name(extract_surface(source, ".ts"))


def test_extract_surface_returns_none_for_non_code():
    assert extract_surface("# Title\n\nSome prose.\n", ".md") is None
    assert extract_surface("binary-ish", ".unknownext") is None


def test_signature_is_kept_verbatim_for_human_eyes_and_still_encodes_as_toon():
    from isidore.toon import encode

    sig = clean_sig("(a: string, b: number | null)")
    # A signature is read by PEOPLE. Pre-mangling commas into `;` "for TOON safety" corrupted exactly
    # the surface a reader looks at, and TOON never needed it: encode() quotes such a field itself.
    assert sig == "(a: string, b: number | null)"
    assert '"(a: string, b: number | null)"' in encode(("t", ["sig"], [{"sig": sig}]))


def test_clean_sig_normalises_whitespace_and_caps_length():
    assert clean_sig("def  f(a,\n   b) {") == "def f(a, b)"
    assert len(clean_sig("x" * (MAX_SIG_CHARS * 2))) <= MAX_SIG_CHARS
