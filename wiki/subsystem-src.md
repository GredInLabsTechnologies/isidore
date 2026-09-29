## What this area is responsible for
`src` is the whole of Isidore's machinery: it turns a repository into an agent-oriented wiki whose statements are checked against the code, and keeps that wiki honest — and cheap to keep — as the code changes. It builds the structure graph, compiles and revises pages from it, verifies what the pages claim, and tells a reader which claims and citations have gone stale.

## How the work is divided
- **Seeing the code.** `src-isidore-graph_py.md` and `src-isidore-langspec_py.md` build and load the structure graph in any language; `src-isidore-changeset_py.md` maps a git diff onto that graph, so a change is known symbol by symbol, and `src-isidore-impact_py.md` reports what a change would touch.
- **Writing pages.** `src-isidore-pipeline_py.md` is the compiler; `src-isidore-revise_py.md` makes it incremental, rewriting only the sections a change affected; `src-isidore-handoff_py.md` lets the caller act as the model so the source never leaves the machine, and `src-isidore-llm_py.md` is the one provider client; `src-isidore-pyramid_py.md` composes module pages into area and product pages, gated for plain language by `src-isidore-plain_py.md`.
- **Proving pages.** `src-isidore-claims_py.md` anchors each claim to the content of the line it cites, `src-isidore-citations_py.md` does the same for the citations in the prose, `src-isidore-pcp_py.md` and `src-isidore-verify_py.md` decide typed claims against the code, and `src-isidore-recertify_py.md` repairs certificates the code has outgrown without a model call.
- **Everything around it.** The CLI (`src-isidore-cli_py.md`), residue, security findings and telemetry (`src-isidore-findings_py.md`, `src-isidore-detectors_py.md`, `src-isidore-journal_py.md`), the external knowledge home (`src-isidore-connectors.md`, `src-isidore-connect_py.md`, `src-isidore-knowledge_py.md`, `src-isidore-home_py.md`), and the free outputs (`src-isidore-render_py.md`, `src-isidore-toon_py.md`, `src-isidore-qa_py.md`, `src-isidore-whatsnew_py.md`, `src-isidore-export_py.md`, `src-isidore-humanpack_py.md`).

The split follows the rule the system rests on: generating prose and trusting prose are different jobs, done by different modules, so nothing a model writes is believed until the proving side has checked it.

## What it depends on, and what depends on it
The area needs git and the repository's own files; claims are parsed from the pages it writes and anchored back to the source lines they cite, and prose citations are anchored the same way. What it promises the rest is a wiki in which every certified statement can be re-verified offline, with no model call.

## Where to start reading
- `src-isidore-pipeline_py.md` — how a page is planned, compiled and written.
- `src-isidore-claims_py.md` — why a claim stays true or goes stale.
- `src-isidore-changeset_py.md` — how a change is traced to the symbols it touches.
- `src-isidore-cli_py.md` — the commands, and which module each one reaches.
