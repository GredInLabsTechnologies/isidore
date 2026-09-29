## Purpose

`src/isidore/toon.py` serialises uniform lists as TOON (Token-Oriented Object Notation), the tabular format Isidore writes for agents to read: its index, claims and findings. A table is one declaration row `name[N]{fields}:` followed by N comma-separated rows, which costs roughly 40% fewer tokens than the equivalent JSON when a model reads uniform lists, with equal or better accuracy (`src/isidore/toon.py:1-L5`). Output is a subset compatible with the TOON 1.0 spec (`src/isidore/toon.py:5`). Because agents re-read these files every turn, the saving compounds.

## Architecture

The module is deliberately small and dependency-free (`src/isidore/toon.py:16`):

- `_field` renders one value (`src/isidore/toon.py:21-L48`): `None` and `""` become an empty field, booleans become `1` or empty (`src/isidore/toon.py:22-L25`), and a value is quoted only when it contains a comma, a quote, a newline or a carriage return, or starts or ends with a space (`src/isidore/toon.py:29-L32`). Inside quotes, backslashes, quotes, newlines and carriage returns are escaped (`src/isidore/toon.py:36-L46`), so a row can never be split or broken by the data in it.
- `_row_values` accepts a row as a mapping (values picked by field name) or as a list/tuple (taken in order), and refuses anything else with a `TypeError` (`src/isidore/toon.py:51-L56`).
- `encode_table` writes the header with the row count and field list, then each row indented two spaces (`src/isidore/toon.py:59-L74`).
- `encode` joins several tables into one document, newline-separated (`src/isidore/toon.py:77-L79`).

## Key entry points

- `encode_table(name, fields, rows)` — one table (`src/isidore/toon.py:59`).
- `encode(*tables)` — several `(name, fields, rows)` tables in one document (`src/isidore/toon.py:77`).

These are the module's whole public surface (`src/isidore/toon.py:18`).

## Dependencies

It imports nothing from the rest of Isidore. It is used across the codebase — `src/isidore/claims.py`, `src/isidore/connect.py`, `src/isidore/contracts.py`, `src/isidore/findings.py`, `src/isidore/impact.py` and `src/isidore/journal.py` — and tested by `tests/test_units.py` and `tests/test_surface.py`.

## How to change safely

1. Keep quoting minimal and exact: a field is quoted only when it must be, and every character that could split a row is escaped. Loosening this lets data corrupt a table; tightening it spends the tokens the format exists to save.
2. Keep the header's row count equal to the rows written — a reader trusts `N` to know where the table ends.
3. Keep the output within the TOON 1.0 subset, since other tools read these files.
4. The module has many consumers; a change to its output changes every TOON file Isidore writes.
