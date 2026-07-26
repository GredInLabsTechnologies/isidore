## Purpose

`src/isidore/handoff.py:1` exists to answer a question every other provider answers badly: whose
machine does your source code end up on. A hosted endpoint means someone else's, and a free hosted
endpoint usually means someone else's training set. This module removes the question instead of
managing it — the caller becomes the model, so the prompt never leaves the machine that already has
the code open.

The trade it makes explicit: prose written here gets **no more trust** for having been written
locally. It re-enters through the ordinary pipeline and faces the same claim parsing, the same
quarantine and the same certificate as any provider's reply.

## Architecture

Two halves that never run at once, joined by a directory.

**Emit** plans the compile with `execute=False` and writes what the run *would* have sent.
`_plan()` at `src/isidore/handoff.py:56` is that dry run; `emit()` at `src/isidore/handoff.py:72`
writes one prompt file per dirty page and a manifest. `handoff_dir()` at
`src/isidore/handoff.py:46` is the single place the location is decided, so the two halves cannot
disagree about where to look.

**Apply** replaces the network with the filesystem. `response_generator()` at
`src/isidore/handoff.py:92` returns a callable with the same shape the pipeline expects from any
provider, so nothing downstream needs to know the answers came from disk.

The pairing between the two is a **content hash of the prompt**, not a filename and not call order.
`prompt_id()` at `src/isidore/handoff.py:50` computes it. That choice is what makes a stale answer
detectable: if the repository moved between emit and apply, the prompt changes, its hash changes, and
the answer written against the old facts no longer matches anything.

## Key entry points

- `emit()` — `src/isidore/handoff.py:72`. Writes the prompts and the manifest. Also clears prompts
  and responses left by a previous run, so a page that is no longer dirty cannot leave an answerable
  prompt behind for the next apply to pick up.
- `response_generator()` — `src/isidore/handoff.py:92`. The generator handed to the pipeline. It
  raises rather than improvises: no manifest, an unknown prompt, a missing answer and an empty answer
  are four distinct refusals.
- `prompt_id()` — `src/isidore/handoff.py:50`. The pairing key.
- `handoff_dir()` — `src/isidore/handoff.py:46`. Where both halves meet.

## Dependencies

Three, all internal: `src/isidore/pipeline.py` for the compile itself, `src/isidore/graph.py` for
locating the structure graph, and `src/isidore/llm.py` for `GenerationError` — the module reports a
missing or mismatched answer with the same error type a failing provider would raise, so callers
handle one failure mode rather than two.

Nothing depends on this module, which is what a leaf that adds an entry point should look like.

## How to change safely

The load-bearing decision is the hash pairing at `src/isidore/handoff.py:50`. Anything that makes an
answer resolvable without matching the exact prompt it was written for — pairing by filename, by
position, by page name alone — reintroduces the failure this design exists to prevent: certifying
prose against facts that have since changed. Certificates would still be produced and would still
verify, because the pipeline has no way to know the answer describes an older repository.

The cleanup in `emit()` at `src/isidore/handoff.py:72` is the other one. It looks like housekeeping
and is not: a leftover prompt is an answerable prompt, and an answered leftover becomes a published
page nobody planned.

If you extend this to more page kinds, extend `_plan()` at `src/isidore/handoff.py:56` rather than
duplicating the compile call — the point of routing through the real planner is that emit and a
normal compile can never disagree about which pages are dirty.
