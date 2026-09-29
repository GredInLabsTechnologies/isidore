# Graph Report - isidore  (2026-09-29)

## Corpus Check
- 214 files · ~143,512 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 2006 nodes · 4494 edges · 132 communities (127 shown, 5 thin omitted)
- Extraction: 97% EXTRACTED · 3% INFERRED · 0% AMBIGUOUS · INFERRED: 156 edges (avg confidence: 0.66)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `4a02d9a2`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- test_handoff.py
- graph.py
- compile_wiki
- findings.py
- IngestOptions
- verify.py
- plan_pages
- quickstart.md
- test_whatsnew.py
- impact.py
- claims.py
- connect.py
- SurfaceSymbol
- qa.py
- test_pyramid.py
- pipeline.py
- ValueError
- Isidore v2 — Incremental compilation, impact detection & residue mining
- surface.py
- mcp.py
- test_connectors_f1.py
- humanpack.py
- test_classification_gate.py
- test_security_prose.py
- test_source_disclosure_gate.py
- compile_overview
- Predicate
- test_mcp_barrier.py
- PCP_SEAMS — the frozen interface for Proof-Carrying Prose (ADR-0033, phase P0)
- read_certificate
- check
- encode
- isidore
- auth.py
- isidore-wiki
- cli.py
- Gmail — instance recipe for the MCP connector
- knowledge.py
- test_surface.py
- test_wiki_dir_env.py
- _JsonRpcClient
- certificate_status
- ClaimVerdict
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
- build_cards
- test_pcp_seams.py
- load_state
- test_hostile_f6.py
- pyramid.py
- langspec.py
- tests-test_surface_py.md
- tests-test_verify_py.md
- tests-test_whatsnew_py.md
- overview.md
- write_scan
- recertify.py
- test_vigil.py
- store.py
- subsystem-tests.md
- build_delta
- whatsnew.py
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
- scan_repo
- subsystem-src.md
- test_connect_cli.py
- configured_wiki_dirname
- Path
- src-isidore-recertify_py.md
- src-isidore-render_py.md
- emit
- tests-test_langspec_oracle_py.md
- tests-test_llms_txt_py.md
- test_pcp_pipeline.py
- tests-test_recertify_py.md
- parse_claims_block
- Slack — instance recipe for the MCP connector
- GenerationError
- test_wiki_not_input.py
- compile_subsystems
- tests-test_connectors_f4_py.md
- generate_prose
- src-isidore-connect_py.md
- tests-test_connect_cli_py.md
- pcp.py
- Contract
- tests-test_connectors_f5_py.md
- tests-test_hostile_f6_py.md
- src-isidore-handoff_py.md
- tests-test_classification_gate_py.md
- tests-test_handoff_py.md
- tests-test_wiki_not_input_py.md
- test_units.py
- repo_with_module_page

## God Nodes (most connected - your core abstractions)
1. `compile_wiki()` - 92 edges
2. `VerifyContext` - 64 edges
3. `IngestOptions` - 54 edges
4. `run_whatsnew()` - 39 edges
5. `Predicate` - 35 edges
6. `_make_repo()` - 31 edges
7. `load_graph()` - 28 edges
8. `read_state()` - 27 edges
9. `main()` - 26 edges
10. `compile_overview()` - 26 edges

## Surprising Connections (you probably didn't know these)
- `test_only_ok_claims_are_exported_by_default()` --calls--> `check_claims()`  [INFERRED]
  tests/test_export.py → src/isidore/claims.py
- `main()` --indirect_call--> `_verify()`  [INFERRED]
  src/isidore/cli.py → tests/test_contracts.py
- `test_a_corrupt_state_reingests_from_scratch_without_crashing()` --calls--> `main()`  [INFERRED]
  tests/test_connect_cli.py → src/isidore/cli.py
- `test_an_unknown_connector_is_named_not_ignored()` --calls--> `main()`  [INFERRED]
  tests/test_connect_cli.py → src/isidore/cli.py
- `test_configure_then_ingest_end_to_end()` --calls--> `main()`  [INFERRED]
  tests/test_connect_cli.py → src/isidore/cli.py

## Import Cycles
- None detected.

## Communities (132 total, 5 thin omitted)

### Community 0 - "test_handoff.py"
Cohesion: 0.12
Nodes (29): apply(), Compile using the written answers. Identical pipeline to any other provider., _answer_all(), _Args, _make_repo(), fixture, Path, `isidore handoff` — the caller is the model, so the source never leaves the… (+21 more)

### Community 1 - "graph.py"
Cohesion: 0.12
Nodes (28): git_head(), git_listed_files(), _is_binary(), _is_wiki_output(), _iter_source_files(), _node_id(), _norm_source_file(), Path (+20 more)

