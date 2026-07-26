# Graph Report - isidore  (2026-07-26)

## Corpus Check
- 168 files · ~105,765 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1458 nodes · 3263 edges · 110 communities (105 shown, 5 thin omitted)
- Extraction: 85% EXTRACTED · 15% INFERRED · 0% AMBIGUOUS · INFERRED: 494 edges (avg confidence: 0.76)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `5782a431`
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
- security_banner
- render.py
- src-isidore-changeset_py.md
- src-isidore-claims_py.md
- src-isidore-cli_py.md
- src-isidore-connectors.md
- src-isidore-detectors_py.md
- src-isidore-findings_py.md
- src-isidore-graph_py.md
- src-isidore-home_py.md
- src-isidore-humanpack_py.md
- src-isidore-knowledge_py.md
- src-isidore-langspec_py.md
- src-isidore-pcp_py.md
- src-isidore-pipeline_py.md
- src-isidore-pyramid_py.md
- src-isidore-qa_py.md
- src-isidore-surface_py.md
- src-isidore-verify_py.md
- src-isidore-whatsnew_py.md
- tests-fixtures-pcp.md
- tests-test_changeset_py.md
- tests-test_detectors_py.md
- tests-test_impact_py.md
- tests-test_mcp_barrier_py.md
- tests-test_overview_py.md
- tests-test_pcp_pipeline_py.md
- tests-test_plain_py.md
- tests-test_pyramid_py.md
- tests-test_reconcile_py.md
- tests-test_residue_py.md
- tests-test_wiki_dir_env_py.md
- create_run_id
- subsystem-src.md
- v_calls
- clean_sig
- build_delta
- render_whatsnew_md
- encode
- write_scan
- literal_value

## God Nodes (most connected - your core abstractions)
1. `compile_wiki()` - 83 edges
2. `VerifyContext` - 62 edges
3. `Predicate` - 35 edges
4. `_make_repo()` - 31 edges
5. `run_whatsnew()` - 29 edges
6. `load_graph()` - 27 edges
7. `build_delta()` - 26 edges
8. `compile_overview()` - 25 edges
9. `read_certificate()` - 24 edges
10. `Verdict` - 23 edges

## Surprising Connections (you probably didn't know these)
- `test_pcp_subcommands_are_registered()` --calls--> `main()`  [INFERRED]
  tests/test_pcp_seams.py → src/isidore/cli.py
- `test_cli_reports_a_bad_ref_without_writing_an_artifact()` --calls--> `main()`  [INFERRED]
  tests/test_whatsnew.py → src/isidore/cli.py
- `test_cli_smoke()` --calls--> `main()`  [INFERRED]
  tests/test_whatsnew.py → src/isidore/cli.py
- `test_golden_graph_loads()` --calls--> `load_graph()`  [INFERRED]
  tests/test_pcp_seams.py → src/isidore/graph.py
- `test_module_of_normalizes_and_buckets()` --calls--> `module_of()`  [INFERRED]
  tests/test_units.py → src/isidore/graph.py

## Import Cycles
- 1-file cycle: `src/isidore/connectors/__init__.py -> src/isidore/connectors/__init__.py`

## Communities (110 total, 5 thin omitted)

### Community 0 - "cli.py"
Cohesion: 0.11
Nodes (34): claims_grep(), Free-text search over verified atomic facts — answers many questions with 0 LLM, _cmd_ask(), _cmd_claims(), _cmd_compile(), _cmd_findings(), _cmd_impact(), _cmd_scan() (+26 more)

### Community 1 - "graph.py"
Cohesion: 0.11
Nodes (30): git_head(), git_listed_files(), _is_binary(), _iter_source_files(), _node_id(), _norm_source_file(), Path, Structure graph: loading, module grouping, and a built-in multi-language scanner (+22 more)

### Community 2 - "compile_wiki"
Cohesion: 0.09
Nodes (57): assemble_context(), compile_wiki(), context_hash(), git_log_for(), lint_cited_paths(), plan_pages(), prompt_for(), Path (+49 more)

