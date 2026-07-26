# Graph Report - isidore  (2026-07-26)

## Corpus Check
- 100 files · ~72,301 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1135 nodes · 2651 edges · 64 communities (59 shown, 5 thin omitted)
- Extraction: 85% EXTRACTED · 15% INFERRED · 0% AMBIGUOUS · INFERRED: 410 edges (avg confidence: 0.77)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `137ef424`
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

## God Nodes (most connected - your core abstractions)
1. `compile_wiki()` - 80 edges
2. `VerifyContext` - 51 edges
3. `_make_repo()` - 31 edges
4. `run_whatsnew()` - 29 edges
5. `build_delta()` - 26 edges
6. `load_graph()` - 25 edges
7. `Predicate` - 22 edges
8. `IngestOptions` - 21 edges
9. `compile_overview()` - 21 edges
10. `anchor_claims()` - 20 edges

## Surprising Connections (you probably didn't know these)
- `test_three_field_parser_captures_predicate()` --calls--> `parse_claims_block()`  [INFERRED]
  tests/test_verify.py → src/isidore/claims.py
- `test_pcp_subcommands_are_registered()` --calls--> `main()`  [INFERRED]
  tests/test_pcp_seams.py → src/isidore/cli.py
- `test_cli_reports_a_bad_ref_without_writing_an_artifact()` --calls--> `main()`  [INFERRED]
  tests/test_whatsnew.py → src/isidore/cli.py
- `test_cli_smoke()` --calls--> `main()`  [INFERRED]
  tests/test_whatsnew.py → src/isidore/cli.py
- `test_filter_findings_drops_hallucinated_paths()` --calls--> `filter_findings()`  [INFERRED]
  tests/test_units.py → src/isidore/findings.py

## Import Cycles
- 1-file cycle: `src/isidore/connectors/__init__.py -> src/isidore/connectors/__init__.py`

## Hyperedges (group relationships)
- **Isidore Compilation Flow** — src_isidore_pipeline, src_isidore_graph, src_isidore_claims, src_isidore_findings [EXTRACTED 1.00]

## Communities (64 total, 5 thin omitted)

### Community 0 - "cli.py"
Cohesion: 0.11
Nodes (35): check_claims(), claims_for_file(), claims_grep(), Re-hash every stored claim's evidence — the zero-LLM staleness audit.      Retur, The documentation contract of a file: every anchored claim whose evidence points, Free-text search over verified atomic facts — answers many questions with 0 LLM, _cmd_ask(), _cmd_claims() (+27 more)

### Community 1 - "graph.py"
Cohesion: 0.07
Nodes (49): Request, isidore — compile an agent-oriented wiki from your codebase's structure graph., build_request(), generate(), GenerationError, RuntimeError, Single-provider LLM client (OpenAI-compatible), fail-closed by design.  One mode, The provider failed. No retry with a different model — fail closed. (+41 more)

### Community 2 - "compile_wiki"
Cohesion: 0.08
Nodes (63): Counter, assemble_context(), compile_wiki(), context_hash(), git_log_for(), lint_cited_paths(), PageSpec, plan_flows() (+55 more)

### Community 3 - "read_certificate"
Cohesion: 0.08
Nodes (38): Certificate, certificate_from_dict(), certificate_to_dict(), Contract, get_verifier(), parse_wiki_uri(), Path, Protocol (+30 more)

