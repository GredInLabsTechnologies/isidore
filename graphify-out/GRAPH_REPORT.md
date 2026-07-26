# Graph Report - isidore  (2026-07-26)

## Corpus Check
- 202 files · ~130,366 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1790 nodes · 3950 edges · 135 communities (130 shown, 5 thin omitted)
- Extraction: 84% EXTRACTED · 16% INFERRED · 0% AMBIGUOUS · INFERRED: 637 edges (avg confidence: 0.77)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `d5d1a1f3`
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
- anchor_claims
- apply_settings
- encode
- test_vigil.py
- GitRepoConnector
- ValueError
- tests-test_connectors_f5_py.md
- generate_prose
- _cap_content
- harvest_todos
- render_findings

## God Nodes (most connected - your core abstractions)
1. `compile_wiki()` - 85 edges
2. `VerifyContext` - 62 edges
3. `IngestOptions` - 51 edges
4. `Predicate` - 35 edges
5. `_make_repo()` - 31 edges
6. `run_whatsnew()` - 29 edges
7. `load_graph()` - 28 edges
8. `read_state()` - 27 edges
9. `build_delta()` - 26 edges
10. `write_items()` - 25 edges

## Surprising Connections (you probably didn't know these)
- `test_three_field_parser_captures_predicate()` --calls--> `parse_claims_block()`  [INFERRED]
  tests/test_verify.py → src/isidore/claims.py
- `test_an_unknown_connector_is_named_not_ignored()` --calls--> `main()`  [INFERRED]
  tests/test_connect_cli.py → src/isidore/cli.py
- `test_pcp_subcommands_are_registered()` --calls--> `main()`  [INFERRED]
  tests/test_pcp_seams.py → src/isidore/cli.py
- `test_cli_reports_a_bad_ref_without_writing_an_artifact()` --calls--> `main()`  [INFERRED]
  tests/test_whatsnew.py → src/isidore/cli.py
- `test_cli_smoke()` --calls--> `main()`  [INFERRED]
  tests/test_whatsnew.py → src/isidore/cli.py

## Import Cycles
- 1-file cycle: `src/isidore/connectors/__init__.py -> src/isidore/connectors/__init__.py`

## Communities (135 total, 5 thin omitted)

### Community 0 - "cli.py"
Cohesion: 0.21
Nodes (19): _cmd_ask(), _cmd_compile(), _cmd_impact(), _cmd_scan(), _cmd_stats(), _cmd_suggest_flows(), _cmd_sync(), main() (+11 more)

### Community 1 - "graph.py"
Cohesion: 0.16
Nodes (22): git_head(), git_listed_files(), _is_binary(), _iter_source_files(), _node_id(), _norm_source_file(), Path, Structure graph: loading, module grouping, and a built-in multi-language scanner (+14 more)

### Community 2 - "compile_wiki"
Cohesion: 0.20
Nodes (28): compile_wiki(), Run the pipeline. With execute=False no LLM is called and no page is written., _gp(), _link(), _make_repo(), _node(), Path, Compiler pipeline tests — no network: the LLM generator is always injected and c (+20 more)

### Community 3 - "read_certificate"
Cohesion: 0.67
Nodes (3): coverage_gap_candidates(), Module pages with no inbound link from any test-looking module., test_orphan_and_coverage_gap_candidates()

### Community 4 - "detectors.py"
Cohesion: 0.07
Nodes (23): IngestOptions, Caps and scoping for a run. All limits live here (in code), never in a prompt., F4 (ADR-0032): RSS, Hacker News and web-search — plus the injection defence they, Measured live on hnrss.org at 4000 bytes: truncated XML never parses, and the ol, I6: a failed fetch must not advance anything, or the entries nobody read are ski, A search nobody ran must be reported as not run. 'success, 0 items' would read a, Providers echo the request back in error messages. A key in a log is impossible, The property the end-to-end path needs, asserted for all three connectors at onc (+15 more)

### Community 5 - "verify.py"
Cohesion: 0.12
Nodes (37): AST, Module, The result of checking one predicate against an oracle. `value` is TRUE|FALSE|UN, undecidable(), Verdict, _ast_of(), _decide(), _file_nodes() (+29 more)

### Community 6 - "humanpack.py"
Cohesion: 0.13
Nodes (27): _cmd_render(), _esc(), format_mark(), generate_architecture_map(), generate_claims_table(), generate_contracts_section(), generate_glossary(), generate_mass_bar() (+19 more)

### Community 7 - "quickstart.md"
Cohesion: 0.33
Nodes (4): Knowledge home (local, not in this repo), Wiki (isidore), Modules, Wiki (isidore)