### Community 2 - "compile_wiki"
Cohesion: 0.15
Nodes (38): compile_wiki(), lint_cited_paths(), File-looking paths cited in the prose that do NOT exist in the repo., Run the pipeline. With execute=False no LLM is called and no page is written.…, _gp(), _graph(), _link(), _make_repo() (+30 more)

### Community 3 - "findings.py"
Cohesion: 0.13
Nodes (24): _cmd_findings(), _churn(), _comment_lines(), filter_findings(), finding_id(), findings_new(), is_finding_resolved(), orphan_file_candidates() (+16 more)

### Community 4 - "IngestOptions"
Cohesion: 0.08
Nodes (28): IngestOptions, Caps and scoping for a run. All limits live here (in code), never in a prompt., (content with any delimiter-shaped line defanged, how many were found). Marked…, seal_content(), isolated_home(), fixture, usefixtures, F4 (ADR-0032): RSS, Hacker News and web-search — plus the injection defence… (+20 more)

### Community 5 - "verify.py"
Cohesion: 0.08
Nodes (60): AST, Module, Check every promoted contract against the current graph. Pure, 0-LLM., verify_contracts(), The result of checking one predicate against an oracle. `value` is…, Everything a verifier needs, assembled once per page/verify run. Read-only to…, undecidable(), Verdict (+52 more)

### Community 6 - "plan_pages"
Cohesion: 0.13
Nodes (20): assemble_context(), context_hash(), git_log_for(), _match_only(), PageSpec, plan_pages(), prompt_for(), Path (+12 more)

### Community 7 - "quickstart.md"
Cohesion: 0.33
Nodes (4): Knowledge home (local, not in this repo), Wiki (isidore), Modules, Wiki (isidore)

### Community 8 - "test_whatsnew.py"
Cohesion: 0.10
Nodes (41): RuntimeError, Git could not answer, or a ref does not resolve. Fail closed: never guess a…, Build the delta, optionally write the prose, and persist page + certificate., run_whatsnew(), WhatsnewError, WhatsnewResult, Its prompts carry an excerpt of every added and changed symbol — a compile by…, test_whatsnew_refuses_at_an_undeclared_host() (+33 more)

### Community 9 - "impact.py"
Cohesion: 0.10
Nodes (32): affected_modules(), changed_lines(), changed_symbols(), _git_diff(), _module_fan_in(), modules_of(), Path, Change-set detection: which graph symbols a git diff touched, and which modules… (+24 more)

### Community 10 - "claims.py"
Cohesion: 0.13
Nodes (30): check_claims(), claims_for_file(), claims_grep(), evidence_hash(), evidence_state(), _hash(), _normalize(), Path (+22 more)

### Community 11 - "connect.py"
Cohesion: 0.11
Nodes (36): apply_settings(), _cmd_connect(), _cmd_ingest(), connector_summary(), load_config(), Path, `isidore connect` and `isidore ingest` — the CLI face of the connector layer…, Add `isidore connect` and `isidore ingest` (registrar loop in cli.main). (+28 more)

