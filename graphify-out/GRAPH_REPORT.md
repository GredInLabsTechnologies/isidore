# Graph Report - isidore  (2026-11-02)

## Corpus Check
- 169 files · ~146,779 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 2004 nodes · 4778 edges · 109 communities (104 shown, 5 thin omitted)
- Extraction: 97% EXTRACTED · 3% INFERRED · 0% AMBIGUOUS · INFERRED: 164 edges (avg confidence: 0.66)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `c30c908e`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- test_handoff.py
- graph.py
- compile_wiki
- test_units.py
- IngestOptions
- verify.py
- prompt_id
- quickstart.md
- test_whatsnew.py
- impact.py
- claims.py
- load_graph
- write_certificate
- qa.py
- repoint
- test_connectors_f1.py
- anchor_claims
- Isidore v2 — Incremental compilation, impact detection & residue mining
- test_surface.py
- iter_items
- store.py
- humanpack.py
- ValueError
- test_security_prose.py
- test_source_disclosure_gate.py
- connect.py
- Predicate
- test_mcp_barrier.py
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
- pipeline.py
- test_wiki_dir_env.py
- _JsonRpcClient
- main
- parse_claims_block
- clean_sig
- test_residue.py
- citations.py
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
- revise.py
- _make_repo
- compile_subsystems
- test_langspec.py
- src-isidore-plain_py.md
- src-isidore-toon_py.md
- is_negative_existential
- overview.md
- surface.py
- recertify.py
- test_pcp_pipeline.py
- knowledge.py
- _cmd_pyramid
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
- reconcile.py
- is_test_path
- scan_repo
- subsystem-src.md
- src-isidore-citations_py.md
- configured_wiki_dirname
- src-isidore-recertify_py.md
- src-isidore-render_py.md
- test_hostile_f6.py
- Slack — instance recipe for the MCP connector
- GenerationError
- pyramid.py
- test_wiki_not_input.py
- generate_prose
- src-isidore-connect_py.md
- test_pyramid.py
- repo_with_module_page
- pcp.py
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
- `test_split_evidence_src()` --calls--> `_split_evidence()`  [EXTRACTED]
  tests/test_knowledge.py → src/isidore/claims.py
- `test_every_ingested_item_can_be_cited()` --calls--> `evidence_hash()`  [INFERRED]
  tests/test_connectors_f4.py → src/isidore/claims.py
- `test_the_mail_item_is_citable_end_to_end()` --calls--> `evidence_hash()`  [INFERRED]
  tests/test_connectors_f5.py → src/isidore/claims.py
- `test_carry_claims_skips_refuted_and_unanchored_claims()` --calls--> `evidence_hash()`  [INFERRED]
  tests/test_incremental.py → src/isidore/claims.py

## Import Cycles
- None detected.

## Communities (109 total, 5 thin omitted)

### Community 0 - "test_handoff.py"
Cohesion: 0.14
Nodes (36): apply(), emit(), handoff_dir(), Path, Compile using the written answers. Identical pipeline to any other provider., Write one prompt file per dirty page. Returns (count, page names)., A generator that answers from disk. Raises GenerationError when an answer is…, response_generator() (+28 more)

### Community 1 - "graph.py"
Cohesion: 0.13
Nodes (28): git_head(), git_listed_files(), _is_binary(), _is_wiki_output(), isidore_ignored(), _iter_source_files(), _node_id(), _norm_source_file() (+20 more)

### Community 2 - "compile_wiki"
Cohesion: 0.12
Nodes (46): compile_wiki(), context_hash(), lint_cited_paths(), plan_pages(), prompt_for(), Module pages from the graph: top-K modules holding at least min_symbols code…, Content-addressed page identity: same prompt -> nothing to regenerate., File-looking paths cited in the prose that do NOT exist in the repo. (+38 more)

### Community 3 - "test_units.py"
Cohesion: 0.07
Nodes (43): _cmd_findings(), _churn(), _comment_lines(), coverage_gap_candidates(), filter_findings(), finding_id(), findings_new(), harvest_todos() (+35 more)

