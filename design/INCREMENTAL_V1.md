# Isidore v2 — Incremental compilation, impact detection & residue mining

Date: 2026-07-10 · Status: **design frozen for execution** · Author: claude-agora (design NOT delegated)
· Execution: Ágora tasks T-series reference the section numbers below. Changing this design = edit this
file first, then the tasks — never silent divergence.

## 0 · Why (user directive)

1. **Scoped updates** — "we built a feature here; document just this zone", without walking the repo.
2. **Change-driven updates** — Isidore detects which zones were already mapped and unchanged, and
   refreshes only what changed **or is affected by the change**, to surface unexpected/emergent
   interactions and candidate bugs.
3. **Squeeze the residues** — every by-product of Isidore's work (claims, findings, state, graph,
   old prose) must be mined for value; nothing thrown away.
4. **Fix the reported bugs correctly** (not symptomatically).
5. GLOSA (sibling effort, own repo): finish it — see §8.

## 1 · Verified bug diagnoses (2026-07-10, against real code — not reports)

| # | Report | Verdict | Evidence |
|---|--------|---------|----------|
| A | Hallucination-lint detects nonexistent cited paths but the page ships anyway (sello + chatgpt/T-da69) | **CONFIRMED** | `pipeline.py` `compile_wiki`: after `lint_cited_paths` the finding is recorded, an HTML comment is appended, and the page is **written unconditionally**. No retry, no quarantine. |
| B | "Citation parser eats the first char (`ello/attestation.py`)" (sello) | **REFUTED** | `_PATH_TOKEN` regex tested against `sello/attestation.py` in 5 contexts (backticks, parens, trailing dot, prose) — extracts the full path every time. The truncated cite was **authored by the LLM in the prose**; the lint correctly caught it. Fix A covers this symptom entirely. **Do NOT "fix" the regex.** |
| C | 2 false-positive claims by "absence-in-excerpt" (claude-gimo, 2026-07-07) | **CONFIRMED (design gap)** | Prompts don't forbid absence assertions; excerpts are partial by construction, so "X does not exist / is not handled" is structurally unverifiable by evidence-hash anchoring. |
| D | Default `--max-calls=12` < routine dirty count (13) leaves one page persistently stale (sello, nit) | **CONFIRMED (ergonomics)** | Cap is honest (reported, never silent) but there is no pending-first draining, so the SAME page can stay stale across runs. |

## 2 · Design principles (unchanged bets, now enforced deeper)

- Deterministic everything except prose; LLM calls bounded **in code**.
- **Never silent**: every skip, truncation, quarantine, drop is counted and reported.
- The graph answers WHAT/WHERE; **git is the source of truth for change**.
- Residues are assets: state, claims, findings, old prose all feed 0-LLM tools.
- Regenerating prose is a **weak** bug detector; **graph diffs and claim staleness are strong, free
  detectors**. Spend LLM calls on prose only after the free layer has said what is affected.

## 3 · C0 — Scoped compile: `isidore compile --only <sel>[,<sel>…]`

Manual targeting: "I documented here."

- `<sel>` matches a module path prefix (`agora/grants`) or a page filename (`agora-grants_py.md`).
- The **full plan is still computed** (the prune universe and `index.toon`/`quickstart.md` stay
  deterministic), but only matching pages are context-assembled / hash-checked / generated.
- **Prune is DISABLED whenever a scope is active** (`--only` or `--since`): scoping must never delete.
- If the graph's recorded commit ≠ `git HEAD`, print a stale-graph warning (suggest `isidore scan`).
- Result reports `scoped: N of M planned pages`.

Seam: `compile_wiki(only: list[str] | None = None)` in `pipeline.py`; arg in `cli.py`. Tests: match by
module and by filename; out-of-scope pages byte-identical after run; prune skipped under scope.

## 4 · C1+C2 — Change-driven compile: `isidore compile --changed [--since <ref>]`

### C1 · Symbol-level change-set (new module `src/isidore/changeset.py`, pure functions)

- Default `since` = `state["commit"]` (recorded at last compile). No state → behave as full compile.
- `changed_lines(repo, since) -> dict[file, set[int]]` — parse `git diff -U0 --find-renames
  <since>..HEAD` hunk headers (`@@ -a,b +c,d @@`, new side). Renamed files: old path counts as
  removed, new path as fully changed.
- `symbol_spans(nodes) -> dict[file, list[(start, end, node_id, label)]]` — spans from
  `source_location`. Scanner upgrade (see below) records `L<start>-L<end>`; fallback for start-only
  locations: a symbol spans until the next symbol's start (last one → EOF). Graphs with no locations
  → file-level fallback: any change marks ALL the file's symbols changed (conservative, correct).
