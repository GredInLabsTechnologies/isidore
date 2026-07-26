# Graph Report - isidore  (2026-07-26)

## Corpus Check
- 180 files · ~113,228 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1538 nodes · 3426 edges · 114 communities (109 shown, 5 thin omitted)
- Extraction: 85% EXTRACTED · 15% INFERRED · 0% AMBIGUOUS · INFERRED: 527 edges (avg confidence: 0.76)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `036487e2`
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

## God Nodes (most connected - your core abstractions)
1. `compile_wiki()` - 83 edges
2. `VerifyContext` - 62 edges
3. `Predicate` - 35 edges
4. `_make_repo()` - 31 edges
5. `run_whatsnew()` - 29 edges
6. `load_graph()` - 27 edges
7. `build_delta()` - 26 edges
8. `IngestOptions` - 25 edges
9. `compile_overview()` - 25 edges
10. `read_certificate()` - 24 edges

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

## Communities (114 total, 5 thin omitted)

### Community 0 - "cli.py"
Cohesion: 0.21
Nodes (19): _cmd_ask(), _cmd_compile(), _cmd_impact(), _cmd_scan(), _cmd_stats(), _cmd_suggest_flows(), main(), isidore — compile an agent-oriented wiki from your codebase's structure graph. (+11 more)

### Community 1 - "graph.py"
Cohesion: 0.10
Nodes (34): git_head(), git_listed_files(), _is_binary(), _iter_source_files(), _node_id(), _norm_source_file(), Path, Structure graph: loading, module grouping, and a built-in multi-language scanner (+26 more)

