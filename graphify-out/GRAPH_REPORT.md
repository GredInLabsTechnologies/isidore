# Graph Report - isidore  (2026-07-26)

## Corpus Check
- 102 files · ~75,020 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1159 nodes · 2709 edges · 69 communities (64 shown, 5 thin omitted)
- Extraction: 85% EXTRACTED · 15% INFERRED · 0% AMBIGUOUS · INFERRED: 418 edges (avg confidence: 0.77)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `1a34c13e`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- cli.py
- graph.py
- compile_wiki
- read_certificate
- detectors.py
- verify.py
- humanpack.py
- quickstart.md
- findings.py
- module_of
- test_claims.py
- home.py
- whatsnew.py
- build_certificate
- pyramid.py
- claims.py
- surface.py
- Isidore v2 — Incremental compilation, impact detection & residue mining
- git_repo.py
- VerifyContext
- IngestOptions
- pipeline.py
- mcp.py
- test_pcp_pipeline.py
- knowledge.py
- plan_pages
- pcp.py
- _tool_read_only
- PCP_SEAMS — the frozen interface for Proof-Carrying Prose (ADR-0033, phase P0)
- encode
- Mark
- write_items
- isidore
- auth.py
- isidore-wiki
- scan
- assemble_context
- GenerationError
- ClaimVerdict
- test_wiki_dir_env.py
- test_reconcile.py
- test_humanpack.py
- src-isidore.md
- tests-test_claims_py.md
- tests-test_connectors_f1_py.md
- tests-test_langspec_py.md
- tests-test_pcp_seams_py.md
- tests-test_pipeline_py.md
- tests-test_security_prose_py.md
- tests-test_units_py.md
- svc.md
- Claims (TOON)
- Findings (TOON)
- Index (TOON)
- verify_page
- load_state
- render_whatsnew_md
- test_changeset.py
- What's new — `HEAD~2..HEAD`
- harvest_todos
- tests-test_surface_py.md
- tests-test_verify_py.md
- tests-test_whatsnew_py.md
- isidore
- SurfaceSymbol
- assemble_context
- compile_subsystems
- reconcile
- subsystem-tests.md

## God Nodes (most connected - your core abstractions)
1. `compile_wiki()` - 80 edges
2. `VerifyContext` - 52 edges
3. `_make_repo()` - 31 edges
4. `run_whatsnew()` - 29 edges
5. `build_delta()` - 26 edges
6. `load_graph()` - 25 edges
7. `Predicate` - 22 edges
8. `compile_overview()` - 22 edges
9. `IngestOptions` - 21 edges
10. `load_state()` - 21 edges

## Surprising Connections (you probably didn't know these)
- `test_three_field_parser_captures_predicate()` --calls--> `parse_claims_block()`  [INFERRED]
  tests/test_verify.py → src/isidore/claims.py
- `test_pcp_subcommands_are_registered()` --calls--> `main()`  [INFERRED]
  tests/test_pcp_seams.py → src/isidore/cli.py
- `test_filter_findings_drops_hallucinated_paths()` --calls--> `filter_findings()`  [INFERRED]
  tests/test_units.py → src/isidore/findings.py
- `test_render_findings_tables_and_summary()` --calls--> `render_findings()`  [INFERRED]
  tests/test_units.py → src/isidore/findings.py
- `test_golden_graph_loads()` --calls--> `load_graph()`  [INFERRED]
  tests/test_pcp_seams.py → src/isidore/graph.py

## Import Cycles
- 1-file cycle: `src/isidore/connectors/__init__.py -> src/isidore/connectors/__init__.py`

## Hyperedges (group relationships)
- **Isidore Compilation Flow** — src_isidore_pipeline, src_isidore_graph, src_isidore_claims, src_isidore_findings [EXTRACTED 1.00]

## Communities (69 total, 5 thin omitted)

### Community 0 - "cli.py"
Cohesion: 0.22
Nodes (14): _cmd_ask(), _cmd_impact(), _cmd_scan(), _cmd_stats(), _cmd_suggest_flows(), main(), isidore — compile an agent-oriented wiki from your codebase's structure graph., Precedence: explicit CLI arg > isidore.json > built-in default. (+6 more)