### Community 12 - "SurfaceSymbol"
Cohesion: 0.20
Nodes (8): One declared symbol of a file, as of one revision of its text. `qualname` is…, SurfaceSymbol, DeltaEntry, _diff_surfaces(), _file_summary(), One typed novelty row. `file` is always the path as of `until` (renames map old…, A compact roll-up of what a whole added/removed file declares., Typed difference between two surfaces of the same file. Identity is the…

### Community 13 - "qa.py"
Cohesion: 0.20
Nodes (21): answer_knowledge_offline(), answer_offline(), ask(), ask_knowledge(), gather_claims(), gather_evidence(), gather_knowledge_claims(), Path (+13 more)

### Community 14 - "test_pyramid.py"
Cohesion: 0.29
Nodes (9): plan_pyramid(), Plan deterministic N2 subsystem + N3 product pages. 0 LLM. Explicit…, _graph(), Lane D gate — the pyramid plans from the real graph, uses imports for cohesion,…, BUG 1 regression: auto-seed used node['path'/'file'/'name'] (absent) -> [].…, BUG 2 regression: `links` was ignored. imports edges must yield depends_on., test_autoseed_groups_by_source_file_on_the_real_graph(), test_explicit_config_still_works() (+1 more)

### Community 15 - "pipeline.py"
Cohesion: 0.07
Nodes (33): Counter, render_findings(), isidore — compile an agent-oriented wiki from your codebase's structure graph.…, append_run(), Compile journal + per-page changelog — residue mining, all zero-LLM. Every…, Map each `## heading` to its body text (content before the first heading is…, (H2 headings whose content changed / were added / removed, new_line_count -…, Append an H2-level changelog entry to a page's state (capped). No-op if the… (+25 more)

### Community 16 - "ValueError"
Cohesion: 0.14
Nodes (15): parse_hits(), The `hits` array, or ValueError. A payload without one is malformed, not empty…, _link(), _local(), parse_feed(), First non-empty child whose local tag is one of `names`, stripped., RSS puts the URL in <link>'s text; Atom puts it in <link href=...>, sometimes…, (feed title, entries) from RSS 2.0 or Atom. Raises ValueError on XML that will… (+7 more)

### Community 17 - "Isidore v2 — Incremental compilation, impact detection & residue mining"
Cohesion: 0.12
Nodes (16): 0 · Why (user directive), 1 · Verified bug diagnoses (2026-07-10, against real code — not reports), 2 · Design principles (unchanged bets, now enforced deeper), 3 · C0 — Scoped compile: `isidore compile --only <sel>[,<sel>…]`, 4 · C1+C2 — Change-driven compile: `isidore compile --changed [--since <ref>]`, 5 · C3 — Impact detection: `isidore impact [--since <ref>] [--md] [--check]` (new, **0 LLM always**), 6 · C4+C5+C6 — Correctness fixes (the right ones), 7 · C7 — Residue mining (all 0-LLM; the "squeeze everything" layer) (+8 more)

### Community 18 - "surface.py"
Cohesion: 0.09
Nodes (27): Match, clean_sig(), _declaration_tail(), generic_surface(), _is_declaration(), _is_public(), logical_lines(), _param_group() (+19 more)

### Community 19 - "mcp.py"
Cohesion: 0.06
Nodes (37): BaseHTTPRequestHandler, _allowed(), McpConnector, Minimal read-only MCP connector (ADR-0032 F3). The implementation deliberately…, Normalise the allowlist into `{entry, arguments}` records, sorted for…, update_cursor(), _config(), fixture (+29 more)

### Community 20 - "test_connectors_f1.py"
Cohesion: 0.13
Nodes (16): GitRepoConnector, (item, None) for a changed repo, (None, None) if HEAD is unchanged, (None,…, Run a git command; return stdout or None on any failure (never raises)., _git(), _head(), _make_repo(), parametrize, F1 (ADR-0032): knowledge home + raw store + git-repo connector. The load-… (+8 more)

### Community 21 - "humanpack.py"
Cohesion: 0.05
Nodes (56): _looks_like_secret(), Path, Lane C — deterministic security detectors: entropy, sinks, topology. 0 LLM.…, Entropy + sink marks for one file. Never raises (unreadable file -> no marks)., Files reachable from an auth/secret/crypto root via imports (BFS, file-level).…, Run all three detector families over the repo -> deterministic marks. Pure,…, Shannon entropy per character (bits). Stdlib only., Return a reason if the literal is credential-shaped, else None. (+48 more)

### Community 22 - "test_classification_gate.py"
Cohesion: 0.23
Nodes (16): home(), _item(), fixture, usefixtures, Ingesting a source does not authorise sending it to a third party. Found by…, The cap is per-item, not per-topic: one restricted item must not blank the…, Seen the moment the gate started withholding: three topics with nothing left to…, A truthy-looking value is not a decision. This one deserves to be made… (+8 more)

### Community 23 - "test_security_prose.py"
Cohesion: 0.13
Nodes (20): insert_security_banner(), is_security_finding(), True if a suspect reads as a security risk (hardcoded secret, auth bypass,…, A prominent, deterministic banner listing this page's security suspects — meant…, Place the banner right under the page's H1 (or at the very top if there is…, security_banner(), security_suspects(), Security escalation: a security suspect forces a loud, deterministic prose… (+12 more)

### Community 24 - "test_source_disclosure_gate.py"
Cohesion: 0.09
Nodes (32): assert_may_send_source(), Classify wherever a compile would send this repository's source, as (kind,…, Fail closed unless the destination may see this repository's content. `what`…, source_destination(), clean_env(), _gp(), _make_repo(), fixture (+24 more)

### Community 25 - "compile_overview"
Cohesion: 0.17
Nodes (17): compile_overview(), missing_sections(), Required headings the page does not have. 0 LLM., Turn `wiki://page` into `page` in PROSE, so the links a reader clicks actually…, Compile the plain-language product page (N3). One LLM call, plus at most one…, relink_wiki_uris(), The N3 product overview: plain language for anyone, resting on claims already…, The invariant the pyramid advertises: break a page below, and the page above… (+9 more)

### Community 26 - "Predicate"
Cohesion: 0.15
Nodes (24): Predicate, A decidable assertion parsed from a claim's third field. Frozen: predicates are…, literal_value(), parameter_names(), Parameter names in declaration order, or None when they cannot be read with…, The literal a constant is bound to, or None when it is not a plain literal.…, signature(fn, a1, a2, ...): fn's positional parameter names, in order. Oracles:…, v_signature() (+16 more)

### Community 27 - "test_mcp_barrier.py"
Cohesion: 0.16
Nodes (13): _name_looks_mutating(), (allowed, reason). Authority order: explicit readOnlyHint/destructiveHint >…, Fallback heuristic ONLY (not exhaustive): does the tool name contain a mutating…, _tool_read_only(), _FakeClient, parametrize, MCP connector read-only barrier (ADR-0032 F3). Regression for the review of…, Stands in for _JsonRpcClient: a server exposing one read tool, one write tool… (+5 more)

### Community 28 - "PCP_SEAMS — the frozen interface for Proof-Carrying Prose (ADR-0033, phase P0)"
Cohesion: 0.15
Nodes (12): Certificate (`<page>.md` → `<page>.md.cert.json`, alongside the page), CLI, Contracts (`contracts.json` in the wiki dir), File ownership matrix (nobody edits another lane's files), How each lane starts (all depend ONLY on P0 = T-1dc9), Marks (lane C output; also the golden `marks.json`), PCP_SEAMS — the frozen interface for Proof-Carrying Prose (ADR-0033, phase P0), Pipeline hooks (lane A wires; signatures frozen) (+4 more)

### Community 29 - "read_certificate"
Cohesion: 0.17
Nodes (31): Load a certificate from disk. Raises ValueError on malformed JSON (fail-closed…, read_certificate(), Re-run the oracles over every certified page. 0 LLM. Writes only with…, recertify(), _cert(), _chained(), _claim(), parametrize (+23 more)

### Community 30 - "check"
Cohesion: 0.13
Nodes (19): check(), explain(), is_plain(), PlainRule, Pattern, Plain-language gate: can a reader who has never seen code use this sentence?…, Human-readable reason for a rejection, for the run summary and the journal., One named check. `kind` mirrors Vale's rule taxonomy so the intent of each is… (+11 more)

### Community 31 - "encode"
Cohesion: 0.22
Nodes (13): _cmd_contracts(), Lane B (part 2) — claim->contract graduation + `isidore contracts`. (T-8dfc) A…, Add `isidore contracts` (promote / list / check)., Command implementation for `isidore contracts`., register_cli(), encode(), encode_table(), _field() (+5 more)

### Community 32 - "isidore"
Cohesion: 0.12
Nodes (16): Bring your own graph, Config (`isidore.json`, optional), Design rules, isidore, Knowledge — the same contract, applied to what is NOT in your repo, Languages, License, One range, three readers (+8 more)

### Community 33 - "auth.py"
Cohesion: 0.32
Nodes (6): authenticate(), Auth service fixture for PCP lane tests. Line numbers are load-bearing: the…, Verify the caller's JWT and enforce the attempt ceiling., Token service fixture for PCP lane tests. verify_jwt is defined on L5 (cited by…, Return the decoded claims if the token's signature checks out, else None., verify_jwt()

### Community 35 - "cli.py"
Cohesion: 0.15
Nodes (24): _cmd_ask(), _cmd_compile(), _cmd_impact(), _cmd_scan(), _cmd_stats(), _cmd_suggest_flows(), main(), isidore — compile an agent-oriented wiki from your codebase's structure graph.… (+16 more)

### Community 36 - "Gmail — instance recipe for the MCP connector"
Cohesion: 0.12
Nodes (14): Gmail — instance recipe for the MCP connector, Sources, The config, The part you should actually worry about, Verifying it works, What it costs you to set up, What you get, Where the caps live (+6 more)

### Community 37 - "knowledge.py"
Cohesion: 0.11
Nodes (32): is_negative_existential(), True for statements asserting existential/definitional ABSENCE (unanchorable).…, Pages owning at least one stale/orphan claim — they must regenerate even if…, stale_pages(), _cmd_sync(), parse_findings_block(), Split a generated page into (clean page, findings rows). Tolerant of malformed…, chmod that never raises; a no-op on Windows where POSIX modes don't apply. (+24 more)

### Community 38 - "test_surface.py"
Cohesion: 0.22
Nodes (19): extract_surface(), python_surface(), Exact surface of one Python source text, or None if it does not parse. None is…, Surface of one file's text, routed by extension. None = not comparable source.…, _by_name(), API surface extraction: qualified names, signatures as change keys, and the…, test_extract_surface_returns_none_for_non_code(), test_generic_surface_disambiguates_same_named_methods_of_different_classes() (+11 more)

### Community 39 - "test_wiki_dir_env.py"
Cohesion: 0.31
Nodes (7): ISIDORE_WIKI_DIR redirects the compiled-wiki output directory. WIKI_DIRNAME is…, A nested WIKI_DIRNAME (e.g. doc/isidore) must create its parents, not crash., _reload_render(), test_save_state_creates_nested_wiki_dir(), test_wiki_dirname_blank_env_falls_back(), test_wiki_dirname_defaults_to_wiki(), test_wiki_dirname_honors_env()

### Community 40 - "_JsonRpcClient"
Cohesion: 0.16
Nodes (9): _JsonRpcClient, Any, Map tool name -> its MCP annotations via tools/list (paginated). Empty if the…, JSON-RPC 2.0 over the two MCP transports (spec 2025-06-18, basic/transports).…, The response to `want_id` if `message` is (or, as a batch, holds) it. Anything…, A server may ask the client something mid-request (`ping`, `roots/list`,…, Read SSE events until the one carrying the reply to `want_id`. Each event's…, The readable text of an MCP tool result, falling back to compact JSON. MCP… (+1 more)

### Community 41 - "certificate_status"
Cohesion: 0.27
Nodes (11): _cert_digest(), certificate_status(), _cmd_verify(), _ctx_for(), Path, Check a page against its sidecar certificate, offline, 0 LLM (invariant I11).…, sha256 of a page's certificate file, "" if it is gone., (ok, cert) for one page. ok is False on any tamper/mismatch/missing-graph. (+3 more)

### Community 42 - "ClaimVerdict"
Cohesion: 0.11
Nodes (29): parse_predicate_field(), Parse a claim's optional third field into a pcp.Predicate (or None). PCP typed-…, ClaimVerdict, prose_hash(), Dispatch one predicate to its registered verifier. No verifier -> UNDECIDABLE…, One claim's line in a certificate: the anchored claim + its typed verdict (if…, The tamper-evidence anchor: sha256 of the page prose (full hex, this is a…, verify_predicate() (+21 more)

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

### Community 54 - "build_cards"
Cohesion: 0.23
Nodes (14): _cmd_export_agora(), build_cards(), Path, export-agora — bridge isidore's verified claims into Living-Library card DRAFTS…, Return [(filename, content)] draft cards — one per wiki page with enough OK…, render_card(), _slug(), write_cards() (+6 more)

### Community 55 - "test_pcp_seams.py"
Cohesion: 0.15
Nodes (16): parse_predicate(), Load promoted contracts (empty list if the file is absent). Malformed ->…, Parse "<kind>:<a>;<b>" -> Predicate, or None if absent/malformed/unknown-kind.…, read_contracts(), parametrize, P0 gate (ADR-0033) — the frozen PCP seam parses its golden fixtures and exposes…, The frozen signatures exist and return the seam's types (whether stub or…, test_golden_certificate_round_trips() (+8 more)

### Community 56 - "load_state"
Cohesion: 0.44
Nodes (8): load_state(), _git(), Residue-mining units: section diff, compile journal/stats, per-page history,…, _repo(), test_claims_for_file_and_grep(), test_findings_new_reports_todos_in_changed_files(), test_journal_and_stats_track_calls_saved_and_unstable(), test_page_history_records_section_changes()

### Community 57 - "test_hostile_f6.py"
Cohesion: 0.20
Nodes (20): home(), _item(), fixture, usefixtures, F6's hostile gate: what the knowledge home does when its own data is broken,…, A cap that bites silently turns a partial answer into a confident one., The whole point of I8, end to end: an item that issues commands and forges a…, The second half of the defence: even if a forged URI reaches a claim, it has to… (+12 more)

### Community 58 - "pyramid.py"
Cohesion: 0.24
Nodes (12): _cmd_overview(), _cmd_pyramid(), _cmd_subsystems(), _load_graph_for(), _norm(), Lane D — the pyramid: hierarchical synthesis with wiki:// claim chains. (T-af65…, 0-LLM subsystem suggester: group files by top directory (the isidore graph uses…, Add `isidore pyramid` (plan/preview) and `isidore overview` (the N3 product… (+4 more)

### Community 59 - "langspec.py"
Cohesion: 0.14
Nodes (23): _brace(), _doc(), extract(), _js(), _kw_func(), _kw_type(), LanguageSpec, _Pending (+15 more)

### Community 60 - "tests-test_surface_py.md"
Cohesion: 0.33
Nodes (5): Architecture, Dependencies, How to change safely, Key entry points, Purpose

### Community 61 - "tests-test_verify_py.md"
Cohesion: 0.33
Nodes (5): Architecture, Dependencies, How to change safely, Key entry points, Purpose

### Community 62 - "tests-test_whatsnew_py.md"
Cohesion: 0.33
Nodes (5): Architecture, Dependencies, How to change safely, Key entry points, Purpose

### Community 63 - "overview.md"
Cohesion: 0.50
Nodes (3): How the pieces fit together, What this is, What you can do with it

### Community 64 - "write_scan"
Cohesion: 0.44
Nodes (8): Run the scanner and persist the graph to .isidore/graph.json., write_scan(), _git(), isidore impact — the 0-LLM emergent-interaction detector, over a real git repo…, _seed_repo(), test_impact_check_exit_signal_and_clean(), test_impact_reports_a_new_cross_module_edge_as_emergent(), test_impact_reports_a_removed_edge()

### Community 65 - "recertify.py"
Cohesion: 0.07
Nodes (40): cert_file_digest(), Certificate, certificate_to_dict(), parse_stored_predicate(), parse_wiki_uri(), Path, Parse a predicate read back from a CERTIFICATE rather than from model output.…, The re-verifiable sidecar for one page. Persisted as JSON (machine-read).… (+32 more)

### Community 66 - "test_vigil.py"
Cohesion: 0.22
Nodes (8): Verify that negation patterns do not trigger false positive security findings…, Verify that safety-checks catch risks even with intermediate/intervening words., If the model attempts social engineering in prose while findings report the…, Vigil case: A camouflaged auth backdoor reported in findings but justified by…, test_adversarial_backdoor_detection(), test_false_negative_intervening_words(), test_negations_false_positives(), test_vigil_impossible_to_clean_by_model()

### Community 67 - "store.py"
Cohesion: 0.07
Nodes (68): Exception, IngestResult, Outcome of one ingest run. `raw_files` are the JSONL files written this run., A connector's persisted config, or {} if absent or corrupt. Never raises. Lives…, stored_config(), git-repo connector (ADR-0032 F1): local repositories as a knowledge source. No…, _as_list(), feed_url() (+60 more)

### Community 68 - "subsystem-tests.md"
Cohesion: 0.40
Nodes (4): How the work is divided, What it depends on, and what depends on it, What this area is responsible for, Where to start reading

### Community 69 - "build_delta"
Cohesion: 0.13
Nodes (19): build_delta(), impact_summary(), _md_section(), The zero-LLM core: a typed API-surface difference between two revisions.…, The consequence of this range, in plain words, with zero LLM calls. A non-…, The machine/agent view: one table per area, product surface first., The page, layered by READER rather than by topic. The same range has three…, render_whatsnew_md() (+11 more)

### Community 70 - "whatsnew.py"
Cohesion: 0.14
Nodes (24): _blob(), _cmd_whatsnew(), commit_hints(), _git(), _is_comparable(), _name_status(), _prompt_for_module(), Path (+16 more)

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

### Community 101 - "scan_repo"
Cohesion: 0.14
Nodes (19): python_import_roots(), Directories an absolute Python import is resolved from: the repo root, plus the…, Map an import to a repo file id if the module resolves inside the repo.…, Build a structure graph for a repo in ANY language, zero dependencies (see…, _resolve_import(), scan_repo(), _names(), Multi-language scanner: the declarative engine (langspec) and its wiring into… (+11 more)

### Community 102 - "subsystem-src.md"
Cohesion: 0.40
Nodes (4): How the work is divided, What it depends on, and what depends on it, What this area is responsible for, Where to start reading

### Community 103 - "test_connect_cli.py"
Cohesion: 0.09
Nodes (37): parse_setting(), `key=value` -> (key, value). A value that parses as JSON is stored as JSON, so…, _cap_content(), Epoch second a commit must reach to be inside the window, or (None, note) if…, Cap an item's content to `max_bytes` UTF-8 bytes, cutting on a character…, _window_floor(), _git(), isolated_home() (+29 more)

### Community 104 - "configured_wiki_dirname"
Cohesion: 0.09
Nodes (38): _cmd_llms(), configured_wiki_dirname(), _first_sentence(), Path, The wiki, in the layout agents are converging on for being handed…, Write llms.txt at the repo root — where the convention puts it, so a fetcher…, Where this repository keeps its living docs, relative to its root. Precedence:…, Add `isidore llms` (regenerate llms.txt from whatever is compiled). 0 LLM. (+30 more)

### Community 105 - "Path"
Cohesion: 0.20
Nodes (14): _module_pages_of(), overview_facts(), _page_purpose(), Path, The compiled module pages that belong to one subsystem, keyed by page file name., The first sentence of a module page's `## Purpose` — what that module says it…, What one subsystem page is written from: its module pages, what each says it is…, Every claim the pages below PROVED, as citable `wiki://page#id` facts. This is… (+6 more)

### Community 106 - "src-isidore-recertify_py.md"
Cohesion: 0.33
Nodes (5): Architecture, Dependencies, How to change safely, Key entry points, Purpose

### Community 107 - "src-isidore-render_py.md"
Cohesion: 0.33
Nodes (5): Architecture, Dependencies, How to change safely, Key entry points, Purpose

### Community 108 - "emit"
Cohesion: 0.18
Nodes (20): _cmd_handoff(), emit(), handoff_dir(), _plan(), prompt_id(), Path, `isidore handoff` — let the CALLER be the model, instead of shipping the code…, Add `isidore handoff emit|apply` (registrar loop in cli.main). (+12 more)

### Community 109 - "tests-test_langspec_oracle_py.md"
Cohesion: 0.33
Nodes (5): Architecture, Dependencies, How to change safely, Key entry points, Purpose

### Community 110 - "tests-test_llms_txt_py.md"
Cohesion: 0.33
Nodes (5): Architecture, Dependencies, How to change safely, Key entry points, Purpose

### Community 111 - "test_pcp_pipeline.py"
Cohesion: 0.29
Nodes (10): _compile(), _fake_generator(), _fake_generator_with_a_lie(), Path, P-INT gate — the pipeline wiring ties all five PCP lanes together end to end: a…, test_compile_writes_a_certificate_with_typed_verdicts(), test_deterministic_mark_forces_the_banner_despite_calm_prose(), test_refuted_claim_is_quarantined_not_published() (+2 more)

### Community 112 - "tests-test_recertify_py.md"
Cohesion: 0.33
Nodes (5): Architecture, Dependencies, How to change safely, Key entry points, Purpose

### Community 113 - "parse_claims_block"
Cohesion: 0.13
Nodes (26): anchor_claims(), claim_id(), parse_claims_block(), Split a generated page into (clean page, raw claim rows). Tolerant of malformed…, Deterministic, ledger-friendly id: stable across runs for the same (statement,…, Repair a shortened citation to a real file, or None if it can't be resolved…, Quarantine filter + anchoring. Returns (anchored claims, dropped, repaired). A…, resolve_citation() (+18 more)

### Community 114 - "Slack — instance recipe for the MCP connector"
Cohesion: 0.20
Nodes (9): Confirm the tool names before you trust this block, Setup, Slack — instance recipe for the MCP connector, Sources, The config, The part you should actually worry about, Verifying it works, What you get (+1 more)

### Community 115 - "GenerationError"
Cohesion: 0.21
Nodes (11): Request, build_request(), generate(), generate_via_cli(), GenerationError, RuntimeError, Single-provider LLM client (OpenAI-compatible), fail-closed by design. One…, The provider failed. No retry with a different model — fail closed. (+3 more)

### Community 117 - "test_wiki_not_input.py"
Cohesion: 0.15
Nodes (14): _Cert, nested_wiki_dir(), fixture, usefixtures, The wiki is OUTPUT. It must never round-trip into the input. Reported from GIMO…, GIMO's actual numbers. Writing this silently is how it reached 13 MB before…, Point the toolchain at GIMO's layout. WIKI_DIRNAME is resolved once at import…, GIMO's shape: the wiki lives several directories deep, at whatever the… (+6 more)

### Community 118 - "compile_subsystems"
Cohesion: 0.29
Nodes (10): _chain_verdicts(), compile_subsystems(), Compile the N2 layer: one bounded call per area, each page chained to its…, Resolve `wiki://` claims through lane D's verifier and compose the child…, subsystem_page_name(), _nodes(), test_an_area_page_is_chained_to_the_module_pages_below_it(), test_an_area_with_nothing_proven_under_it_is_skipped_not_invented() (+2 more)

### Community 119 - "tests-test_connectors_f4_py.md"
Cohesion: 0.33
Nodes (5): Architecture, Dependencies, How to change safely, Key entry points, Purpose

### Community 120 - "generate_prose"
Cohesion: 0.14
Nodes (14): annotate_unverified_paths(), Annotate every cited path that does not exist in the repo, inline and visibly —…, generate_prose(), _group_by_module(), _llm_entries(), parse_plain_block(), Split the plain-language block out of a model answer -> (rest, plain text,…, Drop the pipe-separated citation a model appends to its own bullets. Observed… (+6 more)

### Community 121 - "src-isidore-connect_py.md"
Cohesion: 0.33
Nodes (5): Architecture, Dependencies, How to change safely, Key entry points, Purpose

### Community 122 - "tests-test_connect_cli_py.md"
Cohesion: 0.33
Nodes (5): Architecture, Dependencies, How to change safely, Key entry points, Purpose

### Community 125 - "pcp.py"
Cohesion: 0.15
Nodes (15): certificate_from_dict(), get_verifier(), Protocol, Proof-Carrying Prose (PCP) — the frozen seam shared by every PCP lane. This…, A predicate verifier. MUST be deterministic and 0-LLM. Returns UNDECIDABLE,…, A reconciler finding (lane B): the model's own outputs contradict each other.…, Rebuild a Certificate from parsed JSON, reconstructing the nested dataclasses.…, register_verifier() (+7 more)

### Community 128 - "Contract"
Cohesion: 0.33
Nodes (10): Contract, A typed claim a human promoted to an invariant. `isidore verify --contracts`…, _contract_repo(), Path, The PCP fixture repo with one promoted contract and no pages: only the contract…, test_verify_contracts_blocks_when_it_cannot_check(), test_verify_contracts_malformed_predicate(), test_verify_contracts_passes_a_kept_invariant() (+2 more)

### Community 130 - "tests-test_connectors_f5_py.md"
Cohesion: 0.33
Nodes (5): Architecture, Dependencies, How to change safely, Key entry points, Purpose

### Community 132 - "tests-test_hostile_f6_py.md"
Cohesion: 0.33
Nodes (5): Architecture, Dependencies, How to change safely, Key entry points, Purpose

### Community 133 - "src-isidore-handoff_py.md"
Cohesion: 0.33
Nodes (5): Architecture, Dependencies, How to change safely, Key entry points, Purpose

### Community 134 - "tests-test_classification_gate_py.md"
Cohesion: 0.33
Nodes (5): Architecture, Dependencies, How to change safely, Key entry points, Purpose

### Community 135 - "tests-test_handoff_py.md"
Cohesion: 0.33
Nodes (5): Architecture, Dependencies, How to change safely, Key entry points, Purpose

### Community 136 - "tests-test_wiki_not_input_py.md"
Cohesion: 0.33
Nodes (5): Architecture, Dependencies, How to change safely, Key entry points, Purpose

### Community 138 - "test_units.py"
Cohesion: 0.11
Nodes (22): coverage_gap_candidates(), harvest_todos(), TODO/FIXME/HACK/XXX with file:line — regex over the COMMENTS of the files the…, Module pages with no inbound link from any test-looking module., _git_repo(), _qa_repo(), Unit tests: toon encoder, graph scanner, findings residue, QA retrieval, LLM…, A third-party graph (e.g. Graphify) that indexed a gitignored path gets cleaned… (+14 more)

### Community 139 - "repo_with_module_page"
Cohesion: 0.67
Nodes (3): fixture, The module page above, registered in the wiki state so an area can find it., repo_with_module_page()

## Knowledge Gaps
- **342 isolated node(s):** `isidore-wiki`, `Knowledge home (local, not in this repo)`, `Why`, `Quickstart`, `What you get` (+337 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **5 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `IngestOptions` connect `IngestOptions` to `store.py`, `cli.py`, `knowledge.py`, `test_connect_cli.py`, `_JsonRpcClient`, `claims.py`, `connect.py`, `mcp.py`, `test_connectors_f1.py`, `test_hostile_f6.py`, `test_mcp_barrier.py`?**
  _High betweenness centrality (0.089) - this node is a cross-community bridge._
- **Why does `compile_wiki()` connect `compile_wiki` to `test_handoff.py`, `graph.py`, `findings.py`, `verify.py`, `plan_pages`, `impact.py`, `claims.py`, `test_units.py`, `qa.py`, `pipeline.py`, `humanpack.py`, `test_security_prose.py`, `test_source_disclosure_gate.py`, `read_certificate`, `cli.py`, `knowledge.py`, `certificate_status`, `ClaimVerdict`, `build_cards`, `load_state`, `write_scan`, `recertify.py`, `emit`, `test_pcp_pipeline.py`, `parse_claims_block`, `GenerationError`, `generate_prose`, `pcp.py`?**
  _High betweenness centrality (0.049) - this node is a cross-community bridge._
- **Why does `VerifyContext` connect `verify.py` to `Contract`, `compile_wiki`, `plan_pages`, `test_whatsnew.py`, `SurfaceSymbol`, `pipeline.py`, `humanpack.py`, `compile_overview`, `Predicate`, `encode`, `certificate_status`, `ClaimVerdict`, `test_pcp_seams.py`, `pyramid.py`, `recertify.py`, `build_delta`, `whatsnew.py`, `emit`, `compile_subsystems`, `pcp.py`?**
  _High betweenness centrality (0.035) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `compile_wiki()` (e.g. with `test_a_page_with_no_usable_certificate_never_stampedes_a_recompile()` and `test_compile_now_owns_only_the_drift_that_needs_prose()`) actually correct?**
  _`compile_wiki()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Are the 7 inferred relationships involving `VerifyContext` (e.g. with `CompileResult` and `PageSpec`) actually correct?**
  _`VerifyContext` has 7 INFERRED edges - model-reasoned connections that need verification._
- **Are the 9 inferred relationships involving `IngestOptions` (e.g. with `GitRepoConnector` and `HackerNewsConnector`) actually correct?**
  _`IngestOptions` has 9 INFERRED edges - model-reasoned connections that need verification._
- **What connects `isidore-wiki`, `Knowledge home (local, not in this repo)`, `Why` to the rest of the system?**
  _342 weakly-connected nodes found - possible documentation gaps or missing edges._