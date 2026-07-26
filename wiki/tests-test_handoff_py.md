## Purpose

`tests/test_handoff.py` guards the property that gives the handoff loop its reason to exist: the
source never leaves the machine. Its header states the measurement behind that — on 2026-07-26 a
`compile --execute` against a free tier that trains by default carried 87 prompts of private source
out of five repos (`tests/test_handoff.py:4`). The suite's other half guards the balancing constraint:
prose written locally gets no more trust for it, and passes through the same claim anchoring, lint
gate and quarantine as any provider's reply (`tests/test_handoff.py:7`).

## Architecture

The fixture is the assertion. `repo` deletes `ISIDORE_MODEL` and `ISIDORE_API_KEY` before handing back
a repository (`tests/test_handoff.py:65`), and its docstring says why that is not housekeeping: the
loop must work with nothing configured, so every test in the file runs with no provider reachable
(`tests/test_handoff.py:64`). A test that needed a key would fail rather than quietly reach out.

`_make_repo` builds three modules of twelve symbols each — enough per module to clear `min_symbols`,
so each earns its own page and the suite can tell per-page behaviour from whole-run behaviour
(`tests/test_handoff.py:43`). It writes a graph beside the sources rather than scanning, pinning the
input to a literal `graphify-out/graph.json` (`tests/test_handoff.py:57`), which keeps the tests
independent of the scanner.

`_answer_all` plays the model: for each emitted prompt it writes a response next to it and returns the
page names it answered (`tests/test_handoff.py:71`). It pairs by stripping the prompt suffix from the
filename (`tests/test_handoff.py:75`) — deliberately the naive scheme, so that the tests exercising
the real pairing (by prompt hash) are testing the module rather than the helper.

`_Args` stands in for what the CLI hands the functions, duck-typed because the module reads its
arguments with `getattr` (`tests/test_handoff.py:34`).

## Key entry points

- `repo` — the no-provider fixture every test builds on (`tests/test_handoff.py:63`).
- `_make_repo(tmp_path, n_modules)` — three page-worthy modules plus a graph
  (`tests/test_handoff.py:42`).
- `_answer_all(repo, body)` — writes the answers a round is waiting for
  (`tests/test_handoff.py:70`).
- `test_emit_writes_one_prompt_per_dirty_page_and_calls_nothing` — the base case: three prompts, and
  emit as a plan rather than a write (`tests/test_handoff.py:83`).

## Dependencies

The suite imports the module's surface directly — `emit`, `apply`, `response_generator`,
`handoff_dir`, `prompt_id` — together with the constants a caller has to know: `MANIFEST`,
`PROMPT_SUFFIX`, `RESPONSE_SUFFIX` and `REPAIR_MARKER` (`tests/test_handoff.py:17`). Importing
`REPAIR_MARKER` rather than retyping the gate's wording keeps the tests honest if that wording moves.
`GenerationError` comes from `isidore.llm` and is the single failure type the loop speaks
(`tests/test_handoff.py:28`). `PAGE` is the stand-in answer shared across tests
(`tests/test_handoff.py:30`).

## How to change safely

Keep the fixture hostile. Deleting the provider variables is what makes a network call fail instead of
succeeding silently, so a test that sets them back is not a stronger test but a blind one
(`tests/test_handoff.py:65`). Keep `_answer_all` naive: the moment the helper starts pairing by prompt
hash, the tests stop proving that the module does. And when adding a module to `_make_repo`, keep each
one above the symbol threshold the docstring names, or pages silently stop being planned and the
counts in the assertions drift for a reason unrelated to the behaviour under test
(`tests/test_handoff.py:43`).