### Community 1 - "graph.py"
Cohesion: 0.05
Nodes (67): git_head(), git_listed_files(), _is_binary(), _iter_source_files(), _node_id(), _norm_source_file(), Path, Structure graph: loading, module grouping, and a built-in multi-language scanner (+59 more)

### Community 2 - "compile_wiki"
Cohesion: 0.19
Nodes (29): compile_wiki(), lint_cited_paths(), File-looking paths cited in the prose that do NOT exist in the repo., Run the pipeline. With execute=False no LLM is called and no page is written., _gp(), _link(), _make_repo(), _node() (+21 more)

### Community 3 - "read_certificate"
Cohesion: 0.10
Nodes (27): Certificate, certificate_from_dict(), certificate_to_dict(), get_verifier(), Path, Protocol, Proof-Carrying Prose (PCP) — the frozen seam shared by every PCP lane.  This mod, A predicate verifier. MUST be deterministic and 0-LLM. Returns UNDECIDABLE, neve (+19 more)

### Community 4 - "detectors.py"
Cohesion: 0.09
Nodes (27): _looks_like_secret(), Path, Lane C — deterministic security detectors: entropy, sinks, topology. 0 LLM. (T-e, Files reachable from an auth/secret/crypto root via imports (BFS, file-level). 0, Run all three detector families over the repo -> deterministic marks. Pure, 0-LL, Shannon entropy per character (bits). Stdlib only., Return a reason if the literal is credential-shaped, else None., Repo-relative source files to scan: the graph's, or a bounded walk if the graph (+19 more)

### Community 5 - "verify.py"
Cohesion: 0.11
Nodes (43): AST, Module, Lane B (part 2) — claim->contract graduation + `isidore contracts`. (T-8dfc)  A, Check every promoted contract against the current graph. Pure, 0-LLM., verify_contracts(), The result of checking one predicate against an oracle. `value` is TRUE|FALSE|UN, Everything a verifier needs, assembled once per page/verify run. Read-only to ve, undecidable() (+35 more)

### Community 6 - "humanpack.py"
Cohesion: 0.08
Nodes (37): _cmd_contracts(), Add `isidore contracts` (promote / list / check)., Command implementation for `isidore contracts`., register_cli(), _cmd_render(), _esc(), format_mark(), generate_architecture_map() (+29 more)

### Community 7 - "quickstart.md"
Cohesion: 0.40
Nodes (3): Wiki (isidore), Modules, Wiki (isidore)

### Community 8 - "findings.py"
Cohesion: 0.07
Nodes (38): _churn(), insert_security_banner(), is_finding_resolved(), is_security_finding(), Path, Side observations ("residue") harvested during compilation — at ~zero marginal c, Resolve a finding, logging it in wiki/resolved_findings.json., True if a suspect reads as a security risk (hardcoded secret, auth bypass, injec (+30 more)

### Community 9 - "module_of"
Cohesion: 0.13
Nodes (24): affected_modules(), changed_lines(), changed_symbols(), _git_diff(), _module_fan_in(), modules_of(), Path, Change-set detection: which graph symbols a git diff touched, and which modules (+16 more)

### Community 10 - "test_claims.py"
Cohesion: 0.08
Nodes (54): anchor_claims(), check_claims(), claim_id(), claims_for_file(), claims_grep(), evidence_hash(), evidence_state(), _hash() (+46 more)

### Community 11 - "home.py"
Cohesion: 0.16
Nodes (25): git-repo connector (ADR-0032 F1): local repositories as a knowledge source. No n, iter_items(), prune_runs(), The raw store: immutable ingested items + per-connector cursor state (ADR-0032 F, Run ids from state (already newest-first); fall back to sorting the raw dir if s, Drop all but the newest `keep` runs, deleting their raw dirs and trimming state., Append items as JSONL to `raw/<run_id>/items.jsonl`; stamp each with its `chash`, Current state, or a fresh default if missing OR corrupt (I13-style recovery, nev (+17 more)

### Community 12 - "whatsnew.py"
Cohesion: 0.17
Nodes (25): Build the delta, optionally write the prose, and persist page + certificate., run_whatsnew(), WhatsnewResult, _commit(), _git(), _one_file_repo(), isidore whatsnew: the typed surface delta, its artifact, and the verification di, A repository mirroring the shape of the change that motivated this command: a me (+17 more)

### Community 13 - "build_certificate"
Cohesion: 0.13
Nodes (23): parse_predicate_field(), Parse a claim's optional third field into a pcp.Predicate (or None). PCP typed-c, ClaimVerdict, prose_hash(), One claim's line in a certificate: the anchored claim + its typed verdict (if an, The tamper-evidence anchor: sha256 of the page prose (full hex, this is a machin, build_certificate(), _claim_symbols() (+15 more)

### Community 14 - "pyramid.py"
Cohesion: 0.29
Nodes (9): plan_pyramid(), Plan deterministic N2 subsystem + N3 product pages. 0 LLM.      Explicit `pyrami, _graph(), Lane D gate — the pyramid plans from the real graph, uses imports for cohesion,, BUG 1 regression: auto-seed used node['path'/'file'/'name'] (absent) -> []. Must, BUG 2 regression: `links` was ignored. imports edges must yield depends_on., test_autoseed_groups_by_source_file_on_the_real_graph(), test_explicit_config_still_works() (+1 more)

### Community 15 - "claims.py"
Cohesion: 0.10
Nodes (24): coverage_gap_candidates(), orphan_file_candidates(), Code FILE nodes nothing links to — dead-code candidates (entrypoint-looking name, Module pages with no inbound link from any test-looking module., isidore — compile an agent-oriented wiki from your codebase's structure graph., append_run(), annotate_unverified_paths(), CompileResult (+16 more)

### Community 16 - "surface.py"
Cohesion: 0.05
Nodes (70): Match, _brace(), _doc(), extract(), _js(), _kw_func(), _kw_type(), LanguageSpec (+62 more)

### Community 17 - "Isidore v2 — Incremental compilation, impact detection & residue mining"
Cohesion: 0.12
Nodes (16): 0 · Why (user directive), 1 · Verified bug diagnoses (2026-07-10, against real code — not reports), 2 · Design principles (unchanged bets, now enforced deeper), 3 · C0 — Scoped compile: `isidore compile --only <sel>[,<sel>…]`, 4 · C1+C2 — Change-driven compile: `isidore compile --changed [--since <ref>]`, 5 · C3 — Impact detection: `isidore impact [--since <ref>] [--md] [--check]` (new, **0 LLM always**), 6 · C4+C5+C6 — Correctness fixes (the right ones), 7 · C7 — Residue mining (all 0-LLM; the "squeeze everything" layer) (+8 more)

### Community 18 - "git_repo.py"
Cohesion: 0.25
Nodes (13): all_connectors(), Connector, get(), IngestResult, _load_plugins(), missing_env(), Protocol, Connector protocol + registry (ADR-0032 F1).  A connector ingests raw items from (+5 more)

### Community 19 - "VerifyContext"
Cohesion: 0.13
Nodes (20): Counter, context_hash(), _match_seed(), module_dep_edges(), plan_flows(), plan_pages(), prompt_for(), Cross-module dependency edges (src_module, dst_module) -> link count. Shared by (+12 more)

### Community 20 - "IngestOptions"
Cohesion: 0.14
Nodes (17): IngestOptions, Caps and scoping for a run. All limits live here (in code), never in a prompt., GitRepoConnector, Run a git command; return stdout or None on any failure (never raises)., (item, None) for a changed repo, (None, None) if HEAD is unchanged, (None, warni, iso_now(), _git(), _head() (+9 more)

### Community 21 - "pipeline.py"
Cohesion: 0.17
Nodes (18): GraphError, load_graph(), The graph file exists but is not valid (malformed JSON or wrong shape)., _cmd_overview(), _cmd_pyramid(), _cmd_subsystems(), _load_graph_for(), _module_pages_of() (+10 more)

### Community 22 - "mcp.py"
Cohesion: 0.19
Nodes (10): _allowed(), _JsonRpcClient, McpConnector, Any, Minimal read-only MCP connector (ADR-0032 F3).  The implementation deliberately, Map tool name -> its MCP annotations via tools/list (paginated). Empty if the se, Prepend a run summary, keeping the last 20 (newest first)., record_run() (+2 more)

### Community 23 - "test_pcp_pipeline.py"
Cohesion: 0.29
Nodes (10): _compile(), _fake_generator(), _fake_generator_with_a_lie(), Path, P-INT gate — the pipeline wiring ties all five PCP lanes together end to end: a, test_compile_writes_a_certificate_with_typed_verdicts(), test_deterministic_mark_forces_the_banner_despite_calm_prose(), test_refuted_claim_is_quarantined_not_published() (+2 more)

### Community 24 - "knowledge.py"
Cohesion: 0.12
Nodes (28): _cmd_sync(), create_run_id(), Sortable, collision-resistant run id (UTC second + millis)., filter_findings(), parse_findings_block(), Drop findings whose cited path does not exist (mechanical hallucination filter)., Split a generated page into (clean page, findings rows). Tolerant of malformed l, home() (+20 more)

### Community 25 - "plan_pages"
Cohesion: 0.16
Nodes (16): compile_overview(), _plain_violations(), Turn `wiki://page` into `page` in PROSE, so the links a reader clicks actually r, Rule names broken by the PROSE (fenced blocks excluded — those are machine-facin, Compile the plain-language product page (N3). One LLM call, plus at most one rep, relink_wiki_uris(), The N3 product overview: plain language for anyone, resting on claims already pr, The module page above, registered in the wiki state so an area can find it. (+8 more)

### Community 26 - "pcp.py"
Cohesion: 0.12
Nodes (20): parse_predicate(), Predicate, Dispatch one predicate to its registered verifier. No verifier -> UNDECIDABLE (f, A decidable assertion parsed from a claim's third field. Frozen: predicates are, Parse "<kind>:<a>;<b>" -> Predicate, or None if absent/malformed/unknown-kind., verify_predicate(), _chain_verdicts(), Resolve `wiki://` claims through lane D's verifier and compose the child certifi (+12 more)

### Community 27 - "_tool_read_only"
Cohesion: 0.16
Nodes (12): _name_looks_mutating(), Fallback heuristic ONLY (not exhaustive): does the tool name contain a mutating, (allowed, reason). Authority order: explicit readOnlyHint/destructiveHint > name, _tool_read_only(), _FakeClient, MCP connector read-only barrier (ADR-0032 F3). Regression for the review of T-db, Stands in for _JsonRpcClient: a server exposing one read tool, one write tool (a, test_destructive_hint_rejects() (+4 more)

### Community 28 - "PCP_SEAMS — the frozen interface for Proof-Carrying Prose (ADR-0033, phase P0)"
Cohesion: 0.15
Nodes (12): Certificate (`<page>.md` → `<page>.md.cert.json`, alongside the page), CLI, Contracts (`contracts.json` in the wiki dir), File ownership matrix (nobody edits another lane's files), How each lane starts (all depend ONLY on P0 = T-1dc9), Marks (lane C output; also the golden `marks.json`), PCP_SEAMS — the frozen interface for Proof-Carrying Prose (ADR-0033, phase P0), Pipeline hooks (lane A wires; signatures frozen) (+4 more)

### Community 29 - "encode"
Cohesion: 0.15
Nodes (18): Compile journal + per-page changelog — residue mining, all zero-LLM.  Every comp, Map each `## heading` to its body text (content before the first heading is keye, (H2 headings whose content changed / were added / removed, new_line_count - old_, Append an H2-level changelog entry to a page's state (capped). No-op if the pros, record_page_change(), render_stats(), section_diff(), _sections() (+10 more)

### Community 30 - "Mark"
Cohesion: 0.15
Nodes (16): check(), explain(), is_plain(), PlainRule, Pattern, Plain-language gate: can a reader who has never seen code use this sentence?  Do, Human-readable reason for a rejection, for the run summary and the journal., One named check. `kind` mirrors Vale's rule taxonomy so the intent of each is de (+8 more)

### Community 31 - "write_items"
Cohesion: 0.22
Nodes (10): Request, _cmd_compile(), build_request(), generate(), GenerationError, RuntimeError, Single-provider LLM client (OpenAI-compatible), fail-closed by design.  One mode, The provider failed. No retry with a different model — fail closed. (+2 more)

### Community 32 - "isidore"
Cohesion: 0.14
Nodes (13): Bring your own graph, Config (`isidore.json`, optional), Design rules, isidore, Languages, License, One range, three readers, Proof-carrying prose — how to read a certified page (+5 more)

### Community 33 - "auth.py"
Cohesion: 0.29
Nodes (6): authenticate(), Auth service fixture for PCP lane tests. Line numbers are load-bearing: the gold, Verify the caller's JWT and enforce the attempt ceiling., Token service fixture for PCP lane tests. verify_jwt is defined on L5 (cited by, Return the decoded claims if the token's signature checks out, else None., verify_jwt()

### Community 35 - "scan"
Cohesion: 0.50
Nodes (4): Drop the pipe-separated citation a model appends to its own bullets.      Observ, strip_inline_claim_rows(), test_a_bare_trailing_citation_is_stripped_too(), test_a_real_markdown_table_is_left_alone()

### Community 36 - "assemble_context"
Cohesion: 0.23
Nodes (14): _cmd_export_agora(), build_cards(), Path, export-agora — bridge isidore's verified claims into Living-Library card DRAFTS, Return [(filename, content)] draft cards — one per wiki page with enough OK clai, render_card(), _slug(), write_cards() (+6 more)

### Community 37 - "GenerationError"
Cohesion: 0.19
Nodes (15): _blob(), commit_hints(), _git(), _name_status(), Path, Run one git command, argv-style. Any failure is an exception: a changelog built, A ref -> its full commit sha. Raises WhatsnewError if it does not resolve, so a, One file's text at one revision, or None when it is absent or binary. (+7 more)

### Community 38 - "ClaimVerdict"
Cohesion: 0.15
Nodes (18): _cmd_whatsnew(), DeltaEntry, generate_prose(), _group_by_module(), _llm_entries(), parse_plain_block(), _prompt_for_module(), isidore whatsnew — a changelog you can re-verify, instead of one you have to tru (+10 more)

### Community 39 - "test_wiki_dir_env.py"
Cohesion: 0.31
Nodes (7): ISIDORE_WIKI_DIR redirects the compiled-wiki output directory.  WIKI_DIRNAME is, A nested WIKI_DIRNAME (e.g. doc/isidore) must create its parents, not crash., _reload_render(), test_save_state_creates_nested_wiki_dir(), test_wiki_dirname_blank_env_falls_back(), test_wiki_dirname_defaults_to_wiki(), test_wiki_dirname_honors_env()

### Community 40 - "test_reconcile.py"
Cohesion: 0.13
Nodes (17): build_delta(), impact_summary(), _is_comparable(), _md_section(), Skip generated wiki output, the graph store, and anything not source code. Compa, The zero-LLM core: a typed API-surface difference between two revisions.      Pr, The consequence of this range, in plain words, with zero LLM calls.      A non-t, The page, layered by READER rather than by topic.      The same range has three (+9 more)

### Community 41 - "test_humanpack.py"
Cohesion: 0.36
Nodes (10): Run the scanner and persist the graph to .isidore/graph.json., write_scan(), build_impact(), Path, _git(), isidore impact — the 0-LLM emergent-interaction detector, over a real git repo +, _seed_repo(), test_impact_check_exit_signal_and_clean() (+2 more)

### Community 42 - "src-isidore.md"
Cohesion: 0.33
Nodes (5): Architecture, Dependencies, How to change safely, Key entry points, Purpose

### Community 43 - "tests-test_claims_py.md"
Cohesion: 0.33
Nodes (5): Architecture, Dependencies, How to change safely, Key entry points, Purpose

### Community 44 - "tests-test_connectors_f1_py.md"
Cohesion: 0.33
Nodes (5): Architecture, Dependencies, How to change safely, Key entry points, Purpose

### Community 45 - "tests-test_langspec_py.md"
Cohesion: 0.33
Nodes (5): Architecture, Dependencies, How to change safely, Key entry points, Purpose

### Community 46 - "tests-test_pcp_seams_py.md"
Cohesion: 0.33
Nodes (5): Architecture, Dependencies, How to change safely, Key entry points, Purpose

### Community 47 - "tests-test_pipeline_py.md"
Cohesion: 0.33
Nodes (5): Architecture, Dependencies, How to change safely, Key entry points, Purpose

### Community 48 - "tests-test_security_prose_py.md"
Cohesion: 0.33
Nodes (5): Architecture, Dependencies, How to change safely, Key entry points, Purpose

### Community 49 - "tests-test_units_py.md"
Cohesion: 0.33
Nodes (5): Architecture, Dependencies, How to change safely, Key entry points, Purpose

### Community 54 - "verify_page"
Cohesion: 0.43
Nodes (7): _cmd_verify(), _ctx_for(), Path, Re-verify a page against its sidecar certificate, offline, 0 LLM (invariant I11), Add `isidore verify` (called once from cli.main via the registrar loop — P0 owns, register_cli(), verify_page()

### Community 55 - "load_state"
Cohesion: 0.24
Nodes (13): _cmd_findings(), finding_id(), findings_new(), Findings whose evidence lies in files changed since `since` — what this change i, Deterministic, stable id for a finding., load_state(), _git(), Residue-mining units: section diff, compile journal/stats, per-page history, cla (+5 more)

### Community 56 - "render_whatsnew_md"
Cohesion: 0.20
Nodes (11): parse_wiki_uri(), wiki://<page>#<claim-id> -> (page, claim_id), or None if it is not a wiki URI., _claim_verdict(), Resolve (verdict, state) for a cited claim. Truth comes from the page's certific, Resolve a wiki:// chain. Fail-closed: None/invalid/missing -> not TRUE, never cr, _wikichain_verifier(), test_wiki_uri_parsing(), BUG 3 regression: a None predicate crashed with AttributeError. (+3 more)

### Community 57 - "test_changeset.py"
Cohesion: 0.24
Nodes (11): overview_facts(), Path, What one subsystem page is written from: its module pages and the claims they PR, Every claim the pages below PROVED, as citable `wiki://page#id` facts.      This, The project's own words about itself — CONTEXT, never evidence (see OVERVIEW_PRO, Everything the overview is allowed to be written from. 0 LLM., _readme_context(), subsystem_facts() (+3 more)

### Community 58 - "What's new — `HEAD~2..HEAD`"
Cohesion: 0.29
Nodes (6): Every change, in detail, In plain words, Internal surface, Public API, Tests, What's new — `HEAD~2..HEAD`

### Community 59 - "harvest_todos"
Cohesion: 0.24
Nodes (8): harvest_todos(), TODO/FIXME/HACK/XXX with file:line — regex over the files the graph already know, _edges(), ImpactReport, isidore impact — the zero-LLM emergent-interaction detector.  Regenerating a nei, render_impact(), test_harvest_todos_finds_markers_with_lines(), test_harvest_todos_skips_oversized_files()

### Community 60 - "tests-test_surface_py.md"
Cohesion: 0.33
Nodes (5): Architecture, Dependencies, How to change safely, Key entry points, Purpose

### Community 61 - "tests-test_verify_py.md"
Cohesion: 0.33
Nodes (5): Architecture, Dependencies, How to change safely, Key entry points, Purpose

### Community 62 - "tests-test_whatsnew_py.md"
Cohesion: 0.33
Nodes (5): Architecture, Dependencies, How to change safely, Key entry points, Purpose

### Community 63 - "isidore"
Cohesion: 0.40
Nodes (4): How the pieces fit together, isidore, What this is, What you can do with it

### Community 64 - "SurfaceSymbol"
Cohesion: 0.18
Nodes (10): One declared symbol of a file, as of one revision of its text.      `qualname` i, SurfaceSymbol, _diff_surfaces(), _file_summary(), RuntimeError, Git could not answer, or a ref does not resolve. Fail closed: never guess a rang, A compact roll-up of what a whole added/removed file declares., Typed difference between two surfaces of the same file.      Identity is the qua (+2 more)

### Community 65 - "assemble_context"
Cohesion: 0.24
Nodes (10): assemble_context(), git_log_for(), Path, ±radius lines around a graph `L<n>` location. Tolerates stale files/locations., Gather one page's facts. Returns (context, truncation-warnings)., read_excerpt(), save_state(), test_assemble_context_includes_docs_excerpts_deps_and_budget_warning() (+2 more)

### Community 66 - "compile_subsystems"
Cohesion: 0.31
Nodes (9): default_generator(), Build the env-configured generator. Fails closed if no model is set., compile_subsystems(), Compile the N2 layer: one bounded call per area, each page chained to its module, subsystem_page_name(), _nodes(), test_an_area_page_is_chained_to_the_module_pages_below_it(), test_an_area_with_nothing_proven_under_it_is_skipped_not_invented() (+1 more)

### Community 67 - "reconcile"
Cohesion: 0.40
Nodes (5): Lane B (part 1) — the reconciler: the model's own outputs cross-checked, 0 LLM., Helper to split file:line into (file, line)., Cross-check prose vs findings vs claims vs marks -> internal contradictions. Pur, reconcile(), _split_evidence()

### Community 68 - "subsystem-tests.md"
Cohesion: 0.40
Nodes (4): How the work is divided, What it depends on, and what depends on it, What this area is responsible for, Where to start reading

## Knowledge Gaps
- **109 isolated node(s):** `isidore-wiki`, `Wiki (isidore)`, `Why`, `Quickstart`, `What you get` (+104 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **5 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `VerifyContext` connect `verify.py` to `SurfaceSymbol`, `compile_wiki`, `read_certificate`, `detectors.py`, `compile_subsystems`, `ClaimVerdict`, `GenerationError`, `whatsnew.py`, `build_certificate`, `claims.py`, `pipeline.py`, `verify_page`, `render_whatsnew_md`, `plan_pages`, `pcp.py`?**
  _High betweenness centrality (0.096) - this node is a cross-community bridge._
- **Why does `IngestOptions` connect `IngestOptions` to `cli.py`, `home.py`, `git_repo.py`, `mcp.py`, `knowledge.py`, `_tool_read_only`?**
  _High betweenness centrality (0.084) - this node is a cross-community bridge._
- **Why does `compile_wiki()` connect `compile_wiki` to `cli.py`, `graph.py`, `read_certificate`, `detectors.py`, `verify.py`, `findings.py`, `module_of`, `test_claims.py`, `build_certificate`, `claims.py`, `VerifyContext`, `pipeline.py`, `test_pcp_pipeline.py`, `knowledge.py`, `encode`, `write_items`, `assemble_context`, `test_humanpack.py`, `load_state`, `harvest_todos`, `assemble_context`, `compile_subsystems`, `reconcile`?**
  _High betweenness centrality (0.072) - this node is a cross-community bridge._
- **Are the 30 inferred relationships involving `compile_wiki()` (e.g. with `test_compile_stores_claims_and_writes_claims_toon()` and `test_dry_run_still_detects_stale_claims_for_free()`) actually correct?**
  _`compile_wiki()` has 30 INFERRED edges - model-reasoned connections that need verification._
- **Are the 12 inferred relationships involving `VerifyContext` (e.g. with `CompileResult` and `PageSpec`) actually correct?**
  _`VerifyContext` has 12 INFERRED edges - model-reasoned connections that need verification._
- **Are the 12 inferred relationships involving `run_whatsnew()` (e.g. with `test_a_false_predicate_is_kept_in_the_certificate_but_never_published()` and `test_a_phantom_path_earns_one_repair_attempt_then_a_visible_quarantine()`) actually correct?**
  _`run_whatsnew()` has 12 INFERRED edges - model-reasoned connections that need verification._
- **Are the 14 inferred relationships involving `build_delta()` (e.g. with `test_deleted_file_is_reported_but_carries_no_line_to_cite()` and `test_delta_reports_exactly_the_real_changes_and_invents_nothing()`) actually correct?**
  _`build_delta()` has 14 INFERRED edges - model-reasoned connections that need verification._