### Community 4 - "IngestOptions"
Cohesion: 0.08
Nodes (30): IngestOptions, Caps and scoping for a run. All limits live here (in code), never in a prompt., (content with any delimiter-shaped line defanged, how many were found). Marked…, seal_content(), isolated_home(), fixture, usefixtures, F4 (ADR-0032): RSS, Hacker News and web-search — plus the injection defence… (+22 more)

### Community 5 - "verify.py"
Cohesion: 0.09
Nodes (52): AST, Module, The result of checking one predicate against an oracle. `value` is…, Everything a verifier needs, assembled once per page/verify run. Read-only to…, undecidable(), Verdict, VerifyContext, literal_value() (+44 more)

### Community 6 - "prompt_id"
Cohesion: 0.67
Nodes (3): prompt_id(), Content identity of a prompt. The pairing key, so a response can only answer…, test_prompt_id_is_content_identity()

### Community 7 - "quickstart.md"
Cohesion: 0.33
Nodes (4): Knowledge home (local, not in this repo), Wiki (isidore), Modules, Wiki (isidore)

### Community 8 - "test_whatsnew.py"
Cohesion: 0.10
Nodes (41): RuntimeError, Git could not answer, or a ref does not resolve. Fail closed: never guess a…, Build the delta, optionally write the prose, and persist page + certificate., run_whatsnew(), WhatsnewError, WhatsnewResult, Its prompts carry an excerpt of every added and changed symbol — a compile by…, test_whatsnew_refuses_at_an_undeclared_host() (+33 more)

### Community 9 - "impact.py"
Cohesion: 0.09
Nodes (38): affected_modules(), changed_lines(), changed_symbols(), _git_diff(), _module_fan_in(), modules_of(), Path, Change-set detection: which graph symbols a git diff touched, and which modules… (+30 more)

### Community 10 - "claims.py"
Cohesion: 0.18
Nodes (23): check_claims(), claims_for_file(), claims_grep(), evidence_hash(), evidence_state(), Path, Claims: the atomic, evidence-anchored form of wiki knowledge. A claim is a…, Fingerprint of the CITED LINE's normalized content (whole normalized file if no… (+15 more)

### Community 11 - "load_graph"
Cohesion: 0.12
Nodes (23): _cmd_scan(), load_graph(), Run the scanner and persist the graph to .isidore/graph.json., write_scan(), overview_facts(), The project's own words about itself — CONTEXT, never evidence (see…, Everything the overview is allowed to be written from. 0 LLM., _readme_context() (+15 more)

