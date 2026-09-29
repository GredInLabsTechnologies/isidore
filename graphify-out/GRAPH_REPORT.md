# Graph Report - isidore  (2026-09-29)

## Corpus Check
- 230 files · ~168,086 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 2162 nodes · 4875 edges · 139 communities (133 shown, 6 thin omitted)
- Extraction: 97% EXTRACTED · 3% INFERRED · 0% AMBIGUOUS · INFERRED: 164 edges (avg confidence: 0.66)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `c0fff515`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- test_handoff.py
- graph.py
- compile_wiki
- test_units.py
- test_connectors_f4.py
- verify.py
- emit
- quickstart.md
- test_whatsnew.py
- impact.py
- claims.py
- knowledge.py
- build_delta
- qa.py
- citations.py
- test_residue.py
- parse_claims_block
- Isidore v2 — Incremental compilation, impact detection & residue mining
- test_surface.py
- McpConnector
- rss.py
- humanpack.py
- connect.py
- test_security_prose.py
- test_source_disclosure_gate.py
- IngestOptions
- Predicate
- mcp.py
- PCP_SEAMS — the frozen interface for Proof-Carrying Prose (ADR-0033, phase P0)
- read_certificate
- check
- render.py
- isidore
- auth.py
- isidore-wiki
- cli.py
- Gmail — instance recipe for the MCP connector
- assemble_topic_context
- PageSpec
- test_wiki_dir_env.py
- _JsonRpcClient
- test_connect_cli.py
- verify_predicate
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
- test_incremental.py
- compile_overview
- pipeline.py
- _make_repo
- pyramid.py
- langspec.py
- tests-test_surface_py.md
- tests-test_verify_py.md
- tests-test_whatsnew_py.md
- overview.md
- surface.py
- write_certificate
- test_pcp_pipeline.py
- store.py
- subsystem-tests.md
- DeltaEntry
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
- src-isidore-citations_py.md
- configured_wiki_dirname
- tests-test_citations_py.md
- src-isidore-recertify_py.md
- src-isidore-render_py.md
- WhatsnewError
- tests-test_langspec_oracle_py.md
- tests-test_llms_txt_py.md
- test_hostile_f6.py
- tests-test_recertify_py.md
- compile_subsystems
- Slack — instance recipe for the MCP connector
- GenerationError
- pcp.py
- test_wiki_not_input.py
- certificate_status
- tests-test_connectors_f4_py.md
- strip_inline_claim_rows
- src-isidore-connect_py.md
- tests-test_connect_cli_py.md
- test_pyramid.py
- _git_repo
- parse_plain_block
- repo_with_module_page
- _overview_identity
- read_contracts
- src-isidore-revise_py.md
- tests-test_connectors_f5_py.md
- tests-test_incremental_py.md
- tests-test_hostile_f6_py.md
- src-isidore-handoff_py.md
- tests-test_classification_gate_py.md
- tests-test_handoff_py.md
- tests-test_wiki_not_input_py.md
- tests-test_source_disclosure_gate_py.md
- tests-test_wiki_dir_config_py.md

## God Nodes (most connected - your core abstractions)
1. `compile_wiki()` - 112 edges
2. `VerifyContext` - 64 edges
3. `IngestOptions` - 54 edges
4. `run_whatsnew()` - 39 edges
5. `Predicate` - 35 edges
6. `compile_overview()` - 32 edges
7. `_make_repo()` - 31 edges
8. `load_state()` - 29 edges
9. `load_graph()` - 28 edges
10. `main()` - 27 edges

## Surprising Connections (you probably didn't know these)
- `test_cli_reports_a_bad_ref_without_writing_an_artifact()` --calls--> `main()`  [INFERRED]
  tests/test_whatsnew.py → src/isidore/cli.py
- `test_cli_smoke()` --calls--> `main()`  [INFERRED]
  tests/test_whatsnew.py → src/isidore/cli.py
- `test_three_field_parser_captures_predicate()` --calls--> `parse_claims_block()`  [EXTRACTED]
  tests/test_verify.py → src/isidore/claims.py
- `test_every_ingested_item_can_be_cited()` --calls--> `evidence_hash()`  [INFERRED]
  tests/test_connectors_f4.py → src/isidore/claims.py
- `test_the_mail_item_is_citable_end_to_end()` --calls--> `evidence_hash()`  [INFERRED]
  tests/test_connectors_f5.py → src/isidore/claims.py

## Import Cycles
- None detected.

## Communities (139 total, 6 thin omitted)

