# Graph Report - isidore  (2026-07-26)

## Corpus Check
- 189 files · ~119,975 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1655 nodes · 3702 edges · 124 communities (119 shown, 5 thin omitted)
- Extraction: 85% EXTRACTED · 15% INFERRED · 0% AMBIGUOUS · INFERRED: 573 edges (avg confidence: 0.76)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `b78c8361`
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
- tests-test_langspec_oracle_py.md
- tests-test_llms_txt_py.md
- literal_value
- tests-test_recertify_py.md
- strip_inline_claim_rows
- verify_predicate
- SurfaceSymbol
- test_pcp_pipeline.py
- main
- apply_settings
- ClaimVerdict
- GitRepoConnector
- src-isidore-connect_py.md
- tests-test_connect_cli_py.md
- CertStatus

## God Nodes (most connected - your core abstractions)
1. `compile_wiki()` - 83 edges
2. `VerifyContext` - 62 edges
3. `IngestOptions` - 45 edges
4. `Predicate` - 35 edges
5. `_make_repo()` - 31 edges
6. `run_whatsnew()` - 29 edges
7. `load_graph()` - 27 edges
8. `build_delta()` - 26 edges
9. `compile_overview()` - 25 edges
10. `read_certificate()` - 24 edges

## Surprising Connections (you probably didn't know these)
- `test_three_field_parser_captures_predicate()` --calls--> `parse_claims_block()`  [INFERRED]
  tests/test_verify.py → src/isidore/claims.py
- `test_the_listing_reports_readiness_without_reading_a_secret()` --calls--> `connector_summary()`  [INFERRED]
  tests/test_connect_cli.py → src/isidore/connect.py
- `test_filter_findings_drops_hallucinated_paths()` --calls--> `filter_findings()`  [INFERRED]
  tests/test_units.py → src/isidore/findings.py
- `test_findings_toon_lists_security_first_and_in_summary()` --calls--> `render_findings()`  [INFERRED]
  tests/test_security_prose.py → src/isidore/findings.py
- `test_golden_graph_loads()` --calls--> `load_graph()`  [INFERRED]
  tests/test_pcp_seams.py → src/isidore/graph.py

## Import Cycles
- 1-file cycle: `src/isidore/connectors/__init__.py -> src/isidore/connectors/__init__.py`

## Communities (124 total, 5 thin omitted)

### Community 0 - "cli.py"
Cohesion: 0.12
Nodes (23): Request, _cmd_ask(), _cmd_compile(), _cmd_impact(), _cmd_sync(), isidore — compile an agent-oriented wiki from your codebase's structure graph., Precedence: explicit CLI arg > isidore.json > built-in default., _setting() (+15 more)

### Community 1 - "graph.py"
Cohesion: 0.16
Nodes (22): git_head(), git_listed_files(), _is_binary(), _iter_source_files(), _node_id(), _norm_source_file(), Path, Structure graph: loading, module grouping, and a built-in multi-language scanner (+14 more)