### Community 3 - "read_certificate"
Cohesion: 0.12
Nodes (19): Contract, get_verifier(), Protocol, Everything a verifier needs, assembled once per page/verify run. Read-only to ve, A predicate verifier. MUST be deterministic and 0-LLM. Returns UNDECIDABLE, neve, Dispatch one predicate to its registered verifier. No verifier -> UNDECIDABLE (f, A typed claim a human promoted to an invariant. `isidore verify --contracts` fai, Verifier (+11 more)

### Community 4 - "detectors.py"
Cohesion: 0.06
Nodes (47): _churn(), coverage_gap_candidates(), filter_findings(), finding_id(), insert_security_banner(), is_finding_resolved(), is_security_finding(), orphan_file_candidates() (+39 more)

### Community 5 - "verify.py"
Cohesion: 0.16
Nodes (23): AST, register_verifier(), _file_nodes(), ground_symbols(), _langspec_symbols(), _literal_str(), _norm(), _prose_identifiers() (+15 more)

### Community 6 - "humanpack.py"
Cohesion: 0.17
Nodes (20): _cmd_render(), _esc(), generate_architecture_map(), generate_claims_table(), generate_contracts_section(), generate_glossary(), generate_mass_bar(), minimal_markdown_to_html() (+12 more)

### Community 7 - "quickstart.md"
Cohesion: 0.40
Nodes (3): Wiki (isidore), Modules, Wiki (isidore)

### Community 8 - "findings.py"
Cohesion: 0.13
Nodes (30): RuntimeError, Git could not answer, or a ref does not resolve. Fail closed: never guess a rang, Build the delta, optionally write the prose, and persist page + certificate., run_whatsnew(), WhatsnewError, WhatsnewResult, _commit(), _git() (+22 more)

### Community 9 - "module_of"
Cohesion: 0.13
Nodes (24): affected_modules(), changed_lines(), changed_symbols(), _git_diff(), _module_fan_in(), modules_of(), Path, Change-set detection: which graph symbols a git diff touched, and which modules (+16 more)

### Community 10 - "test_claims.py"
Cohesion: 0.07
Nodes (54): anchor_claims(), claim_id(), claims_for_file(), evidence_hash(), evidence_state(), is_negative_existential(), parse_claims_block(), parse_predicate_field() (+46 more)

### Community 11 - "home.py"
Cohesion: 0.15
Nodes (24): _hash(), _normalize(), Collapse all whitespace runs to single spaces and trim — so re-indentation, trai, chash(), prune_runs(), The raw store: immutable ingested items + per-connector cursor state (ADR-0032 F, Run ids from state (already newest-first); fall back to sorting the raw dir if s, Drop all but the newest `keep` runs, deleting their raw dirs and trimming state. (+16 more)

### Community 12 - "whatsnew.py"
Cohesion: 0.16
Nodes (16): annotate_unverified_paths(), Annotate every cited path that does not exist in the repo, inline and visibly —, _cmd_whatsnew(), generate_prose(), _group_by_module(), parse_plain_block(), _prompt_for_module(), isidore whatsnew — a changelog you can re-verify, instead of one you have to tru (+8 more)

### Community 13 - "build_certificate"
Cohesion: 0.13
Nodes (18): Match, _declaration_tail(), generic_surface(), _is_declaration(), _is_public(), logical_lines(), _param_group(), API surface extraction from SOURCE TEXT — the zero-LLM substrate of `isidore wha (+10 more)

### Community 14 - "pyramid.py"
Cohesion: 0.29
Nodes (9): plan_pyramid(), Plan deterministic N2 subsystem + N3 product pages. 0 LLM.      Explicit `pyrami, _graph(), Lane D gate — the pyramid plans from the real graph, uses imports for cohesion,, BUG 1 regression: auto-seed used node['path'/'file'/'name'] (absent) -> []. Must, BUG 2 regression: `links` was ignored. imports edges must yield depends_on., test_autoseed_groups_by_source_file_on_the_real_graph(), test_explicit_config_still_works() (+1 more)

### Community 15 - "claims.py"
Cohesion: 0.11
Nodes (23): Counter, Request, render_claims(), isidore — compile an agent-oriented wiki from your codebase's structure graph., build_request(), generate(), GenerationError, RuntimeError (+15 more)

### Community 16 - "surface.py"
Cohesion: 0.48
Nodes (6): _names(), Multi-language scanner: the declarative engine (langspec) and its wiring into sc, test_control_flow_is_not_mistaken_for_a_symbol(), test_go_func_and_type(), test_ruby_uses_end_blocks_not_braces(), test_sanitize_handles_escaped_quote()

### Community 17 - "Isidore v2 — Incremental compilation, impact detection & residue mining"
Cohesion: 0.12
Nodes (16): 0 · Why (user directive), 1 · Verified bug diagnoses (2026-07-10, against real code — not reports), 2 · Design principles (unchanged bets, now enforced deeper), 3 · C0 — Scoped compile: `isidore compile --only <sel>[,<sel>…]`, 4 · C1+C2 — Change-driven compile: `isidore compile --changed [--since <ref>]`, 5 · C3 — Impact detection: `isidore impact [--since <ref>] [--md] [--check]` (new, **0 LLM always**), 6 · C4+C5+C6 — Correctness fixes (the right ones), 7 · C7 — Residue mining (all 0-LLM; the "squeeze everything" layer) (+8 more)

### Community 18 - "git_repo.py"
Cohesion: 0.23
Nodes (14): all_connectors(), Connector, get(), IngestResult, _load_plugins(), missing_env(), Protocol, Connector protocol + registry (ADR-0032 F1).  A connector ingests raw items from (+6 more)

### Community 19 - "VerifyContext"
Cohesion: 0.13
Nodes (19): harvest_todos(), TODO/FIXME/HACK/XXX with file:line — regex over the files the graph already know, _git_repo(), _qa_repo(), Unit tests: toon encoder, graph scanner, findings residue, QA retrieval, LLM req, A third-party graph (e.g. Graphify) that indexed a gitignored path gets cleaned, Outside a git tree we cannot tell what's ignored -> index everything, unchanged., Init a minimal git repo at `path`; skip the test if git is unavailable. (+11 more)

### Community 20 - "IngestOptions"
Cohesion: 0.13
Nodes (18): IngestOptions, Caps and scoping for a run. All limits live here (in code), never in a prompt., GitRepoConnector, Run a git command; return stdout or None on any failure (never raises)., (item, None) for a changed repo, (None, None) if HEAD is unchanged, (None, warni, iso_now(), _git(), _head() (+10 more)

### Community 21 - "pipeline.py"
Cohesion: 0.23
Nodes (12): overview_facts(), _page_purpose(), Path, The first sentence of a module page's `## Purpose` — what that module says it is, What one subsystem page is written from: its module pages, what each says it is, Every claim the pages below PROVED, as citable `wiki://page#id` facts.      This, The project's own words about itself — CONTEXT, never evidence (see OVERVIEW_PRO, Everything the overview is allowed to be written from. 0 LLM. (+4 more)

### Community 22 - "mcp.py"
Cohesion: 0.21
Nodes (9): _allowed(), _JsonRpcClient, McpConnector, Any, Minimal read-only MCP connector (ADR-0032 F3).  The implementation deliberately, Map tool name -> its MCP annotations via tools/list (paginated). Empty if the se, Prepend a run summary, keeping the last 20 (newest first)., record_run() (+1 more)

### Community 23 - "test_pcp_pipeline.py"
Cohesion: 0.29
Nodes (10): _compile(), _fake_generator(), _fake_generator_with_a_lie(), Path, P-INT gate — the pipeline wiring ties all five PCP lanes together end to end: a, test_compile_writes_a_certificate_with_typed_verdicts(), test_deterministic_mark_forces_the_banner_despite_calm_prose(), test_refuted_claim_is_quarantined_not_published() (+2 more)

### Community 24 - "knowledge.py"
Cohesion: 0.14
Nodes (24): Pages owning at least one stale/orphan claim — they must regenerate even if thei, stale_pages(), iter_items(), Yield stored items, newest run first. A corrupt/half-written JSONL line is skipp, parse_findings_block(), Split a generated page into (clean page, findings rows). Tolerant of malformed l, chmod that never raises; a no-op on Windows where POSIX modes don't apply., mkdir -p with restrictive mode, best-effort — never raises on a perms/FS quirk. (+16 more)

### Community 25 - "plan_pages"
Cohesion: 0.15
Nodes (19): compile_overview(), missing_sections(), Required headings the page does not have. 0 LLM., Turn `wiki://page` into `page` in PROSE, so the links a reader clicks actually r, Compile the plain-language product page (N3). One LLM call, plus at most one rep, relink_wiki_uris(), The N3 product overview: plain language for anyone, resting on claims already pr, The module page above, registered in the wiki state so an area can find it. (+11 more)

### Community 26 - "pcp.py"
Cohesion: 0.17
Nodes (24): Predicate, A decidable assertion parsed from a claim's third field. Frozen: predicates are, parameter_names(), Parameter names in declaration order, or None when they cannot be read with conf, value(name, literal): a module-level assignment `name = literal`. Oracles: AST,, signature(fn, a1, a2, ...): fn's positional parameter names, in order. Oracles:, v_signature(), v_value() (+16 more)

### Community 27 - "_tool_read_only"
Cohesion: 0.15
Nodes (13): _name_looks_mutating(), Fallback heuristic ONLY (not exhaustive): does the tool name contain a mutating, (allowed, reason). Authority order: explicit readOnlyHint/destructiveHint > name, _tool_read_only(), _FakeClient, MCP connector read-only barrier (ADR-0032 F3). Regression for the review of T-db, Stands in for _JsonRpcClient: a server exposing one read tool, one write tool (a, test_destructive_hint_rejects() (+5 more)

### Community 28 - "PCP_SEAMS — the frozen interface for Proof-Carrying Prose (ADR-0033, phase P0)"
Cohesion: 0.15
Nodes (12): Certificate (`<page>.md` → `<page>.md.cert.json`, alongside the page), CLI, Contracts (`contracts.json` in the wiki dir), File ownership matrix (nobody edits another lane's files), How each lane starts (all depend ONLY on P0 = T-1dc9), Marks (lane C output; also the golden `marks.json`), PCP_SEAMS — the frozen interface for Proof-Carrying Prose (ADR-0033, phase P0), Pipeline hooks (lane A wires; signatures frozen) (+4 more)

### Community 29 - "encode"
Cohesion: 0.19
Nodes (26): Load a certificate from disk. Raises ValueError on malformed JSON (fail-closed f, read_certificate(), _cert(), _chained(), _claim(), Path, `isidore recertify`: repair a certificate the code outgrew, and refuse to repair, A parent page resting on svc.md through a wiki:// chain, with the child hash rec (+18 more)

### Community 30 - "Mark"
Cohesion: 0.13
Nodes (19): check(), explain(), is_plain(), PlainRule, Pattern, Plain-language gate: can a reader who has never seen code use this sentence?  Do, Human-readable reason for a rejection, for the run summary and the journal., One named check. `kind` mirrors Vale's rule taxonomy so the intent of each is de (+11 more)

### Community 31 - "write_items"
Cohesion: 0.13
Nodes (20): parse_stored_predicate(), Parse a predicate read back from a CERTIFICATE rather than from model output., _child_digest(), _cmd_recertify(), _level(), PageRecert, Path, `isidore recertify` — re-run the claim oracles over unchanged prose and rewrite (+12 more)

### Community 32 - "isidore"
Cohesion: 0.13
Nodes (14): Bring your own graph, Config (`isidore.json`, optional), Design rules, isidore, Languages, License, One range, three readers, Proof-carrying prose — how to read a certified page (+6 more)

### Community 33 - "auth.py"
Cohesion: 0.29
Nodes (6): authenticate(), Auth service fixture for PCP lane tests. Line numbers are load-bearing: the gold, Verify the caller's JWT and enforce the attempt ceiling., Token service fixture for PCP lane tests. verify_jwt is defined on L5 (cited by, Return the decoded claims if the token's signature checks out, else None., verify_jwt()

### Community 35 - "scan"
Cohesion: 0.14
Nodes (22): _looks_like_secret(), Path, Lane C — deterministic security detectors: entropy, sinks, topology. 0 LLM. (T-e, Files reachable from an auth/secret/crypto root via imports (BFS, file-level). 0, Run all three detector families over the repo -> deterministic marks. Pure, 0-LL, Shannon entropy per character (bits). Stdlib only., Return a reason if the literal is credential-shaped, else None., Repo-relative source files to scan: the graph's, or a bounded walk if the graph (+14 more)

### Community 36 - "assemble_context"
Cohesion: 0.23
Nodes (14): _cmd_export_agora(), build_cards(), Path, export-agora — bridge isidore's verified claims into Living-Library card DRAFTS, Return [(filename, content)] draft cards — one per wiki page with enough OK clai, render_card(), _slug(), write_cards() (+6 more)

### Community 37 - "GenerationError"
Cohesion: 0.19
Nodes (22): check_claims(), Re-hash every stored claim's evidence — the zero-LLM staleness audit.      Ret, answer_knowledge_offline(), answer_offline(), ask(), ask_knowledge(), gather_claims(), gather_evidence() (+14 more)

### Community 38 - "ClaimVerdict"
Cohesion: 0.22
Nodes (19): extract_surface(), python_surface(), Exact surface of one Python source text, or None if it does not parse.      No, Surface of one file's text, routed by extension. None = not comparable source., _by_name(), API surface extraction: qualified names, signatures as change keys, and the fold, test_extract_surface_returns_none_for_non_code(), test_generic_surface_disambiguates_same_named_methods_of_different_classes() (+11 more)

### Community 39 - "test_wiki_dir_env.py"
Cohesion: 0.31
Nodes (7): ISIDORE_WIKI_DIR redirects the compiled-wiki output directory.  WIKI_DIRNAME is, A nested WIKI_DIRNAME (e.g. doc/isidore) must create its parents, not crash., _reload_render(), test_save_state_creates_nested_wiki_dir(), test_wiki_dirname_blank_env_falls_back(), test_wiki_dirname_defaults_to_wiki(), test_wiki_dirname_honors_env()

### Community 40 - "test_reconcile.py"
Cohesion: 0.09
Nodes (37): append_run(), Compile journal + per-page changelog — residue mining, all zero-LLM.  Every comp, Map each `## heading` to its body text (content before the first heading is keye, (H2 headings whose content changed / were added / removed, new_line_count - old_, Append an H2-level changelog entry to a page's state (capped). No-op if the pros, record_page_change(), section_diff(), _sections() (+29 more)

### Community 41 - "test_humanpack.py"
Cohesion: 0.27
Nodes (11): _cert_digest(), certificate_status(), _cmd_verify(), _ctx_for(), Path, Check a page against its sidecar certificate, offline, 0 LLM (invariant I11)., sha256 of a page's certificate file, "" if it is gone., (ok, cert) for one page. ok is False on any tamper/mismatch/missing-graph. (+3 more)

### Community 42 - "src-isidore.md"
Cohesion: 0.12
Nodes (25): Certificate, certificate_to_dict(), ClaimVerdict, prose_hash(), One claim's line in a certificate: the anchored claim + its typed verdict (if an, The re-verifiable sidecar for one page. Persisted as JSON (machine-read). Tamper, The tamper-evidence anchor: sha256 of the page prose (full hex, this is a machin, Certificate -> plain dict (asdict handles the nested dataclasses). The JSON on d (+17 more)

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
Cohesion: 0.20
Nodes (9): DeltaEntry, _llm_entries(), One typed novelty row. `file` is always the path as of `until` (renames map old, The machine/agent view: one table per area, product surface first., What the model is allowed to write about: product surface, and only what can be, render_whatsnew_toon(), _rows(), SurfaceDelta (+1 more)

### Community 55 - "load_state"
Cohesion: 0.10
Nodes (20): parse_predicate(), parse_wiki_uri(), Path, Load promoted contracts (empty list if the file is absent). Malformed -> ValueEr, Persist contracts as JSON (machine-read gate input)., wiki://<page>#<claim-id> -> (page, claim_id), or None if it is not a wiki URI., Parse "<kind>:<a>;<b>" -> Predicate, or None if absent/malformed/unknown-kind., read_contracts() (+12 more)

### Community 56 - "render_whatsnew_md"
Cohesion: 0.44
Nodes (8): load_state(), _git(), Residue-mining units: section diff, compile journal/stats, per-page history, cla, _repo(), test_claims_for_file_and_grep(), test_findings_new_reports_todos_in_changed_files(), test_journal_and_stats_track_calls_saved_and_unstable(), test_page_history_records_section_changes()

### Community 57 - "test_changeset.py"
Cohesion: 0.39
Nodes (8): compile_subsystems(), Compile the N2 layer: one bounded call per area, each page chained to its module, subsystem_page_name(), _nodes(), test_an_area_page_is_chained_to_the_module_pages_below_it(), test_an_area_with_nothing_proven_under_it_is_skipped_not_invented(), test_the_machine_scheme_never_reaches_a_reader_facing_link(), test_the_product_page_prefers_the_layer_directly_below_it()

### Community 58 - "What's new — `HEAD~2..HEAD`"
Cohesion: 0.29
Nodes (6): Every change, in detail, In plain words, Internal surface, Public API, Tests, What's new — `HEAD~2..HEAD`

### Community 59 - "harvest_todos"
Cohesion: 0.13
Nodes (21): _cmd_contracts(), Lane B (part 2) — claim->contract graduation + `isidore contracts`. (T-8dfc)  A, Check every promoted contract against the current graph. Pure, 0-LLM., Add `isidore contracts` (promote / list / check)., Command implementation for `isidore contracts`., register_cli(), verify_contracts(), The result of checking one predicate against an oracle. `value` is TRUE|FALSE|UN (+13 more)

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
Cohesion: 0.14
Nodes (23): _brace(), _doc(), extract(), _js(), _kw_func(), _kw_type(), LanguageSpec, _Pending (+15 more)

### Community 65 - "assemble_context"
Cohesion: 0.19
Nodes (14): format_mark(), generate_security_banner(), certificate_from_dict(), Mark, Proof-Carrying Prose (PCP) — the frozen seam shared by every PCP lane.  This mod, A deterministic security-relevant flag raised BEFORE the LLM call (lane C)., A reconciler finding (lane B): the model's own outputs contradict each other. 0-, Rebuild a Certificate from parsed JSON, reconstructing the nested dataclasses. T (+6 more)

### Community 66 - "compile_subsystems"
Cohesion: 0.50
Nodes (5): _cmd_overview(), _cmd_subsystems(), _load_graph_for(), Add `isidore pyramid` (plan/preview) and `isidore overview` (the N3 product page, register_cli()

### Community 67 - "reconcile"
Cohesion: 0.25
Nodes (3): Ensure reconcile.py does not import pipeline, claims, or verify (frozen boundary, test_pure_reconcile_imports_constraint(), test_reconcile_mark_uncovered()

### Community 68 - "subsystem-tests.md"
Cohesion: 0.40
Nodes (4): How the work is divided, What it depends on, and what depends on it, What this area is responsible for, Where to start reading

### Community 69 - "security_banner"
Cohesion: 0.33
Nodes (6): _module_pages_of(), _norm(), 0-LLM subsystem suggester: group files by top directory (the isidore graph uses, The compiled module pages that belong to one subsystem, keyed by page file name., _seed_subsystems(), _top_dir()

### Community 70 - "render.py"
Cohesion: 0.19
Nodes (15): _blob(), commit_hints(), _git(), _name_status(), Path, Run one git command, argv-style. Any failure is an exception: a changelog built, A ref -> its full commit sha. Raises WhatsnewError if it does not resolve, so a, One file's text at one revision, or None when it is absent or binary. (+7 more)

### Community 71 - "src-isidore-changeset_py.md"
Cohesion: 0.33
Nodes (5): Architecture, Dependencies, How to change safely, Key entry points, Purpose

### Community 72 - "src-isidore-claims_py.md"
Cohesion: 0.33
Nodes (5): Architecture, Dependencies, How to change safely, Key entry points, Purpose

### Community 73 - "src-isidore-cli_py.md"
Cohesion: 0.33
Nodes (5): Architecture, Dependencies, How to change safely, Key entry points, Purpose

### Community 74 - "src-isidore-connectors.md"
Cohesion: 0.33
Nodes (5): Architecture, Dependencies, How to change safely, Key entry points, Purpose

### Community 75 - "src-isidore-detectors_py.md"
Cohesion: 0.33
Nodes (5): Architecture, Dependencies, How to change safely, Key entry points, Purpose

### Community 76 - "src-isidore-findings_py.md"
Cohesion: 0.33
Nodes (5): Architecture, Dependencies, How to change safely, Key entry points, Purpose

### Community 77 - "src-isidore-graph_py.md"
Cohesion: 0.33
Nodes (5): Architecture, Dependencies, How to change safely, Key entry points, Purpose

### Community 78 - "src-isidore-home_py.md"
Cohesion: 0.33
Nodes (5): Architecture, Dependencies, How to change safely, Key entry points, Purpose

### Community 79 - "src-isidore-humanpack_py.md"
Cohesion: 0.33
Nodes (5): Architecture, Dependencies, How to change safely, Key entry points, Purpose

### Community 80 - "src-isidore-knowledge_py.md"
Cohesion: 0.33
Nodes (5): Architecture, Dependencies, How to change safely, Key entry points, Purpose

### Community 81 - "src-isidore-langspec_py.md"
Cohesion: 0.33
Nodes (5): Architecture, Dependencies, How to change safely, Key entry points, Purpose

### Community 82 - "src-isidore-pcp_py.md"
Cohesion: 0.33
Nodes (5): Architecture, Dependencies, How to change safely, Key entry points, Purpose

### Community 83 - "src-isidore-pipeline_py.md"
Cohesion: 0.33
Nodes (5): Architecture, Dependencies, How to change safely, Key entry points, Purpose

### Community 84 - "src-isidore-pyramid_py.md"
Cohesion: 0.33
Nodes (5): Architecture, Dependencies, How to change safely, Key entry points, Purpose

### Community 85 - "src-isidore-qa_py.md"
Cohesion: 0.33
Nodes (5): Architecture, Dependencies, How to change safely, Key entry points, Purpose

### Community 86 - "src-isidore-surface_py.md"
Cohesion: 0.33
Nodes (5): Architecture, Dependencies, How to change safely, Key entry points, Purpose

### Community 87 - "src-isidore-verify_py.md"
Cohesion: 0.33
Nodes (5): Architecture, Dependencies, How to change safely, Key entry points, Purpose

### Community 88 - "src-isidore-whatsnew_py.md"
Cohesion: 0.33
Nodes (5): Architecture, Dependencies, How to change safely, Key entry points, Purpose

### Community 89 - "tests-fixtures-pcp.md"
Cohesion: 0.33
Nodes (5): Architecture, Dependencies, How to change safely, Key entry points, Purpose

### Community 90 - "tests-test_changeset_py.md"
Cohesion: 0.33
Nodes (5): Architecture, Dependencies, How to change safely, Key entry points, Purpose

### Community 91 - "tests-test_detectors_py.md"
Cohesion: 0.33
Nodes (5): Architecture, Dependencies, How to change safely, Key entry points, Purpose

### Community 92 - "tests-test_impact_py.md"
Cohesion: 0.33
Nodes (5): Architecture, Dependencies, How to change safely, Key entry points, Purpose

### Community 93 - "tests-test_mcp_barrier_py.md"
Cohesion: 0.33
Nodes (5): Architecture, Dependencies, How to change safely, Key entry points, Purpose

### Community 94 - "tests-test_overview_py.md"
Cohesion: 0.33
Nodes (5): Architecture, Dependencies, How to change safely, Key entry points, Purpose

### Community 95 - "tests-test_pcp_pipeline_py.md"
Cohesion: 0.33
Nodes (5): Architecture, Dependencies, How to change safely, Key entry points, Purpose

### Community 96 - "tests-test_plain_py.md"
Cohesion: 0.33
Nodes (5): Architecture, Dependencies, How to change safely, Key entry points, Purpose

### Community 97 - "tests-test_pyramid_py.md"
Cohesion: 0.33
Nodes (5): Architecture, Dependencies, How to change safely, Key entry points, Purpose

### Community 98 - "tests-test_reconcile_py.md"
Cohesion: 0.33
Nodes (5): Architecture, Dependencies, How to change safely, Key entry points, Purpose

### Community 99 - "tests-test_residue_py.md"
Cohesion: 0.33
Nodes (5): Architecture, Dependencies, How to change safely, Key entry points, Purpose

### Community 100 - "tests-test_wiki_dir_env_py.md"
Cohesion: 0.33
Nodes (5): Architecture, Dependencies, How to change safely, Key entry points, Purpose

### Community 101 - "create_run_id"
Cohesion: 0.29
Nodes (6): create_run_id(), Sortable, collision-resistant run id (UTC second + millis)., Algorithmically suggest topics from ingested raw items (0-LLM, term frequency ba, suggest_topics(), test_filter_findings_with_src(), test_suggest_topics()

### Community 102 - "subsystem-src.md"
Cohesion: 0.40
Nodes (4): How the work is divided, What it depends on, and what depends on it, What this area is responsible for, Where to start reading

### Community 103 - "v_calls"
Cohesion: 0.25
Nodes (9): Module, _ast_of(), _find_funcdef(), AsyncFunctionDef, FunctionDef, Graph nodes whose symbol label matches `name` (last dotted component tolerated)., calls(caller, callee): the caller symbol's body contains a call to callee. Oracl, _symbol_nodes() (+1 more)

### Community 104 - "clean_sig"
Cohesion: 0.18
Nodes (11): clean_sig(), AsyncFunctionDef, _py_constant(), FunctionDef, _py_signature(), Collapse a declaration header into a stable one-line comparison key, readable as, The parameter list and return annotation, rendered from the AST rather than the, A module-level binding -> (name, `= value`). Config constants are API: a consume (+3 more)

### Community 105 - "build_delta"
Cohesion: 0.15
Nodes (13): build_delta(), _diff_surfaces(), _file_summary(), _is_comparable(), Skip generated wiki output, the graph store, and anything not source code. Compa, A compact roll-up of what a whole added/removed file declares., Typed difference between two surfaces of the same file.      Identity is the qua, The zero-LLM core: a typed API-surface difference between two revisions.      Pr (+5 more)

### Community 106 - "render_whatsnew_md"
Cohesion: 0.25
Nodes (8): impact_summary(), _md_section(), The consequence of this range, in plain words, with zero LLM calls.      A non-t, The page, layered by READER rather than by topic.      The same range has three, render_whatsnew_md(), test_empty_range_is_valid_and_not_an_error(), test_impact_summary_answers_do_i_have_to_do_anything_without_jargon(), test_page_is_layered_so_a_non_technical_reader_can_stop_after_the_top()

### Community 107 - "encode"
Cohesion: 0.29
Nodes (6): Lane E gate — the human pack renders from golden artifacts, is deterministic, an, I12: the renderer must be 0-LLM. Guard it at the source level., test_humanpack_does_not_import_llm(), test_pdf_flag_writes_print_html(), test_render_pack_content(), test_render_pack_is_deterministic()

### Community 108 - "write_scan"
Cohesion: 0.23
Nodes (14): Run the scanner and persist the graph to .isidore/graph.json., write_scan(), build_impact(), _edges(), ImpactReport, Path, isidore impact — the zero-LLM emergent-interaction detector.  Regenerating a nei, render_impact() (+6 more)

### Community 111 - "literal_value"
Cohesion: 0.29
Nodes (7): literal_value(), The literal a constant is bound to, or None when it is not a plain literal., Strip one layer of matching quotes. Applied to BOTH sides of a literal compariso, `value` decided outside Python, via the declaration the scanner already extracte, _unquote(), _value_via_langspec(), test_literal_value_reads_only_comparable_literals()

## Knowledge Gaps
- **258 isolated node(s):** `isidore-wiki`, `Wiki (isidore)`, `Why`, `Quickstart`, `What you get` (+253 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **5 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `IngestOptions` connect `IngestOptions` to `cli.py`, `git_repo.py`, `_tool_read_only`, `mcp.py`?**
  _High betweenness centrality (0.069) - this node is a cross-community bridge._
- **Why does `compile_wiki()` connect `compile_wiki` to `cli.py`, `graph.py`, `read_certificate`, `detectors.py`, `module_of`, `test_claims.py`, `whatsnew.py`, `claims.py`, `VerifyContext`, `test_pcp_pipeline.py`, `knowledge.py`, `encode`, `scan`, `assemble_context`, `GenerationError`, `test_reconcile.py`, `test_humanpack.py`, `src-isidore.md`, `render_whatsnew_md`, `assemble_context`, `write_scan`?**
  _High betweenness centrality (0.047) - this node is a cross-community bridge._
- **Why does `VerifyContext` connect `read_certificate` to `compile_wiki`, `verify.py`, `findings.py`, `test_claims.py`, `whatsnew.py`, `claims.py`, `plan_pages`, `pcp.py`, `write_items`, `scan`, `test_humanpack.py`, `src-isidore.md`, `verify_page`, `load_state`, `test_changeset.py`, `harvest_todos`, `assemble_context`, `render.py`, `v_calls`, `literal_value`?**
  _High betweenness centrality (0.046) - this node is a cross-community bridge._
- **Are the 32 inferred relationships involving `compile_wiki()` (e.g. with `test_compile_stores_claims_and_writes_claims_toon()` and `test_dry_run_still_detects_stale_claims_for_free()`) actually correct?**
  _`compile_wiki()` has 32 INFERRED edges - model-reasoned connections that need verification._
- **Are the 13 inferred relationships involving `VerifyContext` (e.g. with `CompileResult` and `PageSpec`) actually correct?**
  _`VerifyContext` has 13 INFERRED edges - model-reasoned connections that need verification._
- **Are the 15 inferred relationships involving `Predicate` (e.g. with `CertStatus` and `test_a_unique_declaration_can_still_be_refuted()`) actually correct?**
  _`Predicate` has 15 INFERRED edges - model-reasoned connections that need verification._
- **Are the 12 inferred relationships involving `run_whatsnew()` (e.g. with `test_a_false_predicate_is_kept_in_the_certificate_but_never_published()` and `test_a_phantom_path_earns_one_repair_attempt_then_a_visible_quarantine()`) actually correct?**
  _`run_whatsnew()` has 12 INFERRED edges - model-reasoned connections that need verification._