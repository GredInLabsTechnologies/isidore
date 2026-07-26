## Purpose

`src/isidore/pipeline.py` is the compiler: plan a set of pages, assemble each one's facts, delegate
exactly one bounded call for the prose, cache, and lint what comes back
(`src/isidore/pipeline.py:1`). Its governing idea is that the graph already answers WHAT exists and
WHERE, so planning, context assembly, cache invalidation and citation linting are plain deterministic
code and only the prose is delegated (`src/isidore/pipeline.py:3`).

The second idea is where its hard limits live: in code, not in prompts — a per-run call cap whose
skips are always reported, a per-prompt character budget whose truncation is always reported, one
model, one timeout (`src/isidore/pipeline.py:7`). A limit written into a prompt is a request; a limit
written here is a fact about the run.

## Architecture

Everything downstream depends on this module — the CLI, `handoff`, `qa`, `whatsnew`, `impact` and
`export` all route through it — while it depends on the graph, the claim machinery and the
verifiers. That shape is why a rule enforced here is enforced everywhere, and why one that is missing
here is missing everywhere.

The newest part is the disclosure gate. Compiling puts real source excerpts into a prompt, so it is a
disclosure, and the module now asks where that disclosure is going before making it.
`source_destination` reads the answer out of the environment, because the environment is where a
destination actually lives (`src/isidore/pipeline.py:157`). It recognises the caller's own Claude
session (`src/isidore/pipeline.py:166`), a model on this machine (`src/isidore/pipeline.py:173`), an
endpoint held under an agreement the operator already has (`src/isidore/pipeline.py:175`), and a host
the operator has explicitly declared fit (`src/isidore/pipeline.py:177`). Anything else comes back
undeclared (`src/isidore/pipeline.py:179`).

`assert_may_send_source` turns that classification into a decision (`src/isidore/pipeline.py:182`).
An undeclared destination raises rather than sends (`src/isidore/pipeline.py:196`), and a declared
third party is allowed but returns a line to record (`src/isidore/pipeline.py:206`) — consent is not
the end of it, because a disclosure nobody can see afterwards is one nobody can audit. The trust
variable is named once (`src/isidore/pipeline.py:144`) and the endpoint lists are deliberately short:
`LOCAL_HOSTS` covers the ways of addressing this machine (`src/isidore/pipeline.py:145`) and
`TRUSTED_HOSTS` is a statement about terms rather than about quality
(`src/isidore/pipeline.py:148`).

The other loud failure in the module guards the output rather than the input.
`degenerate_certificate` refuses to write a certificate whose violation or mark counts have run away
(`src/isidore/pipeline.py:256`), against caps that sit in code beside it
(`src/isidore/pipeline.py:252`).

## Key entry points

- `source_destination()` — classify where a compile would send the source
  (`src/isidore/pipeline.py:157`).
- `assert_may_send_source(what)` — fail closed, or return the disclosure to record
  (`src/isidore/pipeline.py:182`).
- `PageSpec` — what one page is planned from (`src/isidore/pipeline.py:212`).
- `module_dep_edges(nodes, links)` — the module-level dependency edges pages are ordered by
  (`src/isidore/pipeline.py:232`).
- `degenerate_certificate(cert)` — the reason a certificate must not be written, if there is one
  (`src/isidore/pipeline.py:256`).

## Dependencies

Facts come from `src/isidore/graph.py`; claims and findings from `src/isidore/claims.py` and
`src/isidore/findings.py`; verification and certificates from `src/isidore/verify.py` and
`src/isidore/pcp.py`; incremental scoping from `src/isidore/changeset.py`; telemetry from
`src/isidore/journal.py`. The single delegated call goes through `src/isidore/llm.py`, which is also
where `GenerationError` — the one failure type the compile speaks — comes from.

## How to change safely

Anything that reaches a provider belongs behind `assert_may_send_source`, called before the request
is built rather than after. Keep the environment as the source of truth for the destination: reading
it anywhere else creates a second answer to the same question. And keep the refusal informative — it
names the host and every way out, because a gate that only says no teaches people to disable it.