### Community 0 - "test_handoff.py"
Cohesion: 0.16
Nodes (25): apply(), Compile using the written answers. Identical pipeline to any other provider., _answer_all(), _Args, `isidore handoff` — the caller is the model, so the source never leaves the…, A provider's budget bounds spend. There is no spend here, so a cap would only…, Otherwise the next `apply` certifies a page nobody asked about, from an answer…, The lint gate asks a provider for one repair round. There is nobody to ask here… (+17 more)

### Community 1 - "graph.py"
Cohesion: 0.16
Nodes (22): git_head(), git_listed_files(), _is_binary(), _iter_source_files(), _node_id(), _norm_source_file(), Path, Structure graph: loading, module grouping, and a built-in multi-language… (+14 more)

### Community 2 - "compile_wiki"
Cohesion: 0.12
Nodes (46): compile_wiki(), context_hash(), lint_cited_paths(), plan_pages(), prompt_for(), Module pages from the graph: top-K modules holding at least min_symbols code…, Content-addressed page identity: same prompt -> nothing to regenerate., File-looking paths cited in the prose that do NOT exist in the repo. (+38 more)

### Community 3 - "test_units.py"
Cohesion: 0.10
Nodes (32): _churn(), _comment_lines(), coverage_gap_candidates(), filter_findings(), finding_id(), harvest_todos(), is_finding_resolved(), orphan_file_candidates() (+24 more)

### Community 4 - "test_connectors_f4.py"
Cohesion: 0.07
Nodes (30): (content with any delimiter-shaped line defanged, how many were found). Marked…, seal_content(), isolated_home(), fixture, usefixtures, F4 (ADR-0032): RSS, Hacker News and web-search — plus the injection defence…, Measured live on hnrss.org at 4000 bytes: truncated XML never parses, and the…, I6: a failed fetch must not advance anything, or the entries nobody read are… (+22 more)

### Community 5 - "verify.py"
Cohesion: 0.08
Nodes (55): AST, Module, The result of checking one predicate against an oracle. `value` is…, Everything a verifier needs, assembled once per page/verify run. Read-only to…, undecidable(), Verdict, VerifyContext, _claim_verdict() (+47 more)

### Community 6 - "emit"
Cohesion: 0.18
Nodes (19): _cmd_handoff(), emit(), handoff_dir(), _plan(), prompt_id(), Path, `isidore handoff` — let the CALLER be the model, instead of shipping the code…, Add `isidore handoff emit|apply` (registrar loop in cli.main). (+11 more)

### Community 7 - "quickstart.md"
Cohesion: 0.33
Nodes (4): Knowledge home (local, not in this repo), Wiki (isidore), Modules, Wiki (isidore)

### Community 8 - "test_whatsnew.py"
Cohesion: 0.11
Nodes (35): Build the delta, optionally write the prose, and persist page + certificate., run_whatsnew(), _commit(), _git(), _one_file_repo(), fixture, isidore whatsnew: the typed surface delta, its artifact, and the verification…, A date answers "when did someone run this", which nobody asks. A tag answers… (+27 more)

### Community 9 - "impact.py"
Cohesion: 0.08
Nodes (42): affected_modules(), changed_lines(), changed_symbols(), _git_diff(), _module_fan_in(), modules_of(), Path, Change-set detection: which graph symbols a git diff touched, and which modules… (+34 more)

### Community 10 - "claims.py"
Cohesion: 0.14
Nodes (29): check_claims(), claims_for_file(), claims_grep(), evidence_hash(), evidence_state(), _hash(), _normalize(), Path (+21 more)

### Community 11 - "knowledge.py"
Cohesion: 0.12
Nodes (31): _cmd_sync(), Run ids from state (already newest-first); fall back to sorting the raw dir if…, _run_ids_newest_first(), parse_findings_block(), Split a generated page into (clean page, findings rows). Tolerant of malformed…, connector_dir(), home(), knowledge_dir() (+23 more)

### Community 12 - "build_delta"
Cohesion: 0.12
Nodes (19): build_delta(), _diff_surfaces(), _file_summary(), impact_summary(), _md_section(), A compact roll-up of what a whole added/removed file declares., Typed difference between two surfaces of the same file. Identity is the…, The zero-LLM core: a typed API-surface difference between two revisions.… (+11 more)

### Community 13 - "qa.py"
Cohesion: 0.10
Nodes (28): isidore — compile an agent-oriented wiki from your codebase's structure graph.…, answer_knowledge_offline(), answer_offline(), ask(), ask_knowledge(), gather_claims(), gather_evidence(), gather_knowledge_claims() (+20 more)