### Community 2 - "compile_wiki"
Cohesion: 0.13
Nodes (42): compile_wiki(), lint_cited_paths(), File-looking paths cited in the prose that do NOT exist in the repo., Run the pipeline. With execute=False no LLM is called and no page is written., agents_md_block(), Insert or replace the delimited block without touching the rest of the file (ide, upsert_agents_block(), _gp() (+34 more)

### Community 3 - "read_certificate"
Cohesion: 0.18
Nodes (12): parse_wiki_uri(), wiki://<page>#<claim-id> -> (page, claim_id), or None if it is not a wiki URI., _chain_verdicts(), _claim_verdict(), Resolve (verdict, state) for a cited claim. Truth comes from the page's certific, Resolve `wiki://` claims through lane D's verifier and compose the child certifi, Resolve a wiki:// chain. Fail-closed: None/invalid/missing -> not TRUE, never cr, _wikichain_verifier() (+4 more)

### Community 4 - "detectors.py"
Cohesion: 0.07
Nodes (24): IngestOptions, Caps and scoping for a run. All limits live here (in code), never in a prompt., check_item_id(), Raise ValueError if `item_id` cannot be addressed by a `src://` URI., F4 (ADR-0032): RSS, Hacker News and web-search — plus the injection defence they, Measured live on hnrss.org at 4000 bytes: truncated XML never parses, and the ol, I6: a failed fetch must not advance anything, or the entries nobody read are ski, A search nobody ran must be reported as not run. 'success, 0 items' would read a (+16 more)

### Community 5 - "verify.py"
Cohesion: 0.20
Nodes (19): Everything a verifier needs, assembled once per page/verify run. Read-only to ve, VerifyContext, _ast_of(), _file_nodes(), _langspec_symbols(), _norm(), defines(file, symbol): the file defines a symbol of that name. Oracles: graph, t, exports(file, symbol): Python has no explicit exports -> same as defines. Non-Py (+11 more)

### Community 6 - "humanpack.py"
Cohesion: 0.12
Nodes (28): _cmd_render(), _esc(), format_mark(), generate_architecture_map(), generate_claims_table(), generate_contracts_section(), generate_glossary(), generate_mass_bar() (+20 more)

### Community 7 - "quickstart.md"
Cohesion: 0.40
Nodes (3): Wiki (isidore), Modules, Wiki (isidore)

### Community 8 - "findings.py"
Cohesion: 0.17
Nodes (25): Build the delta, optionally write the prose, and persist page + certificate., run_whatsnew(), WhatsnewResult, _commit(), _git(), _one_file_repo(), isidore whatsnew: the typed surface delta, its artifact, and the verification di, A repository mirroring the shape of the change that motivated this command: a me (+17 more)

### Community 9 - "module_of"
Cohesion: 0.09
Nodes (40): affected_modules(), changed_lines(), changed_symbols(), _git_diff(), _module_fan_in(), modules_of(), Path, Change-set detection: which graph symbols a git diff touched, and which modules (+32 more)

### Community 10 - "test_claims.py"
Cohesion: 0.06
Nodes (67): anchor_claims(), check_claims(), claim_id(), claims_for_file(), claims_grep(), evidence_hash(), evidence_state(), _hash() (+59 more)

### Community 11 - "home.py"
Cohesion: 0.12
Nodes (37): _cmd_connect(), _cmd_ingest(), connector_summary(), load_config(), Path, `isidore connect` and `isidore ingest` — the CLI face of the connector layer (AD, Add `isidore connect` and `isidore ingest` (registrar loop in cli.main)., A connector's stored config, or {} if absent/corrupt. Never raises. (+29 more)

### Community 12 - "whatsnew.py"
Cohesion: 0.16
Nodes (16): annotate_unverified_paths(), Annotate every cited path that does not exist in the repo, inline and visibly —, _cmd_whatsnew(), generate_prose(), _group_by_module(), parse_plain_block(), _prompt_for_module(), isidore whatsnew — a changelog you can re-verify, instead of one you have to tru (+8 more)

### Community 13 - "build_certificate"
Cohesion: 0.19
Nodes (14): _cap_content(), Cap an item's content to `max_bytes` UTF-8 bytes, cutting on a character boundar, _git(), _make_repo(), F1's two missing commands (`isidore connect`, `isidore ingest`) and the caps the, The gate F1 could never run: configure two repos, ingest, re-ingest for nothing., test_a_cap_that_does_not_bite_changes_nothing(), test_a_corrupt_state_reingests_from_scratch_without_crashing() (+6 more)

### Community 14 - "pyramid.py"
Cohesion: 0.29
Nodes (9): plan_pyramid(), Plan deterministic N2 subsystem + N3 product pages. 0 LLM.      Explicit `pyrami, _graph(), Lane D gate — the pyramid plans from the real graph, uses imports for cohesion,, BUG 1 regression: auto-seed used node['path'/'file'/'name'] (absent) -> []. Must, BUG 2 regression: `links` was ignored. imports edges must yield depends_on., test_autoseed_groups_by_source_file_on_the_real_graph(), test_explicit_config_still_works() (+1 more)

### Community 15 - "claims.py"
Cohesion: 0.10
Nodes (29): coverage_gap_candidates(), Module pages with no inbound link from any test-looking module., assemble_context(), CompileResult, context_hash(), git_log_for(), _match_only(), _match_seed() (+21 more)

### Community 16 - "surface.py"
Cohesion: 0.11
Nodes (27): Exception, _check_url(), fetch(), fetch_json(), FetchError, Bounded HTTP for the direct-API connectors (ADR-0032 F4). stdlib urllib, no depe, A fetch that did not produce a usable body. Carries a reason fit to show a user., Refuse anything that is not plain http(s).      urllib will happily open `file:/ (+19 more)

### Community 17 - "Isidore v2 — Incremental compilation, impact detection & residue mining"
Cohesion: 0.12
Nodes (16): 0 · Why (user directive), 1 · Verified bug diagnoses (2026-07-10, against real code — not reports), 2 · Design principles (unchanged bets, now enforced deeper), 3 · C0 — Scoped compile: `isidore compile --only <sel>[,<sel>…]`, 4 · C1+C2 — Change-driven compile: `isidore compile --changed [--since <ref>]`, 5 · C3 — Impact detection: `isidore impact [--since <ref>] [--md] [--check]` (new, **0 LLM always**), 6 · C4+C5+C6 — Correctness fixes (the right ones), 7 · C7 — Residue mining (all 0-LLM; the "squeeze everything" layer) (+8 more)

### Community 18 - "git_repo.py"
Cohesion: 0.24
Nodes (14): all_connectors(), Connector, get(), _load_plugins(), missing_env(), Protocol, Connector protocol + registry (ADR-0032 F1).  A connector ingests raw items from, Discover third-party connectors once. A broken entry-point warns and is skipped (+6 more)

### Community 19 - "VerifyContext"
Cohesion: 0.11
Nodes (24): Counter, parse_findings_block(), Split a generated page into (clean page, findings rows). Tolerant of malformed l, render_findings(), render_stats(), encode(), encode_table(), _field() (+16 more)

### Community 20 - "IngestOptions"
Cohesion: 0.16
Nodes (12): _git(), _head(), _make_repo(), F1 (ADR-0032): knowledge home + raw store + git-repo connector.  The load-bearin, Regression: a real repo's commit messages carry UTF-8 (accents, emoji). On Windo, test_git_repo_bad_path_warns_not_crashes(), test_git_repo_handles_non_ascii_commit_messages(), test_git_repo_ingest_persists_and_is_idempotent() (+4 more)

### Community 21 - "pipeline.py"
Cohesion: 0.17
Nodes (19): _cmd_suggest_flows(), find_graph(), load_graph(), Resolve the graph source.      Precedence: explicit --graph > this tool's own, explain(), Human-readable reason for a rejection, for the run summary and the journal., _cmd_overview(), _cmd_pyramid() (+11 more)

### Community 22 - "mcp.py"
Cohesion: 0.19
Nodes (9): _allowed(), _JsonRpcClient, McpConnector, Any, Minimal read-only MCP connector (ADR-0032 F3).  The implementation deliberately, Map tool name -> its MCP annotations via tools/list (paginated). Empty if the se, iso_now(), update_cursor() (+1 more)

### Community 23 - "test_pcp_pipeline.py"
Cohesion: 0.06
Nodes (50): _cmd_findings(), _churn(), filter_findings(), finding_id(), findings_new(), harvest_todos(), insert_security_banner(), is_finding_resolved() (+42 more)

### Community 24 - "knowledge.py"
Cohesion: 0.12
Nodes (22): IngestResult, Outcome of one ingest run. `raw_files` are the JSONL files written this run., create_run_id(), Prepend a run summary, keeping the last 20 (newest first)., Sortable, collision-resistant run id (UTC second + millis)., Append items as JSONL to `raw/<run_id>/items.jsonl`; stamp each with its `chash`, record_run(), write_items() (+14 more)

### Community 25 - "plan_pages"
Cohesion: 0.15
Nodes (19): compile_overview(), missing_sections(), Required headings the page does not have. 0 LLM., Turn `wiki://page` into `page` in PROSE, so the links a reader clicks actually r, Compile the plain-language product page (N3). One LLM call, plus at most one rep, relink_wiki_uris(), The N3 product overview: plain language for anyone, resting on claims already pr, The module page above, registered in the wiki state so an area can find it. (+11 more)

### Community 26 - "pcp.py"
Cohesion: 0.17
Nodes (24): Predicate, A decidable assertion parsed from a claim's third field. Frozen: predicates are, parameter_names(), Parameter names in declaration order, or None when they cannot be read with conf, value(name, literal): a module-level assignment `name = literal`. Oracles: AST,, signature(fn, a1, a2, ...): fn's positional parameter names, in order. Oracles:, v_signature(), v_value() (+16 more)

### Community 27 - "_tool_read_only"
Cohesion: 0.16
Nodes (12): _name_looks_mutating(), Fallback heuristic ONLY (not exhaustive): does the tool name contain a mutating, (allowed, reason). Authority order: explicit readOnlyHint/destructiveHint > name, _tool_read_only(), _FakeClient, MCP connector read-only barrier (ADR-0032 F3). Regression for the review of T-db, Stands in for _JsonRpcClient: a server exposing one read tool, one write tool (a, test_destructive_hint_rejects() (+4 more)

### Community 28 - "PCP_SEAMS — the frozen interface for Proof-Carrying Prose (ADR-0033, phase P0)"
Cohesion: 0.15
Nodes (12): Certificate (`<page>.md` → `<page>.md.cert.json`, alongside the page), CLI, Contracts (`contracts.json` in the wiki dir), File ownership matrix (nobody edits another lane's files), How each lane starts (all depend ONLY on P0 = T-1dc9), Marks (lane C output; also the golden `marks.json`), PCP_SEAMS — the frozen interface for Proof-Carrying Prose (ADR-0033, phase P0), Pipeline hooks (lane A wires; signatures frozen) (+4 more)

### Community 29 - "encode"
Cohesion: 0.19
Nodes (28): Load a certificate from disk. Raises ValueError on malformed JSON (fail-closed f, read_certificate(), Re-run the oracles over every certified page. 0 LLM. Writes only with `write=Tru, recertify(), _cert(), _chained(), _claim(), Path (+20 more)

### Community 30 - "Mark"
Cohesion: 0.15
Nodes (17): check(), is_plain(), PlainRule, Pattern, Plain-language gate: can a reader who has never seen code use this sentence?  Do, One named check. `kind` mirrors Vale's rule taxonomy so the intent of each is de, Names of every rule the text breaks. Empty list = nothing disqualifying was foun, _vocabulary() (+9 more)

### Community 31 - "write_items"
Cohesion: 0.16
Nodes (15): parse_stored_predicate(), Parse a predicate read back from a CERTIFICATE rather than from model output., _child_digest(), _cmd_recertify(), _level(), PageRecert, Path, `isidore recertify` — re-run the claim oracles over unchanged prose and rewrite (+7 more)

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
Cohesion: 0.14
Nodes (21): assemble_topic_context(), compile_topics(), data_fence(), knowledge_dir(), load_topics(), Path, The knowledge core: user-defined topics compile + 0-LLM suggest topics (ADR-0032, Algorithmically suggest topics from ingested raw items (0-LLM, term frequency ba (+13 more)

### Community 37 - "GenerationError"
Cohesion: 0.17
Nodes (24): isidore — compile an agent-oriented wiki from your codebase's structure graph., load_knowledge_state(), ±radius lines around a graph `L<n>` location. Tolerates stale files/locations., read_excerpt(), answer_knowledge_offline(), answer_offline(), ask(), ask_knowledge() (+16 more)

### Community 38 - "ClaimVerdict"
Cohesion: 0.22
Nodes (19): extract_surface(), python_surface(), Exact surface of one Python source text, or None if it does not parse.      No, Surface of one file's text, routed by extension. None = not comparable source., _by_name(), API surface extraction: qualified names, signatures as change keys, and the fold, test_extract_surface_returns_none_for_non_code(), test_generic_surface_disambiguates_same_named_methods_of_different_classes() (+11 more)

### Community 39 - "test_wiki_dir_env.py"
Cohesion: 0.31
Nodes (7): ISIDORE_WIKI_DIR redirects the compiled-wiki output directory.  WIKI_DIRNAME is, A nested WIKI_DIRNAME (e.g. doc/isidore) must create its parents, not crash., _reload_render(), test_save_state_creates_nested_wiki_dir(), test_wiki_dirname_blank_env_falls_back(), test_wiki_dirname_defaults_to_wiki(), test_wiki_dirname_honors_env()

### Community 40 - "test_reconcile.py"
Cohesion: 0.21
Nodes (18): _cmd_llms(), _first_sentence(), Path, Deterministic outputs: quickstart.md, index.toon, llms.txt, and the AGENTS.md re, The wiki, in the layout agents are converging on for being handed documentation., Write llms.txt at the repo root — where the convention puts it, so a fetcher fin, Add `isidore llms` (regenerate llms.txt from whatever is compiled). 0 LLM., register_cli() (+10 more)

### Community 41 - "test_humanpack.py"
Cohesion: 0.16
Nodes (21): AST, Check every promoted contract against the current graph. Pure, 0-LLM., verify_contracts(), _cert_digest(), certificate_status(), _cmd_verify(), _ctx_for(), ground_symbols() (+13 more)

### Community 42 - "src-isidore.md"
Cohesion: 0.18
Nodes (16): parse_predicate_field(), Parse a claim's optional third field into a pcp.Predicate (or None). PCP typed-c, prose_hash(), The tamper-evidence anchor: sha256 of the page prose (full hex, this is a machin, build_certificate(), Verify each claim's predicate, classify prose mass, hash the prose -> a re-verif, _anchored(), _ctx() (+8 more)

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
Cohesion: 0.25
Nodes (8): Epoch second a commit must reach to be inside the window, or (None, note) if unb, _window_floor(), A window has to REMOVE something to be a window, and only what it was asked to r, Measured live: agora's manifest under a 24h window listed no commits at all. Cor, A window is only trustworthy if the cases it cannot express SAY so instead of co, test_a_window_excludes_old_commits_without_pruning_the_walk(), test_a_window_that_cannot_be_expressed_reports_instead_of_returning_nothing(), test_a_windowed_manifest_says_it_is_windowed()

### Community 55 - "load_state"
Cohesion: 0.09
Nodes (31): Certificate, certificate_to_dict(), Contract, parse_predicate(), Path, Proof-Carrying Prose (PCP) — the frozen seam shared by every PCP lane.  This mod, The re-verifiable sidecar for one page. Persisted as JSON (machine-read). Tamper, Certificate -> plain dict (asdict handles the nested dataclasses). The JSON on d (+23 more)

### Community 56 - "render_whatsnew_md"
Cohesion: 0.17
Nodes (17): append_run(), Compile journal + per-page changelog — residue mining, all zero-LLM.  Every comp, Map each `## heading` to its body text (content before the first heading is keye, (H2 headings whose content changed / were added / removed, new_line_count - old_, Append an H2-level changelog entry to a page's state (capped). No-op if the pros, record_page_change(), section_diff(), _sections() (+9 more)

### Community 57 - "test_changeset.py"
Cohesion: 0.43
Nodes (7): compile_subsystems(), Compile the N2 layer: one bounded call per area, each page chained to its module, subsystem_page_name(), _nodes(), test_an_area_page_is_chained_to_the_module_pages_below_it(), test_an_area_with_nothing_proven_under_it_is_skipped_not_invented(), test_the_machine_scheme_never_reaches_a_reader_facing_link()

### Community 58 - "What's new — `HEAD~2..HEAD`"
Cohesion: 0.29
Nodes (6): Every change, in detail, In plain words, Internal surface, Public API, Tests, What's new — `HEAD~2..HEAD`

### Community 59 - "harvest_todos"
Cohesion: 0.13
Nodes (20): _cmd_contracts(), Lane B (part 2) — claim->contract graduation + `isidore contracts`. (T-8dfc)  A, Add `isidore contracts` (promote / list / check)., Command implementation for `isidore contracts`., register_cli(), The result of checking one predicate against an oracle. `value` is TRUE|FALSE|UN, undecidable(), Verdict (+12 more)

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
Cohesion: 0.50
Nodes (3): How the pieces fit together, What this is, What you can do with it

### Community 64 - "SurfaceSymbol"
Cohesion: 0.10
Nodes (30): Match, _brace(), _doc(), _js(), _kw_func(), _kw_type(), LanguageSpec, Pattern (+22 more)

### Community 65 - "assemble_context"
Cohesion: 0.21
Nodes (12): certificate_from_dict(), Mark, A deterministic security-relevant flag raised BEFORE the LLM call (lane C)., A reconciler finding (lane B): the model's own outputs contradict each other. 0-, Rebuild a Certificate from parsed JSON, reconstructing the nested dataclasses. T, Violation, Lane B (part 1) — the reconciler: the model's own outputs cross-checked, 0 LLM., Helper to split file:line into (file, line). (+4 more)

### Community 66 - "compile_subsystems"
Cohesion: 0.15
Nodes (17): _as_list(), feed_url(), HackerNewsConnector, parse_hits(), Hacker News connector (ADR-0032 F4): public front-page tags and Algolia searches, (stream, url) for every configured search and listing. Streams are named for wha, Algolia URL for a text search, newest-first so a cursor means something., Algolia URL for a listing tag (front_page, show_hn, ...). (+9 more)

### Community 67 - "reconcile"
Cohesion: 0.25
Nodes (3): Ensure reconcile.py does not import pipeline, claims, or verify (frozen boundary, test_pure_reconcile_imports_constraint(), test_reconcile_mark_uncovered()

### Community 68 - "subsystem-tests.md"
Cohesion: 0.40
Nodes (4): How the work is divided, What it depends on, and what depends on it, What this area is responsible for, Where to start reading

### Community 69 - "security_banner"
Cohesion: 0.13
Nodes (17): build_delta(), impact_summary(), _is_comparable(), _md_section(), Skip generated wiki output, the graph store, and anything not source code. Compa, The zero-LLM core: a typed API-surface difference between two revisions.      Pr, The consequence of this range, in plain words, with zero LLM calls.      A non-t, The page, layered by READER rather than by topic.      The same range has three (+9 more)

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
Cohesion: 0.12
Nodes (16): Map an import to a repo file id if the module resolves inside the repo., Build a structure graph for a repo in ANY language, zero dependencies (see modul, _resolve_import(), scan_repo(), test_scan_repo_is_multilanguage(), test_scan_repo_skips_binary_files(), test_scan_repo_tolerates_unreadable_and_empty(), test_scan_repo_unknown_text_becomes_bare_file_node() (+8 more)

### Community 102 - "subsystem-src.md"
Cohesion: 0.40
Nodes (4): How the work is divided, What it depends on, and what depends on it, What this area is responsible for, Where to start reading

### Community 103 - "v_calls"
Cohesion: 0.50
Nodes (4): Module, _find_funcdef(), AsyncFunctionDef, FunctionDef

### Community 104 - "clean_sig"
Cohesion: 0.18
Nodes (11): clean_sig(), AsyncFunctionDef, _py_constant(), FunctionDef, _py_signature(), Collapse a declaration header into a stable one-line comparison key, readable as, The parameter list and return annotation, rendered from the AST rather than the, A module-level binding -> (name, `= value`). Config constants are API: a consume (+3 more)

### Community 105 - "build_delta"
Cohesion: 0.22
Nodes (15): extract(), _Pending, Extract (symbols, imported-module-names) from one file's source.      symbols:, The LanguageSpec for a file extension (lowercased), or None if we do not extract, spec_for(), _names(), Multi-language scanner: the declarative engine (langspec) and its wiring into sc, test_bodiless_declaration_stays_start_only() (+7 more)

### Community 106 - "render_whatsnew_md"
Cohesion: 0.33
Nodes (5): Architecture, Dependencies, How to change safely, Key entry points, Purpose

### Community 107 - "encode"
Cohesion: 0.33
Nodes (5): Architecture, Dependencies, How to change safely, Key entry points, Purpose

### Community 108 - "write_scan"
Cohesion: 0.18
Nodes (15): _module_pages_of(), overview_facts(), _page_purpose(), Path, The compiled module pages that belong to one subsystem, keyed by page file name., The first sentence of a module page's `## Purpose` — what that module says it is, What one subsystem page is written from: its module pages, what each says it is, Every claim the pages below PROVED, as citable `wiki://page#id` facts.      This (+7 more)

### Community 109 - "tests-test_langspec_oracle_py.md"
Cohesion: 0.33
Nodes (5): Architecture, Dependencies, How to change safely, Key entry points, Purpose

### Community 110 - "tests-test_llms_txt_py.md"
Cohesion: 0.33
Nodes (5): Architecture, Dependencies, How to change safely, Key entry points, Purpose

### Community 111 - "literal_value"
Cohesion: 0.67
Nodes (3): literal_value(), The literal a constant is bound to, or None when it is not a plain literal., test_literal_value_reads_only_comparable_literals()

### Community 112 - "tests-test_recertify_py.md"
Cohesion: 0.33
Nodes (5): Architecture, Dependencies, How to change safely, Key entry points, Purpose

### Community 113 - "strip_inline_claim_rows"
Cohesion: 0.22
Nodes (8): DeltaEntry, _llm_entries(), One typed novelty row. `file` is always the path as of `until` (renames map old, The machine/agent view: one table per area, product surface first., What the model is allowed to write about: product surface, and only what can be, render_whatsnew_toon(), _rows(), SurfaceDelta

### Community 114 - "verify_predicate"
Cohesion: 0.18
Nodes (10): get_verifier(), Protocol, A predicate verifier. MUST be deterministic and 0-LLM. Returns UNDECIDABLE, neve, Dispatch one predicate to its registered verifier. No verifier -> UNDECIDABLE (f, register_verifier(), Verifier, verify_predicate(), Dispatch through the registry (kept local so callers don't import pcp directly). (+2 more)

### Community 115 - "SurfaceSymbol"
Cohesion: 0.18
Nodes (10): One declared symbol of a file, as of one revision of its text.      `qualname`, SurfaceSymbol, _diff_surfaces(), _file_summary(), RuntimeError, Git could not answer, or a ref does not resolve. Fail closed: never guess a rang, A compact roll-up of what a whole added/removed file declares., Typed difference between two surfaces of the same file.      Identity is the qua (+2 more)

### Community 116 - "test_pcp_pipeline.py"
Cohesion: 0.29
Nodes (10): _compile(), _fake_generator(), _fake_generator_with_a_lie(), Path, P-INT gate — the pipeline wiring ties all five PCP lanes together end to end: a, test_compile_writes_a_certificate_with_typed_verdicts(), test_deterministic_mark_forces_the_banner_despite_calm_prose(), test_refuted_claim_is_quarantined_not_published() (+2 more)

### Community 117 - "main"
Cohesion: 0.20
Nodes (10): _cmd_scan(), _cmd_stats(), main(), Invariant I6: a connector that cannot authenticate is skipped BEFORE it can reac, test_an_unknown_connector_is_named_not_ignored(), test_ingest_fails_closed_on_a_missing_env_var(), test_one_broken_connector_does_not_stop_the_others(), test_pcp_subcommands_are_registered() (+2 more)

### Community 118 - "apply_settings"
Cohesion: 0.22
Nodes (9): apply_settings(), parse_setting(), `key=value` -> (key, value). A value that parses as JSON is stored as JSON, so n, Fold `key=value` settings into a config. Repeating a key ACCUMULATES into a list, Invariant I9: a connector's config holds the NAME of an env var, never its value, test_a_credential_shaped_value_is_refused_and_never_written(), test_a_json_shaped_value_keeps_its_type(), test_a_setting_without_an_equals_is_rejected() (+1 more)

### Community 119 - "ClaimVerdict"
Cohesion: 0.32
Nodes (8): ClaimVerdict, One claim's line in a certificate: the anchored claim + its typed verdict (if an, _claim_symbols(), classify_mass(), The code identifiers a claim is about: its predicate args (last dotted component, Per-sentence confidence, 0-LLM: green if a sentence mentions a symbol from a cla, _sentence_split(), test_verified_mass_classifies_sentences()

### Community 120 - "GitRepoConnector"
Cohesion: 0.53
Nodes (3): GitRepoConnector, (item, None) for a changed repo, (None, None) if HEAD is unchanged, (None, warni, Run a git command; return stdout or None on any failure (never raises).

### Community 121 - "src-isidore-connect_py.md"
Cohesion: 0.33
Nodes (5): Architecture, Dependencies, How to change safely, Key entry points, Purpose

### Community 122 - "tests-test_connect_cli_py.md"
Cohesion: 0.33
Nodes (5): Architecture, Dependencies, How to change safely, Key entry points, Purpose

### Community 123 - "CertStatus"
Cohesion: 0.40
Nodes (3): CertStatus, Why a page's certificate does or does not still describe the page. 0 LLM., Drift that re-running the oracles CANNOT repair: the page states it, the code de

## Knowledge Gaps
- **293 isolated node(s):** `isidore-wiki`, `Wiki (isidore)`, `Why`, `Quickstart`, `What you get` (+288 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **5 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `IngestOptions` connect `detectors.py` to `cli.py`, `compile_subsystems`, `home.py`, `build_certificate`, `surface.py`, `git_repo.py`, `IngestOptions`, `mcp.py`, `knowledge.py`, `_tool_read_only`, `GitRepoConnector`?**
  _High betweenness centrality (0.089) - this node is a cross-community bridge._
- **Why does `compile_wiki()` connect `compile_wiki` to `cli.py`, `graph.py`, `verify.py`, `module_of`, `test_claims.py`, `whatsnew.py`, `claims.py`, `VerifyContext`, `pipeline.py`, `test_pcp_pipeline.py`, `encode`, `scan`, `GenerationError`, `test_humanpack.py`, `src-isidore.md`, `load_state`, `render_whatsnew_md`, `assemble_context`, `test_pcp_pipeline.py`?**
  _High betweenness centrality (0.047) - this node is a cross-community bridge._
- **Why does `VerifyContext` connect `verify.py` to `compile_wiki`, `read_certificate`, `findings.py`, `whatsnew.py`, `claims.py`, `pipeline.py`, `plan_pages`, `pcp.py`, `scan`, `test_humanpack.py`, `src-isidore.md`, `load_state`, `test_changeset.py`, `harvest_todos`, `render.py`, `strip_inline_claim_rows`, `verify_predicate`, `SurfaceSymbol`, `CertStatus`?**
  _High betweenness centrality (0.046) - this node is a cross-community bridge._
- **Are the 32 inferred relationships involving `compile_wiki()` (e.g. with `test_compile_stores_claims_and_writes_claims_toon()` and `test_dry_run_still_detects_stale_claims_for_free()`) actually correct?**
  _`compile_wiki()` has 32 INFERRED edges - model-reasoned connections that need verification._
- **Are the 13 inferred relationships involving `VerifyContext` (e.g. with `CompileResult` and `PageSpec`) actually correct?**
  _`VerifyContext` has 13 INFERRED edges - model-reasoned connections that need verification._
- **Are the 27 inferred relationships involving `IngestOptions` (e.g. with `GitRepoConnector` and `HackerNewsConnector`) actually correct?**
  _`IngestOptions` has 27 INFERRED edges - model-reasoned connections that need verification._
- **Are the 15 inferred relationships involving `Predicate` (e.g. with `CertStatus` and `test_a_unique_declaration_can_still_be_refuted()`) actually correct?**
  _`Predicate` has 15 INFERRED edges - model-reasoned connections that need verification._