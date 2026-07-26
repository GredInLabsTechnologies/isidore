## Purpose

`src/isidore/handoff.py` answers one question the rest of the compiler cannot: *whose machine does
your source code end up on?* Every hosted provider is an answer you may not like, and a free hosted
provider is usually the worst one — the module's own header records the measurement that motivated it,
87 prompts of private source sent to a free tier that trains by default (`src/isidore/handoff.py:5`).

The module removes the question instead of managing it. `emit` writes the exact prompts to disk and
calls nothing; whoever is already reading the repository writes the answers next to them; `apply`
feeds those answers back through the ordinary pipeline (`src/isidore/handoff.py:7`). The prose earns
no privilege for having been written locally: it goes through the same claim parsing, quarantine,
certificate and verification as any provider's reply (`src/isidore/handoff.py:9`).

## Architecture

Three small pieces sit between the caller and `compile_wiki`.

`_plan` is the dry run. It calls `compile_wiki` with `execute=False`, so working out which pages are
dirty and what each would ask never reaches a model (`src/isidore/handoff.py:66`). It also passes
`max_calls=0` deliberately: a call cap exists to bound spend, and there is no spend here, so the cap
belongs to whoever answers rather than to the planner (`src/isidore/handoff.py:70`).

`emit` turns that plan into files. Before writing a round it deletes the previous prompts *and*
responses, so a page that is no longer dirty cannot leave an answerable prompt behind for the next
`apply` to certify (`src/isidore/handoff.py:86`). Each prompt is written out and recorded in a
manifest keyed by `prompt_id` — the pairing is by content, never by filename order
(`src/isidore/handoff.py:92`).

`response_generator` is the seam that makes the whole thing safe. It reads the manifest, failing
closed with an instruction to run `emit` first if it cannot (`src/isidore/handoff.py:104`), and
returns a function shaped exactly like a provider call. Its `_lookup` tries the exact prompt hash
first (`src/isidore/handoff.py:120`). The fallback exists because the lint gate appends a correction
addendum to the original prompt and asks again — a round nobody can answer here, since the answer was
written before `apply` ran. Serving the same answer lets the gate re-lint it and quarantine the page
with its bad citation annotated, instead of aborting and taking every other page down
(`src/isidore/handoff.py:111`). The tail is required to be that addendum and nothing else: a bare
prefix match would silently certify a stale answer whenever new facts were appended to a page's
context (`src/isidore/handoff.py:116`).

## Key entry points

- `handoff_dir(repo)` — where a round lives, under the wiki directory (`src/isidore/handoff.py:51`).
- `prompt_id(prompt)` — the pairing key, a truncated SHA-256 of the prompt text
  (`src/isidore/handoff.py:58`).
- `emit(repo, config, args)` — one prompt file per dirty page, plus the manifest
  (`src/isidore/handoff.py:77`).
- `response_generator(repo)` — a generator that answers from disk (`src/isidore/handoff.py:97`).

## Dependencies

`src/isidore/pipeline.py` supplies `compile_wiki`, the defaults, `WIKI_DIRNAME` and the lint gate's
addendum (`src/isidore/handoff.py:28`). `REPAIR_MARKER` is derived from that addendum rather than
retyped, so a change to the gate's wording moves the marker with it instead of quietly ceasing to
match (`src/isidore/handoff.py:48`). `src/isidore/graph.py` resolves the structure graph and
`src/isidore/llm.py` supplies `GenerationError`, the one failure type the loop speaks
(`src/isidore/handoff.py:26`).

## How to change safely

Treat `prompt_id` as a wire format: it is what a written answer is bound to, so changing how it is
computed invalidates every unanswered round on disk (`src/isidore/handoff.py:58`). Keep refusals
loud — the module's stance is that refusing beats certifying prose written against a repository that
has moved. And keep `_lookup`'s tail check exact; loosening it is the difference between tolerating a
repair round and accepting a stale answer.