### Community 8 - "findings.py"
Cohesion: 0.15
Nodes (27): Build the delta, optionally write the prose, and persist page + certificate., run_whatsnew(), WhatsnewResult, _commit(), _git(), _one_file_repo(), isidore whatsnew: the typed surface delta, its artifact, and the verification di, A repository mirroring the shape of the change that motivated this command: a me (+19 more)

### Community 9 - "module_of"
Cohesion: 0.10
Nodes (29): affected_modules(), changed_lines(), changed_symbols(), _git_diff(), _module_fan_in(), modules_of(), Path, Change-set detection: which graph symbols a git diff touched, and which modules (+21 more)

### Community 10 - "test_claims.py"
Cohesion: 0.19
Nodes (20): evidence_hash(), evidence_state(), _hash(), _normalize(), Path, Claims: the atomic, evidence-anchored form of wiki knowledge.  A claim is a si, Collapse all whitespace runs to single spaces and trim — so re-indentation, trai, Fingerprint of the CITED LINE's normalized content (whole normalized file if no (+12 more)

### Community 11 - "home.py"
Cohesion: 0.15
Nodes (27): _cmd_connect(), _cmd_ingest(), connector_summary(), load_config(), Path, `isidore connect` and `isidore ingest` — the CLI face of the connector layer (AD, Add `isidore connect` and `isidore ingest` (registrar loop in cli.main)., A connector's stored config, or {} if absent/corrupt. Never raises. (+19 more)

### Community 12 - "whatsnew.py"
Cohesion: 0.15
Nodes (14): DeltaEntry, impact_summary(), _md_section(), One typed novelty row. `file` is always the path as of `until` (renames map old, The consequence of this range, in plain words, with zero LLM calls.      A non-t, The machine/agent view: one table per area, product surface first., The page, layered by READER rather than by topic.      The same range has three, render_whatsnew_md() (+6 more)

### Community 13 - "build_certificate"
Cohesion: 0.13
Nodes (18): McpConnector, (content with any delimiter-shaped line defanged, how many were found).      Mar, seal_content(), test_innocent_content_is_left_exactly_as_it_was(), test_the_marking_removes_nothing_from_the_evidence(), _config(), Path, F5 (ADR-0032): the OAuth-heavy sources, delivered as MCP instance recipes rather (+10 more)

### Community 14 - "pyramid.py"
Cohesion: 0.29
Nodes (9): plan_pyramid(), Plan deterministic N2 subsystem + N3 product pages. 0 LLM.      Explicit `pyrami, _graph(), Lane D gate — the pyramid plans from the real graph, uses imports for cohesion,, BUG 1 regression: auto-seed used node['path'/'file'/'name'] (absent) -> []. Must, BUG 2 regression: `links` was ignored. imports edges must yield depends_on., test_autoseed_groups_by_source_file_on_the_real_graph(), test_explicit_config_still_works() (+1 more)

### Community 15 - "claims.py"
Cohesion: 0.08
Nodes (29): isidore — compile an agent-oriented wiki from your codebase's structure graph., append_run(), Append an H2-level changelog entry to a page's state (capped). No-op if the pros, record_page_change(), annotate_unverified_paths(), CompileResult, git_log_for(), lint_cited_paths() (+21 more)

### Community 16 - "surface.py"
Cohesion: 0.12
Nodes (26): Exception, _check_url(), fetch(), fetch_json(), FetchError, Bounded HTTP for the direct-API connectors (ADR-0032 F4). stdlib urllib, no depe, A fetch that did not produce a usable body. Carries a reason fit to show a user., Refuse anything that is not plain http(s).      urllib will happily open `file:/ (+18 more)

### Community 17 - "Isidore v2 — Incremental compilation, impact detection & residue mining"
Cohesion: 0.12
Nodes (16): 0 · Why (user directive), 1 · Verified bug diagnoses (2026-07-10, against real code — not reports), 2 · Design principles (unchanged bets, now enforced deeper), 3 · C0 — Scoped compile: `isidore compile --only <sel>[,<sel>…]`, 4 · C1+C2 — Change-driven compile: `isidore compile --changed [--since <ref>]`, 5 · C3 — Impact detection: `isidore impact [--since <ref>] [--md] [--check]` (new, **0 LLM always**), 6 · C4+C5+C6 — Correctness fixes (the right ones), 7 · C7 — Residue mining (all 0-LLM; the "squeeze everything" layer) (+8 more)

### Community 18 - "git_repo.py"
Cohesion: 0.26
Nodes (13): all_connectors(), Connector, get(), _load_plugins(), missing_env(), Protocol, Connector protocol + registry (ADR-0032 F1).  A connector ingests raw items from, Discover third-party connectors once. A broken entry-point warns and is skipped (+5 more)

### Community 19 - "VerifyContext"
Cohesion: 0.15
Nodes (16): _git_repo(), _qa_repo(), Unit tests: toon encoder, graph scanner, findings residue, QA retrieval, LLM req, A third-party graph (e.g. Graphify) that indexed a gitignored path gets cleaned, Init a minimal git repo at `path`; skip the test if git is unavailable., The reported GIMO bug: a gitignored build-artifact copy must NOT be indexed as s, test_ask_uses_single_injected_generator_call(), test_ask_without_evidence_refuses_instead_of_calling() (+8 more)

### Community 20 - "IngestOptions"
Cohesion: 0.14
Nodes (14): GitRepoConnector, (item, None) for a changed repo, (None, None) if HEAD is unchanged, (None, warni, Run a git command; return stdout or None on any failure (never raises)., _git(), _head(), _make_repo(), F1 (ADR-0032): knowledge home + raw store + git-repo connector.  The load-bearin, Regression: a real repo's commit messages carry UTF-8 (accents, emoji). On Windo (+6 more)

### Community 21 - "pipeline.py"
Cohesion: 0.18
Nodes (16): explain(), Human-readable reason for a rejection, for the run summary and the journal., _cmd_overview(), _cmd_pyramid(), _cmd_subsystems(), _load_graph_for(), _module_pages_of(), _norm() (+8 more)

### Community 22 - "mcp.py"
Cohesion: 0.22
Nodes (7): _allowed(), _JsonRpcClient, Any, Map tool name -> its MCP annotations via tools/list (paginated). Empty if the se, Normalise the allowlist into `{entry, arguments}` records, sorted for determinis, The readable text of an MCP tool result, falling back to compact JSON.      MCP, _result_text()

### Community 23 - "test_pcp_pipeline.py"
Cohesion: 0.06
Nodes (50): _cmd_findings(), _churn(), filter_findings(), finding_id(), findings_new(), harvest_todos(), insert_security_banner(), is_finding_resolved() (+42 more)

### Community 24 - "knowledge.py"
Cohesion: 0.10
Nodes (37): A connector's persisted config, or {} if absent or corrupt. Never raises.      L, stored_config(), git-repo connector (ADR-0032 F1): local repositories as a knowledge source. No n, Minimal read-only MCP connector (ADR-0032 F3).  The implementation deliberately, create_run_id(), iso_now(), prune_runs(), The raw store: immutable ingested items + per-connector cursor state (ADR-0032 F (+29 more)

### Community 25 - "plan_pages"
Cohesion: 0.15
Nodes (19): compile_overview(), missing_sections(), Required headings the page does not have. 0 LLM., Turn `wiki://page` into `page` in PROSE, so the links a reader clicks actually r, Compile the plain-language product page (N3). One LLM call, plus at most one rep, relink_wiki_uris(), The N3 product overview: plain language for anyone, resting on claims already pr, The module page above, registered in the wiki state so an area can find it. (+11 more)

### Community 26 - "pcp.py"
Cohesion: 0.17
Nodes (24): Predicate, A decidable assertion parsed from a claim's third field. Frozen: predicates are, parameter_names(), Parameter names in declaration order, or None when they cannot be read with conf, value(name, literal): a module-level assignment `name = literal`. Oracles: AST,, signature(fn, a1, a2, ...): fn's positional parameter names, in order. Oracles:, v_signature(), v_value() (+16 more)

### Community 27 - "_tool_read_only"
Cohesion: 0.15
Nodes (13): _name_looks_mutating(), (allowed, reason). Authority order: explicit readOnlyHint/destructiveHint > name, Fallback heuristic ONLY (not exhaustive): does the tool name contain a mutating, _tool_read_only(), _FakeClient, MCP connector read-only barrier (ADR-0032 F3). Regression for the review of T-db, Stands in for _JsonRpcClient: a server exposing one read tool, one write tool (a, test_destructive_hint_rejects() (+5 more)

### Community 28 - "PCP_SEAMS — the frozen interface for Proof-Carrying Prose (ADR-0033, phase P0)"
Cohesion: 0.15
Nodes (12): Certificate (`<page>.md` → `<page>.md.cert.json`, alongside the page), CLI, Contracts (`contracts.json` in the wiki dir), File ownership matrix (nobody edits another lane's files), How each lane starts (all depend ONLY on P0 = T-1dc9), Marks (lane C output; also the golden `marks.json`), PCP_SEAMS — the frozen interface for Proof-Carrying Prose (ADR-0033, phase P0), Pipeline hooks (lane A wires; signatures frozen) (+4 more)

### Community 29 - "encode"
Cohesion: 0.20
Nodes (26): Re-run the oracles over every certified page. 0 LLM. Writes only with `write=Tru, recertify(), _cert(), _chained(), _claim(), Path, `isidore recertify`: repair a certificate the code outgrew, and refuse to repair, A parent page resting on svc.md through a wiki:// chain, with the child hash rec (+18 more)

### Community 30 - "Mark"
Cohesion: 0.15
Nodes (17): check(), is_plain(), PlainRule, Pattern, Plain-language gate: can a reader who has never seen code use this sentence?  Do, One named check. `kind` mirrors Vale's rule taxonomy so the intent of each is de, Names of every rule the text breaks. Empty list = nothing disqualifying was foun, _vocabulary() (+9 more)

### Community 31 - "write_items"
Cohesion: 0.14
Nodes (16): _child_digest(), _cmd_recertify(), _level(), PageRecert, Path, `isidore recertify` — re-run the claim oracles over unchanged prose and rewrite, Add `isidore recertify` (called once from cli.main via the registrar loop)., Pyramid level, so children are recertified before the pages that cite them. (+8 more)

### Community 32 - "isidore"
Cohesion: 0.12
Nodes (16): Bring your own graph, Config (`isidore.json`, optional), Design rules, isidore, Knowledge — the same contract, applied to what is NOT in your repo, Languages, License, One range, three readers (+8 more)

### Community 33 - "auth.py"
Cohesion: 0.29
Nodes (6): authenticate(), Auth service fixture for PCP lane tests. Line numbers are load-bearing: the gold, Verify the caller's JWT and enforce the attempt ceiling., Token service fixture for PCP lane tests. verify_jwt is defined on L5 (cited by, Return the decoded claims if the token's signature checks out, else None., verify_jwt()

### Community 35 - "scan"
Cohesion: 0.09
Nodes (29): _looks_like_secret(), Path, Lane C — deterministic security detectors: entropy, sinks, topology. 0 LLM. (T-e, Files reachable from an auth/secret/crypto root via imports (BFS, file-level). 0, Run all three detector families over the repo -> deterministic marks. Pure, 0-LL, Shannon entropy per character (bits). Stdlib only., Return a reason if the literal is credential-shaped, else None., Repo-relative source files to scan: the graph's, or a bounded walk if the graph (+21 more)

### Community 36 - "assemble_context"
Cohesion: 0.12
Nodes (14): Gmail — instance recipe for the MCP connector, Sources, The config, The part you should actually worry about, Verifying it works, What it costs you to set up, What you get, Where the caps live (+6 more)

### Community 37 - "GenerationError"
Cohesion: 0.21
Nodes (21): load_knowledge_state(), answer_knowledge_offline(), answer_offline(), ask(), ask_knowledge(), gather_claims(), gather_evidence(), gather_knowledge_claims() (+13 more)

### Community 38 - "ClaimVerdict"
Cohesion: 0.08
Nodes (46): Match, clean_sig(), _declaration_tail(), extract_surface(), generic_surface(), _is_declaration(), _is_public(), logical_lines() (+38 more)

### Community 39 - "test_wiki_dir_env.py"
Cohesion: 0.31
Nodes (7): ISIDORE_WIKI_DIR redirects the compiled-wiki output directory.  WIKI_DIRNAME is, A nested WIKI_DIRNAME (e.g. doc/isidore) must create its parents, not crash., _reload_render(), test_save_state_creates_nested_wiki_dir(), test_wiki_dirname_blank_env_falls_back(), test_wiki_dirname_defaults_to_wiki(), test_wiki_dirname_honors_env()

### Community 40 - "test_reconcile.py"
Cohesion: 0.14
Nodes (21): is_negative_existential(), True for statements asserting existential/definitional ABSENCE (unanchorable). C, Pages owning at least one stale/orphan claim — they must regenerate even if thei, stale_pages(), parse_findings_block(), Split a generated page into (clean page, findings rows). Tolerant of malformed l, compile_topics(), data_fence() (+13 more)

### Community 41 - "test_humanpack.py"
Cohesion: 0.16
Nodes (18): prose_hash(), The tamper-evidence anchor: sha256 of the page prose (full hex, this is a machin, build_certificate(), _cert_digest(), certificate_status(), _cmd_verify(), _ctx_for(), Path (+10 more)

### Community 42 - "src-isidore.md"
Cohesion: 0.22
Nodes (13): parse_predicate_field(), Parse a claim's optional third field into a pcp.Predicate (or None). PCP typed-c, Dispatch one predicate to its registered verifier. No verifier -> UNDECIDABLE (f, verify_predicate(), _anchored(), _ctx(), Lane A gate — the typed-claim verifiers decide truth against the two oracles, bu, Dogfood regression: the graph's import edges are partial and `value` can't compa (+5 more)

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
Cohesion: 0.23
Nodes (14): _cmd_export_agora(), build_cards(), Path, export-agora — bridge isidore's verified claims into Living-Library card DRAFTS, Return [(filename, content)] draft cards — one per wiki page with enough OK clai, render_card(), _slug(), write_cards() (+6 more)

### Community 55 - "load_state"
Cohesion: 0.13
Nodes (21): _cmd_contracts(), Lane B (part 2) — claim->contract graduation + `isidore contracts`. (T-8dfc)  A, Check every promoted contract against the current graph. Pure, 0-LLM., Add `isidore contracts` (promote / list / check)., Command implementation for `isidore contracts`., register_cli(), verify_contracts(), Contract (+13 more)

### Community 56 - "render_whatsnew_md"
Cohesion: 0.23
Nodes (15): check_claims(), claims_for_file(), claims_grep(), Re-hash every stored claim's evidence — the zero-LLM staleness audit.      Ret, The documentation contract of a file: every anchored claim whose evidence points, Free-text search over verified atomic facts — answers many questions with 0 LLM, _cmd_claims(), load_state() (+7 more)

### Community 57 - "test_changeset.py"
Cohesion: 0.43
Nodes (7): compile_subsystems(), Compile the N2 layer: one bounded call per area, each page chained to its module, subsystem_page_name(), _nodes(), test_an_area_page_is_chained_to_the_module_pages_below_it(), test_an_area_with_nothing_proven_under_it_is_skipped_not_invented(), test_the_machine_scheme_never_reaches_a_reader_facing_link()

### Community 58 - "What's new — `HEAD~2..HEAD`"
Cohesion: 0.29
Nodes (6): Every change, in detail, In plain words, Internal surface, Public API, Tests, What's new — `HEAD~2..HEAD`

### Community 59 - "harvest_todos"
Cohesion: 0.26
Nodes (12): _brace(), _doc(), _js(), _kw_func(), _kw_type(), LanguageSpec, Pattern, Language-agnostic symbol extraction: one engine, the language is *data*.  Isid (+4 more)

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
Cohesion: 0.17
Nodes (19): assemble_topic_context(), item_classification(), provider_is_trusted(), An item's confidentiality: `meta.classification`, else `classification:` in its, Whether the operator has declared the configured LLM provider fit to receive res, Assemble items matching streams and filters into citable facts.      External co, _item(), Ingesting a source does not authorise sending it to a third party.  Found by run (+11 more)

### Community 65 - "assemble_context"
Cohesion: 0.32
Nodes (7): A reconciler finding (lane B): the model's own outputs contradict each other. 0-, Violation, Lane B (part 1) — the reconciler: the model's own outputs cross-checked, 0 LLM., Helper to split file:line into (file, line)., Cross-check prose vs findings vs claims vs marks -> internal contradictions. Pur, reconcile(), _split_evidence()

### Community 66 - "compile_subsystems"
Cohesion: 0.19
Nodes (16): Run the scanner and persist the graph to .isidore/graph.json., write_scan(), build_impact(), _edges(), ImpactReport, Path, isidore impact — the zero-LLM emergent-interaction detector.  Regenerating a nei, render_impact() (+8 more)

### Community 67 - "reconcile"
Cohesion: 0.17
Nodes (16): IngestResult, Outcome of one ingest run. `raw_files` are the JSONL files written this run., _as_list(), feed_url(), HackerNewsConnector, parse_hits(), Hacker News connector (ADR-0032 F4): public front-page tags and Algolia searches, (stream, url) for every configured search and listing. Streams are named for wha (+8 more)

### Community 68 - "subsystem-tests.md"
Cohesion: 0.40
Nodes (4): How the work is divided, What it depends on, and what depends on it, What this area is responsible for, Where to start reading

### Community 69 - "security_banner"
Cohesion: 0.22
Nodes (9): build_delta(), _is_comparable(), Skip generated wiki output, the graph store, and anything not source code. Compa, The zero-LLM core: a typed API-surface difference between two revisions.      Pr, test_deleted_file_is_reported_but_carries_no_line_to_cite(), test_delta_reports_exactly_the_real_changes_and_invents_nothing(), test_multiline_typescript_signature_is_cited_at_its_declaration(), test_rename_maps_to_the_new_path() (+1 more)

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
Cohesion: 0.20
Nodes (10): Map an import to a repo file id if the module resolves inside the repo., Build a structure graph for a repo in ANY language, zero dependencies (see modul, _resolve_import(), scan_repo(), test_scan_repo_is_multilanguage(), test_scan_repo_skips_binary_files(), test_scan_repo_tolerates_unreadable_and_empty(), test_scan_repo_unknown_text_becomes_bare_file_node() (+2 more)

### Community 102 - "subsystem-src.md"
Cohesion: 0.40
Nodes (4): How the work is divided, What it depends on, and what depends on it, What this area is responsible for, Where to start reading

### Community 103 - "v_calls"
Cohesion: 0.08
Nodes (34): apply_settings(), parse_setting(), `key=value` -> (key, value). A value that parses as JSON is stored as JSON, so n, Fold `key=value` settings into a config. Repeating a key ACCUMULATES into a list, _cap_content(), Epoch second a commit must reach to be inside the window, or (None, note) if unb, Cap an item's content to `max_bytes` UTF-8 bytes, cutting on a character boundar, _window_floor() (+26 more)

### Community 104 - "clean_sig"
Cohesion: 0.21
Nodes (17): _cmd_llms(), _first_sentence(), Path, The wiki, in the layout agents are converging on for being handed documentation., Write llms.txt at the repo root — where the convention puts it, so a fetcher fin, Add `isidore llms` (regenerate llms.txt from whatever is compiled). 0 LLM., register_cli(), render_llms_txt() (+9 more)

### Community 105 - "build_delta"
Cohesion: 0.19
Nodes (17): extract(), _Pending, Extract (symbols, imported-module-names) from one file's source.      symbols:, The LanguageSpec for a file extension (lowercased), or None if we do not extract, Blank out comment (and, by default, string) *contents*, preserving newlines and, sanitize(), spec_for(), _names() (+9 more)

### Community 106 - "render_whatsnew_md"
Cohesion: 0.33
Nodes (5): Architecture, Dependencies, How to change safely, Key entry points, Purpose

### Community 107 - "encode"
Cohesion: 0.33
Nodes (5): Architecture, Dependencies, How to change safely, Key entry points, Purpose

### Community 108 - "write_scan"
Cohesion: 0.21
Nodes (13): overview_facts(), _page_purpose(), Path, The first sentence of a module page's `## Purpose` — what that module says it is, What one subsystem page is written from: its module pages, what each says it is, Every claim the pages below PROVED, as citable `wiki://page#id` facts.      This, The project's own words about itself — CONTEXT, never evidence (see OVERVIEW_PRO, Everything the overview is allowed to be written from. 0 LLM. (+5 more)

### Community 109 - "tests-test_langspec_oracle_py.md"
Cohesion: 0.33
Nodes (5): Architecture, Dependencies, How to change safely, Key entry points, Purpose

### Community 110 - "tests-test_llms_txt_py.md"
Cohesion: 0.33
Nodes (5): Architecture, Dependencies, How to change safely, Key entry points, Purpose

### Community 111 - "literal_value"
Cohesion: 0.19
Nodes (17): _item(), F6's hostile gate: what the knowledge home does when its own data is broken, eno, A cap that bites silently turns a partial answer into a confident one., The whole point of I8, end to end: an item that issues commands and forges a del, The second half of the defence: even if a forged URI reaches a claim, it has to, The honest failure. A claim whose evidence is gone must say so — the alternative, An interrupted append leaves a truncated last line. Losing the whole run over it, _store() (+9 more)

### Community 112 - "tests-test_recertify_py.md"
Cohesion: 0.33
Nodes (5): Architecture, Dependencies, How to change safely, Key entry points, Purpose

### Community 113 - "strip_inline_claim_rows"
Cohesion: 0.14
Nodes (25): anchor_claims(), claim_id(), parse_claims_block(), Split a generated page into (clean page, raw claim rows). Tolerant of malformed, Deterministic, ledger-friendly id: stable across runs for the same (statement, e, Repair a shortened citation to a real file, or None if it can't be resolved uniq, Quarantine filter + anchoring. Returns (anchored claims, dropped, repaired)., resolve_citation() (+17 more)

### Community 114 - "verify_predicate"
Cohesion: 0.20
Nodes (9): Confirm the tool names before you trust this block, Setup, Slack — instance recipe for the MCP connector, Sources, The config, The part you should actually worry about, Verifying it works, What you get (+1 more)

### Community 115 - "SurfaceSymbol"
Cohesion: 0.18
Nodes (10): One declared symbol of a file, as of one revision of its text.      `qualname`, SurfaceSymbol, _diff_surfaces(), _file_summary(), RuntimeError, Git could not answer, or a ref does not resolve. Fail closed: never guess a rang, A compact roll-up of what a whole added/removed file declares., Typed difference between two surfaces of the same file.      Identity is the qua (+2 more)

### Community 116 - "test_pcp_pipeline.py"
Cohesion: 0.29
Nodes (10): _compile(), _fake_generator(), _fake_generator_with_a_lie(), Path, P-INT gate — the pipeline wiring ties all five PCP lanes together end to end: a, test_compile_writes_a_certificate_with_typed_verdicts(), test_deterministic_mark_forces_the_banner_despite_calm_prose(), test_refuted_claim_is_quarantined_not_published() (+2 more)

### Community 117 - "main"
Cohesion: 0.18
Nodes (12): degenerate_certificate(), A short reason when a certificate is a symptom rather than a certificate, else N, _Cert, nested_wiki_dir(), The wiki is OUTPUT. It must never round-trip into the input.  Reported from GIMO, GIMO's actual numbers. Writing this silently is how it reached 13 MB before anyo, Point the toolchain at GIMO's layout. WIKI_DIRNAME is resolved once at import so, GIMO's shape: the wiki lives several directories deep, at whatever the toolchain (+4 more)

### Community 118 - "apply_settings"
Cohesion: 0.22
Nodes (13): Certificate, certificate_to_dict(), Path, The re-verifiable sidecar for one page. Persisted as JSON (machine-read). Tamper, Certificate -> plain dict (asdict handles the nested dataclasses). The JSON on d, Persist a certificate as pretty JSON (stable key order for byte-deterministic di, Load a certificate from disk. Raises ValueError on malformed JSON (fail-closed f, read_certificate() (+5 more)

### Community 119 - "ClaimVerdict"
Cohesion: 0.33
Nodes (5): Architecture, Dependencies, How to change safely, Key entry points, Purpose

### Community 120 - "GitRepoConnector"
Cohesion: 0.16
Nodes (16): _cmd_whatsnew(), generate_prose(), _group_by_module(), _llm_entries(), parse_plain_block(), _prompt_for_module(), isidore whatsnew — a changelog you can re-verify, instead of one you have to tru, Split the plain-language block out of a model answer -> (rest, plain text, broke (+8 more)

### Community 121 - "src-isidore-connect_py.md"
Cohesion: 0.33
Nodes (5): Architecture, Dependencies, How to change safely, Key entry points, Purpose

### Community 122 - "tests-test_connect_cli_py.md"
Cohesion: 0.33
Nodes (5): Architecture, Dependencies, How to change safely, Key entry points, Purpose

### Community 123 - "CertStatus"
Cohesion: 0.14
Nodes (16): parse_predicate(), parse_stored_predicate(), Parse a predicate read back from a CERTIFICATE rather than from model output., Load promoted contracts (empty list if the file is absent). Malformed -> ValueEr, Parse "<kind>:<a>;<b>" -> Predicate, or None if absent/malformed/unknown-kind., read_contracts(), P0 gate (ADR-0033) — the frozen PCP seam parses its golden fixtures and exposes, The frozen signatures exist and return the seam's types (whether stub or impleme (+8 more)

### Community 124 - "anchor_claims"
Cohesion: 0.17
Nodes (13): parse_wiki_uri(), wiki://<page>#<claim-id> -> (page, claim_id), or None if it is not a wiki URI., _chain_verdicts(), _claim_verdict(), Resolve (verdict, state) for a cited claim. Truth comes from the page's certific, Resolve `wiki://` claims through lane D's verifier and compose the child certifi, Resolve a wiki:// chain. Fail-closed: None/invalid/missing -> not TRUE, never cr, _wikichain_verifier() (+5 more)

### Community 125 - "apply_settings"
Cohesion: 0.21
Nodes (11): certificate_from_dict(), ClaimVerdict, One claim's line in a certificate: the anchored claim + its typed verdict (if an, Rebuild a Certificate from parsed JSON, reconstructing the nested dataclasses. T, VerifiedMass, _claim_symbols(), classify_mass(), The code identifiers a claim is about: its predicate args (last dotted component (+3 more)

### Community 126 - "encode"
Cohesion: 0.18
Nodes (15): Compile journal + per-page changelog — residue mining, all zero-LLM.  Every comp, Map each `## heading` to its body text (content before the first heading is keye, (H2 headings whose content changed / were added / removed, new_line_count - old_, render_stats(), section_diff(), _sections(), encode(), encode_table() (+7 more)

### Community 127 - "test_vigil.py"
Cohesion: 0.28
Nodes (8): Request, build_request(), generate(), GenerationError, RuntimeError, Single-provider LLM client (OpenAI-compatible), fail-closed by design.  One mode, The provider failed. No retry with a different model — fail closed., test_build_request_openai_compat_temperature_zero_and_bearer()

### Community 128 - "GitRepoConnector"
Cohesion: 0.29
Nodes (8): _is_wiki_output(), The repo-relative posix path of the wiki OUTPUT directory, normalised for prefix, wiki_output_prefix(), drop_wiki_output(), Nodes that do not live inside the wiki output directory.      The second barrier, The second barrier: a graph can arrive from `--graph` or Graphify, whose produce, test_no_page_is_planned_for_the_wiki_itself(), test_the_prefix_is_a_path_not_a_name()

### Community 129 - "ValueError"
Cohesion: 0.29
Nodes (6): check_item_id(), Raise ValueError if `item_id` cannot be addressed by a `src://` URI., Both were found in production, and both silently emptied the claims block instea, test_a_derived_id_is_addressable_readable_and_stable(), test_the_two_characters_that_break_a_src_uri_are_rejected(), ValueError

### Community 130 - "tests-test_connectors_f5_py.md"
Cohesion: 0.33
Nodes (5): Architecture, Dependencies, How to change safely, Key entry points, Purpose

### Community 131 - "generate_prose"
Cohesion: 0.29
Nodes (7): ground_symbols(), _prose_identifiers(), Return prose identifiers that DON'T resolve to any graph symbol or file (groundi, authenticate()' -> 'authenticate', 'MyClass' -> 'MyClass'., Graph nodes whose symbol label matches `name` (last dotted component tolerated)., _symbol_base(), _symbol_nodes()

### Community 132 - "_cap_content"
Cohesion: 0.33
Nodes (5): Architecture, Dependencies, How to change safely, Key entry points, Purpose

### Community 133 - "harvest_todos"
Cohesion: 0.67
Nodes (3): literal_value(), The literal a constant is bound to, or None when it is not a plain literal., test_literal_value_reads_only_comparable_literals()

### Community 134 - "render_findings"
Cohesion: 0.12
Nodes (24): Counter, render_findings(), assemble_context(), context_hash(), _match_seed(), module_dep_edges(), PageSpec, plan_flows() (+16 more)

## Knowledge Gaps
- **327 isolated node(s):** `isidore-wiki`, `Knowledge home (local, not in this repo)`, `Why`, `Quickstart`, `What you get` (+322 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **5 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `IngestOptions` connect `detectors.py` to `cli.py`, `reconcile`, `v_calls`, `test_claims.py`, `home.py`, `build_certificate`, `literal_value`, `surface.py`, `git_repo.py`, `IngestOptions`, `mcp.py`, `knowledge.py`, `_tool_read_only`?**
  _High betweenness centrality (0.083) - this node is a cross-community bridge._
- **Why does `VerifyContext` connect `load_state` to `compile_wiki`, `generate_prose`, `verify.py`, `render_findings`, `findings.py`, `whatsnew.py`, `claims.py`, `pipeline.py`, `plan_pages`, `pcp.py`, `write_items`, `scan`, `test_humanpack.py`, `src-isidore.md`, `test_changeset.py`, `render.py`, `SurfaceSymbol`, `GitRepoConnector`, `CertStatus`, `anchor_claims`?**
  _High betweenness centrality (0.031) - this node is a cross-community bridge._
- **Why does `compile_wiki()` connect `compile_wiki` to `cli.py`, `graph.py`, `read_certificate`, `render_findings`, `module_of`, `test_claims.py`, `claims.py`, `test_pcp_pipeline.py`, `encode`, `scan`, `GenerationError`, `test_reconcile.py`, `test_humanpack.py`, `verify_page`, `load_state`, `render_whatsnew_md`, `assemble_context`, `compile_subsystems`, `strip_inline_claim_rows`, `test_pcp_pipeline.py`, `main`, `apply_settings`, `test_vigil.py`?**
  _High betweenness centrality (0.030) - this node is a cross-community bridge._
- **Are the 32 inferred relationships involving `compile_wiki()` (e.g. with `test_compile_stores_claims_and_writes_claims_toon()` and `test_dry_run_still_detects_stale_claims_for_free()`) actually correct?**
  _`compile_wiki()` has 32 INFERRED edges - model-reasoned connections that need verification._
- **Are the 13 inferred relationships involving `VerifyContext` (e.g. with `CompileResult` and `PageSpec`) actually correct?**
  _`VerifyContext` has 13 INFERRED edges - model-reasoned connections that need verification._
- **Are the 33 inferred relationships involving `IngestOptions` (e.g. with `GitRepoConnector` and `HackerNewsConnector`) actually correct?**
  _`IngestOptions` has 33 INFERRED edges - model-reasoned connections that need verification._
- **Are the 15 inferred relationships involving `Predicate` (e.g. with `CertStatus` and `test_a_unique_declaration_can_still_be_refuted()`) actually correct?**
  _`Predicate` has 15 INFERRED edges - model-reasoned connections that need verification._