### Community 14 - "citations.py"
Cohesion: 0.10
Nodes (39): anchors_for(), _definition_lines(), _Files, _fingerprint(), _inside_block(), _matches(), migrate_by_symbol(), Match (+31 more)

### Community 15 - "test_residue.py"
Cohesion: 0.22
Nodes (12): Map each `## heading` to its body text (content before the first heading is…, (H2 headings whose content changed / were added / removed, new_line_count -…, section_diff(), _sections(), _git(), Residue-mining units: section diff, compile journal/stats, per-page history,…, _repo(), test_claims_for_file_and_grep() (+4 more)

### Community 16 - "parse_claims_block"
Cohesion: 0.11
Nodes (30): anchor_claims(), claim_id(), is_negative_existential(), parse_claims_block(), True for statements asserting existential/definitional ABSENCE (unanchorable).…, Split a generated page into (clean page, raw claim rows). Tolerant of malformed…, Deterministic, ledger-friendly id: stable across runs for the same (statement,…, Repair a shortened citation to a real file, or None if it can't be resolved… (+22 more)

### Community 17 - "Isidore v2 — Incremental compilation, impact detection & residue mining"
Cohesion: 0.11
Nodes (18): 0 · Why (user directive), 10 · C8 — Semantic dirtiness + section-level revision (2026-09-29, supersedes the page-level half of §4), 11 · C9 — Prose citations follow the code (2026-09-29), 1 · Verified bug diagnoses (2026-07-10, against real code — not reports), 2 · Design principles (unchanged bets, now enforced deeper), 3 · C0 — Scoped compile: `isidore compile --only <sel>[,<sel>…]`, 4 · C1+C2 — Change-driven compile: `isidore compile --changed [--since <ref>]`, 5 · C3 — Impact detection: `isidore impact [--since <ref>] [--md] [--check]` (new, **0 LLM always**) (+10 more)

### Community 18 - "test_surface.py"
Cohesion: 0.22
Nodes (19): extract_surface(), python_surface(), Exact surface of one Python source text, or None if it does not parse. None is…, Surface of one file's text, routed by extension. None = not comparable source.…, _by_name(), API surface extraction: qualified names, signatures as change keys, and the…, test_extract_surface_returns_none_for_non_code(), test_generic_surface_disambiguates_same_named_methods_of_different_classes() (+11 more)

### Community 19 - "McpConnector"
Cohesion: 0.09
Nodes (28): BaseHTTPRequestHandler, _allowed(), McpConnector, Normalise the allowlist into `{entry, arguments}` records, sorted for…, _config(), fixture, parametrize, Path (+20 more)

### Community 20 - "rss.py"
Cohesion: 0.08
Nodes (40): Exception, IngestResult, Outcome of one ingest run. `raw_files` are the JSONL files written this run., A connector's persisted config, or {} if absent or corrupt. Never raises. Lives…, stored_config(), _check_url(), fetch(), fetch_json() (+32 more)

### Community 21 - "humanpack.py"
Cohesion: 0.07
Nodes (52): _looks_like_secret(), Path, Lane C — deterministic security detectors: entropy, sinks, topology. 0 LLM.…, Entropy + sink marks for one file. Never raises (unreadable file -> no marks)., Files reachable from an auth/secret/crypto root via imports (BFS, file-level).…, Run all three detector families over the repo -> deterministic marks. Pure,…, Shannon entropy per character (bits). Stdlib only., Return a reason if the literal is credential-shaped, else None. (+44 more)

### Community 22 - "connect.py"
Cohesion: 0.18
Nodes (22): _cmd_connect(), _cmd_ingest(), connector_summary(), load_config(), `isidore connect` and `isidore ingest` — the CLI face of the connector layer…, Add `isidore connect` and `isidore ingest` (registrar loop in cli.main)., A connector's stored config, or {} if absent/corrupt. Never raises., One row of `connect --list`: what it is, whether it can run, and what it has… (+14 more)

### Community 23 - "test_security_prose.py"
Cohesion: 0.09
Nodes (28): insert_security_banner(), is_security_finding(), True if a suspect reads as a security risk (hardcoded secret, auth bypass,…, A prominent, deterministic banner listing this page's security suspects — meant…, Place the banner right under the page's H1 (or at the very top if there is…, security_banner(), security_suspects(), Verify that negation patterns do not trigger false positive security findings… (+20 more)

### Community 24 - "test_source_disclosure_gate.py"
Cohesion: 0.11
Nodes (27): Classify wherever a compile would send this repository's source, as (kind,…, source_destination(), clean_env(), _gp(), _make_repo(), fixture, parametrize, Path (+19 more)

### Community 25 - "IngestOptions"
Cohesion: 0.14
Nodes (17): IngestOptions, Caps and scoping for a run. All limits live here (in code), never in a prompt., GitRepoConnector, Run a git command; return stdout or None on any failure (never raises)., _git(), _head(), _make_repo(), parametrize (+9 more)

### Community 26 - "Predicate"
Cohesion: 0.15
Nodes (27): Predicate, A decidable assertion parsed from a claim's third field. Frozen: predicates are…, literal_value(), parameter_names(), Parameter names in declaration order, or None when they cannot be read with…, The literal a constant is bound to, or None when it is not a plain literal.…, value(name, literal): a module-level assignment `name = literal`. Oracles: AST,…, signature(fn, a1, a2, ...): fn's positional parameter names, in order. Oracles:… (+19 more)

### Community 27 - "mcp.py"
Cohesion: 0.15
Nodes (14): _name_looks_mutating(), Minimal read-only MCP connector (ADR-0032 F3). The implementation deliberately…, (allowed, reason). Authority order: explicit readOnlyHint/destructiveHint >…, Fallback heuristic ONLY (not exhaustive): does the tool name contain a mutating…, _tool_read_only(), _FakeClient, parametrize, MCP connector read-only barrier (ADR-0032 F3). Regression for the review of… (+6 more)

### Community 28 - "PCP_SEAMS — the frozen interface for Proof-Carrying Prose (ADR-0033, phase P0)"
Cohesion: 0.15
Nodes (12): Certificate (`<page>.md` → `<page>.md.cert.json`, alongside the page), CLI, Contracts (`contracts.json` in the wiki dir), File ownership matrix (nobody edits another lane's files), How each lane starts (all depend ONLY on P0 = T-1dc9), Marks (lane C output; also the golden `marks.json`), PCP_SEAMS — the frozen interface for Proof-Carrying Prose (ADR-0033, phase P0), Pipeline hooks (lane A wires; signatures frozen) (+4 more)

### Community 29 - "read_certificate"
Cohesion: 0.15
Nodes (32): Load a certificate from disk. Raises ValueError on malformed JSON (fail-closed…, read_certificate(), VerifiedMass, Re-run the oracles over every certified page. 0 LLM. Writes only with…, recertify(), _cert(), _chained(), _claim() (+24 more)

### Community 30 - "check"
Cohesion: 0.13
Nodes (19): check(), explain(), is_plain(), PlainRule, Pattern, Plain-language gate: can a reader who has never seen code use this sentence?…, Human-readable reason for a rejection, for the run summary and the journal., One named check. `kind` mirrors Vale's rule taxonomy so the intent of each is… (+11 more)

### Community 31 - "render.py"
Cohesion: 0.15
Nodes (18): agents_md_block(), Deterministic outputs: quickstart.md, index.toon, llms.txt, and the AGENTS.md…, The self-reference an agent reads before touching the repo. 0 LLM, idempotent.…, Insert or replace the delimited block without touching the rest of the file…, render_quickstart(), render_toon_index(), upsert_agents_block(), encode() (+10 more)

### Community 32 - "isidore"
Cohesion: 0.12
Nodes (16): Bring your own graph, Config (`isidore.json`, optional), Design rules, isidore, Knowledge — the same contract, applied to what is NOT in your repo, Languages, License, One range, three readers (+8 more)

### Community 33 - "auth.py"
Cohesion: 0.32
Nodes (6): authenticate(), Auth service fixture for PCP lane tests. Line numbers are load-bearing: the…, Verify the caller's JWT and enforce the attempt ceiling., Token service fixture for PCP lane tests. verify_jwt is defined on L5 (cited by…, Return the decoded claims if the token's signature checks out, else None., verify_jwt()

### Community 35 - "cli.py"
Cohesion: 0.14
Nodes (27): _cmd_ask(), _cmd_compile(), _cmd_findings(), _cmd_impact(), _cmd_scan(), _cmd_stats(), _cmd_suggest_flows(), main() (+19 more)

### Community 36 - "Gmail — instance recipe for the MCP connector"
Cohesion: 0.12
Nodes (14): Gmail — instance recipe for the MCP connector, Sources, The config, The part you should actually worry about, Verifying it works, What it costs you to set up, What you get, Where the caps live (+6 more)

### Community 37 - "assemble_topic_context"
Cohesion: 0.15
Nodes (24): assemble_topic_context(), data_fence(), item_classification(), provider_is_trusted(), A per-assembly nonce for the excerpt delimiter. Ingested content is attacker-…, An item's confidentiality: `meta.classification`, else `classification:` in its…, Whether the operator has declared the configured LLM provider fit to receive…, Assemble items matching streams and filters into citable facts. External… (+16 more)

### Community 38 - "PageSpec"
Cohesion: 0.20
Nodes (9): Counter, render_findings(), _match_only(), _match_seed(), PageSpec, plan_flows(), Cross-cutting flow pages: BFS over the graph from user-declared seeds. Config…, A page matches a selector if the selector equals its filename, or is a prefix… (+1 more)

### Community 39 - "test_wiki_dir_env.py"
Cohesion: 0.31
Nodes (7): ISIDORE_WIKI_DIR redirects the compiled-wiki output directory. WIKI_DIRNAME is…, A nested WIKI_DIRNAME (e.g. doc/isidore) must create its parents, not crash., _reload_render(), test_save_state_creates_nested_wiki_dir(), test_wiki_dirname_blank_env_falls_back(), test_wiki_dirname_defaults_to_wiki(), test_wiki_dirname_honors_env()

### Community 40 - "_JsonRpcClient"
Cohesion: 0.09
Nodes (19): _JsonRpcClient, Any, Map tool name -> its MCP annotations via tools/list (paginated). Empty if the…, JSON-RPC 2.0 over the two MCP transports (spec 2025-06-18, basic/transports).…, The response to `want_id` if `message` is (or, as a batch, holds) it. Anything…, A server may ask the client something mid-request (`ping`, `roots/list`,…, Read SSE events until the one carrying the reply to `want_id`. Each event's…, The readable text of an MCP tool result, falling back to compact JSON. MCP… (+11 more)

### Community 41 - "test_connect_cli.py"
Cohesion: 0.08
Nodes (41): apply_settings(), parse_setting(), Path, Write a connector's config with the home's restrictive permissions., `key=value` -> (key, value). A value that parses as JSON is stored as JSON, so…, Fold `key=value` settings into a config. Repeating a key ACCUMULATES into a…, save_config(), _cap_content() (+33 more)

### Community 42 - "verify_predicate"
Cohesion: 0.08
Nodes (33): parse_predicate_field(), Parse a claim's optional third field into a pcp.Predicate (or None). PCP typed-…, Lane B (part 2) — claim->contract graduation + `isidore contracts`. (T-8dfc) A…, Check every promoted contract against the current graph. Pure, 0-LLM., verify_contracts(), parse_predicate(), Dispatch one predicate to its registered verifier. No verifier -> UNDECIDABLE…, Parse "<kind>:<a>;<b>" -> Predicate, or None if absent/malformed/unknown-kind.… (+25 more)

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

### Community 54 - "test_incremental.py"
Cohesion: 0.09
Nodes (51): _cmd_export_agora(), build_cards(), Path, export-agora — bridge isidore's verified claims into Living-Library card DRAFTS…, Return [(filename, content)] draft cards — one per wiki page with enough OK…, render_card(), _slug(), write_cards() (+43 more)

### Community 55 - "compile_overview"
Cohesion: 0.15
Nodes (22): compile_overview(), missing_sections(), Required headings the page does not have. 0 LLM., Compile the plain-language product page (N3). One LLM call, plus at most one…, _nodes(), The N3 product overview: plain language for anyone, resting on claims already…, The invariant the pyramid advertises: break a page below, and the page above…, test_a_chained_claim_is_actually_re_verified_and_not_silently_skipped() (+14 more)

### Community 56 - "pipeline.py"
Cohesion: 0.07
Nodes (38): append_run(), Compile journal + per-page changelog — residue mining, all zero-LLM. Every…, Append an H2-level changelog entry to a page's state (capped). No-op if the…, record_page_change(), annotate_unverified_paths(), assemble_context(), git_log_for(), _newer_than_graph() (+30 more)

### Community 57 - "_make_repo"
Cohesion: 0.29
Nodes (6): _make_repo(), fixture, Path, Three modules of twelve symbols each — over `min_symbols`, so each earns its…, No provider, no key, no network — the loop must work with nothing configured., repo()

### Community 58 - "pyramid.py"
Cohesion: 0.13
Nodes (27): _cmd_overview(), _cmd_subsystems(), _facts_fp(), _load_graph_for(), _module_pages_of(), _norm(), overview_facts(), _page_purpose() (+19 more)

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

### Community 64 - "surface.py"
Cohesion: 0.08
Nodes (29): clean_sig(), _declaration_tail(), generic_surface(), _is_declaration(), _is_public(), logical_lines(), _param_group(), AsyncFunctionDef (+21 more)

### Community 65 - "write_certificate"
Cohesion: 0.06
Nodes (50): After citations moved, the page's certificate must describe the new bytes: same…, reprose_certificate(), cert_file_digest(), Certificate, certificate_to_dict(), ClaimVerdict, parse_stored_predicate(), parse_wiki_uri() (+42 more)

### Community 66 - "test_pcp_pipeline.py"
Cohesion: 0.29
Nodes (10): _compile(), _fake_generator(), _fake_generator_with_a_lie(), Path, P-INT gate — the pipeline wiring ties all five PCP lanes together end to end: a…, test_compile_writes_a_certificate_with_typed_verdicts(), test_deterministic_mark_forces_the_banner_despite_calm_prose(), test_refuted_claim_is_quarantined_not_published() (+2 more)

### Community 67 - "store.py"
Cohesion: 0.09
Nodes (41): git-repo connector (ADR-0032 F1): local repositories as a knowledge source. No…, (item, None) for a changed repo, (None, None) if HEAD is unchanged, (None,…, _as_list(), feed_url(), HackerNewsConnector, parse_hits(), Hacker News connector (ADR-0032 F4): public front-page tags and Algolia…, (stream, url) for every configured search and listing. Streams are named for… (+33 more)

### Community 68 - "subsystem-tests.md"
Cohesion: 0.40
Nodes (4): How the work is divided, What it depends on, and what depends on it, What this area is responsible for, Where to start reading

### Community 69 - "DeltaEntry"
Cohesion: 0.17
Nodes (11): DeltaEntry, _group_by_module(), _llm_entries(), _prompt_for_module(), One typed novelty row. `file` is always the path as of `until` (renames map old…, The machine/agent view: one table per area, product surface first., What the model is allowed to write about: product surface, and only what can be…, render_whatsnew_toon() (+3 more)

### Community 70 - "whatsnew.py"
Cohesion: 0.14
Nodes (23): _blob(), _cmd_whatsnew(), commit_hints(), _git(), _is_comparable(), _name_status(), Path, isidore whatsnew — a changelog you can re-verify, instead of one you have to… (+15 more)

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
Cohesion: 0.13
Nodes (20): python_import_roots(), Directories an absolute Python import is resolved from: the repo root, plus the…, Map an import to a repo file id if the module resolves inside the repo.…, Build a structure graph for a repo in ANY language, zero dependencies (see…, _resolve_import(), scan_repo(), _names(), Multi-language scanner: the declarative engine (langspec) and its wiring into… (+12 more)

### Community 102 - "subsystem-src.md"
Cohesion: 0.40
Nodes (4): How the work is divided, What it depends on, and what depends on it, What this area is responsible for, Where to start reading

### Community 103 - "src-isidore-citations_py.md"
Cohesion: 0.33
Nodes (5): Architecture, Dependencies, How to change safely, Key entry points, Purpose

### Community 104 - "configured_wiki_dirname"
Cohesion: 0.09
Nodes (40): _cmd_llms(), configured_wiki_dirname(), _first_sentence(), Path, The wiki, in the layout agents are converging on for being handed…, Write llms.txt at the repo root — where the convention puts it, so a fetcher…, Where this repository keeps its living docs, relative to its root. Precedence:…, Add `isidore llms` (regenerate llms.txt from whatever is compiled). 0 LLM. (+32 more)

### Community 105 - "tests-test_citations_py.md"
Cohesion: 0.33
Nodes (5): Architecture, Dependencies, How to change safely, Key entry points, Purpose

### Community 106 - "src-isidore-recertify_py.md"
Cohesion: 0.33
Nodes (5): Architecture, Dependencies, How to change safely, Key entry points, Purpose

### Community 107 - "src-isidore-render_py.md"
Cohesion: 0.33
Nodes (5): Architecture, Dependencies, How to change safely, Key entry points, Purpose

### Community 108 - "WhatsnewError"
Cohesion: 0.29
Nodes (7): RuntimeError, Git could not answer, or a ref does not resolve. Fail closed: never guess a…, WhatsnewError, Its prompts carry an excerpt of every added and changed symbol — a compile by…, test_whatsnew_refuses_at_an_undeclared_host(), test_execute_refuses_a_range_that_does_not_end_at_head(), test_unresolvable_ref_fails_closed()

### Community 109 - "tests-test_langspec_oracle_py.md"
Cohesion: 0.33
Nodes (5): Architecture, Dependencies, How to change safely, Key entry points, Purpose

### Community 110 - "tests-test_llms_txt_py.md"
Cohesion: 0.33
Nodes (5): Architecture, Dependencies, How to change safely, Key entry points, Purpose

### Community 111 - "test_hostile_f6.py"
Cohesion: 0.20
Nodes (20): home(), _item(), fixture, usefixtures, F6's hostile gate: what the knowledge home does when its own data is broken,…, A cap that bites silently turns a partial answer into a confident one., The whole point of I8, end to end: an item that issues commands and forges a…, The second half of the defence: even if a forged URI reaches a claim, it has to… (+12 more)

### Community 112 - "tests-test_recertify_py.md"
Cohesion: 0.33
Nodes (5): Architecture, Dependencies, How to change safely, Key entry points, Purpose

### Community 113 - "compile_subsystems"
Cohesion: 0.20
Nodes (11): default_generator(), Build the env-configured generator. Fails closed if no model is set., assert_may_send_source(), Fail closed unless the destination may see this repository's content. `what`…, compile_subsystems(), Compile the N2 layer: one bounded call per area, each page chained to its…, Turn `wiki://page` into `page` in PROSE, so the links a reader clicks actually…, relink_wiki_uris() (+3 more)

### Community 114 - "Slack — instance recipe for the MCP connector"
Cohesion: 0.20
Nodes (9): Confirm the tool names before you trust this block, Setup, Slack — instance recipe for the MCP connector, Sources, The config, The part you should actually worry about, Verifying it works, What you get (+1 more)

### Community 115 - "GenerationError"
Cohesion: 0.17
Nodes (14): Request, A generator that answers from disk. Raises GenerationError when an answer is…, response_generator(), build_request(), generate(), generate_via_cli(), GenerationError, RuntimeError (+6 more)

### Community 116 - "pcp.py"
Cohesion: 0.17
Nodes (13): certificate_from_dict(), get_verifier(), Protocol, Proof-Carrying Prose (PCP) — the frozen seam shared by every PCP lane. This…, A predicate verifier. MUST be deterministic and 0-LLM. Returns UNDECIDABLE,…, A reconciler finding (lane B): the model's own outputs contradict each other.…, Rebuild a Certificate from parsed JSON, reconstructing the nested dataclasses.…, register_verifier() (+5 more)

### Community 117 - "test_wiki_not_input.py"
Cohesion: 0.10
Nodes (23): _is_wiki_output(), The repo-relative posix path of the wiki OUTPUT directory, normalised for…, wiki_output_prefix(), degenerate_certificate(), drop_wiki_output(), A short reason when a certificate is a symptom rather than a certificate, else…, Nodes that do not live inside the wiki output directory. The second barrier.…, _Cert (+15 more)

### Community 118 - "certificate_status"
Cohesion: 0.27
Nodes (11): _cert_digest(), certificate_status(), _cmd_verify(), _ctx_for(), Path, Check a page against its sidecar certificate, offline, 0 LLM (invariant I11).…, sha256 of a page's certificate file, "" if it is gone., (ok, cert) for one page. ok is False on any tamper/mismatch/missing-graph. (+3 more)

### Community 119 - "tests-test_connectors_f4_py.md"
Cohesion: 0.33
Nodes (5): Architecture, Dependencies, How to change safely, Key entry points, Purpose

### Community 120 - "strip_inline_claim_rows"
Cohesion: 0.50
Nodes (4): Drop the pipe-separated citation a model appends to its own bullets. Observed…, strip_inline_claim_rows(), test_a_bare_trailing_citation_is_stripped_too(), test_a_real_markdown_table_is_left_alone()

### Community 121 - "src-isidore-connect_py.md"
Cohesion: 0.33
Nodes (5): Architecture, Dependencies, How to change safely, Key entry points, Purpose

### Community 122 - "tests-test_connect_cli_py.md"
Cohesion: 0.33
Nodes (5): Architecture, Dependencies, How to change safely, Key entry points, Purpose

### Community 123 - "test_pyramid.py"
Cohesion: 0.29
Nodes (9): plan_pyramid(), Plan deterministic N2 subsystem + N3 product pages. 0 LLM. Explicit…, _graph(), Lane D gate — the pyramid plans from the real graph, uses imports for cohesion,…, BUG 1 regression: auto-seed used node['path'/'file'/'name'] (absent) -> [].…, BUG 2 regression: `links` was ignored. imports edges must yield depends_on., test_autoseed_groups_by_source_file_on_the_real_graph(), test_explicit_config_still_works() (+1 more)

### Community 124 - "_git_repo"
Cohesion: 0.33
Nodes (6): _git_repo(), A third-party graph (e.g. Graphify) that indexed a gitignored path gets cleaned…, Init a minimal git repo at `path`; skip the test if git is unavailable., The reported GIMO bug: a gitignored build-artifact copy must NOT be indexed as…, test_restrict_to_tracked_filters_foreign_graph(), test_scan_excludes_gitignored_build_artifacts()

### Community 125 - "parse_plain_block"
Cohesion: 0.67
Nodes (3): parse_plain_block(), Split the plain-language block out of a model answer -> (rest, plain text,…, test_plain_language_block_is_dropped_when_it_comes_back_as_jargon()

### Community 126 - "repo_with_module_page"
Cohesion: 0.67
Nodes (3): fixture, The module page above, registered in the wiki state so an area can find it., repo_with_module_page()

### Community 128 - "read_contracts"
Cohesion: 0.12
Nodes (23): _cmd_contracts(), Add `isidore contracts` (promote / list / check)., Command implementation for `isidore contracts`., register_cli(), Contract, Path, Load promoted contracts (empty list if the file is absent). Malformed ->…, Persist contracts as JSON (machine-read gate input). (+15 more)

### Community 129 - "src-isidore-revise_py.md"
Cohesion: 0.33
Nodes (5): Architecture, Dependencies, How to change safely, Key entry points, Purpose

### Community 130 - "tests-test_connectors_f5_py.md"
Cohesion: 0.33
Nodes (5): Architecture, Dependencies, How to change safely, Key entry points, Purpose

### Community 131 - "tests-test_incremental_py.md"
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

### Community 137 - "tests-test_source_disclosure_gate_py.md"
Cohesion: 0.33
Nodes (5): Architecture, Dependencies, How to change safely, Key entry points, Purpose

### Community 139 - "tests-test_wiki_dir_config_py.md"
Cohesion: 0.33
Nodes (5): Architecture, Dependencies, How to change safely, Key entry points, Purpose

## Knowledge Gaps
- **374 isolated node(s):** `isidore-wiki`, `Knowledge home (local, not in this repo)`, `Why`, `Quickstart`, `What you get` (+369 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **6 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `IngestOptions` connect `IngestOptions` to `store.py`, `cli.py`, `test_connectors_f4.py`, `_JsonRpcClient`, `test_connect_cli.py`, `knowledge.py`, `test_hostile_f6.py`, `McpConnector`, `rss.py`, `connect.py`, `mcp.py`?**
  _High betweenness centrality (0.078) - this node is a cross-community bridge._
- **Why does `compile_wiki()` connect `compile_wiki` to `test_handoff.py`, `graph.py`, `test_units.py`, `verify.py`, `emit`, `impact.py`, `claims.py`, `knowledge.py`, `qa.py`, `citations.py`, `test_residue.py`, `parse_claims_block`, `humanpack.py`, `test_security_prose.py`, `test_source_disclosure_gate.py`, `read_certificate`, `render.py`, `cli.py`, `PageSpec`, `test_incremental.py`, `pipeline.py`, `write_certificate`, `test_pcp_pipeline.py`, `compile_subsystems`, `GenerationError`, `test_wiki_not_input.py`, `certificate_status`?**
  _High betweenness centrality (0.062) - this node is a cross-community bridge._
- **Why does `VerifyContext` connect `verify.py` to `read_contracts`, `write_certificate`, `compile_wiki`, `Predicate`, `DeltaEntry`, `emit`, `PageSpec`, `whatsnew.py`, `verify_predicate`, `WhatsnewError`, `compile_subsystems`, `pcp.py`, `humanpack.py`, `certificate_status`, `compile_overview`, `pipeline.py`, `pyramid.py`?**
  _High betweenness centrality (0.035) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `compile_wiki()` (e.g. with `read_excerpt()` and `test_a_page_with_no_usable_certificate_never_stampedes_a_recompile()`) actually correct?**
  _`compile_wiki()` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Are the 7 inferred relationships involving `VerifyContext` (e.g. with `CompileResult` and `PageSpec`) actually correct?**
  _`VerifyContext` has 7 INFERRED edges - model-reasoned connections that need verification._
- **Are the 9 inferred relationships involving `IngestOptions` (e.g. with `GitRepoConnector` and `HackerNewsConnector`) actually correct?**
  _`IngestOptions` has 9 INFERRED edges - model-reasoned connections that need verification._
- **What connects `isidore-wiki`, `Knowledge home (local, not in this repo)`, `Why` to the rest of the system?**
  _374 weakly-connected nodes found - possible documentation gaps or missing edges._