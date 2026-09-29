# Graph Report - isidore  (2026-09-29)

## Corpus Check
- 169 files · ~146,210 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1996 nodes · 4762 edges · 110 communities (105 shown, 5 thin omitted)
- Extraction: 97% EXTRACTED · 3% INFERRED · 0% AMBIGUOUS · INFERRED: 164 edges (avg confidence: 0.66)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `25e46585`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- test_handoff.py
- graph.py
- compile_wiki
- findings.py
- IngestOptions
- verify.py
- emit
- quickstart.md
- test_whatsnew.py
- impact.py
- claims.py
- write_scan
- build_delta
- qa.py
- citations.py
- build_cards
- anchor_claims
- Isidore v2 — Incremental compilation, impact detection & residue mining
- test_surface.py
- iter_items
- hackernews.py
- humanpack.py
- ValueError
- test_security_prose.py
- test_source_disclosure_gate.py
- test_pcp_seams.py
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
- plan_pages
- test_wiki_dir_env.py
- _JsonRpcClient
- connect.py
- parse_claims_block
- clean_sig
- test_vigil.py
- harvest_todos
- src-isidore-export_py.md
- src-isidore-impact_py.md
- src-isidore-journal_py.md
- src-isidore-llm_py.md
- svc.md
- Claims (TOON)
- Findings (TOON)
- Index (TOON)
- test_incremental.py
- compile_overview
- pipeline.py
- _make_repo
- Path
- langspec.py
- src-isidore-plain_py.md
- src-isidore-toon_py.md
- is_negative_existential
- overview.md
- surface.py
- write_certificate
- test_pcp_pipeline.py
- store.py
- _load_graph_for
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
- scan_repo
- subsystem-src.md
- src-isidore-citations_py.md
- render.py
- src-isidore-recertify_py.md
- src-isidore-render_py.md
- WhatsnewError
- test_hostile_f6.py
- compile_subsystems
- Slack — instance recipe for the MCP connector
- GenerationError
- pyramid.py
- test_wiki_not_input.py
- generate_prose
- src-isidore-connect_py.md
- test_pyramid.py
- test_units.py
- repo_with_module_page
- read_contracts
- src-isidore-revise_py.md
- src-isidore-handoff_py.md

## God Nodes (most connected - your core abstractions)
1. `compile_wiki()` - 116 edges
2. `VerifyContext` - 64 edges
3. `IngestOptions` - 54 edges
4. `run_whatsnew()` - 39 edges
5. `Predicate` - 35 edges
6. `compile_overview()` - 32 edges
7. `load_graph()` - 31 edges
8. `load_state()` - 31 edges
9. `_make_repo()` - 31 edges
10. `write_scan()` - 28 edges

## Surprising Connections (you probably didn't know these)
- `test_parse_claims_block_extracts_and_strips()` --calls--> `parse_claims_block()`  [EXTRACTED]
  tests/test_claims.py → src/isidore/claims.py
- `test_every_ingested_item_can_be_cited()` --calls--> `evidence_hash()`  [INFERRED]
  tests/test_connectors_f4.py → src/isidore/claims.py
- `test_the_mail_item_is_citable_end_to_end()` --calls--> `evidence_hash()`  [INFERRED]
  tests/test_connectors_f5.py → src/isidore/claims.py
- `test_carry_claims_skips_refuted_and_unanchored_claims()` --calls--> `evidence_hash()`  [INFERRED]
  tests/test_incremental.py → src/isidore/claims.py
- `test_only_ok_claims_are_exported_by_default()` --calls--> `check_claims()`  [INFERRED]
  tests/test_export.py → src/isidore/claims.py

## Import Cycles
- None detected.

## Communities (110 total, 5 thin omitted)

### Community 0 - "test_handoff.py"
Cohesion: 0.16
Nodes (25): apply(), Compile using the written answers. Identical pipeline to any other provider., _answer_all(), _Args, `isidore handoff` — the caller is the model, so the source never leaves the…, A provider's budget bounds spend. There is no spend here, so a cap would only…, Otherwise the next `apply` certifies a page nobody asked about, from an answer…, The lint gate asks a provider for one repair round. There is nobody to ask here… (+17 more)

### Community 1 - "graph.py"
Cohesion: 0.12
Nodes (29): git_head(), git_listed_files(), _is_binary(), _is_wiki_output(), _iter_source_files(), _node_id(), _norm_source_file(), Path (+21 more)

### Community 2 - "compile_wiki"
Cohesion: 0.13
Nodes (41): compile_wiki(), context_hash(), lint_cited_paths(), Content-addressed page identity: same prompt -> nothing to regenerate., File-looking paths cited in the prose that do NOT exist in the repo., Run the pipeline. With execute=False no LLM is called and no page is written.…, _gp(), _graph() (+33 more)

