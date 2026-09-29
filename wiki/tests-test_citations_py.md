## Purpose

`tests/test_citations.py` tests the pure parts of `src/isidore/citations.py` over a real file on disk: what counts as the same cited line, what is never touched, and every way the legacy migration must refuse to move a citation (`tests/test_citations.py:1-L6`). The end-to-end behaviour — a compile re-pointing citations, certificates following, revisions seeing corrected pages — is tested elsewhere (`tests/test_citations.py:3-L4`). The negative migration cases matter most: each is a real miss of the migration's first version on isidore's own wiki, where 9 of 14 proposed moves would have broken a correct citation (`tests/test_citations.py:5-L6`).

## Architecture

Every test works on one small module, `SRC` (`tests/test_citations.py:16`): an import, a `helper` function that reads the working directory, and an `other` function that calls it. The `repo()` fixture writes it to a temporary directory (`tests/test_citations.py:30-L32`), and `_shift()` rewrites it with `n` padding lines on top (`tests/test_citations.py:35-L36`) — the simplest edit that moves every line without changing any of them.

The tests fall into two groups:

- **Re-pointing.** A citation and a range follow their lines, the range keeping its length (`tests/test_citations.py:39-L45`); when the same code appears twice, the citation resolves to the copy it was written for, not the first one (`tests/test_citations.py:48-L55`); a cited line whose content changed is left as written and reported stale (`tests/test_citations.py:58-L63`). A path inside a code fence and a missing file are never anchored or rewritten, while a citation of a blank line is recorded — as unanchored, with an empty fingerprint — so that it is remembered without ever being followed (`tests/test_citations.py:66-L73`).
- **Migration.** A citation that names its symbol and no longer lands on it is moved to the symbol's definition (`tests/test_citations.py:79-L82`); the remaining cases check that it refuses whenever the move cannot be validated.

## Key entry points

- `repo()` — the fixture that writes `SRC` to disk (`tests/test_citations.py:30`).
- `_shift()` — moves every line down by `n` (`tests/test_citations.py:35`).
- `test_a_citation_and_its_range_follow_their_lines` — the basic re-pointing contract (`tests/test_citations.py:39`).
- `test_the_same_code_twice_resolves_to_the_nearest_copy` — a fingerprint is resolved nearest-first (`tests/test_citations.py:48`).
- `test_changed_content_is_reported_and_left_as_written` — changed content is never guessed (`tests/test_citations.py:58`).
- `test_migration_moves_a_citation_that_names_its_symbol_and_missed_it` — the positive migration case (`tests/test_citations.py:79`).

## Dependencies

The module depends on `src/isidore/citations.py` alone, importing `anchors_for`, `migrate_by_symbol` and `repoint` (`tests/test_citations.py:14`).

## How to change safely

1. Keep the negative migration cases. Each one pins a move that looked right and would have broken a correct citation; removing one reopens exactly that miss.
2. Keep `SRC` small and its line numbers meaningful: the expected values in the assertions are literal line numbers.
3. Change the source through `_shift()` or an explicit rewrite, never by hand-editing expected numbers to match new behaviour.
