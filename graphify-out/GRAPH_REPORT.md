# Graph Report - isidore  (2026-07-27)

## Corpus Check
- 212 files · ~139,346 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1932 nodes · 4267 edges · 132 communities (127 shown, 5 thin omitted)
- Extraction: 83% EXTRACTED · 17% INFERRED · 0% AMBIGUOUS · INFERRED: 720 edges (avg confidence: 0.77)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `600a6c74`
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
- .ingest
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
- test_hostile_f6.py
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
- Path
- render_whatsnew_md
- encode
- write_scan
- tests-test_langspec_oracle_py.md
- tests-test_llms_txt_py.md
- test_pcp_pipeline.py
- tests-test_recertify_py.md
- strip_inline_claim_rows
- verify_predicate
- SurfaceSymbol
- render.py
- main
- apply_settings
- ClaimVerdict
- GitRepoConnector
- src-isidore-connect_py.md
- tests-test_connect_cli_py.md
- WhatsnewError
- seal_content
- render_whatsnew_toon
- tests-test_connectors_f5_py.md
- _cap_content
- harvest_todos
- render_findings
- tests-test_handoff_py.md
- tests-test_wiki_not_input_py.md

## God Nodes (most connected - your core abstractions)
1. `compile_wiki()` - 92 edges
2. `VerifyContext` - 64 edges
3. `IngestOptions` - 51 edges
4. `run_whatsnew()` - 39 edges
5. `Predicate` - 35 edges
6. `_make_repo()` - 31 edges
7. `load_graph()` - 28 edges
8. `read_state()` - 27 edges
9. `compile_overview()` - 26 edges
10. `build_delta()` - 26 edges

## Surprising Connections (you probably didn't know these)
- `test_an_unknown_connector_is_named_not_ignored()` --calls--> `main()`  [INFERRED]
  tests/test_connect_cli.py → src/isidore/cli.py
- `test_pcp_subcommands_are_registered()` --calls--> `main()`  [INFERRED]
  tests/test_pcp_seams.py → src/isidore/cli.py
- `test_cli_reports_a_bad_ref_without_writing_an_artifact()` --calls--> `main()`  [INFERRED]
  tests/test_whatsnew.py → src/isidore/cli.py
- `test_cli_smoke()` --calls--> `main()`  [INFERRED]
  tests/test_whatsnew.py → src/isidore/cli.py
- `test_the_listing_reports_readiness_without_reading_a_secret()` --calls--> `connector_summary()`  [INFERRED]
  tests/test_connect_cli.py → src/isidore/connect.py

## Import Cycles
- 1-file cycle: `src/isidore/connectors/__init__.py -> src/isidore/connectors/__init__.py`

## Communities (132 total, 5 thin omitted)

### Community 0 - "cli.py"
Cohesion: 0.13
Nodes (25): _answer_all(), _Args, _make_repo(), Path, `isidore handoff` — the caller is the model, so the source never leaves the mach, A provider's budget bounds spend. There is no spend here, so a cap would only hi, The lint gate asks a provider for one repair round. There is nobody to ask here, The facts moved under the answer. Certifying it would publish prose about a repo (+17 more)

### Community 1 - "graph.py"
Cohesion: 0.16
Nodes (22): git_head(), git_listed_files(), _is_binary(), _iter_source_files(), _node_id(), _norm_source_file(), Path, Structure graph: loading, module grouping, and a built-in multi-language scanner (+14 more)

### Community 2 - "compile_wiki"
Cohesion: 0.15
Nodes (38): compile_wiki(), lint_cited_paths(), File-looking paths cited in the prose that do NOT exist in the repo., Run the pipeline. With execute=False no LLM is called and no page is written., _gp(), _graph(), _link(), _make_repo() (+30 more)

### Community 3 - "read_certificate"
Cohesion: 0.11
Nodes (27): _cmd_findings(), _churn(), coverage_gap_candidates(), filter_findings(), finding_id(), findings_new(), harvest_todos(), insert_security_banner() (+19 more)