### Community 3 - "findings.py"
Cohesion: 0.13
Nodes (25): _cmd_findings(), _churn(), coverage_gap_candidates(), filter_findings(), finding_id(), findings_new(), is_finding_resolved(), orphan_file_candidates() (+17 more)

### Community 4 - "IngestOptions"
Cohesion: 0.05
Nodes (46): IngestOptions, Caps and scoping for a run. All limits live here (in code), never in a prompt., GitRepoConnector, (item, None) for a changed repo, (None, None) if HEAD is unchanged, (None,…, Run a git command; return stdout or None on any failure (never raises)., (content with any delimiter-shaped line defanged, how many were found). Marked…, seal_content(), _git() (+38 more)

### Community 5 - "verify.py"
Cohesion: 0.08
Nodes (58): AST, Module, Lane B (part 2) — claim->contract graduation + `isidore contracts`. (T-8dfc) A…, Check every promoted contract against the current graph. Pure, 0-LLM., verify_contracts(), The result of checking one predicate against an oracle. `value` is…, Everything a verifier needs, assembled once per page/verify run. Read-only to…, undecidable() (+50 more)

### Community 6 - "emit"
Cohesion: 0.18
Nodes (19): _cmd_handoff(), emit(), handoff_dir(), _plan(), prompt_id(), Path, `isidore handoff` — let the CALLER be the model, instead of shipping the code…, Add `isidore handoff emit|apply` (registrar loop in cli.main). (+11 more)

### Community 7 - "quickstart.md"
Cohesion: 0.33
Nodes (4): Knowledge home (local, not in this repo), Wiki (isidore), Modules, Wiki (isidore)

### Community 8 - "test_whatsnew.py"
Cohesion: 0.12
Nodes (34): Build the delta, optionally write the prose, and persist page + certificate., run_whatsnew(), WhatsnewResult, _commit(), _git(), _one_file_repo(), fixture, isidore whatsnew: the typed surface delta, its artifact, and the verification… (+26 more)

### Community 9 - "impact.py"
Cohesion: 0.09
Nodes (35): affected_modules(), changed_lines(), changed_symbols(), _git_diff(), _module_fan_in(), modules_of(), Path, Change-set detection: which graph symbols a git diff touched, and which modules… (+27 more)

### Community 10 - "claims.py"
Cohesion: 0.15
Nodes (28): check_claims(), claims_for_file(), claims_grep(), evidence_hash(), evidence_state(), _hash(), _normalize(), Path (+20 more)

### Community 11 - "write_scan"
Cohesion: 0.14
Nodes (20): is_test_path(), Run the scanner and persist the graph to .isidore/graph.json., Is this file part of a test suite rather than of the product? By the…, write_scan(), overview_facts(), Everything the overview is allowed to be written from. 0 LLM., test_a_graph_older_than_the_code_is_said_out_loud(), fixture (+12 more)

### Community 12 - "build_delta"
Cohesion: 0.18
Nodes (11): build_delta(), _diff_surfaces(), _file_summary(), A compact roll-up of what a whole added/removed file declares., Typed difference between two surfaces of the same file. Identity is the…, The zero-LLM core: a typed API-surface difference between two revisions.…, test_deleted_file_is_reported_but_carries_no_line_to_cite(), test_delta_reports_exactly_the_real_changes_and_invents_nothing() (+3 more)

### Community 13 - "qa.py"
Cohesion: 0.12
Nodes (24): isidore — compile an agent-oriented wiki from your codebase's structure graph.…, answer_knowledge_offline(), answer_offline(), ask(), ask_knowledge(), gather_claims(), gather_evidence(), gather_knowledge_claims() (+16 more)

### Community 14 - "citations.py"
Cohesion: 0.10
Nodes (39): anchors_for(), _definition_lines(), _Files, _fingerprint(), _inside_block(), _matches(), migrate_by_symbol(), Match (+31 more)

### Community 15 - "build_cards"
Cohesion: 0.23
Nodes (14): _cmd_export_agora(), build_cards(), Path, export-agora — bridge isidore's verified claims into Living-Library card DRAFTS…, Return [(filename, content)] draft cards — one per wiki page with enough OK…, render_card(), _slug(), write_cards() (+6 more)

### Community 16 - "anchor_claims"
Cohesion: 0.15
Nodes (23): anchor_claims(), claim_id(), Deterministic, ledger-friendly id: stable across runs for the same (statement,…, Repair a shortened citation to a real file, or None if it can't be resolved…, Quarantine filter + anchoring. Returns (anchored claims, dropped, repaired). A…, resolve_citation(), _gp(), _make_repo() (+15 more)

### Community 17 - "Isidore v2 — Incremental compilation, impact detection & residue mining"
Cohesion: 0.10
Nodes (19): 0 · Why (user directive), 10 · C8 — Semantic dirtiness + section-level revision (2026-09-29, supersedes the page-level half of §4), 11 · C9 — Prose citations follow the code (2026-09-29), 12 · C10 — Tests are evidence, not pages (2026-09-29), 1 · Verified bug diagnoses (2026-07-10, against real code — not reports), 2 · Design principles (unchanged bets, now enforced deeper), 3 · C0 — Scoped compile: `isidore compile --only <sel>[,<sel>…]`, 4 · C1+C2 — Change-driven compile: `isidore compile --changed [--since <ref>]` (+11 more)

### Community 18 - "test_surface.py"
Cohesion: 0.22
Nodes (19): extract_surface(), python_surface(), Exact surface of one Python source text, or None if it does not parse. None is…, Surface of one file's text, routed by extension. None = not comparable source.…, _by_name(), API surface extraction: qualified names, signatures as change keys, and the…, test_extract_surface_returns_none_for_non_code(), test_generic_surface_disambiguates_same_named_methods_of_different_classes() (+11 more)

### Community 19 - "iter_items"
Cohesion: 0.07
Nodes (36): BaseHTTPRequestHandler, _allowed(), McpConnector, Normalise the allowlist into `{entry, arguments}` records, sorted for…, iter_items(), Yield stored items, newest run first. A corrupt/half-written JSONL line is…, _config(), fixture (+28 more)

### Community 20 - "hackernews.py"
Cohesion: 0.06
Nodes (54): Exception, all_connectors(), Connector, get(), IngestResult, _load_plugins(), Protocol, Connector protocol + registry (ADR-0032 F1). A connector ingests raw items from… (+46 more)

### Community 21 - "humanpack.py"
Cohesion: 0.07
Nodes (52): _looks_like_secret(), Path, Lane C — deterministic security detectors: entropy, sinks, topology. 0 LLM.…, Entropy + sink marks for one file. Never raises (unreadable file -> no marks)., Files reachable from an auth/secret/crypto root via imports (BFS, file-level).…, Run all three detector families over the repo -> deterministic marks. Pure,…, Shannon entropy per character (bits). Stdlib only., Return a reason if the literal is credential-shaped, else None. (+44 more)

### Community 22 - "ValueError"
Cohesion: 0.14
Nodes (15): _link(), _local(), parse_feed(), First non-empty child whose local tag is one of `names`, stripped., RSS puts the URL in <link>'s text; Atom puts it in <link href=...>, sometimes…, (feed title, entries) from RSS 2.0 or Atom. Raises ValueError on XML that will…, _text(), check_item_id() (+7 more)

### Community 23 - "test_security_prose.py"
Cohesion: 0.12
Nodes (22): insert_security_banner(), is_security_finding(), True if a suspect reads as a security risk (hardcoded secret, auth bypass,…, A prominent, deterministic banner listing this page's security suspects — meant…, Place the banner right under the page's H1 (or at the very top if there is…, render_findings(), security_banner(), security_suspects() (+14 more)

### Community 24 - "test_source_disclosure_gate.py"
Cohesion: 0.11
Nodes (27): Classify wherever a compile would send this repository's source, as (kind,…, source_destination(), clean_env(), _gp(), _make_repo(), fixture, parametrize, Path (+19 more)

### Community 25 - "test_pcp_seams.py"
Cohesion: 0.23
Nodes (11): parse_predicate(), Parse "<kind>:<a>;<b>" -> Predicate, or None if absent/malformed/unknown-kind.…, parametrize, P0 gate (ADR-0033) — the frozen PCP seam parses its golden fixtures and exposes…, test_golden_certificate_round_trips(), test_golden_graph_loads(), test_golden_marks_and_pyramid_config_parse(), test_pcp_subcommands_are_registered() (+3 more)

### Community 26 - "Predicate"
Cohesion: 0.15
Nodes (27): Predicate, A decidable assertion parsed from a claim's third field. Frozen: predicates are…, literal_value(), parameter_names(), Parameter names in declaration order, or None when they cannot be read with…, The literal a constant is bound to, or None when it is not a plain literal.…, value(name, literal): a module-level assignment `name = literal`. Oracles: AST,…, signature(fn, a1, a2, ...): fn's positional parameter names, in order. Oracles:… (+19 more)

### Community 27 - "test_mcp_barrier.py"
Cohesion: 0.15
Nodes (14): _name_looks_mutating(), (allowed, reason). Authority order: explicit readOnlyHint/destructiveHint >…, Fallback heuristic ONLY (not exhaustive): does the tool name contain a mutating…, _tool_read_only(), _FakeClient, parametrize, MCP connector read-only barrier (ADR-0032 F3). Regression for the review of…, Stands in for _JsonRpcClient: a server exposing one read tool, one write tool… (+6 more)

### Community 28 - "PCP_SEAMS — the frozen interface for Proof-Carrying Prose (ADR-0033, phase P0)"
Cohesion: 0.15
Nodes (12): Certificate (`<page>.md` → `<page>.md.cert.json`, alongside the page), CLI, Contracts (`contracts.json` in the wiki dir), File ownership matrix (nobody edits another lane's files), How each lane starts (all depend ONLY on P0 = T-1dc9), Marks (lane C output; also the golden `marks.json`), PCP_SEAMS — the frozen interface for Proof-Carrying Prose (ADR-0033, phase P0), Pipeline hooks (lane A wires; signatures frozen) (+4 more)

### Community 29 - "read_certificate"
Cohesion: 0.12
Nodes (42): Load a certificate from disk. Raises ValueError on malformed JSON (fail-closed…, read_certificate(), Re-run the oracles over every certified page. 0 LLM. Writes only with…, recertify(), _cert_digest(), certificate_status(), _cmd_verify(), _ctx_for() (+34 more)

### Community 30 - "check"
Cohesion: 0.13
Nodes (19): check(), explain(), is_plain(), PlainRule, Pattern, Plain-language gate: can a reader who has never seen code use this sentence?…, Human-readable reason for a rejection, for the run summary and the journal., One named check. `kind` mirrors Vale's rule taxonomy so the intent of each is… (+11 more)

### Community 31 - "encode"
Cohesion: 0.26
Nodes (11): render_toon_index(), encode(), encode_table(), _field(), Any, TOON (Token-Oriented Object Notation) serializer — tabular subset. One…, Serialize one table. >>> print(encode_table("pages", ["file", "module"], [ ...…, Serialize several tables into one TOON document (newline-separated). (+3 more)

### Community 32 - "isidore"
Cohesion: 0.12
Nodes (16): Bring your own graph, Config (`isidore.json`, optional), Design rules, isidore, Knowledge — the same contract, applied to what is NOT in your repo, Languages, License, One range, three readers (+8 more)

### Community 33 - "auth.py"
Cohesion: 0.32
Nodes (6): authenticate(), Auth service fixture for PCP lane tests. Line numbers are load-bearing: the…, Verify the caller's JWT and enforce the attempt ceiling., Token service fixture for PCP lane tests. verify_jwt is defined on L5 (cited by…, Return the decoded claims if the token's signature checks out, else None., verify_jwt()

### Community 35 - "cli.py"
Cohesion: 0.14
Nodes (24): _cmd_ask(), _cmd_compile(), _cmd_impact(), _cmd_scan(), _cmd_suggest_flows(), isidore — compile an agent-oriented wiki from your codebase's structure graph.…, Precedence: explicit CLI arg > isidore.json > built-in default., _setting() (+16 more)

### Community 36 - "Gmail — instance recipe for the MCP connector"
Cohesion: 0.12
Nodes (14): Gmail — instance recipe for the MCP connector, Sources, The config, The part you should actually worry about, Verifying it works, What it costs you to set up, What you get, Where the caps live (+6 more)

### Community 37 - "knowledge.py"
Cohesion: 0.09
Nodes (44): _cmd_sync(), parse_findings_block(), Split a generated page into (clean page, findings rows). Tolerant of malformed…, home(), `$ISIDORE_HOME` if set, else `~/.isidore`., assemble_topic_context(), compile_topics(), data_fence() (+36 more)

### Community 38 - "plan_pages"
Cohesion: 0.17
Nodes (15): Counter, module_of(), _match_only(), _match_seed(), module_dep_edges(), PageSpec, plan_flows(), plan_pages() (+7 more)

### Community 39 - "test_wiki_dir_env.py"
Cohesion: 0.31
Nodes (7): ISIDORE_WIKI_DIR redirects the compiled-wiki output directory. WIKI_DIRNAME is…, A nested WIKI_DIRNAME (e.g. doc/isidore) must create its parents, not crash., _reload_render(), test_save_state_creates_nested_wiki_dir(), test_wiki_dirname_blank_env_falls_back(), test_wiki_dirname_defaults_to_wiki(), test_wiki_dirname_honors_env()

### Community 40 - "_JsonRpcClient"
Cohesion: 0.13
Nodes (11): _JsonRpcClient, Any, Map tool name -> its MCP annotations via tools/list (paginated). Empty if the…, JSON-RPC 2.0 over the two MCP transports (spec 2025-06-18, basic/transports).…, The response to `want_id` if `message` is (or, as a batch, holds) it. Anything…, A server may ask the client something mid-request (`ping`, `roots/list`,…, Read SSE events until the one carrying the reply to `want_id`. Each event's…, The readable text of an MCP tool result, falling back to compact JSON. MCP… (+3 more)

### Community 41 - "connect.py"
Cohesion: 0.06
Nodes (58): main(), apply_settings(), _cmd_connect(), _cmd_ingest(), connector_summary(), load_config(), parse_setting(), Path (+50 more)

### Community 42 - "parse_claims_block"
Cohesion: 0.10
Nodes (32): After citations moved, the page's certificate must describe the new bytes: same…, reprose_certificate(), parse_claims_block(), parse_predicate_field(), Parse a claim's optional third field into a pcp.Predicate (or None). PCP typed-…, Split a generated page into (clean page, raw claim rows). Tolerant of malformed…, ClaimVerdict, prose_hash() (+24 more)

### Community 43 - "clean_sig"
Cohesion: 0.18
Nodes (11): clean_sig(), AsyncFunctionDef, _py_constant(), FunctionDef, _py_signature(), Collapse a declaration header into a stable one-line comparison key, readable…, The parameter list and return annotation, rendered from the AST rather than the…, A module-level binding -> (name, `= value`). Config constants are API: a… (+3 more)

### Community 44 - "test_vigil.py"
Cohesion: 0.22
Nodes (8): Verify that negation patterns do not trigger false positive security findings…, Verify that safety-checks catch risks even with intermediate/intervening words., If the model attempts social engineering in prose while findings report the…, Vigil case: A camouflaged auth backdoor reported in findings but justified by…, test_adversarial_backdoor_detection(), test_false_negative_intervening_words(), test_negations_false_positives(), test_vigil_impossible_to_clean_by_model()

### Community 45 - "harvest_todos"
Cohesion: 0.29
Nodes (7): _comment_lines(), harvest_todos(), The file's lines with everything but COMMENT text blanked, so a marker is…, TODO/FIXME/HACK/XXX with file:line — regex over the COMMENTS of the files the…, test_harvest_todos_finds_markers_with_lines(), test_harvest_todos_reads_comments_not_strings(), test_harvest_todos_skips_oversized_files()

### Community 46 - "src-isidore-export_py.md"
Cohesion: 0.33
Nodes (5): Architecture, Dependencies, How to change safely, Key entry points, Purpose

### Community 47 - "src-isidore-impact_py.md"
Cohesion: 0.33
Nodes (5): Architecture, Dependencies, How to change safely, Key entry points, Purpose

### Community 48 - "src-isidore-journal_py.md"
Cohesion: 0.33
Nodes (5): Architecture, Dependencies, How to change safely, Key entry points, Purpose

### Community 49 - "src-isidore-llm_py.md"
Cohesion: 0.33
Nodes (5): Architecture, Dependencies, How to change safely, Key entry points, Purpose

### Community 54 - "test_incremental.py"
Cohesion: 0.08
Nodes (53): _cmd_stats(), append_run(), Compile journal + per-page changelog — residue mining, all zero-LLM. Every…, Map each `## heading` to its body text (content before the first heading is…, (H2 headings whose content changed / were added / removed, new_line_count -…, Append an H2-level changelog entry to a page's state (capped). No-op if the…, record_page_change(), render_stats() (+45 more)

### Community 55 - "compile_overview"
Cohesion: 0.14
Nodes (20): compile_overview(), missing_sections(), _overview_identity(), What the product page is written FROM: the README and the proven claims. Not…, Required headings the page does not have. 0 LLM., Turn `wiki://page` into `page` in PROSE, so the links a reader clicks actually…, Compile the plain-language product page (N3). One LLM call, plus at most one…, relink_wiki_uris() (+12 more)

### Community 56 - "pipeline.py"
Cohesion: 0.09
Nodes (33): assemble_context(), git_log_for(), _newer_than_graph(), Path, The compiler pipeline: plan -> assemble -> generate -> cache -> lint.…, ±radius lines around a graph `L<n>` location. Tolerates stale files/locations., Gather one page's facts. Returns (context, truncation-warnings)., Source files the graph describes that were modified after the graph was written. (+25 more)

### Community 57 - "_make_repo"
Cohesion: 0.29
Nodes (6): _make_repo(), fixture, Path, Three modules of twelve symbols each — over `min_symbols`, so each earns its…, No provider, no key, no network — the loop must work with nothing configured., repo()

### Community 58 - "Path"
Cohesion: 0.15
Nodes (16): _module_pages_of(), _page_purpose(), _prune_areas(), Path, The compiled module pages that belong to one subsystem, keyed by page file name., The first sentence of a module page's `## Purpose` — what that module says it…, What one subsystem page is written from: its module pages, what each says it is…, Delete area pages (and their certificates and stored facts) that no longer have… (+8 more)

### Community 59 - "langspec.py"
Cohesion: 0.14
Nodes (23): _brace(), _doc(), extract(), _js(), _kw_func(), _kw_type(), LanguageSpec, _Pending (+15 more)

### Community 60 - "src-isidore-plain_py.md"
Cohesion: 0.33
Nodes (5): Architecture, Dependencies, How to change safely, Key entry points, Purpose

### Community 61 - "src-isidore-toon_py.md"
Cohesion: 0.33
Nodes (5): Architecture, Dependencies, How to change safely, Key entry points, Purpose

### Community 62 - "is_negative_existential"
Cohesion: 0.40
Nodes (5): is_negative_existential(), True for statements asserting existential/definitional ABSENCE (unanchorable).…, Drop items whose `key` text asserts existential absence (unanchorable). Returns…, _split_negative_existential(), test_is_negative_existential_flags_absence_not_behavior()

### Community 63 - "overview.md"
Cohesion: 0.50
Nodes (3): How the pieces fit together, What this is, What you can do with it

### Community 64 - "surface.py"
Cohesion: 0.13
Nodes (18): _declaration_tail(), generic_surface(), _is_declaration(), _is_public(), logical_lines(), _param_group(), Match, API surface extraction from SOURCE TEXT — the zero-LLM substrate of `isidore… (+10 more)

### Community 65 - "write_certificate"
Cohesion: 0.09
Nodes (32): cert_file_digest(), Certificate, certificate_to_dict(), parse_stored_predicate(), Parse a predicate read back from a CERTIFICATE rather than from model output.…, The re-verifiable sidecar for one page. Persisted as JSON (machine-read).…, Certificate -> plain dict (asdict handles the nested dataclasses). The JSON on…, Persist a certificate as pretty JSON (stable key order for byte-deterministic… (+24 more)

### Community 66 - "test_pcp_pipeline.py"
Cohesion: 0.29
Nodes (10): _compile(), _fake_generator(), _fake_generator_with_a_lie(), Path, P-INT gate — the pipeline wiring ties all five PCP lanes together end to end: a…, test_compile_writes_a_certificate_with_typed_verdicts(), test_deterministic_mark_forces_the_banner_despite_calm_prose(), test_refuted_claim_is_quarantined_not_published() (+2 more)

### Community 67 - "store.py"
Cohesion: 0.12
Nodes (35): git-repo connector (ADR-0032 F1): local repositories as a knowledge source. No…, Minimal read-only MCP connector (ADR-0032 F3). The implementation deliberately…, create_run_id(), iso_now(), prune_runs(), The raw store: immutable ingested items + per-connector cursor state (ADR-0032…, Atomic write (tmp + os.replace) so a crash mid-write never corrupts the live…, Prepend a run summary, keeping the last 20 (newest first). (+27 more)

### Community 68 - "_load_graph_for"
Cohesion: 0.50
Nodes (5): _cmd_overview(), _cmd_subsystems(), _load_graph_for(), Add `isidore pyramid` (plan/preview) and `isidore overview` (the N3 product…, register_cli()

### Community 69 - "DeltaEntry"
Cohesion: 0.13
Nodes (17): _cmd_whatsnew(), DeltaEntry, impact_summary(), _llm_entries(), _md_section(), One typed novelty row. `file` is always the path as of `until` (renames map old…, The consequence of this range, in plain words, with zero LLM calls. A non-…, The machine/agent view: one table per area, product surface first. (+9 more)

### Community 70 - "whatsnew.py"
Cohesion: 0.15
Nodes (23): _blob(), commit_hints(), _git(), _is_comparable(), _name_status(), _prompt_for_module(), Path, isidore whatsnew — a changelog you can re-verify, instead of one you have to… (+15 more)

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

### Community 101 - "scan_repo"
Cohesion: 0.13
Nodes (20): python_import_roots(), Directories an absolute Python import is resolved from: the repo root, plus the…, Map an import to a repo file id if the module resolves inside the repo.…, Build a structure graph for a repo in ANY language, zero dependencies (see…, _resolve_import(), scan_repo(), _names(), Multi-language scanner: the declarative engine (langspec) and its wiring into… (+12 more)

### Community 102 - "subsystem-src.md"
Cohesion: 0.40
Nodes (4): How the work is divided, What it depends on, and what depends on it, What this area is responsible for, Where to start reading

### Community 103 - "src-isidore-citations_py.md"
Cohesion: 0.33
Nodes (5): Architecture, Dependencies, How to change safely, Key entry points, Purpose

### Community 104 - "render.py"
Cohesion: 0.09
Nodes (42): _cmd_llms(), configured_wiki_dirname(), _first_sentence(), Path, Deterministic outputs: quickstart.md, index.toon, llms.txt, and the AGENTS.md…, The wiki, in the layout agents are converging on for being handed…, Write llms.txt at the repo root — where the convention puts it, so a fetcher…, Where this repository keeps its living docs, relative to its root. Precedence:… (+34 more)

### Community 106 - "src-isidore-recertify_py.md"
Cohesion: 0.33
Nodes (5): Architecture, Dependencies, How to change safely, Key entry points, Purpose

### Community 107 - "src-isidore-render_py.md"
Cohesion: 0.33
Nodes (5): Architecture, Dependencies, How to change safely, Key entry points, Purpose

### Community 108 - "WhatsnewError"
Cohesion: 0.29
Nodes (7): RuntimeError, Git could not answer, or a ref does not resolve. Fail closed: never guess a…, WhatsnewError, Its prompts carry an excerpt of every added and changed symbol — a compile by…, test_whatsnew_refuses_at_an_undeclared_host(), test_execute_refuses_a_range_that_does_not_end_at_head(), test_unresolvable_ref_fails_closed()

### Community 111 - "test_hostile_f6.py"
Cohesion: 0.20
Nodes (20): home(), _item(), fixture, usefixtures, F6's hostile gate: what the knowledge home does when its own data is broken,…, A cap that bites silently turns a partial answer into a confident one., The whole point of I8, end to end: an item that issues commands and forges a…, The second half of the defence: even if a forged URI reaches a claim, it has to… (+12 more)

### Community 113 - "compile_subsystems"
Cohesion: 0.23
Nodes (12): compile_subsystems(), _facts_fp(), The page exists, is certified, and was compiled from the same facts. The…, Compile the N2 layer: one bounded call per area, each page chained to its…, subsystem_page_name(), _unchanged(), _nodes(), test_a_reshuffled_module_ranking_does_not_recompile_the_product_page() (+4 more)

### Community 114 - "Slack — instance recipe for the MCP connector"
Cohesion: 0.20
Nodes (9): Confirm the tool names before you trust this block, Setup, Slack — instance recipe for the MCP connector, Sources, The config, The part you should actually worry about, Verifying it works, What you get (+1 more)

### Community 115 - "GenerationError"
Cohesion: 0.17
Nodes (14): Request, A generator that answers from disk. Raises GenerationError when an answer is…, response_generator(), build_request(), generate(), generate_via_cli(), GenerationError, RuntimeError (+6 more)

### Community 116 - "pyramid.py"
Cohesion: 0.09
Nodes (30): certificate_from_dict(), get_verifier(), parse_wiki_uri(), Protocol, Proof-Carrying Prose (PCP) — the frozen seam shared by every PCP lane. This…, A predicate verifier. MUST be deterministic and 0-LLM. Returns UNDECIDABLE,…, Dispatch one predicate to its registered verifier. No verifier -> UNDECIDABLE…, A reconciler finding (lane B): the model's own outputs contradict each other.… (+22 more)

### Community 117 - "test_wiki_not_input.py"
Cohesion: 0.16
Nodes (14): degenerate_certificate(), A short reason when a certificate is a symptom rather than a certificate, else…, _Cert, nested_wiki_dir(), fixture, The wiki is OUTPUT. It must never round-trip into the input. Reported from GIMO…, GIMO's actual numbers. Writing this silently is how it reached 13 MB before…, Point the toolchain at GIMO's layout. WIKI_DIRNAME is resolved once at import… (+6 more)

### Community 120 - "generate_prose"
Cohesion: 0.17
Nodes (12): annotate_unverified_paths(), Annotate every cited path that does not exist in the repo, inline and visibly —…, generate_prose(), _group_by_module(), parse_plain_block(), Split the plain-language block out of a model answer -> (rest, plain text,…, Drop the pipe-separated citation a model appends to its own bullets. Observed…, One bounded call per changed module -> (developer prose, plain-language,… (+4 more)

### Community 121 - "src-isidore-connect_py.md"
Cohesion: 0.33
Nodes (5): Architecture, Dependencies, How to change safely, Key entry points, Purpose

### Community 123 - "test_pyramid.py"
Cohesion: 0.29
Nodes (9): plan_pyramid(), Plan deterministic N2 subsystem + N3 product pages. 0 LLM. Explicit…, _graph(), Lane D gate — the pyramid plans from the real graph, uses imports for cohesion,…, BUG 1 regression: auto-seed used node['path'/'file'/'name'] (absent) -> [].…, BUG 2 regression: `links` was ignored. imports edges must yield depends_on., test_autoseed_groups_by_source_file_on_the_real_graph(), test_explicit_config_still_works() (+1 more)

### Community 124 - "test_units.py"
Cohesion: 0.15
Nodes (16): _git_repo(), _qa_repo(), Unit tests: toon encoder, graph scanner, findings residue, QA retrieval, LLM…, A third-party graph (e.g. Graphify) that indexed a gitignored path gets cleaned…, Outside a git tree we cannot tell what's ignored -> index everything, unchanged., Init a minimal git repo at `path`; skip the test if git is unavailable., The reported GIMO bug: a gitignored build-artifact copy must NOT be indexed as…, test_ask_uses_single_injected_generator_call() (+8 more)

### Community 126 - "repo_with_module_page"
Cohesion: 0.67
Nodes (3): fixture, The module page above, registered in the wiki state so an area can find it., repo_with_module_page()

### Community 128 - "read_contracts"
Cohesion: 0.13
Nodes (22): _cmd_contracts(), Add `isidore contracts` (promote / list / check)., Command implementation for `isidore contracts`., register_cli(), Contract, Path, Load promoted contracts (empty list if the file is absent). Malformed ->…, Persist contracts as JSON (machine-read gate input). (+14 more)

### Community 129 - "src-isidore-revise_py.md"
Cohesion: 0.33
Nodes (5): Architecture, Dependencies, How to change safely, Key entry points, Purpose

### Community 133 - "src-isidore-handoff_py.md"
Cohesion: 0.33
Nodes (5): Architecture, Dependencies, How to change safely, Key entry points, Purpose

## Knowledge Gaps
- **221 isolated node(s):** `isidore-wiki`, `Knowledge home (local, not in this repo)`, `Why`, `Quickstart`, `What you get` (+216 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **5 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `IngestOptions` connect `IngestOptions` to `store.py`, `cli.py`, `knowledge.py`, `_JsonRpcClient`, `connect.py`, `test_hostile_f6.py`, `iter_items`, `hackernews.py`, `test_mcp_barrier.py`?**
  _High betweenness centrality (0.104) - this node is a cross-community bridge._
- **Why does `compile_wiki()` connect `compile_wiki` to `test_handoff.py`, `graph.py`, `findings.py`, `verify.py`, `emit`, `impact.py`, `claims.py`, `write_scan`, `qa.py`, `citations.py`, `build_cards`, `anchor_claims`, `humanpack.py`, `test_security_prose.py`, `test_source_disclosure_gate.py`, `read_certificate`, `encode`, `cli.py`, `knowledge.py`, `plan_pages`, `parse_claims_block`, `harvest_todos`, `test_incremental.py`, `pipeline.py`, `is_negative_existential`, `write_certificate`, `test_pcp_pipeline.py`, `render.py`, `GenerationError`, `pyramid.py`, `test_wiki_not_input.py`, `generate_prose`?**
  _High betweenness centrality (0.072) - this node is a cross-community bridge._
- **Why does `VerifyContext` connect `verify.py` to `read_contracts`, `write_certificate`, `compile_wiki`, `DeltaEntry`, `emit`, `plan_pages`, `whatsnew.py`, `test_whatsnew.py`, `parse_claims_block`, `WhatsnewError`, `compile_subsystems`, `pyramid.py`, `humanpack.py`, `compile_overview`, `pipeline.py`, `test_pcp_seams.py`, `Predicate`, `read_certificate`?**
  _High betweenness centrality (0.037) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `compile_wiki()` (e.g. with `read_excerpt()` and `test_a_page_with_no_usable_certificate_never_stampedes_a_recompile()`) actually correct?**
  _`compile_wiki()` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Are the 7 inferred relationships involving `VerifyContext` (e.g. with `CompileResult` and `PageSpec`) actually correct?**
  _`VerifyContext` has 7 INFERRED edges - model-reasoned connections that need verification._
- **Are the 9 inferred relationships involving `IngestOptions` (e.g. with `GitRepoConnector` and `HackerNewsConnector`) actually correct?**
  _`IngestOptions` has 9 INFERRED edges - model-reasoned connections that need verification._
- **What connects `isidore-wiki`, `Knowledge home (local, not in this repo)`, `Why` to the rest of the system?**
  _221 weakly-connected nodes found - possible documentation gaps or missing edges._