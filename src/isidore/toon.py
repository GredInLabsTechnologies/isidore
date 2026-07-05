"""TOON (Token-Oriented Object Notation) serializer — tabular subset.

One declaration row `name[N]{fields}:` + N CSV-like rows. Roughly 40% fewer tokens than the
equivalent JSON when an LLM reads uniform lists, with equal or better accuracy. Output is a
subset compatible with the TOON 1.0 spec.

Rules:
  - Header: `name[N]{field1,field2,...}:`
  - Rows indented 2 spaces, comma-separated.
  - Booleans: `1` for True, empty for False.
  - None / "" -> empty field.
  - Quotes only when a field contains `,`, `"`, a newline, or leading/trailing spaces.
"""
from __future__ import annotations

from typing import Any, Iterable, Mapping, Sequence

__all__ = ["encode_table", "encode"]


def _field(raw: Any) -> str:
    if raw is None:
        return ""
    if isinstance(raw, bool):
        return "1" if raw else ""
    s = raw if isinstance(raw, str) else str(raw)
    if s == "":
        return ""
    needs_quote = (
        "," in s or '"' in s or "\n" in s or "\r" in s
        or s[:1] == " " or s[-1:] == " "
    )
    if not needs_quote:
        return s
    out = ['"']
    for c in s:
        if c == "\\":
            out.append("\\\\")
        elif c == '"':
            out.append('\\"')
        elif c == "\n":
            out.append("\\n")
        elif c == "\r":
            out.append("\\r")
        else:
            out.append(c)
    out.append('"')
    return "".join(out)


def _row_values(row: Any, fields: Sequence[str]) -> list[Any]:
    if isinstance(row, Mapping):
        return [row.get(f) for f in fields]
    if isinstance(row, (list, tuple)):
        return list(row)
    raise TypeError(f"unsupported row type: {type(row).__name__}")


def encode_table(name: str, fields: Sequence[str], rows: Iterable[Any]) -> str:
    """Serialize one table.

    >>> print(encode_table("pages", ["file", "module"], [
    ...     {"file": "core.md", "module": "src/core"},
    ... ]))
    pages[1]{file,module}:
      core.md,src/core
    """
    rows = list(rows)
    head = f"{name}[{len(rows)}]{{{','.join(fields)}}}:"
    lines = [head]
    for row in rows:
        vals = _row_values(row, fields)
        lines.append("  " + ",".join(_field(v) for v in vals))
    return "\n".join(lines)


def encode(*tables: tuple[str, Sequence[str], Iterable[Any]]) -> str:
    """Serialize several tables into one TOON document (newline-separated)."""
    return "\n".join(encode_table(n, f, r) for (n, f, r) in tables)