### Community 12 - "write_certificate"
Cohesion: 0.12
Nodes (27): After citations moved, the page's certificate must describe the new bytes: same…, reprose_certificate(), Certificate, certificate_to_dict(), ClaimVerdict, prose_hash(), One claim's line in a certificate: the anchored claim + its typed verdict (if…, The re-verifiable sidecar for one page. Persisted as JSON (machine-read).… (+19 more)

### Community 13 - "qa.py"
Cohesion: 0.12
Nodes (24): isidore — compile an agent-oriented wiki from your codebase's structure graph.…, answer_knowledge_offline(), answer_offline(), ask(), ask_knowledge(), gather_claims(), gather_evidence(), gather_knowledge_claims() (+16 more)

### Community 14 - "repoint"
Cohesion: 0.12
Nodes (32): anchors_for(), _definition_lines(), _Files, _matches(), migrate_by_symbol(), Match, Path, `path:line` -> fingerprint for every citation of an existing file (UNANCHORED… (+24 more)

### Community 15 - "test_connectors_f1.py"
Cohesion: 0.13
Nodes (16): GitRepoConnector, (item, None) for a changed repo, (None, None) if HEAD is unchanged, (None,…, Run a git command; return stdout or None on any failure (never raises)., _git(), _head(), _make_repo(), parametrize, F1 (ADR-0032): knowledge home + raw store + git-repo connector. The load-… (+8 more)

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
Nodes (38): BaseHTTPRequestHandler, _allowed(), McpConnector, Normalise the allowlist into `{entry, arguments}` records, sorted for…, iter_items(), Yield stored items, newest run first. A corrupt/half-written JSONL line is…, Run ids from state (already newest-first); fall back to sorting the raw dir if…, _run_ids_newest_first() (+30 more)

### Community 20 - "store.py"
Cohesion: 0.07
Nodes (67): Exception, IngestResult, Outcome of one ingest run. `raw_files` are the JSONL files written this run., A connector's persisted config, or {} if absent or corrupt. Never raises. Lives…, stored_config(), git-repo connector (ADR-0032 F1): local repositories as a knowledge source. No…, _as_list(), feed_url() (+59 more)

### Community 21 - "humanpack.py"
Cohesion: 0.07
Nodes (52): _looks_like_secret(), Path, Lane C — deterministic security detectors: entropy, sinks, topology. 0 LLM.…, Entropy + sink marks for one file. Never raises (unreadable file -> no marks)., Files reachable from an auth/secret/crypto root via imports (BFS, file-level).…, Run all three detector families over the repo -> deterministic marks. Pure,…, Shannon entropy per character (bits). Stdlib only., Return a reason if the literal is credential-shaped, else None. (+44 more)

### Community 22 - "ValueError"
Cohesion: 0.15
Nodes (15): parse_hits(), The `hits` array, or ValueError. A payload without one is malformed, not empty…, _link(), _local(), parse_feed(), First non-empty child whose local tag is one of `names`, stripped., RSS puts the URL in <link>'s text; Atom puts it in <link href=...>, sometimes…, (feed title, entries) from RSS 2.0 or Atom. Raises ValueError on XML that will… (+7 more)

### Community 23 - "test_security_prose.py"
Cohesion: 0.09
Nodes (27): insert_security_banner(), is_security_finding(), True if a suspect reads as a security risk (hardcoded secret, auth bypass,…, A prominent, deterministic banner listing this page's security suspects — meant…, Place the banner right under the page's H1 (or at the very top if there is…, security_banner(), security_suspects(), Verify that negation patterns do not trigger false positive security findings… (+19 more)

### Community 24 - "test_source_disclosure_gate.py"
Cohesion: 0.10
Nodes (30): assert_may_send_source(), Classify wherever a compile would send this repository's source, as (kind,…, Fail closed unless the destination may see this repository's content. `what`…, source_destination(), clean_env(), _gp(), _make_repo(), fixture (+22 more)

### Community 25 - "connect.py"
Cohesion: 0.18
Nodes (20): _cmd_connect(), _cmd_ingest(), connector_summary(), load_config(), `isidore connect` and `isidore ingest` — the CLI face of the connector layer…, Add `isidore connect` and `isidore ingest` (registrar loop in cli.main)., A connector's stored config, or {} if absent/corrupt. Never raises., One row of `connect --list`: what it is, whether it can run, and what it has… (+12 more)

### Community 26 - "Predicate"
Cohesion: 0.17
Nodes (24): Predicate, A decidable assertion parsed from a claim's third field. Frozen: predicates are…, parameter_names(), Parameter names in declaration order, or None when they cannot be read with…, value(name, literal): a module-level assignment `name = literal`. Oracles: AST,…, signature(fn, a1, a2, ...): fn's positional parameter names, in order. Oracles:…, v_signature(), v_value() (+16 more)

### Community 27 - "test_mcp_barrier.py"
Cohesion: 0.15
Nodes (14): _name_looks_mutating(), (allowed, reason). Authority order: explicit readOnlyHint/destructiveHint >…, Fallback heuristic ONLY (not exhaustive): does the tool name contain a mutating…, _tool_read_only(), _FakeClient, parametrize, MCP connector read-only barrier (ADR-0032 F3). Regression for the review of…, Stands in for _JsonRpcClient: a server exposing one read tool, one write tool… (+6 more)

### Community 28 - "PCP_SEAMS — the frozen interface for Proof-Carrying Prose (ADR-0033, phase P0)"
Cohesion: 0.15
Nodes (12): Certificate (`<page>.md` → `<page>.md.cert.json`, alongside the page), CLI, Contracts (`contracts.json` in the wiki dir), File ownership matrix (nobody edits another lane's files), How each lane starts (all depend ONLY on P0 = T-1dc9), Marks (lane C output; also the golden `marks.json`), PCP_SEAMS — the frozen interface for Proof-Carrying Prose (ADR-0033, phase P0), Pipeline hooks (lane A wires; signatures frozen) (+4 more)

### Community 29 - "read_certificate"
Cohesion: 0.14
Nodes (34): certificate_from_dict(), Rebuild a Certificate from parsed JSON, reconstructing the nested dataclasses.…, Load a certificate from disk. Raises ValueError on malformed JSON (fail-closed…, read_certificate(), VerifiedMass, Re-run the oracles over every certified page. 0 LLM. Writes only with…, recertify(), _cert() (+26 more)

### Community 30 - "check"
Cohesion: 0.13
Nodes (19): check(), explain(), is_plain(), PlainRule, Pattern, Plain-language gate: can a reader who has never seen code use this sentence?…, Human-readable reason for a rejection, for the run summary and the journal., One named check. `kind` mirrors Vale's rule taxonomy so the intent of each is… (+11 more)

### Community 31 - "render.py"
Cohesion: 0.16
Nodes (17): agents_md_block(), Deterministic outputs: quickstart.md, index.toon, llms.txt, and the AGENTS.md…, The self-reference an agent reads before touching the repo. 0 LLM, idempotent.…, Insert or replace the delimited block without touching the rest of the file…, render_quickstart(), render_toon_index(), upsert_agents_block(), encode() (+9 more)

### Community 32 - "isidore"
Cohesion: 0.11
Nodes (17): Bring your own graph, Config (`isidore.json`, optional), Design rules, isidore, Knowledge — the same contract, applied to what is NOT in your repo, Languages, License, One range, three readers (+9 more)

### Community 33 - "auth.py"
Cohesion: 0.32
Nodes (6): authenticate(), Auth service fixture for PCP lane tests. Line numbers are load-bearing: the…, Verify the caller's JWT and enforce the attempt ceiling., Token service fixture for PCP lane tests. verify_jwt is defined on L5 (cited by…, Return the decoded claims if the token's signature checks out, else None., verify_jwt()

### Community 35 - "cli.py"
Cohesion: 0.16
Nodes (21): _cmd_ask(), _cmd_compile(), _cmd_impact(), _cmd_suggest_flows(), isidore — compile an agent-oriented wiki from your codebase's structure graph.…, Precedence: explicit CLI arg > isidore.json > built-in default., _setting(), find_graph() (+13 more)

### Community 36 - "Gmail — instance recipe for the MCP connector"
Cohesion: 0.12
Nodes (14): Gmail — instance recipe for the MCP connector, Sources, The config, The part you should actually worry about, Verifying it works, What it costs you to set up, What you get, Where the caps live (+6 more)

### Community 37 - "assemble_topic_context"
Cohesion: 0.15
Nodes (24): assemble_topic_context(), data_fence(), item_classification(), provider_is_trusted(), A per-assembly nonce for the excerpt delimiter. Ingested content is attacker-…, An item's confidentiality: `meta.classification`, else `classification:` in its…, Whether the operator has declared the configured LLM provider fit to receive…, Assemble items matching streams and filters into citable facts. External… (+16 more)

### Community 38 - "pipeline.py"
Cohesion: 0.09
Nodes (30): append_run(), Compile journal + per-page changelog — residue mining, all zero-LLM. Every…, Map each `## heading` to its body text (content before the first heading is…, (H2 headings whose content changed / were added / removed, new_line_count -…, Append an H2-level changelog entry to a page's state (capped). No-op if the…, record_page_change(), section_diff(), _sections() (+22 more)

### Community 39 - "test_wiki_dir_env.py"
Cohesion: 0.31
Nodes (7): ISIDORE_WIKI_DIR redirects the compiled-wiki output directory. WIKI_DIRNAME is…, A nested WIKI_DIRNAME (e.g. doc/isidore) must create its parents, not crash., _reload_render(), test_save_state_creates_nested_wiki_dir(), test_wiki_dirname_blank_env_falls_back(), test_wiki_dirname_defaults_to_wiki(), test_wiki_dirname_honors_env()

### Community 40 - "_JsonRpcClient"
Cohesion: 0.12
Nodes (11): _JsonRpcClient, Any, Map tool name -> its MCP annotations via tools/list (paginated). Empty if the…, JSON-RPC 2.0 over the two MCP transports (spec 2025-06-18, basic/transports).…, The response to `want_id` if `message` is (or, as a batch, holds) it. Anything…, A server may ask the client something mid-request (`ping`, `roots/list`,…, Read SSE events until the one carrying the reply to `want_id`. Each event's…, The readable text of an MCP tool result, falling back to compact JSON. MCP… (+3 more)

### Community 41 - "main"
Cohesion: 0.07
Nodes (46): main(), apply_settings(), parse_setting(), Path, Write a connector's config with the home's restrictive permissions., `key=value` -> (key, value). A value that parses as JSON is stored as JSON, so…, Fold `key=value` settings into a config. Repeating a key ACCUMULATES into a…, save_config() (+38 more)

### Community 42 - "parse_claims_block"
Cohesion: 0.17
Nodes (17): parse_claims_block(), parse_predicate_field(), Parse a claim's optional third field into a pcp.Predicate (or None). PCP typed-…, Split a generated page into (clean page, raw claim rows). Tolerant of malformed…, _anchored(), _ctx(), Lane A gate — the typed-claim verifiers decide truth against the two oracles,…, A predicate names a function, not a file, and helpers repeat across test… (+9 more)

### Community 43 - "clean_sig"
Cohesion: 0.18
Nodes (11): clean_sig(), AsyncFunctionDef, _py_constant(), FunctionDef, _py_signature(), Collapse a declaration header into a stable one-line comparison key, readable…, The parameter list and return annotation, rendered from the AST rather than the…, A module-level binding -> (name, `= value`). Config constants are API: a… (+3 more)

### Community 44 - "test_residue.py"
Cohesion: 0.20
Nodes (13): Counter, _cmd_stats(), render_findings(), render_stats(), _git(), Residue-mining units: section diff, compile journal/stats, per-page history,…, _repo(), test_claims_for_file_and_grep() (+5 more)

### Community 45 - "citations.py"
Cohesion: 0.27
Nodes (11): _fingerprint(), _inside_block(), Prose citations that follow the code they cite. A page cites code as…, Is line `n` in the indented body of the definition on line `start`?, Where the anchored line is now: its window, nearest first; failing that, the…, _relocate(), _window(), _hash() (+3 more)

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
Cohesion: 0.10
Nodes (47): _cmd_export_agora(), build_cards(), Path, export-agora — bridge isidore's verified claims into Living-Library card DRAFTS…, Return [(filename, content)] draft cards — one per wiki page with enough OK…, render_card(), _slug(), write_cards() (+39 more)

### Community 55 - "compile_overview"
Cohesion: 0.12
Nodes (26): compile_overview(), missing_sections(), _overview_identity(), What the product page is written FROM: the README and the proven claims. Not…, Required headings the page does not have. 0 LLM., Turn `wiki://page` into `page` in PROSE, so the links a reader clicks actually…, Compile the plain-language product page (N3). One LLM call, plus at most one…, relink_wiki_uris() (+18 more)

### Community 56 - "revise.py"
Cohesion: 0.11
Nodes (20): carry_claims(), _excerpt_code(), facts_delta(), facts_fingerprint(), facts_record(), _h(), Path, Incremental page updates: change only what changed, keep the rest byte for… (+12 more)

### Community 57 - "_make_repo"
Cohesion: 0.29
Nodes (6): _make_repo(), fixture, Path, Three modules of twelve symbols each — over `min_symbols`, so each earns its…, No provider, no key, no network — the loop must work with nothing configured., repo()

### Community 58 - "compile_subsystems"
Cohesion: 0.14
Nodes (21): save_state(), compile_subsystems(), _facts_fp(), _module_pages_of(), _page_purpose(), _prune_areas(), Path, The compiled module pages that belong to one subsystem, keyed by page file name. (+13 more)

### Community 59 - "test_langspec.py"
Cohesion: 0.22
Nodes (15): extract(), _Pending, Extract (symbols, imported-module-names) from one file's source. symbols:…, The LanguageSpec for a file extension (lowercased), or None if we do not…, spec_for(), _names(), Multi-language scanner: the declarative engine (langspec) and its wiring into…, test_bodiless_declaration_stays_start_only() (+7 more)

### Community 60 - "src-isidore-plain_py.md"
Cohesion: 0.33
Nodes (5): Architecture, Dependencies, How to change safely, Key entry points, Purpose

### Community 61 - "src-isidore-toon_py.md"
Cohesion: 0.33
Nodes (5): Architecture, Dependencies, How to change safely, Key entry points, Purpose

### Community 62 - "is_negative_existential"
Cohesion: 0.67
Nodes (3): is_negative_existential(), True for statements asserting existential/definitional ABSENCE (unanchorable).…, test_is_negative_existential_flags_absence_not_behavior()

### Community 63 - "overview.md"
Cohesion: 0.50
Nodes (3): How the pieces fit together, What this is, What you can do with it

### Community 64 - "surface.py"
Cohesion: 0.09
Nodes (32): _brace(), _doc(), _js(), _kw_func(), _kw_type(), LanguageSpec, Pattern, Language-agnostic symbol extraction: one engine, the language is *data*.… (+24 more)

### Community 65 - "recertify.py"
Cohesion: 0.09
Nodes (31): cert_file_digest(), parse_stored_predicate(), Parse a predicate read back from a CERTIFICATE rather than from model output.…, sha256 of a certificate FILE as a pyramid page records it, line endings…, _child_digest(), _cmd_recertify(), PageRecert, Path (+23 more)

### Community 66 - "test_pcp_pipeline.py"
Cohesion: 0.29
Nodes (10): _compile(), _fake_generator(), _fake_generator_with_a_lie(), Path, P-INT gate — the pipeline wiring ties all five PCP lanes together end to end: a…, test_compile_writes_a_certificate_with_typed_verdicts(), test_deterministic_mark_forces_the_banner_despite_calm_prose(), test_refuted_claim_is_quarantined_not_published() (+2 more)

### Community 67 - "knowledge.py"
Cohesion: 0.12
Nodes (31): _cmd_sync(), config_path(), connector_dir(), home(), knowledge_dir(), Path, The knowledge home (`~/.isidore`, override with `ISIDORE_HOME`). Where…, `$ISIDORE_HOME` if set, else `~/.isidore`. (+23 more)

### Community 68 - "_cmd_pyramid"
Cohesion: 0.33
Nodes (7): _cmd_overview(), _cmd_pyramid(), _cmd_subsystems(), _load_graph_for(), Add `isidore pyramid` (plan/preview) and `isidore overview` (the N3 product…, Print a deterministic JSON plan for humans and scripts., register_cli()

### Community 69 - "build_delta"
Cohesion: 0.09
Nodes (27): build_delta(), DeltaEntry, _diff_surfaces(), _file_summary(), impact_summary(), _llm_entries(), _md_section(), One typed novelty row. `file` is always the path as of `until` (renames map old… (+19 more)

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

### Community 89 - "reconcile.py"
Cohesion: 0.32
Nodes (7): A reconciler finding (lane B): the model's own outputs contradict each other.…, Violation, Lane B (part 1) — the reconciler: the model's own outputs cross-checked, 0 LLM.…, Helper to split file:line into (file, line)., Cross-check prose vs findings vs claims vs marks -> internal contradictions.…, reconcile(), _split_evidence()

### Community 90 - "is_test_path"
Cohesion: 0.40
Nodes (5): is_test_path(), Is this file part of a test suite rather than of the product? By the…, parametrize, test_product_files_are_not(), test_test_files_are_recognised_across_languages()

### Community 101 - "scan_repo"
Cohesion: 0.10
Nodes (21): python_import_roots(), Directories an absolute Python import is resolved from: the repo root, plus the…, Map an import to a repo file id if the module resolves inside the repo.…, Build a structure graph for a repo in ANY language, zero dependencies (see…, _resolve_import(), scan_repo(), test_scan_repo_is_multilanguage(), test_scan_repo_resolves_python_imports_the_way_python_does() (+13 more)

### Community 102 - "subsystem-src.md"
Cohesion: 0.40
Nodes (4): How the work is divided, What it depends on, and what depends on it, What this area is responsible for, Where to start reading

### Community 103 - "src-isidore-citations_py.md"
Cohesion: 0.33
Nodes (5): Architecture, Dependencies, How to change safely, Key entry points, Purpose

### Community 104 - "configured_wiki_dirname"
Cohesion: 0.09
Nodes (40): _cmd_llms(), configured_wiki_dirname(), _first_sentence(), Path, The wiki, in the layout agents are converging on for being handed…, Write llms.txt at the repo root — where the convention puts it, so a fetcher…, Where this repository keeps its living docs, relative to its root. Precedence:…, Add `isidore llms` (regenerate llms.txt from whatever is compiled). 0 LLM. (+32 more)

### Community 106 - "src-isidore-recertify_py.md"
Cohesion: 0.33
Nodes (5): Architecture, Dependencies, How to change safely, Key entry points, Purpose

### Community 107 - "src-isidore-render_py.md"
Cohesion: 0.33
Nodes (5): Architecture, Dependencies, How to change safely, Key entry points, Purpose

### Community 111 - "test_hostile_f6.py"
Cohesion: 0.20
Nodes (20): home(), _item(), fixture, usefixtures, F6's hostile gate: what the knowledge home does when its own data is broken,…, A cap that bites silently turns a partial answer into a confident one., The whole point of I8, end to end: an item that issues commands and forges a…, The second half of the defence: even if a forged URI reaches a claim, it has to… (+12 more)

### Community 114 - "Slack — instance recipe for the MCP connector"
Cohesion: 0.20
Nodes (9): Confirm the tool names before you trust this block, Setup, Slack — instance recipe for the MCP connector, Sources, The config, The part you should actually worry about, Verifying it works, What you get (+1 more)

### Community 115 - "GenerationError"
Cohesion: 0.21
Nodes (11): Request, build_request(), generate(), generate_via_cli(), GenerationError, RuntimeError, Single-provider LLM client (OpenAI-compatible), fail-closed by design. One…, The provider failed. No retry with a different model — fail closed. (+3 more)

### Community 116 - "pyramid.py"
Cohesion: 0.15
Nodes (16): parse_wiki_uri(), wiki://<page>#<claim-id> -> (page, claim_id), or None if it is not a wiki URI.…, _chain_verdicts(), _claim_verdict(), _norm(), Lane D — the pyramid: hierarchical synthesis with wiki:// claim chains. (T-af65…, 0-LLM subsystem suggester: group files by top directory (the isidore graph uses…, Resolve (verdict, state) for a cited claim. Truth comes from the page's… (+8 more)

### Community 117 - "test_wiki_not_input.py"
Cohesion: 0.11
Nodes (21): The repo-relative posix path of the wiki OUTPUT directory, normalised for…, wiki_output_prefix(), degenerate_certificate(), drop_wiki_output(), A short reason when a certificate is a symptom rather than a certificate, else…, Nodes that do not live inside the wiki output directory. The second barrier.…, _Cert, nested_wiki_dir() (+13 more)

### Community 120 - "generate_prose"
Cohesion: 0.17
Nodes (12): annotate_unverified_paths(), Annotate every cited path that does not exist in the repo, inline and visibly —…, generate_prose(), _group_by_module(), parse_plain_block(), Split the plain-language block out of a model answer -> (rest, plain text,…, Drop the pipe-separated citation a model appends to its own bullets. Observed…, One bounded call per changed module -> (developer prose, plain-language,… (+4 more)

### Community 121 - "src-isidore-connect_py.md"
Cohesion: 0.33
Nodes (5): Architecture, Dependencies, How to change safely, Key entry points, Purpose

### Community 123 - "test_pyramid.py"
Cohesion: 0.29
Nodes (9): plan_pyramid(), Plan deterministic N2 subsystem + N3 product pages. 0 LLM. Explicit…, _graph(), Lane D gate — the pyramid plans from the real graph, uses imports for cohesion,…, BUG 1 regression: auto-seed used node['path'/'file'/'name'] (absent) -> [].…, BUG 2 regression: `links` was ignored. imports edges must yield depends_on., test_autoseed_groups_by_source_file_on_the_real_graph(), test_explicit_config_still_works() (+1 more)

### Community 126 - "repo_with_module_page"
Cohesion: 0.67
Nodes (3): fixture, The module page above, registered in the wiki state so an area can find it., repo_with_module_page()

### Community 128 - "pcp.py"
Cohesion: 0.07
Nodes (44): _cmd_contracts(), Lane B (part 2) — claim->contract graduation + `isidore contracts`. (T-8dfc) A…, Check every promoted contract against the current graph. Pure, 0-LLM., Add `isidore contracts` (promote / list / check)., Command implementation for `isidore contracts`., register_cli(), verify_contracts(), Contract (+36 more)

### Community 129 - "src-isidore-revise_py.md"
Cohesion: 0.33
Nodes (5): Architecture, Dependencies, How to change safely, Key entry points, Purpose

### Community 133 - "src-isidore-handoff_py.md"
Cohesion: 0.33
Nodes (5): Architecture, Dependencies, How to change safely, Key entry points, Purpose

## Knowledge Gaps
- **222 isolated node(s):** `isidore-wiki`, `Knowledge home (local, not in this repo)`, `Why`, `Quickstart`, `What you get` (+217 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **5 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `IngestOptions` connect `IngestOptions` to `knowledge.py`, `cli.py`, `_JsonRpcClient`, `main`, `test_connectors_f1.py`, `test_hostile_f6.py`, `iter_items`, `store.py`, `connect.py`, `test_mcp_barrier.py`?**
  _High betweenness centrality (0.101) - this node is a cross-community bridge._
- **Why does `compile_wiki()` connect `compile_wiki` to `test_handoff.py`, `graph.py`, `test_units.py`, `verify.py`, `impact.py`, `claims.py`, `load_graph`, `write_certificate`, `qa.py`, `repoint`, `anchor_claims`, `humanpack.py`, `test_security_prose.py`, `test_source_disclosure_gate.py`, `read_certificate`, `render.py`, `cli.py`, `pipeline.py`, `parse_claims_block`, `test_residue.py`, `test_incremental.py`, `revise.py`, `compile_subsystems`, `recertify.py`, `test_pcp_pipeline.py`, `knowledge.py`, `reconcile.py`, `is_test_path`, `GenerationError`, `test_wiki_not_input.py`, `generate_prose`?**
  _High betweenness centrality (0.064) - this node is a cross-community bridge._
- **Why does `read_state()` connect `store.py` to `knowledge.py`, `IngestOptions`, `assemble_topic_context`, `main`, `test_hostile_f6.py`, `iter_items`, `connect.py`, `render.py`?**
  _High betweenness centrality (0.028) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `compile_wiki()` (e.g. with `read_excerpt()` and `test_a_page_with_no_usable_certificate_never_stampedes_a_recompile()`) actually correct?**
  _`compile_wiki()` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Are the 7 inferred relationships involving `VerifyContext` (e.g. with `CompileResult` and `PageSpec`) actually correct?**
  _`VerifyContext` has 7 INFERRED edges - model-reasoned connections that need verification._
- **Are the 9 inferred relationships involving `IngestOptions` (e.g. with `GitRepoConnector` and `HackerNewsConnector`) actually correct?**
  _`IngestOptions` has 9 INFERRED edges - model-reasoned connections that need verification._
- **What connects `isidore-wiki`, `Knowledge home (local, not in this repo)`, `Why` to the rest of the system?**
  _222 weakly-connected nodes found - possible documentation gaps or missing edges._