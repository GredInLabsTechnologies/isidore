# Graph Report - isidore  (2026-07-26)

## Corpus Check
- 165 files · ~99,934 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1362 nodes · 2963 edges · 103 communities (97 shown, 6 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 423 edges (avg confidence: 0.77)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `bf9b1d68`
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
- `test_three_field_parser_captures_predicate()` --calls--> `parse_claims_block()`  [INFERRED]
  tests/test_verify.py → src/isidore/claims.py
- `test_pcp_subcommands_are_registered()` --calls--> `main()`  [INFERRED]
  tests/test_pcp_seams.py → src/isidore/cli.py
- `test_cli_reports_a_bad_ref_without_writing_an_artifact()` --calls--> `main()`  [INFERRED]
  tests/test_whatsnew.py → src/isidore/cli.py
- `test_cli_smoke()` --calls--> `main()`  [INFERRED]
  tests/test_whatsnew.py → src/isidore/cli.py
- `test_filter_findings_drops_hallucinated_paths()` --calls--> `filter_findings()`  [INFERRED]
  tests/test_units.py → src/isidore/findings.py

## Import Cycles
- 1-file cycle: `src/isidore/connectors/__init__.py -> src/isidore/connectors/__init__.py`

## Communities (103 total, 6 thin omitted)

### Community 0 - "cli.py"
Cohesion: 0.13
Nodes (33): check_claims(), claims_for_file(), claims_grep(), Re-hash every stored claim's evidence — the zero-LLM staleness audit.      Retur, The documentation contract of a file: every anchored claim whose evidence points, Free-text search over verified atomic facts — answers many questions with 0 LLM, _cmd_ask(), _cmd_claims() (+25 more)

### Community 1 - "graph.py"
Cohesion: 0.10
Nodes (37): answer_knowledge_offline(), answer_offline(), ask(), ask_knowledge(), gather_claims(), gather_evidence(), gather_knowledge_claims(), Path (+29 more)

### Community 2 - "compile_wiki"
Cohesion: 0.18
Nodes (30): compile_wiki(), lint_cited_paths(), File-looking paths cited in the prose that do NOT exist in the repo., Run the pipeline. With execute=False no LLM is called and no page is written., _gp(), _link(), _make_repo(), _node() (+22 more)

### Community 3 - "read_certificate"
Cohesion: 0.20
Nodes (12): Contract, Path, Proof-Carrying Prose (PCP) — the frozen seam shared by every PCP lane.  This mod, Load promoted contracts (empty list if the file is absent). Malformed -> ValueEr, Persist contracts as JSON (machine-read gate input)., A typed claim a human promoted to an invariant. `isidore verify --contracts` fai, read_contracts(), write_contracts() (+4 more)

### Community 4 - "detectors.py"
Cohesion: 0.14
Nodes (22): _looks_like_secret(), Path, Lane C — deterministic security detectors: entropy, sinks, topology. 0 LLM. (T-e, Files reachable from an auth/secret/crypto root via imports (BFS, file-level). 0, Run all three detector families over the repo -> deterministic marks. Pure, 0-LL, Shannon entropy per character (bits). Stdlib only., Return a reason if the literal is credential-shaped, else None., Repo-relative source files to scan: the graph's, or a bounded walk if the graph (+14 more)

### Community 5 - "verify.py"
Cohesion: 0.17
Nodes (29): Lane B (part 2) — claim->contract graduation + `isidore contracts`. (T-8dfc)  A, Check every promoted contract against the current graph. Pure, 0-LLM., verify_contracts(), The result of checking one predicate against an oracle. `value` is TRUE|FALSE|UN, Everything a verifier needs, assembled once per page/verify run. Read-only to ve, undecidable(), Verdict, VerifyContext (+21 more)

### Community 6 - "humanpack.py"
Cohesion: 0.12
Nodes (26): _cmd_render(), _esc(), generate_architecture_map(), generate_claims_table(), generate_contracts_section(), generate_glossary(), generate_mass_bar(), minimal_markdown_to_html() (+18 more)

### Community 7 - "quickstart.md"
Cohesion: 0.40
Nodes (3): Wiki (isidore), Modules, Wiki (isidore)

### Community 8 - "findings.py"
Cohesion: 0.09
Nodes (45): build_delta(), impact_summary(), _md_section(), RuntimeError, Git could not answer, or a ref does not resolve. Fail closed: never guess a rang, The zero-LLM core: a typed API-surface difference between two revisions.      Pr, The consequence of this range, in plain words, with zero LLM calls.      A non-t, The page, layered by READER rather than by topic.      The same range has three (+37 more)

### Community 9 - "module_of"
Cohesion: 0.11
Nodes (28): affected_modules(), changed_lines(), changed_symbols(), _git_diff(), _module_fan_in(), modules_of(), Path, Change-set detection: which graph symbols a git diff touched, and which modules (+20 more)

### Community 10 - "test_claims.py"
Cohesion: 0.14
Nodes (25): anchor_claims(), claim_id(), parse_claims_block(), Split a generated page into (clean page, raw claim rows). Tolerant of malformed, Deterministic, ledger-friendly id: stable across runs for the same (statement, e, Repair a shortened citation to a real file, or None if it can't be resolved uniq, Quarantine filter + anchoring. Returns (anchored claims, dropped, repaired)., resolve_citation() (+17 more)

### Community 11 - "home.py"
Cohesion: 0.20
Nodes (17): prune_runs(), Run ids from state (already newest-first); fall back to sorting the raw dir if s, Drop all but the newest `keep` runs, deleting their raw dirs and trimming state., Current state, or a fresh default if missing OR corrupt (I13-style recovery, nev, Atomic write (tmp + os.replace) so a crash mid-write never corrupts the live sta, read_state(), _run_ids_newest_first(), write_state() (+9 more)

### Community 12 - "whatsnew.py"
Cohesion: 0.07
Nodes (44): annotate_unverified_paths(), Annotate every cited path that does not exist in the repo, inline and visibly —, One declared symbol of a file, as of one revision of its text.      `qualname` i, SurfaceSymbol, _blob(), _cmd_whatsnew(), commit_hints(), DeltaEntry (+36 more)

### Community 13 - "build_certificate"
Cohesion: 0.18
Nodes (16): parse_predicate_field(), Parse a claim's optional third field into a pcp.Predicate (or None). PCP typed-c, prose_hash(), The tamper-evidence anchor: sha256 of the page prose (full hex, this is a machin, build_certificate(), _cmd_verify(), _ctx_for(), Path (+8 more)

### Community 14 - "pyramid.py"
Cohesion: 0.29
Nodes (9): plan_pyramid(), Plan deterministic N2 subsystem + N3 product pages. 0 LLM.      Explicit `pyrami, _graph(), Lane D gate — the pyramid plans from the real graph, uses imports for cohesion,, BUG 1 regression: auto-seed used node['path'/'file'/'name'] (absent) -> []. Must, BUG 2 regression: `links` was ignored. imports edges must yield depends_on., test_autoseed_groups_by_source_file_on_the_real_graph(), test_explicit_config_still_works() (+1 more)

### Community 15 - "claims.py"
Cohesion: 0.09
Nodes (25): coverage_gap_candidates(), insert_security_banner(), Place the banner right under the page's H1 (or at the very top if there is none), Module pages with no inbound link from any test-looking module., isidore — compile an agent-oriented wiki from your codebase's structure graph., append_run(), CompileResult, context_hash() (+17 more)

### Community 16 - "surface.py"
Cohesion: 0.09
Nodes (40): Match, _brace(), _doc(), extract(), _js(), _kw_func(), _kw_type(), LanguageSpec (+32 more)

### Community 17 - "Isidore v2 — Incremental compilation, impact detection & residue mining"
Cohesion: 0.12
Nodes (16): 0 · Why (user directive), 1 · Verified bug diagnoses (2026-07-10, against real code — not reports), 2 · Design principles (unchanged bets, now enforced deeper), 3 · C0 — Scoped compile: `isidore compile --only <sel>[,<sel>…]`, 4 · C1+C2 — Change-driven compile: `isidore compile --changed [--since <ref>]`, 5 · C3 — Impact detection: `isidore impact [--since <ref>] [--md] [--check]` (new, **0 LLM always**), 6 · C4+C5+C6 — Correctness fixes (the right ones), 7 · C7 — Residue mining (all 0-LLM; the "squeeze everything" layer) (+8 more)

### Community 18 - "git_repo.py"
Cohesion: 0.23
Nodes (14): all_connectors(), Connector, get(), IngestResult, _load_plugins(), missing_env(), Protocol, Connector protocol + registry (ADR-0032 F1).  A connector ingests raw items from (+6 more)

### Community 19 - "VerifyContext"
Cohesion: 0.17
Nodes (17): Counter, render_findings(), _match_seed(), module_dep_edges(), plan_flows(), plan_pages(), Cross-module dependency edges (src_module, dst_module) -> link count. Shared by, Module pages from the graph: top-K modules holding at least min_symbols code sym (+9 more)

### Community 20 - "IngestOptions"
Cohesion: 0.18
Nodes (15): IngestOptions, Caps and scoping for a run. All limits live here (in code), never in a prompt., GitRepoConnector, _git(), _head(), _make_repo(), F1 (ADR-0032): knowledge home + raw store + git-repo connector.  The load-bearin, Regression: a real repo's commit messages carry UTF-8 (accents, emoji). On Windo (+7 more)

### Community 21 - "pipeline.py"
Cohesion: 0.11
Nodes (30): _chain_verdicts(), _cmd_overview(), _cmd_pyramid(), _cmd_subsystems(), _load_graph_for(), _module_pages_of(), _norm(), overview_facts() (+22 more)

### Community 22 - "mcp.py"
Cohesion: 0.17
Nodes (11): _allowed(), _JsonRpcClient, McpConnector, Any, Minimal read-only MCP connector (ADR-0032 F3).  The implementation deliberately, Map tool name -> its MCP annotations via tools/list (paginated). Empty if the se, create_run_id(), Sortable, collision-resistant run id (UTC second + millis). (+3 more)

### Community 23 - "test_pcp_pipeline.py"
Cohesion: 0.26
Nodes (12): Load a certificate from disk. Raises ValueError on malformed JSON (fail-closed f, read_certificate(), _compile(), _fake_generator(), _fake_generator_with_a_lie(), Path, P-INT gate — the pipeline wiring ties all five PCP lanes together end to end: a, test_compile_writes_a_certificate_with_typed_verdicts() (+4 more)

### Community 24 - "knowledge.py"
Cohesion: 0.15
Nodes (23): is_negative_existential(), True for statements asserting existential/definitional ABSENCE (unanchorable). C, parse_findings_block(), Split a generated page into (clean page, findings rows). Tolerant of malformed l, chmod that never raises; a no-op on Windows where POSIX modes don't apply., mkdir -p with restrictive mode, best-effort — never raises on a perms/FS quirk., safe_chmod(), safe_mkdir() (+15 more)

### Community 25 - "plan_pages"
Cohesion: 0.13
Nodes (25): compile_overview(), compile_subsystems(), missing_sections(), Compile the N2 layer: one bounded call per area, each page chained to its module, Required headings the page does not have. 0 LLM., Turn `wiki://page` into `page` in PROSE, so the links a reader clicks actually r, Compile the plain-language product page (N3). One LLM call, plus at most one rep, relink_wiki_uris() (+17 more)

### Community 26 - "pcp.py"
Cohesion: 0.16
Nodes (15): parse_predicate(), Predicate, A decidable assertion parsed from a claim's third field. Frozen: predicates are, Parse "<kind>:<a>;<b>" -> Predicate, or None if absent/malformed/unknown-kind., _claim_verdict(), Resolve (verdict, state) for a cited claim. Truth comes from the page's certific, Resolve a wiki:// chain. Fail-closed: None/invalid/missing -> not TRUE, never cr, _wikichain_verifier() (+7 more)

### Community 27 - "_tool_read_only"
Cohesion: 0.26
Nodes (11): _name_looks_mutating(), Fallback heuristic ONLY (not exhaustive): does the tool name contain a mutating, (allowed, reason). Authority order: explicit readOnlyHint/destructiveHint > name, _tool_read_only(), MCP connector read-only barrier (ADR-0032 F3). Regression for the review of T-db, test_destructive_hint_rejects(), test_ingest_invokes_only_read_only_tools(), test_mutating_names_are_rejected_without_annotation() (+3 more)

### Community 28 - "PCP_SEAMS — the frozen interface for Proof-Carrying Prose (ADR-0033, phase P0)"
Cohesion: 0.15
Nodes (12): Certificate (`<page>.md` → `<page>.md.cert.json`, alongside the page), CLI, Contracts (`contracts.json` in the wiki dir), File ownership matrix (nobody edits another lane's files), How each lane starts (all depend ONLY on P0 = T-1dc9), Marks (lane C output; also the golden `marks.json`), PCP_SEAMS — the frozen interface for Proof-Carrying Prose (ADR-0033, phase P0), Pipeline hooks (lane A wires; signatures frozen) (+4 more)

### Community 29 - "encode"
Cohesion: 0.08
Nodes (35): _cmd_contracts(), Add `isidore contracts` (promote / list / check)., Command implementation for `isidore contracts`., register_cli(), Run the scanner and persist the graph to .isidore/graph.json., write_scan(), Compile journal + per-page changelog — residue mining, all zero-LLM.  Every comp, Map each `## heading` to its body text (content before the first heading is keye (+27 more)

### Community 30 - "Mark"
Cohesion: 0.15
Nodes (17): check(), explain(), is_plain(), PlainRule, Pattern, Plain-language gate: can a reader who has never seen code use this sentence?  Do, Human-readable reason for a rejection, for the run summary and the journal., One named check. `kind` mirrors Vale's rule taxonomy so the intent of each is de (+9 more)

### Community 31 - "write_items"
Cohesion: 0.24
Nodes (10): Request, build_request(), default_generator(), generate(), GenerationError, RuntimeError, Single-provider LLM client (OpenAI-compatible), fail-closed by design.  One mode, The provider failed. No retry with a different model — fail closed. (+2 more)

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
Cohesion: 0.17
Nodes (23): evidence_hash(), evidence_state(), _hash(), _normalize(), Path, Claims: the atomic, evidence-anchored form of wiki knowledge.  A claim is a sing, Collapse all whitespace runs to single spaces and trim — so re-indentation, trai, Fingerprint of the CITED LINE's normalized content (whole normalized file if no (+15 more)

### Community 38 - "ClaimVerdict"
Cohesion: 0.12
Nodes (30): clean_sig(), extract_surface(), AsyncFunctionDef, _py_constant(), FunctionDef, _py_signature(), python_surface(), Collapse a declaration header into a stable one-line comparison key, readable as (+22 more)

### Community 39 - "test_wiki_dir_env.py"
Cohesion: 0.31
Nodes (7): ISIDORE_WIKI_DIR redirects the compiled-wiki output directory.  WIKI_DIRNAME is, A nested WIKI_DIRNAME (e.g. doc/isidore) must create its parents, not crash., _reload_render(), test_save_state_creates_nested_wiki_dir(), test_wiki_dirname_blank_env_falls_back(), test_wiki_dirname_defaults_to_wiki(), test_wiki_dirname_honors_env()

### Community 40 - "test_reconcile.py"
Cohesion: 0.21
Nodes (17): _cmd_llms(), _first_sentence(), Path, The wiki, in the layout agents are converging on for being handed documentation., Write llms.txt at the repo root — where the convention puts it, so a fetcher fin, Add `isidore llms` (regenerate llms.txt from whatever is compiled). 0 LLM., register_cli(), render_llms_txt() (+9 more)

### Community 41 - "test_humanpack.py"
Cohesion: 0.23
Nodes (12): get_verifier(), Dispatch one predicate to its registered verifier. No verifier -> UNDECIDABLE (f, verify_predicate(), _anchored(), _ctx(), Lane A gate — the typed-claim verifiers decide truth against the two oracles, bu, Dogfood regression: the graph's import edges are partial and `value` can't compa, test_certificate_matches_golden_verdicts() (+4 more)

### Community 42 - "src-isidore.md"
Cohesion: 0.23
Nodes (12): Certificate, certificate_to_dict(), ClaimVerdict, One claim's line in a certificate: the anchored claim + its typed verdict (if an, The re-verifiable sidecar for one page. Persisted as JSON (machine-read). Tamper, Certificate -> plain dict (asdict handles the nested dataclasses). The JSON on d, Persist a certificate as pretty JSON (stable key order for byte-deterministic di, write_certificate() (+4 more)

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
Nodes (16): AST, _claim_symbols(), classify_mass(), ground_symbols(), _literal_str(), _prose_identifiers(), Lane A — typed-claim verifiers, certificate building, `isidore verify`. (ADR-003, Return prose identifiers that DON'T resolve to any graph symbol or file (groundi (+8 more)

### Community 55 - "load_state"
Cohesion: 0.20
Nodes (9): parse_wiki_uri(), wiki://<page>#<claim-id> -> (page, claim_id), or None if it is not a wiki URI., P0 gate (ADR-0033) — the frozen PCP seam parses its golden fixtures and exposes, The frozen signatures exist and return the seam's types (whether stub or impleme, test_golden_graph_loads(), test_golden_marks_and_pyramid_config_parse(), test_lane_public_surfaces_return_frozen_types(), test_pcp_subcommands_are_registered() (+1 more)

### Community 56 - "render_whatsnew_md"
Cohesion: 0.32
Nodes (3): Run a git command; return stdout or None on any failure (never raises)., (item, None) for a changed repo, (None, None) if HEAD is unchanged, (None, warni, iso_now()

### Community 58 - "What's new — `HEAD~2..HEAD`"
Cohesion: 0.29
Nodes (6): Every change, in detail, In plain words, Internal surface, Public API, Tests, What's new — `HEAD~2..HEAD`

### Community 59 - "harvest_todos"
Cohesion: 0.06
Nodes (48): _cmd_findings(), _churn(), filter_findings(), finding_id(), findings_new(), harvest_todos(), is_finding_resolved(), is_security_finding() (+40 more)

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
Cohesion: 0.32
Nodes (8): assemble_context(), git_log_for(), Path, ±radius lines around a graph `L<n>` location. Tolerates stale files/locations., Gather one page's facts. Returns (context, truncation-warnings)., read_excerpt(), save_state(), test_read_excerpt_exact_lines_and_tolerance()

### Community 66 - "compile_subsystems"
Cohesion: 0.40
Nodes (4): Protocol, A predicate verifier. MUST be deterministic and 0-LLM. Returns UNDECIDABLE, neve, register_verifier(), Verifier

### Community 67 - "reconcile"
Cohesion: 0.20
Nodes (13): format_mark(), generate_security_banner(), certificate_from_dict(), Mark, A deterministic security-relevant flag raised BEFORE the LLM call (lane C)., A reconciler finding (lane B): the model's own outputs contradict each other. 0-, Rebuild a Certificate from parsed JSON, reconstructing the nested dataclasses. T, Violation (+5 more)

### Community 68 - "subsystem-tests.md"
Cohesion: 0.40
Nodes (4): How the work is divided, What it depends on, and what depends on it, What this area is responsible for, Where to start reading

### Community 69 - "security_banner"
Cohesion: 0.50
Nodes (4): Module, _find_funcdef(), AsyncFunctionDef, FunctionDef

### Community 70 - "render.py"
Cohesion: 0.50
Nodes (4): Drop the pipe-separated citation a model appends to its own bullets.      Observ, strip_inline_claim_rows(), test_a_bare_trailing_citation_is_stripped_too(), test_a_real_markdown_table_is_left_alone()

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
Cohesion: 0.33
Nodes (4): Algorithmically suggest topics from ingested raw items (0-LLM, term frequency ba, suggest_topics(), test_filter_findings_with_src(), test_suggest_topics()

### Community 102 - "subsystem-src.md"
Cohesion: 0.40
Nodes (4): How the work is divided, What it depends on, and what depends on it, What this area is responsible for, Where to start reading

## Knowledge Gaps
- **258 isolated node(s):** `isidore-wiki`, `Wiki (isidore)`, `Why`, `Quickstart`, `What you get` (+253 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **6 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `compile_wiki()` connect `compile_wiki` to `cli.py`, `graph.py`, `detectors.py`, `verify.py`, `module_of`, `test_claims.py`, `whatsnew.py`, `build_certificate`, `claims.py`, `VerifyContext`, `test_pcp_pipeline.py`, `knowledge.py`, `encode`, `write_items`, `scan`, `assemble_context`, `GenerationError`, `src-isidore.md`, `harvest_todos`, `assemble_context`, `reconcile`?**
  _High betweenness centrality (0.054) - this node is a cross-community bridge._
- **Why does `IngestOptions` connect `IngestOptions` to `cli.py`, `git_repo.py`, `mcp.py`, `render_whatsnew_md`, `test_changeset.py`, `_tool_read_only`?**
  _High betweenness centrality (0.043) - this node is a cross-community bridge._
- **Why does `VerifyContext` connect `verify.py` to `compile_subsystems`, `read_certificate`, `detectors.py`, `compile_wiki`, `findings.py`, `test_humanpack.py`, `whatsnew.py`, `build_certificate`, `claims.py`, `pipeline.py`, `verify_page`, `load_state`, `plan_pages`, `pcp.py`?**
  _High betweenness centrality (0.042) - this node is a cross-community bridge._
- **Are the 30 inferred relationships involving `compile_wiki()` (e.g. with `test_compile_stores_claims_and_writes_claims_toon()` and `test_dry_run_still_detects_stale_claims_for_free()`) actually correct?**
  _`compile_wiki()` has 30 INFERRED edges - model-reasoned connections that need verification._
- **Are the 12 inferred relationships involving `VerifyContext` (e.g. with `CompileResult` and `PageSpec`) actually correct?**
  _`VerifyContext` has 12 INFERRED edges - model-reasoned connections that need verification._
- **Are the 12 inferred relationships involving `run_whatsnew()` (e.g. with `test_a_false_predicate_is_kept_in_the_certificate_but_never_published()` and `test_a_phantom_path_earns_one_repair_attempt_then_a_visible_quarantine()`) actually correct?**
  _`run_whatsnew()` has 12 INFERRED edges - model-reasoned connections that need verification._
- **Are the 7 inferred relationships involving `load_graph()` (e.g. with `_ctx()` and `test_golden_graph_loads()`) actually correct?**
  _`load_graph()` has 7 INFERRED edges - model-reasoned connections that need verification._