### Community 2 - "compile_wiki"
Cohesion: 0.15
Nodes (34): compile_wiki(), lint_cited_paths(), File-looking paths cited in the prose that do NOT exist in the repo., Run the pipeline. With execute=False no LLM is called and no page is written., agents_md_block(), Insert or replace the delimited block without touching the rest of the file (ide, upsert_agents_block(), _gp() (+26 more)

### Community 3 - "read_certificate"
Cohesion: 0.33
Nodes (6): _claim_verdict(), Resolve (verdict, state) for a cited claim. Truth comes from the page's certific, Resolve a wiki:// chain. Fail-closed: None/invalid/missing -> not TRUE, never cr, _wikichain_verifier(), BUG 3 regression: a None predicate crashed with AttributeError., test_wikichain_none_does_not_crash()

### Community 4 - "detectors.py"
Cohesion: 0.12
Nodes (17): is_security_finding(), True if a suspect reads as a security risk (hardcoded secret, auth bypass, injec, Verify that negation patterns do not trigger false positive security findings (6, Verify that safety-checks catch risks even with intermediate/intervening words., If the model attempts social engineering in prose while findings report the bug,, Vigil case: A camouflaged auth backdoor reported in findings but justified by pr, test_adversarial_backdoor_detection(), test_false_negative_intervening_words() (+9 more)

### Community 5 - "verify.py"
Cohesion: 0.11
Nodes (46): AST, Check every promoted contract against the current graph. Pure, 0-LLM., verify_contracts(), The result of checking one predicate against an oracle. `value` is TRUE|FALSE|UN, Everything a verifier needs, assembled once per page/verify run. Read-only to ve, undecidable(), Verdict, VerifyContext (+38 more)

### Community 6 - "humanpack.py"
Cohesion: 0.12
Nodes (26): _cmd_render(), _esc(), generate_architecture_map(), generate_claims_table(), generate_contracts_section(), generate_glossary(), generate_mass_bar(), minimal_markdown_to_html() (+18 more)

### Community 7 - "quickstart.md"
Cohesion: 0.40
Nodes (3): Wiki (isidore), Modules, Wiki (isidore)

### Community 8 - "findings.py"
Cohesion: 0.10
Nodes (41): build_delta(), RuntimeError, Git could not answer, or a ref does not resolve. Fail closed: never guess a rang, The zero-LLM core: a typed API-surface difference between two revisions.      Pr, Build the delta, optionally write the prose, and persist page + certificate., run_whatsnew(), WhatsnewError, _commit() (+33 more)

### Community 9 - "module_of"
Cohesion: 0.11
Nodes (28): affected_modules(), changed_lines(), changed_symbols(), _git_diff(), _module_fan_in(), modules_of(), Path, Change-set detection: which graph symbols a git diff touched, and which modules (+20 more)

### Community 10 - "test_claims.py"
Cohesion: 0.05
Nodes (88): anchor_claims(), check_claims(), claim_id(), claims_for_file(), claims_grep(), evidence_hash(), evidence_state(), _hash() (+80 more)

### Community 11 - "home.py"
Cohesion: 0.21
Nodes (16): _cmd_connect(), _cmd_ingest(), connector_summary(), load_config(), `isidore connect` and `isidore ingest` — the CLI face of the connector layer (AD, Add `isidore connect` and `isidore ingest` (registrar loop in cli.main)., A connector's stored config, or {} if absent/corrupt. Never raises., One row of `connect --list`: what it is, whether it can run, and what it has ing (+8 more)

### Community 12 - "whatsnew.py"
Cohesion: 0.10
Nodes (32): annotate_unverified_paths(), Annotate every cited path that does not exist in the repo, inline and visibly —, One declared symbol of a file, as of one revision of its text.      `qualname`, SurfaceSymbol, _cmd_whatsnew(), DeltaEntry, _diff_surfaces(), _file_summary() (+24 more)

### Community 13 - "build_certificate"
Cohesion: 0.08
Nodes (32): apply_settings(), parse_setting(), Path, Write a connector's config with the home's restrictive permissions., `key=value` -> (key, value). A value that parses as JSON is stored as JSON, so n, Fold `key=value` settings into a config. Repeating a key ACCUMULATES into a list, save_config(), _cap_content() (+24 more)

### Community 14 - "pyramid.py"
Cohesion: 0.32
Nodes (7): _graph(), Lane D gate — the pyramid plans from the real graph, uses imports for cohesion,, BUG 1 regression: auto-seed used node['path'/'file'/'name'] (absent) -> []. Must, BUG 2 regression: `links` was ignored. imports edges must yield depends_on., test_autoseed_groups_by_source_file_on_the_real_graph(), test_explicit_config_still_works(), test_links_used_for_inter_subsystem_deps()

### Community 15 - "claims.py"
Cohesion: 0.12
Nodes (21): isidore — compile an agent-oriented wiki from your codebase's structure graph., append_run(), Compile journal + per-page changelog — residue mining, all zero-LLM.  Every comp, Append an H2-level changelog entry to a page's state (capped). No-op if the pros, record_page_change(), assemble_context(), CompileResult, git_log_for() (+13 more)

### Community 16 - "surface.py"
Cohesion: 0.14
Nodes (21): Counter, context_hash(), _match_seed(), module_dep_edges(), plan_flows(), plan_pages(), prompt_for(), Cross-module dependency edges (src_module, dst_module) -> link count. Shared by (+13 more)

### Community 17 - "Isidore v2 — Incremental compilation, impact detection & residue mining"
Cohesion: 0.12
Nodes (16): 0 · Why (user directive), 1 · Verified bug diagnoses (2026-07-10, against real code — not reports), 2 · Design principles (unchanged bets, now enforced deeper), 3 · C0 — Scoped compile: `isidore compile --only <sel>[,<sel>…]`, 4 · C1+C2 — Change-driven compile: `isidore compile --changed [--since <ref>]`, 5 · C3 — Impact detection: `isidore impact [--since <ref>] [--md] [--check]` (new, **0 LLM always**), 6 · C4+C5+C6 — Correctness fixes (the right ones), 7 · C7 — Residue mining (all 0-LLM; the "squeeze everything" layer) (+8 more)

### Community 18 - "git_repo.py"
Cohesion: 0.24
Nodes (13): _cmd_sync(), all_connectors(), Connector, get(), IngestResult, _load_plugins(), Protocol, Connector protocol + registry (ADR-0032 F1).  A connector ingests raw items from (+5 more)

### Community 19 - "VerifyContext"
Cohesion: 0.15
Nodes (16): _git_repo(), _qa_repo(), Unit tests: toon encoder, graph scanner, findings residue, QA retrieval, LLM req, A third-party graph (e.g. Graphify) that indexed a gitignored path gets cleaned, Outside a git tree we cannot tell what's ignored -> index everything, unchanged., Init a minimal git repo at `path`; skip the test if git is unavailable., The reported GIMO bug: a gitignored build-artifact copy must NOT be indexed as s, test_ask_uses_single_injected_generator_call() (+8 more)

### Community 20 - "IngestOptions"
Cohesion: 0.17
Nodes (17): IngestOptions, Caps and scoping for a run. All limits live here (in code), never in a prompt., GitRepoConnector, test_max_bytes_reaches_the_connector_through_ingest(), test_the_streams_filter_leaves_other_repos_untouched(), _git(), _head(), _make_repo() (+9 more)

### Community 21 - "pipeline.py"
Cohesion: 0.14
Nodes (25): _cmd_overview(), _cmd_pyramid(), _cmd_subsystems(), _load_graph_for(), _module_pages_of(), _norm(), overview_facts(), _page_purpose() (+17 more)

### Community 22 - "mcp.py"
Cohesion: 0.15
Nodes (14): _allowed(), _JsonRpcClient, McpConnector, Any, Minimal read-only MCP connector (ADR-0032 F3).  The implementation deliberately, Map tool name -> its MCP annotations via tools/list (paginated). Empty if the se, create_run_id(), Sortable, collision-resistant run id (UTC second + millis). (+6 more)

### Community 23 - "test_pcp_pipeline.py"
Cohesion: 0.13
Nodes (20): _cmd_findings(), _churn(), filter_findings(), finding_id(), findings_new(), harvest_todos(), is_finding_resolved(), Path (+12 more)

### Community 24 - "knowledge.py"
Cohesion: 0.18
Nodes (11): coverage_gap_candidates(), insert_security_banner(), orphan_file_candidates(), parse_findings_block(), Side observations ("residue") harvested during compilation — at ~zero marginal c, Place the banner right under the page's H1 (or at the very top if there is none), Code FILE nodes nothing links to — dead-code candidates (entrypoint-looking name, Module pages with no inbound link from any test-looking module. (+3 more)

### Community 25 - "plan_pages"
Cohesion: 0.13
Nodes (21): compile_overview(), missing_sections(), _plain_violations(), Required headings the page does not have. 0 LLM., Turn `wiki://page` into `page` in PROSE, so the links a reader clicks actually r, Rule names broken by the PROSE (fenced blocks excluded — those are machine-facin, Compile the plain-language product page (N3). One LLM call, plus at most one rep, relink_wiki_uris() (+13 more)

### Community 26 - "pcp.py"
Cohesion: 0.18
Nodes (22): Predicate, A decidable assertion parsed from a claim's third field. Frozen: predicates are, parameter_names(), Parameter names in declaration order, or None when they cannot be read with conf, signature(fn, a1, a2, ...): fn's positional parameter names, in order. Oracles:, v_signature(), _ctx(), `signature` and `value` decided outside Python, and — just as important — the ca (+14 more)

### Community 27 - "_tool_read_only"
Cohesion: 0.16
Nodes (12): _name_looks_mutating(), Fallback heuristic ONLY (not exhaustive): does the tool name contain a mutating, (allowed, reason). Authority order: explicit readOnlyHint/destructiveHint > name, _tool_read_only(), _FakeClient, MCP connector read-only barrier (ADR-0032 F3). Regression for the review of T-db, Stands in for _JsonRpcClient: a server exposing one read tool, one write tool (a, test_destructive_hint_rejects() (+4 more)

### Community 28 - "PCP_SEAMS — the frozen interface for Proof-Carrying Prose (ADR-0033, phase P0)"
Cohesion: 0.15
Nodes (12): Certificate (`<page>.md` → `<page>.md.cert.json`, alongside the page), CLI, Contracts (`contracts.json` in the wiki dir), File ownership matrix (nobody edits another lane's files), How each lane starts (all depend ONLY on P0 = T-1dc9), Marks (lane C output; also the golden `marks.json`), PCP_SEAMS — the frozen interface for Proof-Carrying Prose (ADR-0033, phase P0), Pipeline hooks (lane A wires; signatures frozen) (+4 more)

### Community 29 - "encode"
Cohesion: 0.10
Nodes (44): Path, Persist a certificate as pretty JSON (stable key order for byte-deterministic di, Load a certificate from disk. Raises ValueError on malformed JSON (fail-closed f, read_certificate(), write_certificate(), _level(), Re-run the oracles over every certified page. 0 LLM. Writes only with `write=Tru, Pyramid level, so children are recertified before the pages that cite them. (+36 more)

### Community 30 - "Mark"
Cohesion: 0.15
Nodes (17): check(), explain(), is_plain(), PlainRule, Pattern, Plain-language gate: can a reader who has never seen code use this sentence?  Do, Human-readable reason for a rejection, for the run summary and the journal., One named check. `kind` mirrors Vale's rule taxonomy so the intent of each is de (+9 more)

### Community 31 - "write_items"
Cohesion: 0.11
Nodes (25): Certificate, parse_stored_predicate(), parse_wiki_uri(), Parse a predicate read back from a CERTIFICATE rather than from model output., The re-verifiable sidecar for one page. Persisted as JSON (machine-read). Tamper, wiki://<page>#<claim-id> -> (page, claim_id), or None if it is not a wiki URI., _child_digest(), _cmd_recertify() (+17 more)

### Community 32 - "isidore"
Cohesion: 0.13
Nodes (14): Bring your own graph, Config (`isidore.json`, optional), Design rules, isidore, Languages, License, One range, three readers, Proof-carrying prose — how to read a certified page (+6 more)

### Community 33 - "auth.py"
Cohesion: 0.29
Nodes (6): authenticate(), Auth service fixture for PCP lane tests. Line numbers are load-bearing: the gold, Verify the caller's JWT and enforce the attempt ceiling., Token service fixture for PCP lane tests. verify_jwt is defined on L5 (cited by, Return the decoded claims if the token's signature checks out, else None., verify_jwt()

### Community 35 - "scan"
Cohesion: 0.18
Nodes (13): _looks_like_secret(), Path, Lane C — deterministic security detectors: entropy, sinks, topology. 0 LLM. (T-e, Files reachable from an auth/secret/crypto root via imports (BFS, file-level). 0, Shannon entropy per character (bits). Stdlib only., Return a reason if the literal is credential-shaped, else None., Repo-relative source files to scan: the graph's, or a bounded walk if the graph, Entropy + sink marks for one file. Never raises (unreadable file -> no marks). (+5 more)

### Community 36 - "assemble_context"
Cohesion: 0.23
Nodes (14): _cmd_export_agora(), build_cards(), Path, export-agora — bridge isidore's verified claims into Living-Library card DRAFTS, Return [(filename, content)] draft cards — one per wiki page with enough OK clai, render_card(), _slug(), write_cards() (+6 more)

### Community 37 - "GenerationError"
Cohesion: 0.21
Nodes (21): load_knowledge_state(), answer_knowledge_offline(), answer_offline(), ask(), ask_knowledge(), gather_claims(), gather_evidence(), gather_knowledge_claims() (+13 more)

### Community 38 - "ClaimVerdict"
Cohesion: 0.22
Nodes (19): extract_surface(), python_surface(), Exact surface of one Python source text, or None if it does not parse.      No, Surface of one file's text, routed by extension. None = not comparable source., _by_name(), API surface extraction: qualified names, signatures as change keys, and the fold, test_extract_surface_returns_none_for_non_code(), test_generic_surface_disambiguates_same_named_methods_of_different_classes() (+11 more)

### Community 39 - "test_wiki_dir_env.py"
Cohesion: 0.31
Nodes (7): ISIDORE_WIKI_DIR redirects the compiled-wiki output directory.  WIKI_DIRNAME is, A nested WIKI_DIRNAME (e.g. doc/isidore) must create its parents, not crash., _reload_render(), test_save_state_creates_nested_wiki_dir(), test_wiki_dirname_blank_env_falls_back(), test_wiki_dirname_defaults_to_wiki(), test_wiki_dirname_honors_env()

### Community 40 - "test_reconcile.py"
Cohesion: 0.19
Nodes (19): _cmd_llms(), _first_sentence(), Path, Deterministic outputs: quickstart.md, index.toon, llms.txt, and the AGENTS.md re, The wiki, in the layout agents are converging on for being handed documentation., Write llms.txt at the repo root — where the convention puts it, so a fetcher fin, Add `isidore llms` (regenerate llms.txt from whatever is compiled). 0 LLM., register_cli() (+11 more)

### Community 41 - "test_humanpack.py"
Cohesion: 0.17
Nodes (16): Load promoted contracts (empty list if the file is absent). Malformed -> ValueEr, read_contracts(), _cert_digest(), certificate_status(), _cmd_verify(), _ctx_for(), Path, Check a page against its sidecar certificate, offline, 0 LLM (invariant I11). (+8 more)

### Community 42 - "src-isidore.md"
Cohesion: 0.11
Nodes (26): parse_predicate_field(), Parse a claim's optional third field into a pcp.Predicate (or None). PCP typed-c, ClaimVerdict, prose_hash(), One claim's line in a certificate: the anchored claim + its typed verdict (if an, The tamper-evidence anchor: sha256 of the page prose (full hex, this is a machin, build_certificate(), _claim_symbols() (+18 more)

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
Cohesion: 0.16
Nodes (9): (item, None) for a changed repo, (None, None) if HEAD is unchanged, (None, warni, Run a git command; return stdout or None on any failure (never raises)., Epoch second a commit must reach to be inside the window, or (None, note) if unb, _window_floor(), iso_now(), Measured live: agora's manifest under a 24h window listed no commits at all. Cor, A window is only trustworthy if the cases it cannot express SAY so instead of co, test_a_window_that_cannot_be_expressed_reports_instead_of_returning_nothing() (+1 more)

### Community 55 - "load_state"
Cohesion: 0.12
Nodes (19): certificate_to_dict(), get_verifier(), parse_predicate(), Protocol, Proof-Carrying Prose (PCP) — the frozen seam shared by every PCP lane.  This mod, A predicate verifier. MUST be deterministic and 0-LLM. Returns UNDECIDABLE, neve, Dispatch one predicate to its registered verifier. No verifier -> UNDECIDABLE (f, Certificate -> plain dict (asdict handles the nested dataclasses). The JSON on d (+11 more)

### Community 56 - "render_whatsnew_md"
Cohesion: 0.23
Nodes (13): Map each `## heading` to its body text (content before the first heading is keye, (H2 headings whose content changed / were added / removed, new_line_count - old_, section_diff(), _sections(), load_state(), _git(), Residue-mining units: section diff, compile journal/stats, per-page history, cla, _repo() (+5 more)

### Community 57 - "test_changeset.py"
Cohesion: 0.21
Nodes (13): _chain_verdicts(), compile_subsystems(), Compile the N2 layer: one bounded call per area, each page chained to its module, Every claim the pages below PROVED, as citable `wiki://page#id` facts.      This, Resolve `wiki://` claims through lane D's verifier and compose the child certifi, subsystem_page_name(), verified_claims(), _nodes() (+5 more)

### Community 58 - "What's new — `HEAD~2..HEAD`"
Cohesion: 0.29
Nodes (6): Every change, in detail, In plain words, Internal surface, Public API, Tests, What's new — `HEAD~2..HEAD`

### Community 59 - "harvest_todos"
Cohesion: 0.18
Nodes (12): _cmd_contracts(), Lane B (part 2) — claim->contract graduation + `isidore contracts`. (T-8dfc)  A, Add `isidore contracts` (promote / list / check)., Command implementation for `isidore contracts`., register_cli(), Contract, Persist contracts as JSON (machine-read gate input)., A typed claim a human promoted to an invariant. `isidore verify --contracts` fai (+4 more)

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
Cohesion: 0.08
Nodes (39): Match, _brace(), _doc(), extract(), _js(), _kw_func(), _kw_type(), LanguageSpec (+31 more)

### Community 65 - "assemble_context"
Cohesion: 0.20
Nodes (13): format_mark(), generate_security_banner(), certificate_from_dict(), Mark, A deterministic security-relevant flag raised BEFORE the LLM call (lane C)., A reconciler finding (lane B): the model's own outputs contradict each other. 0-, Rebuild a Certificate from parsed JSON, reconstructing the nested dataclasses. T, Violation (+5 more)

### Community 66 - "compile_subsystems"
Cohesion: 0.23
Nodes (11): A prominent, deterministic banner listing this page's security suspects — meant, render_findings(), security_banner(), security_suspects(), Security escalation: a security suspect forces a loud, deterministic prose banne, test_banner_goes_under_the_h1(), test_banner_is_loud_and_lists_evidence(), test_findings_toon_lists_security_first_and_in_summary() (+3 more)

### Community 67 - "reconcile"
Cohesion: 0.25
Nodes (3): Ensure reconcile.py does not import pipeline, claims, or verify (frozen boundary, test_pure_reconcile_imports_constraint(), test_reconcile_mark_uncovered()

### Community 68 - "subsystem-tests.md"
Cohesion: 0.40
Nodes (4): How the work is divided, What it depends on, and what depends on it, What this area is responsible for, Where to start reading

### Community 69 - "security_banner"
Cohesion: 0.24
Nodes (10): Request, build_request(), default_generator(), generate(), GenerationError, RuntimeError, Single-provider LLM client (OpenAI-compatible), fail-closed by design.  One mode, The provider failed. No retry with a different model — fail closed. (+2 more)

### Community 70 - "render.py"
Cohesion: 0.16
Nodes (16): _blob(), commit_hints(), _git(), _is_comparable(), _name_status(), Path, Run one git command, argv-style. Any failure is an exception: a changelog built, A ref -> its full commit sha. Raises WhatsnewError if it does not resolve, so a (+8 more)

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
Cohesion: 0.38
Nodes (9): Run all three detector families over the repo -> deterministic marks. Pure, 0-LL, scan(), _ctx(), Lane C gate — deterministic detectors flag by facts, are specific, and don't cra, test_determinism(), test_entropy_flags_the_backdoor_token(), test_specificity_no_false_positive_on_ordinary_strings(), test_topology_reaches_tokens_from_auth() (+1 more)

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
Cohesion: 0.39
Nodes (8): encode(), encode_table(), _field(), Any, TOON (Token-Oriented Object Notation) serializer — tabular subset.  One declarat, Serialize one table.      >>> print(encode_table("pages", ["file", "module"], [, Serialize several tables into one TOON document (newline-separated)., _row_values()

### Community 106 - "render_whatsnew_md"
Cohesion: 0.33
Nodes (5): Architecture, Dependencies, How to change safely, Key entry points, Purpose

### Community 107 - "encode"
Cohesion: 0.33
Nodes (5): Architecture, Dependencies, How to change safely, Key entry points, Purpose

### Community 108 - "write_scan"
Cohesion: 0.20
Nodes (15): Drop graph nodes whose source_file is gitignored/untracked, from ANY producer., Run the scanner and persist the graph to .isidore/graph.json., restrict_to_tracked(), write_scan(), build_impact(), _edges(), ImpactReport, Path (+7 more)

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
Cohesion: 0.50
Nodes (4): Drop the pipe-separated citation a model appends to its own bullets.      Observ, strip_inline_claim_rows(), test_a_bare_trailing_citation_is_stripped_too(), test_a_real_markdown_table_is_left_alone()

## Knowledge Gaps
- **283 isolated node(s):** `isidore-wiki`, `Wiki (isidore)`, `Why`, `Quickstart`, `What you get` (+278 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **5 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `compile_wiki()` connect `compile_wiki` to `cli.py`, `verify.py`, `module_of`, `test_claims.py`, `whatsnew.py`, `claims.py`, `surface.py`, `test_pcp_pipeline.py`, `knowledge.py`, `encode`, `assemble_context`, `GenerationError`, `test_reconcile.py`, `test_humanpack.py`, `src-isidore.md`, `render_whatsnew_md`, `assemble_context`, `compile_subsystems`, `security_banner`, `create_run_id`, `write_scan`?**
  _High betweenness centrality (0.037) - this node is a cross-community bridge._
- **Why does `IngestOptions` connect `IngestOptions` to `cli.py`, `home.py`, `git_repo.py`, `verify_page`, `mcp.py`, `_tool_read_only`?**
  _High betweenness centrality (0.034) - this node is a cross-community bridge._
- **Why does `VerifyContext` connect `verify.py` to `compile_wiki`, `scan`, `read_certificate`, `create_run_id`, `render.py`, `findings.py`, `test_humanpack.py`, `src-isidore.md`, `whatsnew.py`, `claims.py`, `pipeline.py`, `load_state`, `test_changeset.py`, `pcp.py`, `harvest_todos`, `plan_pages`, `write_items`?**
  _High betweenness centrality (0.034) - this node is a cross-community bridge._
- **Are the 32 inferred relationships involving `compile_wiki()` (e.g. with `test_compile_stores_claims_and_writes_claims_toon()` and `test_dry_run_still_detects_stale_claims_for_free()`) actually correct?**
  _`compile_wiki()` has 32 INFERRED edges - model-reasoned connections that need verification._
- **Are the 13 inferred relationships involving `VerifyContext` (e.g. with `CompileResult` and `PageSpec`) actually correct?**
  _`VerifyContext` has 13 INFERRED edges - model-reasoned connections that need verification._
- **Are the 15 inferred relationships involving `Predicate` (e.g. with `CertStatus` and `test_a_unique_declaration_can_still_be_refuted()`) actually correct?**
  _`Predicate` has 15 INFERRED edges - model-reasoned connections that need verification._
- **Are the 12 inferred relationships involving `run_whatsnew()` (e.g. with `test_a_false_predicate_is_kept_in_the_certificate_but_never_published()` and `test_a_phantom_path_earns_one_repair_attempt_then_a_visible_quarantine()`) actually correct?**
  _`run_whatsnew()` has 12 INFERRED edges - model-reasoned connections that need verification._