# Graph Report - isidore  (2026-07-26)

## Corpus Check
- 164 files · ~98,887 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1344 nodes · 2924 edges · 103 communities (98 shown, 5 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 415 edges (avg confidence: 0.77)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `a60216c6`
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

## God Nodes (most connected - your core abstractions)
1. `compile_wiki()` - 80 edges
2. `VerifyContext` - 53 edges
3. `_make_repo()` - 31 edges
4. `run_whatsnew()` - 29 edges
5. `load_graph()` - 26 edges
6. `build_delta()` - 26 edges
7. `compile_overview()` - 24 edges
8. `Predicate` - 23 edges
9. `IngestOptions` - 21 edges
10. `load_state()` - 21 edges

## Surprising Connections (you probably didn't know these)
- `test_is_negative_existential_flags_absence_not_behavior()` --calls--> `is_negative_existential()`  [INFERRED]
  tests/test_claims.py → src/isidore/claims.py
- `test_filter_findings_drops_hallucinated_paths()` --calls--> `filter_findings()`  [INFERRED]
  tests/test_units.py → src/isidore/findings.py
- `test_findings_toon_lists_security_first_and_in_summary()` --calls--> `render_findings()`  [INFERRED]
  tests/test_security_prose.py → src/isidore/findings.py
- `test_render_findings_tables_and_summary()` --calls--> `render_findings()`  [INFERRED]
  tests/test_units.py → src/isidore/findings.py
- `test_module_of_normalizes_and_buckets()` --calls--> `module_of()`  [INFERRED]
  tests/test_units.py → src/isidore/graph.py

## Import Cycles
- 1-file cycle: `src/isidore/connectors/__init__.py -> src/isidore/connectors/__init__.py`

## Communities (103 total, 5 thin omitted)

### Community 0 - "cli.py"
Cohesion: 0.14
Nodes (21): _cmd_impact(), _cmd_scan(), _cmd_stats(), _cmd_suggest_flows(), _cmd_sync(), main(), isidore — compile an agent-oriented wiki from your codebase's structure graph., Precedence: explicit CLI arg > isidore.json > built-in default. (+13 more)

### Community 1 - "graph.py"
Cohesion: 0.09
Nodes (38): answer_knowledge_offline(), answer_offline(), ask(), ask_knowledge(), gather_claims(), gather_evidence(), gather_knowledge_claims(), Path (+30 more)

### Community 2 - "compile_wiki"
Cohesion: 0.25
Nodes (20): compile_wiki(), Run the pipeline. With execute=False no LLM is called and no page is written., _gp(), _make_repo(), Path, test_absence_claims_and_findings_dropped_but_behavioral_kept(), test_compile_preserves_crlf_line_endings_in_agents_md(), test_dry_run_reports_dirty_and_never_calls_generator() (+12 more)

### Community 3 - "read_certificate"
Cohesion: 0.10
Nodes (27): Certificate, certificate_to_dict(), Contract, Path, The re-verifiable sidecar for one page. Persisted as JSON (machine-read). Tamper, Certificate -> plain dict (asdict handles the nested dataclasses). The JSON on d, Persist a certificate as pretty JSON (stable key order for byte-deterministic di, Load a certificate from disk. Raises ValueError on malformed JSON (fail-closed f (+19 more)

### Community 4 - "detectors.py"
Cohesion: 0.14
Nodes (22): _looks_like_secret(), Path, Lane C — deterministic security detectors: entropy, sinks, topology. 0 LLM. (T-e, Files reachable from an auth/secret/crypto root via imports (BFS, file-level). 0, Run all three detector families over the repo -> deterministic marks. Pure, 0-LL, Shannon entropy per character (bits). Stdlib only., Return a reason if the literal is credential-shaped, else None., Repo-relative source files to scan: the graph's, or a bounded walk if the graph (+14 more)

### Community 5 - "verify.py"
Cohesion: 0.12
Nodes (42): AST, Module, Check every promoted contract against the current graph. Pure, 0-LLM., verify_contracts(), The result of checking one predicate against an oracle. `value` is TRUE|FALSE|UN, Everything a verifier needs, assembled once per page/verify run. Read-only to ve, undecidable(), Verdict (+34 more)

### Community 6 - "humanpack.py"
Cohesion: 0.10
Nodes (32): _cmd_render(), _esc(), format_mark(), generate_architecture_map(), generate_claims_table(), generate_contracts_section(), generate_glossary(), generate_mass_bar() (+24 more)

### Community 7 - "quickstart.md"
Cohesion: 0.40
Nodes (3): Wiki (isidore), Modules, Wiki (isidore)

### Community 8 - "findings.py"
Cohesion: 0.20
Nodes (13): is_security_finding(), True if a suspect reads as a security risk (hardcoded secret, auth bypass, injec, security_suspects(), Security escalation: a security suspect forces a loud, deterministic prose banne, False-positive regression: a note that CLEARS the code must not raise the banner, False-negative regression: 'hardcoded SERVICE token' has a word between hardcode, test_detects_common_security_vocabulary(), test_detects_the_camouflaged_backdoor() (+5 more)

### Community 9 - "module_of"
Cohesion: 0.11
Nodes (28): affected_modules(), changed_lines(), changed_symbols(), _git_diff(), _module_fan_in(), modules_of(), Path, Change-set detection: which graph symbols a git diff touched, and which modules (+20 more)

### Community 10 - "test_claims.py"
Cohesion: 0.13
Nodes (27): anchor_claims(), claim_id(), parse_claims_block(), Split a generated page into (clean page, raw claim rows). Tolerant of malformed, Deterministic, ledger-friendly id: stable across runs for the same (statement, e, Repair a shortened citation to a real file, or None if it can't be resolved uniq, Quarantine filter + anchoring. Returns (anchored claims, dropped, repaired)., resolve_citation() (+19 more)

### Community 11 - "home.py"
Cohesion: 0.17
Nodes (21): iter_items(), prune_runs(), The raw store: immutable ingested items + per-connector cursor state (ADR-0032 F, Run ids from state (already newest-first); fall back to sorting the raw dir if s, Drop all but the newest `keep` runs, deleting their raw dirs and trimming state., Current state, or a fresh default if missing OR corrupt (I13-style recovery, nev, Atomic write (tmp + os.replace) so a crash mid-write never corrupts the live sta, Yield stored items, newest run first. A corrupt/half-written JSONL line is skipp (+13 more)

### Community 12 - "whatsnew.py"
Cohesion: 0.05
Nodes (87): _blob(), build_delta(), _cmd_whatsnew(), commit_hints(), DeltaEntry, _diff_surfaces(), _file_summary(), generate_prose() (+79 more)

### Community 13 - "build_certificate"
Cohesion: 0.13
Nodes (24): parse_predicate_field(), Parse a claim's optional third field into a pcp.Predicate (or None). PCP typed-c, prose_hash(), The tamper-evidence anchor: sha256 of the page prose (full hex, this is a machin, build_certificate(), _cmd_verify(), _ctx_for(), Path (+16 more)

### Community 14 - "pyramid.py"
Cohesion: 0.29
Nodes (9): plan_pyramid(), Plan deterministic N2 subsystem + N3 product pages. 0 LLM.      Explicit `pyrami, _graph(), Lane D gate — the pyramid plans from the real graph, uses imports for cohesion,, BUG 1 regression: auto-seed used node['path'/'file'/'name'] (absent) -> []. Must, BUG 2 regression: `links` was ignored. imports edges must yield depends_on., test_autoseed_groups_by_source_file_on_the_real_graph(), test_explicit_config_still_works() (+1 more)

### Community 15 - "claims.py"
Cohesion: 0.09
Nodes (27): Counter, coverage_gap_candidates(), orphan_file_candidates(), Code FILE nodes nothing links to — dead-code candidates (entrypoint-looking name, Module pages with no inbound link from any test-looking module., render_findings(), isidore — compile an agent-oriented wiki from your codebase's structure graph., annotate_unverified_paths() (+19 more)

### Community 16 - "surface.py"
Cohesion: 0.05
Nodes (72): Match, _brace(), _doc(), extract(), _js(), _kw_func(), _kw_type(), LanguageSpec (+64 more)

### Community 17 - "Isidore v2 — Incremental compilation, impact detection & residue mining"
Cohesion: 0.12
Nodes (16): 0 · Why (user directive), 1 · Verified bug diagnoses (2026-07-10, against real code — not reports), 2 · Design principles (unchanged bets, now enforced deeper), 3 · C0 — Scoped compile: `isidore compile --only <sel>[,<sel>…]`, 4 · C1+C2 — Change-driven compile: `isidore compile --changed [--since <ref>]`, 5 · C3 — Impact detection: `isidore impact [--since <ref>] [--md] [--check]` (new, **0 LLM always**), 6 · C4+C5+C6 — Correctness fixes (the right ones), 7 · C7 — Residue mining (all 0-LLM; the "squeeze everything" layer) (+8 more)

### Community 18 - "git_repo.py"
Cohesion: 0.23
Nodes (14): all_connectors(), Connector, get(), IngestResult, _load_plugins(), missing_env(), Protocol, Connector protocol + registry (ADR-0032 F1).  A connector ingests raw items from (+6 more)

### Community 19 - "VerifyContext"
Cohesion: 0.23
Nodes (15): plan_pages(), Module pages from the graph: top-K modules holding at least min_symbols code sym, _graph(), _link(), _node(), Compiler pipeline tests — no network: the LLM generator is always injected and c, test_assemble_context_includes_docs_excerpts_deps_and_budget_warning(), test_changed_scopes_to_blast_radius_over_a_real_git_repo() (+7 more)

### Community 20 - "IngestOptions"
Cohesion: 0.14
Nodes (17): IngestOptions, Caps and scoping for a run. All limits live here (in code), never in a prompt., GitRepoConnector, Run a git command; return stdout or None on any failure (never raises)., (item, None) for a changed repo, (None, None) if HEAD is unchanged, (None, warni, iso_now(), _git(), _head() (+9 more)

### Community 21 - "pipeline.py"
Cohesion: 0.18
Nodes (16): _cmd_ask(), find_graph(), Resolve the graph source.      Precedence: explicit --graph > this tool's own, default_generator(), Build the env-configured generator. Fails closed if no model is set., _cmd_overview(), _cmd_pyramid(), _cmd_subsystems() (+8 more)

### Community 22 - "mcp.py"
Cohesion: 0.18
Nodes (10): _allowed(), _JsonRpcClient, McpConnector, Any, Minimal read-only MCP connector (ADR-0032 F3).  The implementation deliberately, Map tool name -> its MCP annotations via tools/list (paginated). Empty if the se, Prepend a run summary, keeping the last 20 (newest first)., record_run() (+2 more)

### Community 23 - "test_pcp_pipeline.py"
Cohesion: 0.29
Nodes (10): _compile(), _fake_generator(), _fake_generator_with_a_lie(), Path, P-INT gate — the pipeline wiring ties all five PCP lanes together end to end: a, test_compile_writes_a_certificate_with_typed_verdicts(), test_deterministic_mark_forces_the_banner_despite_calm_prose(), test_refuted_claim_is_quarantined_not_published() (+2 more)

### Community 24 - "knowledge.py"
Cohesion: 0.12
Nodes (29): is_negative_existential(), True for statements asserting existential/definitional ABSENCE (unanchorable). C, Pages owning at least one stale/orphan claim — they must regenerate even if thei, stale_pages(), Append items as JSONL to `raw/<run_id>/items.jsonl`; stamp each with its `chash`, write_items(), filter_findings(), parse_findings_block() (+21 more)

### Community 25 - "plan_pages"
Cohesion: 0.16
Nodes (17): compile_overview(), missing_sections(), Required headings the page does not have. 0 LLM., Turn `wiki://page` into `page` in PROSE, so the links a reader clicks actually r, Compile the plain-language product page (N3). One LLM call, plus at most one rep, relink_wiki_uris(), The N3 product overview: plain language for anyone, resting on claims already pr, The module page above, registered in the wiki state so an area can find it. (+9 more)

### Community 26 - "pcp.py"
Cohesion: 0.13
Nodes (22): get_verifier(), parse_predicate(), parse_wiki_uri(), Predicate, Protocol, Proof-Carrying Prose (PCP) — the frozen seam shared by every PCP lane.  This mod, A predicate verifier. MUST be deterministic and 0-LLM. Returns UNDECIDABLE, neve, Dispatch one predicate to its registered verifier. No verifier -> UNDECIDABLE (f (+14 more)

### Community 27 - "_tool_read_only"
Cohesion: 0.16
Nodes (12): _name_looks_mutating(), Fallback heuristic ONLY (not exhaustive): does the tool name contain a mutating, (allowed, reason). Authority order: explicit readOnlyHint/destructiveHint > name, _tool_read_only(), _FakeClient, MCP connector read-only barrier (ADR-0032 F3). Regression for the review of T-db, Stands in for _JsonRpcClient: a server exposing one read tool, one write tool (a, test_destructive_hint_rejects() (+4 more)

### Community 28 - "PCP_SEAMS — the frozen interface for Proof-Carrying Prose (ADR-0033, phase P0)"
Cohesion: 0.15
Nodes (12): Certificate (`<page>.md` → `<page>.md.cert.json`, alongside the page), CLI, Contracts (`contracts.json` in the wiki dir), File ownership matrix (nobody edits another lane's files), How each lane starts (all depend ONLY on P0 = T-1dc9), Marks (lane C output; also the golden `marks.json`), PCP_SEAMS — the frozen interface for Proof-Carrying Prose (ADR-0033, phase P0), Pipeline hooks (lane A wires; signatures frozen) (+4 more)

### Community 29 - "encode"
Cohesion: 0.22
Nodes (13): _cmd_contracts(), Lane B (part 2) — claim->contract graduation + `isidore contracts`. (T-8dfc)  A, Add `isidore contracts` (promote / list / check)., Command implementation for `isidore contracts`., register_cli(), encode(), encode_table(), _field() (+5 more)

### Community 30 - "Mark"
Cohesion: 0.13
Nodes (19): check(), explain(), is_plain(), PlainRule, Pattern, Plain-language gate: can a reader who has never seen code use this sentence?  Do, Human-readable reason for a rejection, for the run summary and the journal., One named check. `kind` mirrors Vale's rule taxonomy so the intent of each is de (+11 more)

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
Cohesion: 0.11
Nodes (30): git_head(), git_listed_files(), _is_binary(), _iter_source_files(), _node_id(), _norm_source_file(), Path, Structure graph: loading, module grouping, and a built-in multi-language scanner (+22 more)

### Community 36 - "assemble_context"
Cohesion: 0.23
Nodes (14): _cmd_export_agora(), build_cards(), Path, export-agora — bridge isidore's verified claims into Living-Library card DRAFTS, Return [(filename, content)] draft cards — one per wiki page with enough OK clai, render_card(), _slug(), write_cards() (+6 more)

### Community 37 - "GenerationError"
Cohesion: 0.22
Nodes (14): evidence_hash(), evidence_state(), _hash(), _normalize(), Claims: the atomic, evidence-anchored form of wiki knowledge.  A claim is a sing, Collapse all whitespace runs to single spaces and trim — so re-indentation, trai, Fingerprint of the CITED LINE's normalized content (whole normalized file if no, ok" | "stale" | "orphan" | "superseded" — content-anchored, tolerant of line shi (+6 more)

### Community 38 - "ClaimVerdict"
Cohesion: 0.24
Nodes (9): append_run(), Compile journal + per-page changelog — residue mining, all zero-LLM.  Every comp, Map each `## heading` to its body text (content before the first heading is keye, (H2 headings whose content changed / were added / removed, new_line_count - old_, Append an H2-level changelog entry to a page's state (capped). No-op if the pros, record_page_change(), section_diff(), _sections() (+1 more)

### Community 39 - "test_wiki_dir_env.py"
Cohesion: 0.31
Nodes (7): ISIDORE_WIKI_DIR redirects the compiled-wiki output directory.  WIKI_DIRNAME is, A nested WIKI_DIRNAME (e.g. doc/isidore) must create its parents, not crash., _reload_render(), test_save_state_creates_nested_wiki_dir(), test_wiki_dirname_blank_env_falls_back(), test_wiki_dirname_defaults_to_wiki(), test_wiki_dirname_honors_env()

### Community 40 - "test_reconcile.py"
Cohesion: 0.36
Nodes (9): check_claims(), claims_for_file(), claims_grep(), Path, Re-hash every stored claim's evidence — the zero-LLM staleness audit.      Retur, The documentation contract of a file: every anchored claim whose evidence points, Free-text search over verified atomic facts — answers many questions with 0 LLM, render_claims() (+1 more)

### Community 41 - "test_humanpack.py"
Cohesion: 0.36
Nodes (10): Run the scanner and persist the graph to .isidore/graph.json., write_scan(), build_impact(), Path, _git(), isidore impact — the 0-LLM emergent-interaction detector, over a real git repo +, _seed_repo(), test_impact_check_exit_signal_and_clean() (+2 more)

### Community 42 - "src-isidore.md"
Cohesion: 0.22
Nodes (8): Verify that negation patterns do not trigger false positive security findings (6, Verify that safety-checks catch risks even with intermediate/intervening words., If the model attempts social engineering in prose while findings report the bug,, Vigil case: A camouflaged auth backdoor reported in findings but justified by pr, test_adversarial_backdoor_detection(), test_false_negative_intervening_words(), test_negations_false_positives(), test_vigil_impossible_to_clean_by_model()

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
Cohesion: 0.32
Nodes (8): ClaimVerdict, One claim's line in a certificate: the anchored claim + its typed verdict (if an, _claim_symbols(), classify_mass(), The code identifiers a claim is about: its predicate args (last dotted component, Per-sentence confidence, 0-LLM: green if a sentence mentions a symbol from a cla, _sentence_split(), test_verified_mass_classifies_sentences()

### Community 55 - "load_state"
Cohesion: 0.44
Nodes (8): load_state(), _git(), Residue-mining units: section diff, compile journal/stats, per-page history, cla, _repo(), test_claims_for_file_and_grep(), test_findings_new_reports_todos_in_changed_files(), test_journal_and_stats_track_calls_saved_and_unstable(), test_page_history_records_section_changes()

### Community 56 - "render_whatsnew_md"
Cohesion: 0.33
Nodes (6): _claim_verdict(), Resolve (verdict, state) for a cited claim. Truth comes from the page's certific, Resolve a wiki:// chain. Fail-closed: None/invalid/missing -> not TRUE, never cr, _wikichain_verifier(), BUG 3 regression: a None predicate crashed with AttributeError., test_wikichain_none_does_not_crash()

### Community 57 - "test_changeset.py"
Cohesion: 0.21
Nodes (12): _module_pages_of(), overview_facts(), _page_purpose(), Path, The compiled module pages that belong to one subsystem, keyed by page file name., The first sentence of a module page's `## Purpose` — what that module says it is, What one subsystem page is written from: its module pages, what each says it is, The project's own words about itself — CONTEXT, never evidence (see OVERVIEW_PRO (+4 more)

### Community 58 - "What's new — `HEAD~2..HEAD`"
Cohesion: 0.29
Nodes (6): Every change, in detail, In plain words, Internal surface, Public API, Tests, What's new — `HEAD~2..HEAD`

### Community 59 - "harvest_todos"
Cohesion: 0.16
Nodes (18): _cmd_findings(), _churn(), finding_id(), findings_new(), harvest_todos(), is_finding_resolved(), Path, Side observations ("residue") harvested during compilation — at ~zero marginal c (+10 more)

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
Cohesion: 0.25
Nodes (3): Ensure reconcile.py does not import pipeline, claims, or verify (frozen boundary, test_pure_reconcile_imports_constraint(), test_reconcile_mark_uncovered()

### Community 65 - "assemble_context"
Cohesion: 0.18
Nodes (13): assemble_context(), git_log_for(), lint_cited_paths(), Path, ±radius lines around a graph `L<n>` location. Tolerates stale files/locations., Gather one page's facts. Returns (context, truncation-warnings)., File-looking paths cited in the prose that do NOT exist in the repo., read_excerpt() (+5 more)

### Community 66 - "compile_subsystems"
Cohesion: 0.25
Nodes (11): compile_subsystems(), Compile the N2 layer: one bounded call per area, each page chained to its module, Every claim the pages below PROVED, as citable `wiki://page#id` facts.      This, subsystem_page_name(), verified_claims(), _nodes(), test_an_area_page_is_chained_to_the_module_pages_below_it(), test_an_area_with_nothing_proven_under_it_is_skipped_not_invented() (+3 more)

### Community 67 - "reconcile"
Cohesion: 0.32
Nodes (7): A reconciler finding (lane B): the model's own outputs contradict each other. 0-, Violation, Lane B (part 1) — the reconciler: the model's own outputs cross-checked, 0 LLM., Helper to split file:line into (file, line)., Cross-check prose vs findings vs claims vs marks -> internal contradictions. Pur, reconcile(), _split_evidence()

### Community 68 - "subsystem-tests.md"
Cohesion: 0.40
Nodes (4): How the work is divided, What it depends on, and what depends on it, What this area is responsible for, Where to start reading

### Community 69 - "security_banner"
Cohesion: 0.29
Nodes (7): insert_security_banner(), A prominent, deterministic banner listing this page's security suspects — meant, Place the banner right under the page's H1 (or at the very top if there is none), security_banner(), test_banner_goes_under_the_h1(), test_banner_is_loud_and_lists_evidence(), test_no_banner_without_security_suspects()

### Community 70 - "render.py"
Cohesion: 0.33
Nodes (6): agents_md_block(), Deterministic outputs: quickstart.md, index.toon, and the AGENTS.md reference bl, Insert or replace the delimited block without touching the rest of the file (ide, render_quickstart(), upsert_agents_block(), test_upsert_agents_block_is_idempotent_and_preserves_content()

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
Cohesion: 0.40
Nodes (5): create_run_id(), Sortable, collision-resistant run id (UTC second + millis)., Algorithmically suggest topics from ingested raw items (0-LLM, term frequency ba, suggest_topics(), test_suggest_topics()

### Community 102 - "subsystem-src.md"
Cohesion: 0.40
Nodes (4): How the work is divided, What it depends on, and what depends on it, What this area is responsible for, Where to start reading

## Knowledge Gaps
- **258 isolated node(s):** `isidore-wiki`, `Wiki (isidore)`, `Why`, `Quickstart`, `What you get` (+253 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **5 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `IngestOptions` connect `IngestOptions` to `cli.py`, `git_repo.py`, `_tool_read_only`, `mcp.py`?**
  _High betweenness centrality (0.076) - this node is a cross-community bridge._
- **Why does `compile_wiki()` connect `compile_wiki` to `cli.py`, `graph.py`, `read_certificate`, `detectors.py`, `verify.py`, `module_of`, `test_claims.py`, `build_certificate`, `claims.py`, `VerifyContext`, `pipeline.py`, `test_pcp_pipeline.py`, `knowledge.py`, `write_items`, `scan`, `assemble_context`, `ClaimVerdict`, `test_reconcile.py`, `test_humanpack.py`, `load_state`, `harvest_todos`, `assemble_context`, `reconcile`, `security_banner`, `render.py`?**
  _High betweenness centrality (0.049) - this node is a cross-community bridge._
- **Why does `VerifyContext` connect `verify.py` to `compile_wiki`, `compile_subsystems`, `detectors.py`, `read_certificate`, `whatsnew.py`, `build_certificate`, `claims.py`, `pipeline.py`, `render_whatsnew_md`, `plan_pages`, `pcp.py`, `encode`?**
  _High betweenness centrality (0.044) - this node is a cross-community bridge._
- **Are the 30 inferred relationships involving `compile_wiki()` (e.g. with `test_compile_stores_claims_and_writes_claims_toon()` and `test_dry_run_still_detects_stale_claims_for_free()`) actually correct?**
  _`compile_wiki()` has 30 INFERRED edges - model-reasoned connections that need verification._
- **Are the 12 inferred relationships involving `VerifyContext` (e.g. with `CompileResult` and `PageSpec`) actually correct?**
  _`VerifyContext` has 12 INFERRED edges - model-reasoned connections that need verification._
- **Are the 12 inferred relationships involving `run_whatsnew()` (e.g. with `test_a_false_predicate_is_kept_in_the_certificate_but_never_published()` and `test_a_phantom_path_earns_one_repair_attempt_then_a_visible_quarantine()`) actually correct?**
  _`run_whatsnew()` has 12 INFERRED edges - model-reasoned connections that need verification._
- **Are the 7 inferred relationships involving `load_graph()` (e.g. with `_ctx()` and `test_golden_graph_loads()`) actually correct?**
  _`load_graph()` has 7 INFERRED edges - model-reasoned connections that need verification._