- `changed_symbols(...) -> set[node_id]` plus changed non-code files (docs/config → they feed page
  context via doc excerpts, so they dirty their module's page).

**Scanner upgrade** (`graph.py::_scan_python_file`): record `end_lineno` (stdlib ast) →
`source_location = "L<start>-L<end>"`. Backwards compatible: `read_excerpt`'s `L(\d+)` regex already
tolerates the new form (uses start). All new parsers MUST accept both `L<n>` and `L<a>-L<b>`.

### C2 · Affected-set

```
affected_modules(changed_syms) =
    modules(changed_syms)                                 # where the change lives
  ∪ { module(src) : link src → s ∈ changed_syms }         # who USES what changed (fan-in, depth 1)
  ∪ BFS over module-dep edges up to --affected-depth N    # default 1
affected_pages = pages(affected_modules)
  ∪ pages whose claims anchor to changed files            # reuse claims.stale_pages — exists
  ∪ flow pages whose flow_edges touch changed symbols
```

`--changed` restricts evaluation to `affected_pages`; the existing `context_hash` double-gate still
decides what is actually regenerated (affected but context-identical → 0 calls). This is precision,
not a new cache: the win is (1) the impact REPORT (§5), (2) less I/O, (3) explicit intent.

## 5 · C3 — Impact detection: `isidore impact [--since <ref>] [--md] [--check]` (new, **0 LLM always**)

The emergent-interaction detector. Regenerating neighbours' prose does NOT detect interactions —
**a new graph edge does**, and it's free. Requires persisting a dependency fingerprint:

- `state["deps"]` = sorted cross-module edges `[(src_mod, dst_mod, count)]` — computed from the plan
  (expose `module_dep_edges(nodes, links, depth)` next to `plan_pages`, which already builds it).
- Report sections:
  1. Change-set summary (files, symbols, renames) since `<ref>` (default: last compile's commit).
  2. **Emergent interactions**: cross-module edges NEW vs `state["deps"]`; removed edges (dead
     coupling). This is the headline.
  3. Fan-in table: changed symbols × their consumers (top N) — "what you touched is used by…".
  4. Claims at risk: `check_claims` filtered to changed files (candidate doc/behavior drift).
  5. Pages that would be dirty under `--changed` (dry-run of §4).
  6. Findings (`findings.toon`) filtered to affected modules.
- `--check` → exit 1 if dirty pages or stale claims exist (CI gate; pairs with `claims --check`).

Seam: new `src/isidore/impact.py`; state schema addition; `cli.py` subcommand. TOON default, `--md` mirror.

## 6 · C4+C5+C6 — Correctness fixes (the right ones)

### C4 · Lint gate (Bug A) — 3-level escalation, never silent
1. Page fails `lint_cited_paths` → **one bounded retry**: same prompt + repair addendum listing the
   phantom paths ("These cited paths do not exist… remove or replace each with a path present in
   FACTS"). The retry consumes `--max-calls` budget (honest cost).
2. Still failing → write the page with each phantom citation **annotated inline**
   (`path [⚠ isidore: path not found]` — annotate, don't strip: deterministic, visible, reversible
   on next regen), mark `state.pages[name].quarantined = true`, count in
   `CompileResult.quarantined`.
3. `--strict` → exit nonzero if any page quarantined (CI). Default: loud warning.
- Task note: **B is refuted** — `_PATH_TOKEN` untouched.

### C5 · Absence-hallucination filter (report C)
- Prompt rule added to MODULE_PROMPT/FLOW_PROMPT + CLAIMS/FINDINGS addendums: "Never assert that
  something does NOT exist, is NOT used, or is NOT handled anywhere — your facts are excerpts, not
  the whole repo. Describe only what IS evidenced."
- Deterministic backstop in `anchor_claims` (and `filter_findings`): drop claims matching a
  **conservative** negative-existential pattern (negation token + existential verb: "there is no X",
  "X is missing/absent", "no X exists/is defined/handled/configured"). Property negations about
  evidenced code ("X is not thread-safe" anchored to X) are NOT dropped — only existential absence.
- New counter `claims_dropped_negative` (and findings equivalent) in `CompileResult` — reported.
- Rationale: absence-of-a-thing is structurally outside evidence-hash anchoring (its evidence cannot
  be a positive location), so it is excluded **by construction**, not by discipline.

### C6 · `--max-calls` ergonomics (report D)
- `--max-calls 0` = unlimited (explicit opt-out; default stays 12 — bounded-cost bet).
- **Deterministic dirty ordering** so the cap bites the least important: pending-from-last-run
  first, then claims-stale, then changed-set pages (under `--changed`), then fan-in desc, then name.
- `state.pages[name].pending = true` for skipped-by-cap pages → next run drains the backlog instead
  of re-skipping the same page forever.

## 7 · C7 — Residue mining (all 0-LLM; the "squeeze everything" layer)

| Residue | New tool | Value |
|---|---|---|
| `claims.toon` | `isidore claims --by-file <path>` | The **documentation contract** of a file: which wiki assertions anchor to it. Agent pre-flight: "before editing X, these claims must stay true (or recompile these pages after)." |
| `claims.toon` | `isidore claims --grep <term>` | Free search over **verified atomic facts** — answers many `ask` questions with 0 LLM. |
| `.isidore-state.json` | compile **journal** (append per-run record `{commit, planned, dirty, generated, skipped, quarantined, calls_saved}`, capped at 50) → `isidore stats` | Cost telemetry: calls saved by cache vs paid; **most-unstable pages** (context re-dirtied run after run = unstable module contract = architecture smell — a free finding no test suite gives you); quarantine history. |
| old prose at regen time | per-page changelog: at write time diff old file vs new content at H2-heading level → `state.pages[name].history` (last 5: `{commit, sections_changed, line_delta}`) | "What changed in the understanding of this module" — the wiki's own drift log, readable via `stats`. |
| `findings.toon` | `isidore findings --new [--since <ref>]` | Findings whose evidence lies in changed files: "new TODOs/hotspots **introduced by this change**" — reviewer's residue. |
| wiki + claims | `ask` upgrade: score claims.toon entries as first-class evidence (atomic, verified, cheap) alongside pages; `ask --offline` answers from claims+excerpts with 0 LLM or honestly refuses | `ask` already reads quickstart + top-2 pages (verified in `qa.py::gather_evidence`) — the gap is claims-as-evidence and the free path. |
| claims/findings | `isidore export-agora` (**backlog, optional**): render high-signal claims/findings into Living-Library card DRAFTS (`library/<domain>/`) for review — never auto-post | Bridges Isidore residues into the collective's memory. |

Shared seam warning: nearly every task touches `cli.py`. Contract: **`cli.py` is append-only for
subparsers** — each task appends its parser block at the end, never reformats existing blocks;
integrator re-greps after each merge.

## 8 · GLOSA — completion plan (own repo `Github/glosa`; spec `glosa/SPEC.md` is FROZEN — do not edit v0)

State: spec v0 frozen; F1 bench DONE with the finding that encoding tricks alone win only 5–12% and
regress on citable-column payloads → **the thesis lives or dies on F2 (deltas/rereads)**, the
97%-cache-read / 230:1 economics.

- **F2-T1 · Delta emitter v0**: deterministic CLI, cursor-based, emitting full-row delta blocks +
  tombstones over a real table stream (Ágora `sitrep`/`board` output = the real workload). Property
  tests that enforce the invariants **syntactically**: I2 (grammar cannot express a sub-row patch)
  and I3 (emitter never re-emits a stale row after a fresh one — LWW property test).
- **F2-T2 · Multi-turn reread bench**: simulate a K-turn agent conversation where context is re-read
  each turn; measure TOTAL tokens (tiktoken) for JSON vs TOON vs GLOSA-delta including prompt-cache
  pricing (cache-write vs cache-read rates); paired QA accuracy with the F1 non-inferiority gate.
- **F2-T3 · Go/kill decision**: against the kill criteria already frozen in the spec; documented in
  `glosa/FINDINGS.md` either way. GO → F3: pilot behind a flag (e.g. `agora sitrep --glosa`) +
  public English spec. KILL → archived with evidence, collective informed.
- **Now (no code)**: a Living-Library card explaining to the collective what GLOSA is, its status,
  and that **there is nothing to "use" yet** — it is a measurement effort until F2 passes.

## 9 · Task graph (Ágora T-series; bodies carry the seams verbatim)

```
T1 correctness pass (C4+C5+C6)          pipeline.py, claims.py, findings.py, cli.py, tests   [FIRST — same seam as T2]
T2 changeset core (C0+C1+C2)            NEW changeset.py, graph.py scanner, pipeline, cli    [after T1]
T3 impact + deps fingerprint (C3)       NEW impact.py, state schema, cli                     [after T2]
T4 residue tools (C7 journal/stats/…)   NEW journal.py, claims.py, findings.py, cli          [after T3]
T5 ask upgrade (C7 claims-evidence)     qa.py, cli                                           [parallel with T2–T4; cli append-only]
T6 GLOSA F2 delta emitter               glosa repo                                            [independent]
T7 GLOSA F2 bench + go/kill             glosa repo                                            [after T6]
T8 export-agora bridge                  NEW export module, cli                                [backlog, after T4]
```

Every task: full pytest suite + ruff + vulture green, and the REAL flow exercised (a live compile on
a real repo with the new flags) before any "done" — green tests alone are not proof.