### Community 4 - "detectors.py"
Cohesion: 0.07
Nodes (34): _looks_like_secret(), Path, Lane C — deterministic security detectors: entropy, sinks, topology. 0 LLM. (T-e, Files reachable from an auth/secret/crypto root via imports (BFS, file-level). 0, Run all three detector families over the repo -> deterministic marks. Pure, 0-LL, Shannon entropy per character (bits). Stdlib only., Return a reason if the literal is credential-shaped, else None., Repo-relative source files to scan: the graph's, or a bounded walk if the graph (+26 more)

### Community 5 - "verify.py"
Cohesion: 0.11
Nodes (43): AST, Module, Lane B (part 2) — claim->contract graduation + `isidore contracts`. (T-8dfc)  A, Check every promoted contract against the current graph. Pure, 0-LLM., verify_contracts(), The result of checking one predicate against an oracle. `value` is TRUE|FALSE|UN, Everything a verifier needs, assembled once per page/verify run. Read-only to ve, undecidable() (+35 more)

### Community 6 - "humanpack.py"
Cohesion: 0.12
Nodes (28): _cmd_render(), _esc(), format_mark(), generate_architecture_map(), generate_claims_table(), generate_contracts_section(), generate_glossary(), generate_mass_bar() (+20 more)

### Community 7 - "quickstart.md"
Cohesion: 0.40
Nodes (3): Wiki (isidore), Modules, Wiki (isidore)

### Community 8 - "findings.py"
Cohesion: 0.06
Nodes (48): _churn(), coverage_gap_candidates(), filter_findings(), finding_id(), insert_security_banner(), is_finding_resolved(), is_security_finding(), orphan_file_candidates() (+40 more)

### Community 9 - "module_of"
Cohesion: 0.12
Nodes (27): affected_modules(), changed_lines(), changed_symbols(), _git_diff(), _module_fan_in(), modules_of(), Path, Change-set detection: which graph symbols a git diff touched, and which modules (+19 more)

### Community 10 - "test_claims.py"
Cohesion: 0.14
Nodes (25): anchor_claims(), claim_id(), parse_claims_block(), Split a generated page into (clean page, raw claim rows). Tolerant of malformed, Deterministic, ledger-friendly id: stable across runs for the same (statement, e, Repair a shortened citation to a real file, or None if it can't be resolved uniq, Quarantine filter + anchoring. Returns (anchored claims, dropped, repaired)., resolve_citation() (+17 more)

### Community 11 - "home.py"
Cohesion: 0.23
Nodes (15): prune_runs(), Drop all but the newest `keep` runs, deleting their raw dirs and trimming state., Current state, or a fresh default if missing OR corrupt (I13-style recovery, nev, Atomic write (tmp + os.replace) so a crash mid-write never corrupts the live sta, read_state(), write_state(), config_path(), connector_dir() (+7 more)

### Community 12 - "whatsnew.py"
Cohesion: 0.13
Nodes (30): RuntimeError, Git could not answer, or a ref does not resolve. Fail closed: never guess a rang, Build the delta, optionally write the prose, and persist page + certificate., run_whatsnew(), WhatsnewError, WhatsnewResult, _commit(), _git() (+22 more)

### Community 13 - "build_certificate"
Cohesion: 0.12
Nodes (25): parse_predicate_field(), Parse a claim's optional third field into a pcp.Predicate (or None). PCP typed-c, ClaimVerdict, Dispatch one predicate to its registered verifier. No verifier -> UNDECIDABLE (f, One claim's line in a certificate: the anchored claim + its typed verdict (if an, verify_predicate(), build_certificate(), _claim_symbols() (+17 more)

### Community 14 - "pyramid.py"
Cohesion: 0.16
Nodes (15): _claim_verdict(), plan_pyramid(), Plan deterministic N2 subsystem + N3 product pages. 0 LLM.      Explicit `pyrami, Resolve (verdict, state) for a cited claim. Truth comes from the page's certific, Resolve a wiki:// chain. Fail-closed: None/invalid/missing -> not TRUE, never cr, _wikichain_verifier(), _graph(), Lane D gate — the pyramid plans from the real graph, uses imports for cohesion, (+7 more)

### Community 15 - "claims.py"
Cohesion: 0.16
Nodes (24): evidence_hash(), evidence_state(), _hash(), _normalize(), Path, Claims: the atomic, evidence-anchored form of wiki knowledge.  A claim is a sing, Collapse all whitespace runs to single spaces and trim — so re-indentation, trai, Fingerprint of the CITED LINE's normalized content (whole normalized file if no (+16 more)

### Community 16 - "surface.py"
Cohesion: 0.05
Nodes (72): Match, _brace(), _doc(), extract(), _js(), _kw_func(), _kw_type(), LanguageSpec (+64 more)

### Community 17 - "Isidore v2 — Incremental compilation, impact detection & residue mining"
Cohesion: 0.12
Nodes (16): 0 · Why (user directive), 1 · Verified bug diagnoses (2026-07-10, against real code — not reports), 2 · Design principles (unchanged bets, now enforced deeper), 3 · C0 — Scoped compile: `isidore compile --only <sel>[,<sel>…]`, 4 · C1+C2 — Change-driven compile: `isidore compile --changed [--since <ref>]`, 5 · C3 — Impact detection: `isidore impact [--since <ref>] [--md] [--check]` (new, **0 LLM always**), 6 · C4+C5+C6 — Correctness fixes (the right ones), 7 · C7 — Residue mining (all 0-LLM; the "squeeze everything" layer) (+8 more)

### Community 18 - "git_repo.py"
Cohesion: 0.21
Nodes (15): all_connectors(), Connector, get(), IngestResult, _load_plugins(), Protocol, Connector protocol + registry (ADR-0032 F1).  A connector ingests raw items from, Outcome of one ingest run. `raw_files` are the JSONL files written this run. (+7 more)

### Community 19 - "VerifyContext"
Cohesion: 0.50
Nodes (4): _cmd_contracts(), Add `isidore contracts` (promote / list / check)., Command implementation for `isidore contracts`., register_cli()

### Community 20 - "IngestOptions"
Cohesion: 0.13
Nodes (16): GitRepoConnector, Run a git command; return stdout or None on any failure (never raises)., (item, None) for a changed repo, (None, None) if HEAD is unchanged, (None, warni, iso_now(), _git(), _head(), _make_repo(), F1 (ADR-0032): knowledge home + raw store + git-repo connector.  The load-bearin (+8 more)

### Community 21 - "pipeline.py"
Cohesion: 0.11
Nodes (30): git_head(), git_listed_files(), _is_binary(), _iter_source_files(), _node_id(), _norm_source_file(), Path, Structure graph: loading, module grouping, and a built-in multi-language scanner (+22 more)

### Community 22 - "mcp.py"
Cohesion: 0.22
Nodes (9): IngestOptions, Caps and scoping for a run. All limits live here (in code), never in a prompt., _allowed(), _JsonRpcClient, McpConnector, Any, Map tool name -> its MCP annotations via tools/list (paginated). Empty if the se, update_cursor() (+1 more)

### Community 23 - "test_pcp_pipeline.py"
Cohesion: 0.29
Nodes (10): _compile(), _fake_generator(), _fake_generator_with_a_lie(), Path, P-INT gate — the pipeline wiring ties all five PCP lanes together end to end: a, test_compile_writes_a_certificate_with_typed_verdicts(), test_deterministic_mark_forces_the_banner_despite_calm_prose(), test_refuted_claim_is_quarantined_not_published() (+2 more)

### Community 24 - "knowledge.py"
Cohesion: 0.14
Nodes (25): is_negative_existential(), True for statements asserting existential/definitional ABSENCE (unanchorable). C, parse_findings_block(), Split a generated page into (clean page, findings rows). Tolerant of malformed l, chmod that never raises; a no-op on Windows where POSIX modes don't apply., mkdir -p with restrictive mode, best-effort — never raises on a perms/FS quirk., safe_chmod(), safe_mkdir() (+17 more)

### Community 25 - "plan_pages"
Cohesion: 0.12
Nodes (27): _chain_verdicts(), _cmd_overview(), compile_overview(), _norm(), overview_facts(), Path, Lane D — the pyramid: hierarchical synthesis with wiki:// claim chains. (T-af65, 0-LLM subsystem suggester: group files by top directory (the isidore graph uses (+19 more)

### Community 26 - "pcp.py"
Cohesion: 0.19
Nodes (11): parse_predicate(), Predicate, A decidable assertion parsed from a claim's third field. Frozen: predicates are, Parse "<kind>:<a>;<b>" -> Predicate, or None if absent/malformed/unknown-kind., P0 gate (ADR-0033) — the frozen PCP seam parses its golden fixtures and exposes, test_golden_graph_loads(), test_golden_marks_and_pyramid_config_parse(), test_pcp_subcommands_are_registered() (+3 more)

### Community 27 - "_tool_read_only"
Cohesion: 0.16
Nodes (12): _name_looks_mutating(), Fallback heuristic ONLY (not exhaustive): does the tool name contain a mutating, (allowed, reason). Authority order: explicit readOnlyHint/destructiveHint > name, _tool_read_only(), _FakeClient, MCP connector read-only barrier (ADR-0032 F3). Regression for the review of T-db, Stands in for _JsonRpcClient: a server exposing one read tool, one write tool (a, test_destructive_hint_rejects() (+4 more)

### Community 28 - "PCP_SEAMS — the frozen interface for Proof-Carrying Prose (ADR-0033, phase P0)"
Cohesion: 0.15
Nodes (12): Certificate (`<page>.md` → `<page>.md.cert.json`, alongside the page), CLI, Contracts (`contracts.json` in the wiki dir), File ownership matrix (nobody edits another lane's files), How each lane starts (all depend ONLY on P0 = T-1dc9), Marks (lane C output; also the golden `marks.json`), PCP_SEAMS — the frozen interface for Proof-Carrying Prose (ADR-0033, phase P0), Pipeline hooks (lane A wires; signatures frozen) (+4 more)

### Community 29 - "encode"
Cohesion: 0.16
Nodes (17): append_run(), Compile journal + per-page changelog — residue mining, all zero-LLM.  Every comp, Map each `## heading` to its body text (content before the first heading is keye, (H2 headings whose content changed / were added / removed, new_line_count - old_, Append an H2-level changelog entry to a page's state (capped). No-op if the pros, record_page_change(), section_diff(), _sections() (+9 more)

### Community 30 - "Mark"
Cohesion: 0.13
Nodes (18): check(), explain(), is_plain(), PlainRule, Pattern, Plain-language gate: can a reader who has never seen code use this sentence?  Do, Human-readable reason for a rejection, for the run summary and the journal., One named check. `kind` mirrors Vale's rule taxonomy so the intent of each is de (+10 more)

### Community 31 - "write_items"
Cohesion: 0.24
Nodes (8): create_run_id(), Sortable, collision-resistant run id (UTC second + millis)., Append items as JSONL to `raw/<run_id>/items.jsonl`; stamp each with its `chash`, write_items(), Algorithmically suggest topics from ingested raw items (0-LLM, term frequency ba, suggest_topics(), test_filter_findings_with_src(), test_suggest_topics()

### Community 32 - "isidore"
Cohesion: 0.15
Nodes (12): Bring your own graph, Config (`isidore.json`, optional), Design rules, isidore, Languages, License, One range, three readers, Proof-carrying prose — how to read a certified page (+4 more)

### Community 33 - "auth.py"
Cohesion: 0.29
Nodes (6): authenticate(), Auth service fixture for PCP lane tests. Line numbers are load-bearing: the gold, Verify the caller's JWT and enforce the attempt ceiling., Token service fixture for PCP lane tests. verify_jwt is defined on L5 (cited by, Return the decoded claims if the token's signature checks out, else None., verify_jwt()

### Community 35 - "scan"
Cohesion: 0.16
Nodes (16): annotate_unverified_paths(), Annotate every cited path that does not exist in the repo, inline and visibly —, _cmd_whatsnew(), generate_prose(), _group_by_module(), parse_plain_block(), _prompt_for_module(), isidore whatsnew — a changelog you can re-verify, instead of one you have to tru (+8 more)

### Community 36 - "assemble_context"
Cohesion: 0.23
Nodes (14): _cmd_export_agora(), build_cards(), Path, export-agora — bridge isidore's verified claims into Living-Library card DRAFTS, Return [(filename, content)] draft cards — one per wiki page with enough OK clai, render_card(), _slug(), write_cards() (+6 more)

### Community 37 - "GenerationError"
Cohesion: 0.19
Nodes (15): _blob(), commit_hints(), _git(), _name_status(), Path, Run one git command, argv-style. Any failure is an exception: a changelog built, A ref -> its full commit sha. Raises WhatsnewError if it does not resolve, so a, One file's text at one revision, or None when it is absent or binary. (+7 more)

### Community 38 - "ClaimVerdict"
Cohesion: 0.20
Nodes (9): DeltaEntry, _llm_entries(), One typed novelty row. `file` is always the path as of `until` (renames map old, The machine/agent view: one table per area, product surface first., What the model is allowed to write about: product surface, and only what can be, render_whatsnew_toon(), _rows(), SurfaceDelta (+1 more)

### Community 39 - "test_wiki_dir_env.py"
Cohesion: 0.31
Nodes (7): ISIDORE_WIKI_DIR redirects the compiled-wiki output directory.  WIKI_DIRNAME is, A nested WIKI_DIRNAME (e.g. doc/isidore) must create its parents, not crash., _reload_render(), test_save_state_creates_nested_wiki_dir(), test_wiki_dirname_blank_env_falls_back(), test_wiki_dirname_defaults_to_wiki(), test_wiki_dirname_honors_env()

### Community 40 - "test_reconcile.py"
Cohesion: 0.15
Nodes (13): build_delta(), _diff_surfaces(), _file_summary(), _is_comparable(), Skip generated wiki output, the graph store, and anything not source code. Compa, A compact roll-up of what a whole added/removed file declares., Typed difference between two surfaces of the same file.      Identity is the qua, The zero-LLM core: a typed API-surface difference between two revisions.      Pr (+5 more)

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
Cohesion: 0.31
Nodes (9): prose_hash(), The tamper-evidence anchor: sha256 of the page prose (full hex, this is a machin, _cmd_verify(), _ctx_for(), Path, Re-verify a page against its sidecar certificate, offline, 0 LLM (invariant I11), Add `isidore verify` (called once from cli.main via the registrar loop — P0 owns, register_cli() (+1 more)

### Community 55 - "load_state"
Cohesion: 0.44
Nodes (8): load_state(), _git(), Residue-mining units: section diff, compile journal/stats, per-page history, cla, _repo(), test_claims_for_file_and_grep(), test_findings_new_reports_todos_in_changed_files(), test_journal_and_stats_track_calls_saved_and_unstable(), test_page_history_records_section_changes()

### Community 56 - "render_whatsnew_md"
Cohesion: 0.25
Nodes (8): impact_summary(), _md_section(), The consequence of this range, in plain words, with zero LLM calls.      A non-t, The page, layered by READER rather than by topic.      The same range has three, render_whatsnew_md(), test_empty_range_is_valid_and_not_an_error(), test_impact_summary_answers_do_i_have_to_do_anything_without_jargon(), test_page_is_layered_so_a_non_technical_reader_can_stop_after_the_top()

### Community 57 - "test_changeset.py"
Cohesion: 0.39
Nodes (7): _code(), _git(), Change-set detection units: symbol spans, changed symbols, affected modules, git, test_affected_modules_is_changed_plus_fan_in_dependents(), test_changed_lines_parses_new_side_hunks(), test_changed_symbols_maps_lines_and_whole_file(), test_symbol_spans_accepts_span_and_start_only_forms()

### Community 58 - "What's new — `HEAD~2..HEAD`"
Cohesion: 0.29
Nodes (6): Every change, in detail, In plain words, Internal surface, Public API, Tests, What's new — `HEAD~2..HEAD`

### Community 59 - "harvest_todos"
Cohesion: 0.33
Nodes (6): findings_new(), harvest_todos(), TODO/FIXME/HACK/XXX with file:line — regex over the files the graph already know, Findings whose evidence lies in files changed since `since` — what this change i, test_harvest_todos_finds_markers_with_lines(), test_harvest_todos_skips_oversized_files()

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

## Knowledge Gaps
- **104 isolated node(s):** `isidore-wiki`, `Wiki (isidore)`, `Why`, `Quickstart`, `What you get` (+99 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **5 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `VerifyContext` connect `verify.py` to `graph.py`, `compile_wiki`, `read_certificate`, `detectors.py`, `scan`, `ClaimVerdict`, `GenerationError`, `module_of`, `test_claims.py`, `whatsnew.py`, `build_certificate`, `pyramid.py`, `verify_page`, `plan_pages`, `pcp.py`?**
  _High betweenness centrality (0.096) - this node is a cross-community bridge._
- **Why does `IngestOptions` connect `mcp.py` to `cli.py`, `git_repo.py`, `_tool_read_only`, `IngestOptions`?**
  _High betweenness centrality (0.082) - this node is a cross-community bridge._
- **Why does `compile_wiki()` connect `compile_wiki` to `cli.py`, `graph.py`, `read_certificate`, `detectors.py`, `verify.py`, `findings.py`, `module_of`, `test_claims.py`, `build_certificate`, `claims.py`, `pipeline.py`, `test_pcp_pipeline.py`, `knowledge.py`, `encode`, `scan`, `assemble_context`, `test_humanpack.py`, `load_state`, `harvest_todos`?**
  _High betweenness centrality (0.075) - this node is a cross-community bridge._
- **Are the 30 inferred relationships involving `compile_wiki()` (e.g. with `test_compile_stores_claims_and_writes_claims_toon()` and `test_dry_run_still_detects_stale_claims_for_free()`) actually correct?**
  _`compile_wiki()` has 30 INFERRED edges - model-reasoned connections that need verification._
- **Are the 12 inferred relationships involving `VerifyContext` (e.g. with `CompileResult` and `PageSpec`) actually correct?**
  _`VerifyContext` has 12 INFERRED edges - model-reasoned connections that need verification._
- **Are the 12 inferred relationships involving `run_whatsnew()` (e.g. with `test_a_false_predicate_is_kept_in_the_certificate_but_never_published()` and `test_a_phantom_path_earns_one_repair_attempt_then_a_visible_quarantine()`) actually correct?**
  _`run_whatsnew()` has 12 INFERRED edges - model-reasoned connections that need verification._
- **Are the 14 inferred relationships involving `build_delta()` (e.g. with `test_deleted_file_is_reported_but_carries_no_line_to_cite()` and `test_delta_reports_exactly_the_real_changes_and_invents_nothing()`) actually correct?**
  _`build_delta()` has 14 INFERRED edges - model-reasoned connections that need verification._