### Community 4 - "detectors.py"
Cohesion: 0.05
Nodes (37): _cmd_sync(), IngestOptions, Caps and scoping for a run. All limits live here (in code), never in a prompt., GitRepoConnector, (item, None) for a changed repo, (None, None) if HEAD is unchanged, (None, warni, Run a git command; return stdout or None on any failure (never raises)., _git(), _head() (+29 more)

### Community 5 - "verify.py"
Cohesion: 0.08
Nodes (57): AST, Module, Check every promoted contract against the current graph. Pure, 0-LLM., verify_contracts(), The result of checking one predicate against an oracle. `value` is TRUE|FALSE|UN, Everything a verifier needs, assembled once per page/verify run. Read-only to ve, undecidable(), Verdict (+49 more)

### Community 6 - "humanpack.py"
Cohesion: 0.05
Nodes (56): _looks_like_secret(), Path, Lane C — deterministic security detectors: entropy, sinks, topology. 0 LLM. (T-e, Files reachable from an auth/secret/crypto root via imports (BFS, file-level). 0, Run all three detector families over the repo -> deterministic marks. Pure, 0-LL, Shannon entropy per character (bits). Stdlib only., Return a reason if the literal is credential-shaped, else None., Repo-relative source files to scan: the graph's, or a bounded walk if the graph (+48 more)

### Community 7 - "quickstart.md"
Cohesion: 0.33
Nodes (4): Knowledge home (local, not in this repo), Wiki (isidore), Modules, Wiki (isidore)

### Community 8 - "findings.py"
Cohesion: 0.11
Nodes (35): Build the delta, optionally write the prose, and persist page + certificate., run_whatsnew(), WhatsnewResult, _commit(), _git(), _one_file_repo(), isidore whatsnew: the typed surface delta, its artifact, and the verification di, A date answers "when did someone run this", which nobody asks. A tag answers "wh (+27 more)

### Community 9 - "module_of"
Cohesion: 0.10
Nodes (32): affected_modules(), changed_lines(), changed_symbols(), _git_diff(), _module_fan_in(), modules_of(), Path, Change-set detection: which graph symbols a git diff touched, and which modules (+24 more)

### Community 10 - "test_claims.py"
Cohesion: 0.16
Nodes (25): check_claims(), claims_for_file(), claims_grep(), evidence_hash(), evidence_state(), _hash(), _normalize(), Path (+17 more)

### Community 11 - "home.py"
Cohesion: 0.11
Nodes (35): apply_settings(), _cmd_connect(), _cmd_ingest(), connector_summary(), load_config(), Path, `isidore connect` and `isidore ingest` — the CLI face of the connector layer (AD, Add `isidore connect` and `isidore ingest` (registrar loop in cli.main). (+27 more)

### Community 12 - "whatsnew.py"
Cohesion: 0.14
Nodes (13): DeltaEntry, _diff_surfaces(), generate_prose(), _group_by_module(), _llm_entries(), parse_plain_block(), One typed novelty row. `file` is always the path as of `until` (renames map old, Typed difference between two surfaces of the same file.      Identity is the q (+5 more)

### Community 13 - "build_certificate"
Cohesion: 0.16
Nodes (18): McpConnector, iter_items(), Yield stored items, newest run first. A corrupt/half-written JSONL line is skipp, _config(), Path, F5 (ADR-0032): the OAuth-heavy sources, delivered as MCP instance recipes rather, Every tool was called with `arguments: {}`, so no real source could be expressed, The card's third gate. A dead credential must not look like an empty mailbox. (+10 more)

### Community 14 - "pyramid.py"
Cohesion: 0.32
Nodes (7): _graph(), Lane D gate — the pyramid plans from the real graph, uses imports for cohesion,, BUG 1 regression: auto-seed used node['path'/'file'/'name'] (absent) -> []. Must, BUG 2 regression: `links` was ignored. imports edges must yield depends_on., test_autoseed_groups_by_source_file_on_the_real_graph(), test_explicit_config_still_works(), test_links_used_for_inter_subsystem_deps()

### Community 15 - "claims.py"
Cohesion: 0.08
Nodes (40): Counter, render_findings(), _is_wiki_output(), The repo-relative posix path of the wiki OUTPUT directory, normalised for prefix, wiki_output_prefix(), annotate_unverified_paths(), assemble_context(), context_hash() (+32 more)

### Community 16 - "surface.py"
Cohesion: 0.10
Nodes (27): Exception, _check_url(), fetch(), fetch_json(), FetchError, Bounded HTTP for the direct-API connectors (ADR-0032 F4). stdlib urllib, no depe, A fetch that did not produce a usable body. Carries a reason fit to show a user., Refuse anything that is not plain http(s).      urllib will happily open `file:/ (+19 more)

### Community 17 - "Isidore v2 — Incremental compilation, impact detection & residue mining"
Cohesion: 0.12
Nodes (16): 0 · Why (user directive), 1 · Verified bug diagnoses (2026-07-10, against real code — not reports), 2 · Design principles (unchanged bets, now enforced deeper), 3 · C0 — Scoped compile: `isidore compile --only <sel>[,<sel>…]`, 4 · C1+C2 — Change-driven compile: `isidore compile --changed [--since <ref>]`, 5 · C3 — Impact detection: `isidore impact [--since <ref>] [--md] [--check]` (new, **0 LLM always**), 6 · C4+C5+C6 — Correctness fixes (the right ones), 7 · C7 — Residue mining (all 0-LLM; the "squeeze everything" layer) (+8 more)

### Community 18 - "git_repo.py"
Cohesion: 0.13
Nodes (18): Match, _declaration_tail(), generic_surface(), _is_declaration(), _is_public(), logical_lines(), _param_group(), API surface extraction from SOURCE TEXT — the zero-LLM substrate of `isidore wha (+10 more)

### Community 19 - "VerifyContext"
Cohesion: 0.13
Nodes (23): all_connectors(), Connector, get(), IngestResult, _load_plugins(), Protocol, Connector protocol + registry (ADR-0032 F1).  A connector ingests raw items from, Outcome of one ingest run. `raw_files` are the JSONL files written this run. (+15 more)

### Community 20 - "IngestOptions"
Cohesion: 0.18
Nodes (11): clean_sig(), AsyncFunctionDef, _py_constant(), FunctionDef, _py_signature(), Collapse a declaration header into a stable one-line comparison key, readable as, The parameter list and return annotation, rendered from the AST rather than the, A module-level binding -> (name, `= value`). Config constants are API: a consume (+3 more)

### Community 21 - "pipeline.py"
Cohesion: 0.22
Nodes (15): extract(), _Pending, Extract (symbols, imported-module-names) from one file's source.      symbols:, The LanguageSpec for a file extension (lowercased), or None if we do not extract, spec_for(), _names(), Multi-language scanner: the declarative engine (langspec) and its wiring into sc, test_bodiless_declaration_stays_start_only() (+7 more)

### Community 22 - "mcp.py"
Cohesion: 0.17
Nodes (17): is_negative_existential(), True for statements asserting existential/definitional ABSENCE (unanchorable). C, parse_findings_block(), Split a generated page into (clean page, findings rows). Tolerant of malformed l, compile_topics(), knowledge_dir(), load_knowledge_state(), load_topics() (+9 more)

### Community 23 - "test_pcp_pipeline.py"
Cohesion: 0.10
Nodes (26): is_security_finding(), True if a suspect reads as a security risk (hardcoded secret, auth bypass, injec, A prominent, deterministic banner listing this page's security suspects — meant, security_banner(), security_suspects(), Verify that negation patterns do not trigger false positive security findings (6, Verify that safety-checks catch risks even with intermediate/intervening words., If the model attempts social engineering in prose while findings report the bug, (+18 more)

### Community 24 - "knowledge.py"
Cohesion: 0.11
Nodes (27): assert_may_send_source(), Classify wherever a compile would send this repository's source, as (kind, detai, Fail closed unless the destination may see this repository's content. `what` nam, source_destination(), _gp(), _make_repo(), Path, Compiling is a disclosure: where is this repository's source allowed to go?  U (+19 more)

### Community 25 - "plan_pages"
Cohesion: 0.15
Nodes (19): compile_overview(), missing_sections(), Required headings the page does not have. 0 LLM., Turn `wiki://page` into `page` in PROSE, so the links a reader clicks actually r, Compile the plain-language product page (N3). One LLM call, plus at most one rep, relink_wiki_uris(), The N3 product overview: plain language for anyone, resting on claims already pr, The module page above, registered in the wiki state so an area can find it. (+11 more)

### Community 26 - "pcp.py"
Cohesion: 0.15
Nodes (27): Predicate, A decidable assertion parsed from a claim's third field. Frozen: predicates are, literal_value(), parameter_names(), Parameter names in declaration order, or None when they cannot be read with conf, The literal a constant is bound to, or None when it is not a plain literal., value(name, literal): a module-level assignment `name = literal`. Oracles: AST,, signature(fn, a1, a2, ...): fn's positional parameter names, in order. Oracles: (+19 more)

### Community 27 - "_tool_read_only"
Cohesion: 0.15
Nodes (13): _name_looks_mutating(), (allowed, reason). Authority order: explicit readOnlyHint/destructiveHint > name, Fallback heuristic ONLY (not exhaustive): does the tool name contain a mutating, _tool_read_only(), _FakeClient, MCP connector read-only barrier (ADR-0032 F3). Regression for the review of T-db, Stands in for _JsonRpcClient: a server exposing one read tool, one write tool (a, test_destructive_hint_rejects() (+5 more)

### Community 28 - "PCP_SEAMS — the frozen interface for Proof-Carrying Prose (ADR-0033, phase P0)"
Cohesion: 0.15
Nodes (12): Certificate (`<page>.md` → `<page>.md.cert.json`, alongside the page), CLI, Contracts (`contracts.json` in the wiki dir), File ownership matrix (nobody edits another lane's files), How each lane starts (all depend ONLY on P0 = T-1dc9), Marks (lane C output; also the golden `marks.json`), PCP_SEAMS — the frozen interface for Proof-Carrying Prose (ADR-0033, phase P0), Pipeline hooks (lane A wires; signatures frozen) (+4 more)

### Community 29 - "encode"
Cohesion: 0.19
Nodes (28): Load a certificate from disk. Raises ValueError on malformed JSON (fail-closed f, read_certificate(), Re-run the oracles over every certified page. 0 LLM. Writes only with `write=Tru, recertify(), _cert(), _chained(), _claim(), Path (+20 more)

### Community 30 - "Mark"
Cohesion: 0.13
Nodes (19): check(), explain(), is_plain(), PlainRule, Pattern, Plain-language gate: can a reader who has never seen code use this sentence?  Do, Human-readable reason for a rejection, for the run summary and the journal., One named check. `kind` mirrors Vale's rule taxonomy so the intent of each is de (+11 more)

### Community 31 - "write_items"
Cohesion: 0.07
Nodes (38): Certificate, certificate_from_dict(), ClaimVerdict, parse_stored_predicate(), parse_wiki_uri(), Parse a predicate read back from a CERTIFICATE rather than from model output., One claim's line in a certificate: the anchored claim + its typed verdict (if an, The re-verifiable sidecar for one page. Persisted as JSON (machine-read). Tamper (+30 more)

### Community 32 - "isidore"
Cohesion: 0.12
Nodes (16): Bring your own graph, Config (`isidore.json`, optional), Design rules, isidore, Knowledge — the same contract, applied to what is NOT in your repo, Languages, License, One range, three readers (+8 more)

### Community 33 - "auth.py"
Cohesion: 0.29
Nodes (6): authenticate(), Auth service fixture for PCP lane tests. Line numbers are load-bearing: the gold, Verify the caller's JWT and enforce the attempt ceiling., Token service fixture for PCP lane tests. verify_jwt is defined on L5 (cited by, Return the decoded claims if the token's signature checks out, else None., verify_jwt()

### Community 35 - "scan"
Cohesion: 0.17
Nodes (23): _cmd_ask(), _cmd_compile(), _cmd_export_agora(), _cmd_impact(), _cmd_scan(), _cmd_stats(), _cmd_suggest_flows(), main() (+15 more)

### Community 36 - "assemble_context"
Cohesion: 0.12
Nodes (14): Gmail — instance recipe for the MCP connector, Sources, The config, The part you should actually worry about, Verifying it works, What it costs you to set up, What you get, Where the caps live (+6 more)

### Community 37 - "GenerationError"
Cohesion: 0.07
Nodes (50): _cmd_contracts(), Lane B (part 2) — claim->contract graduation + `isidore contracts`. (T-8dfc)  A, Add `isidore contracts` (promote / list / check)., Command implementation for `isidore contracts`., register_cli(), isidore — compile an agent-oriented wiki from your codebase's structure graph., answer_knowledge_offline(), answer_offline() (+42 more)

### Community 38 - "ClaimVerdict"
Cohesion: 0.22
Nodes (19): extract_surface(), python_surface(), Exact surface of one Python source text, or None if it does not parse.      No, Surface of one file's text, routed by extension. None = not comparable source., _by_name(), API surface extraction: qualified names, signatures as change keys, and the fold, test_extract_surface_returns_none_for_non_code(), test_generic_surface_disambiguates_same_named_methods_of_different_classes() (+11 more)

### Community 39 - "test_wiki_dir_env.py"
Cohesion: 0.31
Nodes (7): ISIDORE_WIKI_DIR redirects the compiled-wiki output directory.  WIKI_DIRNAME is, A nested WIKI_DIRNAME (e.g. doc/isidore) must create its parents, not crash., _reload_render(), test_save_state_creates_nested_wiki_dir(), test_wiki_dirname_blank_env_falls_back(), test_wiki_dirname_defaults_to_wiki(), test_wiki_dirname_honors_env()

### Community 40 - ".ingest"
Cohesion: 0.11
Nodes (15): parse_hits(), The `hits` array, or ValueError. A payload without one is malformed, not empty (, _allowed(), _JsonRpcClient, Any, Map tool name -> its MCP annotations via tools/list (paginated). Empty if the se, Normalise the allowlist into `{entry, arguments}` records, sorted for determinis, The readable text of an MCP tool result, falling back to compact JSON.      MCP (+7 more)

### Community 41 - "test_humanpack.py"
Cohesion: 0.27
Nodes (11): _cert_digest(), certificate_status(), _cmd_verify(), _ctx_for(), Path, Check a page against its sidecar certificate, offline, 0 LLM (invariant I11)., sha256 of a page's certificate file, "" if it is gone., (ok, cert) for one page. ok is False on any tamper/mismatch/missing-graph. (+3 more)

### Community 42 - "src-isidore.md"
Cohesion: 0.14
Nodes (23): parse_predicate_field(), Parse a claim's optional third field into a pcp.Predicate (or None). PCP typed-c, prose_hash(), Dispatch one predicate to its registered verifier. No verifier -> UNDECIDABLE (f, The tamper-evidence anchor: sha256 of the page prose (full hex, this is a machin, verify_predicate(), build_certificate(), Verify each claim's predicate, classify prose mass, hash the prose -> a re-verif (+15 more)

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
Nodes (13): build_cards(), Path, export-agora — bridge isidore's verified claims into Living-Library card DRAFTS, Return [(filename, content)] draft cards — one per wiki page with enough OK clai, render_card(), _slug(), write_cards(), _yaml_str() (+5 more)

### Community 55 - "load_state"
Cohesion: 0.08
Nodes (33): certificate_to_dict(), Contract, get_verifier(), parse_predicate(), Path, Protocol, Proof-Carrying Prose (PCP) — the frozen seam shared by every PCP lane.  This mod, A predicate verifier. MUST be deterministic and 0-LLM. Returns UNDECIDABLE, neve (+25 more)

### Community 56 - "render_whatsnew_md"
Cohesion: 0.17
Nodes (17): append_run(), Compile journal + per-page changelog — residue mining, all zero-LLM.  Every comp, Map each `## heading` to its body text (content before the first heading is keye, (H2 headings whose content changed / were added / removed, new_line_count - old_, Append an H2-level changelog entry to a page's state (capped). No-op if the pros, record_page_change(), section_diff(), _sections() (+9 more)

### Community 57 - "test_hostile_f6.py"
Cohesion: 0.19
Nodes (17): _item(), F6's hostile gate: what the knowledge home does when its own data is broken, eno, A cap that bites silently turns a partial answer into a confident one., The whole point of I8, end to end: an item that issues commands and forges a del, The second half of the defence: even if a forged URI reaches a claim, it has to, The honest failure. A claim whose evidence is gone must say so — the alternative, An interrupted append leaves a truncated last line. Losing the whole run over it, _store() (+9 more)

### Community 58 - "What's new — `HEAD~2..HEAD`"
Cohesion: 0.22
Nodes (14): _cmd_overview(), _cmd_pyramid(), _cmd_subsystems(), _load_graph_for(), _norm(), plan_pyramid(), Lane D — the pyramid: hierarchical synthesis with wiki:// claim chains. (T-af65, 0-LLM subsystem suggester: group files by top directory (the isidore graph uses (+6 more)

### Community 59 - "harvest_todos"
Cohesion: 0.22
Nodes (14): _brace(), _doc(), _js(), _kw_func(), _kw_type(), LanguageSpec, Pattern, Language-agnostic symbol extraction: one engine, the language is *data*.  Isid (+6 more)

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
Cohesion: 0.15
Nodes (21): assemble_topic_context(), data_fence(), item_classification(), provider_is_trusted(), A per-assembly nonce for the excerpt delimiter.      Ingested content is attacke, An item's confidentiality: `meta.classification`, else `classification:` in its, Whether the operator has declared the configured LLM provider fit to receive res, Assemble items matching streams and filters into citable facts.      External co (+13 more)

### Community 65 - "assemble_context"
Cohesion: 0.32
Nodes (7): A reconciler finding (lane B): the model's own outputs contradict each other. 0-, Violation, Lane B (part 1) — the reconciler: the model's own outputs cross-checked, 0 LLM., Helper to split file:line into (file, line)., Cross-check prose vs findings vs claims vs marks -> internal contradictions. Pur, reconcile(), _split_evidence()

### Community 66 - "compile_subsystems"
Cohesion: 0.44
Nodes (8): Run the scanner and persist the graph to .isidore/graph.json., write_scan(), _git(), isidore impact — the 0-LLM emergent-interaction detector, over a real git repo +, _seed_repo(), test_impact_check_exit_signal_and_clean(), test_impact_reports_a_new_cross_module_edge_as_emergent(), test_impact_reports_a_removed_edge()

### Community 67 - "reconcile"
Cohesion: 0.12
Nodes (36): A connector's persisted config, or {} if absent or corrupt. Never raises.      L, stored_config(), git-repo connector (ADR-0032 F1): local repositories as a knowledge source. No n, Minimal read-only MCP connector (ADR-0032 F3).  The implementation deliberately, create_run_id(), iso_now(), prune_runs(), The raw store: immutable ingested items + per-connector cursor state (ADR-0032 F (+28 more)

### Community 68 - "subsystem-tests.md"
Cohesion: 0.40
Nodes (4): How the work is divided, What it depends on, and what depends on it, What this area is responsible for, Where to start reading

### Community 69 - "security_banner"
Cohesion: 0.13
Nodes (17): build_delta(), _file_summary(), impact_summary(), _md_section(), A compact roll-up of what a whole added/removed file declares., The zero-LLM core: a typed API-surface difference between two revisions., The consequence of this range, in plain words, with zero LLM calls.      A non, The page, layered by READER rather than by topic.      The same range has thre (+9 more)

### Community 70 - "render.py"
Cohesion: 0.15
Nodes (23): _blob(), commit_hints(), _git(), _is_comparable(), _name_status(), _prompt_for_module(), Path, isidore whatsnew — a changelog you can re-verify, instead of one you have to tru (+15 more)

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
Cohesion: 0.18
Nodes (11): Map an import to a repo file id if the module resolves inside the repo., Build a structure graph for a repo in ANY language, zero dependencies (see modul, _resolve_import(), scan_repo(), test_scan_repo_is_multilanguage(), test_scan_repo_skips_binary_files(), test_scan_repo_tolerates_unreadable_and_empty(), test_scan_repo_unknown_text_becomes_bare_file_node() (+3 more)

### Community 102 - "subsystem-src.md"
Cohesion: 0.40
Nodes (4): How the work is divided, What it depends on, and what depends on it, What this area is responsible for, Where to start reading

### Community 103 - "v_calls"
Cohesion: 0.09
Nodes (30): parse_setting(), `key=value` -> (key, value). A value that parses as JSON is stored as JSON, so n, _cap_content(), Epoch second a commit must reach to be inside the window, or (None, note) if unb, Cap an item's content to `max_bytes` UTF-8 bytes, cutting on a character boundar, _window_floor(), _git(), _make_repo() (+22 more)

### Community 104 - "clean_sig"
Cohesion: 0.09
Nodes (34): _cmd_llms(), configured_wiki_dirname(), _first_sentence(), Path, The wiki, in the layout agents are converging on for being handed documentation., Write llms.txt at the repo root — where the convention puts it, so a fetcher fin, Where this repository keeps its living docs, relative to its root.      Preceden, Add `isidore llms` (regenerate llms.txt from whatever is compiled). 0 LLM. (+26 more)

### Community 105 - "Path"
Cohesion: 0.18
Nodes (15): _module_pages_of(), overview_facts(), _page_purpose(), Path, The compiled module pages that belong to one subsystem, keyed by page file name., The first sentence of a module page's `## Purpose` — what that module says it is, What one subsystem page is written from: its module pages, what each says it is, Every claim the pages below PROVED, as citable `wiki://page#id` facts.      This (+7 more)

### Community 106 - "render_whatsnew_md"
Cohesion: 0.33
Nodes (5): Architecture, Dependencies, How to change safely, Key entry points, Purpose

### Community 107 - "encode"
Cohesion: 0.33
Nodes (5): Architecture, Dependencies, How to change safely, Key entry points, Purpose

### Community 108 - "write_scan"
Cohesion: 0.15
Nodes (25): apply(), _cmd_handoff(), emit(), handoff_dir(), _plan(), prompt_id(), Path, `isidore handoff` — let the CALLER be the model, instead of shipping the code to (+17 more)

### Community 109 - "tests-test_langspec_oracle_py.md"
Cohesion: 0.33
Nodes (5): Architecture, Dependencies, How to change safely, Key entry points, Purpose

### Community 110 - "tests-test_llms_txt_py.md"
Cohesion: 0.33
Nodes (5): Architecture, Dependencies, How to change safely, Key entry points, Purpose

### Community 111 - "test_pcp_pipeline.py"
Cohesion: 0.29
Nodes (10): _compile(), _fake_generator(), _fake_generator_with_a_lie(), Path, P-INT gate — the pipeline wiring ties all five PCP lanes together end to end: a, test_compile_writes_a_certificate_with_typed_verdicts(), test_deterministic_mark_forces_the_banner_despite_calm_prose(), test_refuted_claim_is_quarantined_not_published() (+2 more)

### Community 112 - "tests-test_recertify_py.md"
Cohesion: 0.33
Nodes (5): Architecture, Dependencies, How to change safely, Key entry points, Purpose

### Community 113 - "strip_inline_claim_rows"
Cohesion: 0.13
Nodes (26): anchor_claims(), claim_id(), parse_claims_block(), Split a generated page into (clean page, raw claim rows). Tolerant of malformed, Deterministic, ledger-friendly id: stable across runs for the same (statement, e, Repair a shortened citation to a real file, or None if it can't be resolved uniq, Quarantine filter + anchoring. Returns (anchored claims, dropped, repaired)., resolve_citation() (+18 more)

### Community 114 - "verify_predicate"
Cohesion: 0.20
Nodes (9): Confirm the tool names before you trust this block, Setup, Slack — instance recipe for the MCP connector, Sources, The config, The part you should actually worry about, Verifying it works, What you get (+1 more)

### Community 115 - "SurfaceSymbol"
Cohesion: 0.21
Nodes (11): Request, build_request(), generate(), generate_via_cli(), GenerationError, RuntimeError, Single-provider LLM client (OpenAI-compatible), fail-closed by design.  One mode, The provider failed. No retry with a different model — fail closed. (+3 more)

### Community 116 - "render.py"
Cohesion: 0.22
Nodes (9): agents_md_block(), knowledge_summary(), Deterministic outputs: quickstart.md, index.toon, llms.txt, and the AGENTS.md re, The self-reference an agent reads before touching the repo. 0 LLM, idempotent., `{path, pages, streams}` for the local knowledge home, or {} if there is none. N, Insert or replace the delimited block without touching the rest of the file (ide, render_quickstart(), upsert_agents_block() (+1 more)

### Community 117 - "main"
Cohesion: 0.16
Nodes (13): degenerate_certificate(), A short reason when a certificate is a symptom rather than a certificate, else N, _Cert, nested_wiki_dir(), The wiki is OUTPUT. It must never round-trip into the input.  Reported from GIMO, GIMO's actual numbers. Writing this silently is how it reached 13 MB before anyo, Point the toolchain at GIMO's layout. WIKI_DIRNAME is resolved once at import so, GIMO's shape: the wiki lives several directories deep, at whatever the toolchain (+5 more)

### Community 118 - "apply_settings"
Cohesion: 0.31
Nodes (9): _chain_verdicts(), compile_subsystems(), Compile the N2 layer: one bounded call per area, each page chained to its module, Resolve `wiki://` claims through lane D's verifier and compose the child certifi, subsystem_page_name(), _nodes(), test_an_area_page_is_chained_to_the_module_pages_below_it(), test_an_area_with_nothing_proven_under_it_is_skipped_not_invented() (+1 more)

### Community 119 - "ClaimVerdict"
Cohesion: 0.33
Nodes (5): Architecture, Dependencies, How to change safely, Key entry points, Purpose

### Community 120 - "GitRepoConnector"
Cohesion: 0.50
Nodes (4): Drop the pipe-separated citation a model appends to its own bullets.      Obse, strip_inline_claim_rows(), test_a_bare_trailing_citation_is_stripped_too(), test_a_real_markdown_table_is_left_alone()

### Community 121 - "src-isidore-connect_py.md"
Cohesion: 0.33
Nodes (5): Architecture, Dependencies, How to change safely, Key entry points, Purpose

### Community 122 - "tests-test_connect_cli_py.md"
Cohesion: 0.33
Nodes (5): Architecture, Dependencies, How to change safely, Key entry points, Purpose

### Community 123 - "WhatsnewError"
Cohesion: 0.29
Nodes (7): RuntimeError, Git could not answer, or a ref does not resolve. Fail closed: never guess a rang, WhatsnewError, Its prompts carry an excerpt of every added and changed symbol — a compile by an, test_whatsnew_refuses_at_an_undeclared_host(), test_execute_refuses_a_range_that_does_not_end_at_head(), test_unresolvable_ref_fails_closed()

### Community 124 - "seal_content"
Cohesion: 0.50
Nodes (4): (content with any delimiter-shaped line defanged, how many were found).      Mar, seal_content(), test_innocent_content_is_left_exactly_as_it_was(), test_the_marking_removes_nothing_from_the_evidence()

### Community 125 - "render_whatsnew_toon"
Cohesion: 0.50
Nodes (4): _cmd_whatsnew(), The machine/agent view: one table per area, product surface first., render_whatsnew_toon(), test_test_files_are_reported_in_their_own_area()

### Community 130 - "tests-test_connectors_f5_py.md"
Cohesion: 0.33
Nodes (5): Architecture, Dependencies, How to change safely, Key entry points, Purpose

### Community 132 - "_cap_content"
Cohesion: 0.33
Nodes (5): Architecture, Dependencies, How to change safely, Key entry points, Purpose

### Community 133 - "harvest_todos"
Cohesion: 0.33
Nodes (5): Architecture, Dependencies, How to change safely, Key entry points, Purpose

### Community 134 - "render_findings"
Cohesion: 0.33
Nodes (5): Architecture, Dependencies, How to change safely, Key entry points, Purpose

### Community 135 - "tests-test_handoff_py.md"
Cohesion: 0.33
Nodes (5): Architecture, Dependencies, How to change safely, Key entry points, Purpose

### Community 136 - "tests-test_wiki_not_input_py.md"
Cohesion: 0.33
Nodes (5): Architecture, Dependencies, How to change safely, Key entry points, Purpose

## Knowledge Gaps
- **342 isolated node(s):** `isidore-wiki`, `Knowledge home (local, not in this repo)`, `Why`, `Quickstart`, `What you get` (+337 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **5 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `IngestOptions` connect `detectors.py` to `reconcile`, `scan`, `v_calls`, `.ingest`, `home.py`, `build_certificate`, `surface.py`, `VerifyContext`, `test_hostile_f6.py`, `_tool_read_only`?**
  _High betweenness centrality (0.074) - this node is a cross-community bridge._
- **Why does `compile_wiki()` connect `compile_wiki` to `graph.py`, `read_certificate`, `verify.py`, `humanpack.py`, `module_of`, `test_claims.py`, `claims.py`, `mcp.py`, `test_pcp_pipeline.py`, `knowledge.py`, `encode`, `scan`, `GenerationError`, `test_humanpack.py`, `src-isidore.md`, `verify_page`, `load_state`, `render_whatsnew_md`, `assemble_context`, `compile_subsystems`, `write_scan`, `test_pcp_pipeline.py`, `strip_inline_claim_rows`, `SurfaceSymbol`, `render.py`, `main`?**
  _High betweenness centrality (0.063) - this node is a cross-community bridge._
- **Why does `VerifyContext` connect `verify.py` to `compile_wiki`, `pcp.py`, `GenerationError`, `humanpack.py`, `render.py`, `findings.py`, `test_humanpack.py`, `src-isidore.md`, `write_scan`, `whatsnew.py`, `claims.py`, `apply_settings`, `load_state`, `plan_pages`, `What's new — `HEAD~2..HEAD``, `WhatsnewError`, `write_items`?**
  _High betweenness centrality (0.037) - this node is a cross-community bridge._
- **Are the 35 inferred relationships involving `compile_wiki()` (e.g. with `test_compile_stores_claims_and_writes_claims_toon()` and `test_dry_run_still_detects_stale_claims_for_free()`) actually correct?**
  _`compile_wiki()` has 35 INFERRED edges - model-reasoned connections that need verification._
- **Are the 13 inferred relationships involving `VerifyContext` (e.g. with `CompileResult` and `PageSpec`) actually correct?**
  _`VerifyContext` has 13 INFERRED edges - model-reasoned connections that need verification._
- **Are the 33 inferred relationships involving `IngestOptions` (e.g. with `GitRepoConnector` and `HackerNewsConnector`) actually correct?**
  _`IngestOptions` has 33 INFERRED edges - model-reasoned connections that need verification._
- **Are the 19 inferred relationships involving `run_whatsnew()` (e.g. with `test_whatsnew_refuses_at_an_undeclared_host()` and `test_a_false_predicate_is_kept_in_the_certificate_but_never_published()`) actually correct?**
  _`run_whatsnew()` has 19 INFERRED edges - model-reasoned connections that need verification._