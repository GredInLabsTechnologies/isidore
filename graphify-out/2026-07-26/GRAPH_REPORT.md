# Graph Report - isidore  (2026-07-25)

## Corpus Check
- 87 files · ~64,280 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1046 nodes · 2474 edges · 54 communities (49 shown, 5 thin omitted)
- Extraction: 85% EXTRACTED · 15% INFERRED · 0% AMBIGUOUS · INFERRED: 379 edges (avg confidence: 0.76)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `14a96ad8`
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

## God Nodes (most connected - your core abstractions)
1. `compile_wiki()` - 80 edges
2. `VerifyContext` - 49 edges
3. `_make_repo()` - 31 edges
4. `run_whatsnew()` - 26 edges
5. `load_graph()` - 24 edges
6. `build_delta()` - 23 edges
7. `IngestOptions` - 21 edges
8. `Predicate` - 21 edges
9. `check_claims()` - 20 edges
10. `compile_topics()` - 20 edges

## Surprising Connections (you probably didn't know these)
- `test_pcp_subcommands_are_registered()` --calls--> `main()`  [INFERRED]
  tests/test_pcp_seams.py → src/isidore/cli.py
- `test_cli_reports_a_bad_ref_without_writing_an_artifact()` --calls--> `main()`  [INFERRED]
  tests/test_whatsnew.py → src/isidore/cli.py
- `test_cli_smoke()` --calls--> `main()`  [INFERRED]
  tests/test_whatsnew.py → src/isidore/cli.py
- `test_filter_findings_drops_hallucinated_paths()` --calls--> `filter_findings()`  [INFERRED]
  tests/test_units.py → src/isidore/findings.py
- `test_golden_graph_loads()` --calls--> `load_graph()`  [INFERRED]
  tests/test_pcp_seams.py → src/isidore/graph.py

## Import Cycles
- 1-file cycle: `src/isidore/connectors/__init__.py -> src/isidore/connectors/__init__.py`

## Hyperedges (group relationships)
- **Isidore Compilation Flow** — src_isidore_pipeline, src_isidore_graph, src_isidore_claims, src_isidore_findings [EXTRACTED 1.00]

## Communities (54 total, 5 thin omitted)

### Community 0 - "cli.py"
Cohesion: 0.06
Nodes (72): check_claims(), claims_for_file(), claims_grep(), Path, Re-hash every stored claim's evidence — the zero-LLM staleness audit.      Retur, The documentation contract of a file: every anchored claim whose evidence points, Free-text search over verified atomic facts — answers many questions with 0 LLM, render_claims() (+64 more)

### Community 1 - "graph.py"
Cohesion: 0.06
Nodes (67): git_head(), git_listed_files(), _is_binary(), _iter_source_files(), _node_id(), _norm_source_file(), Path, Structure graph: loading, module grouping, and a built-in multi-language scanner (+59 more)

### Community 2 - "compile_wiki"
Cohesion: 0.21
Nodes (27): compile_wiki(), Run the pipeline. With execute=False no LLM is called and no page is written., _gp(), _link(), _make_repo(), _node(), Path, Compiler pipeline tests — no network: the LLM generator is always injected and c (+19 more)

### Community 3 - "read_certificate"
Cohesion: 0.12
Nodes (22): Certificate, certificate_from_dict(), certificate_to_dict(), Path, A reconciler finding (lane B): the model's own outputs contradict each other. 0-, The re-verifiable sidecar for one page. Persisted as JSON (machine-read). Tamper, Certificate -> plain dict (asdict handles the nested dataclasses). The JSON on d, Rebuild a Certificate from parsed JSON, reconstructing the nested dataclasses. T (+14 more)

### Community 4 - "detectors.py"
Cohesion: 0.21
Nodes (11): _looks_like_secret(), Path, Lane C — deterministic security detectors: entropy, sinks, topology. 0 LLM. (T-e, Shannon entropy per character (bits). Stdlib only., Return a reason if the literal is credential-shaped, else None., Repo-relative source files to scan: the graph's, or a bounded walk if the graph, Entropy + sink marks for one file. Never raises (unreadable file -> no marks)., _scan_file() (+3 more)

### Community 5 - "verify.py"
Cohesion: 0.12
Nodes (38): AST, Module, The result of checking one predicate against an oracle. `value` is TRUE|FALSE|UN, undecidable(), Verdict, _ast_of(), _file_nodes(), _find_funcdef() (+30 more)

### Community 6 - "humanpack.py"
Cohesion: 0.17
Nodes (20): _cmd_render(), _esc(), generate_architecture_map(), generate_claims_table(), generate_contracts_section(), generate_glossary(), generate_mass_bar(), minimal_markdown_to_html() (+12 more)

### Community 7 - "quickstart.md"
Cohesion: 0.40
Nodes (3): Wiki (isidore), Modules, Wiki (isidore)

### Community 8 - "findings.py"
Cohesion: 0.06
Nodes (49): _churn(), filter_findings(), finding_id(), harvest_todos(), insert_security_banner(), is_finding_resolved(), is_security_finding(), orphan_file_candidates() (+41 more)

### Community 9 - "module_of"
Cohesion: 0.13
Nodes (24): affected_modules(), changed_lines(), changed_symbols(), _git_diff(), _module_fan_in(), modules_of(), Path, Change-set detection: which graph symbols a git diff touched, and which modules (+16 more)

### Community 10 - "test_claims.py"
Cohesion: 0.13
Nodes (26): anchor_claims(), claim_id(), parse_claims_block(), Split a generated page into (clean page, raw claim rows). Tolerant of malformed, Deterministic, ledger-friendly id: stable across runs for the same (statement, e, Repair a shortened citation to a real file, or None if it can't be resolved uniq, Quarantine filter + anchoring. Returns (anchored claims, dropped, repaired)., resolve_citation() (+18 more)

### Community 11 - "home.py"
Cohesion: 0.23
Nodes (15): prune_runs(), Drop all but the newest `keep` runs, deleting their raw dirs and trimming state., Atomic write (tmp + os.replace) so a crash mid-write never corrupts the live sta, write_state(), config_path(), connector_dir(), home(), knowledge_dir() (+7 more)

### Community 12 - "whatsnew.py"
Cohesion: 0.05
Nodes (81): annotate_unverified_paths(), ±radius lines around a graph `L<n>` location. Tolerates stale files/locations., Annotate every cited path that does not exist in the repo, inline and visibly —, read_excerpt(), _blob(), build_delta(), _cmd_whatsnew(), commit_hints() (+73 more)

### Community 13 - "build_certificate"
Cohesion: 0.14
Nodes (22): parse_predicate_field(), Parse a claim's optional third field into a pcp.Predicate (or None). PCP typed-c, prose_hash(), The tamper-evidence anchor: sha256 of the page prose (full hex, this is a machin, build_certificate(), _cmd_verify(), _ctx_for(), Path (+14 more)

### Community 14 - "pyramid.py"
Cohesion: 0.11
Nodes (25): parse_wiki_uri(), wiki://<page>#<claim-id> -> (page, claim_id), or None if it is not a wiki URI., _claim_verdict(), _norm(), plan_pyramid(), Lane D — the pyramid: hierarchical synthesis with wiki:// claim chains. (T-af65, 0-LLM subsystem suggester: group files by top directory (the isidore graph uses, Plan deterministic N2 subsystem + N3 product pages. 0 LLM.      Explicit `pyrami (+17 more)

### Community 15 - "claims.py"
Cohesion: 0.20
Nodes (19): evidence_hash(), evidence_state(), _hash(), _normalize(), Claims: the atomic, evidence-anchored form of wiki knowledge.  A claim is a sing, Collapse all whitespace runs to single spaces and trim — so re-indentation, trai, Fingerprint of the CITED LINE's normalized content (whole normalized file if no, ok" | "stale" | "orphan" | "superseded" — content-anchored, tolerant of line shi (+11 more)

### Community 16 - "surface.py"
Cohesion: 0.05
Nodes (71): Match, Pattern, _brace(), _doc(), extract(), _js(), _kw_func(), _kw_type() (+63 more)

### Community 17 - "Isidore v2 — Incremental compilation, impact detection & residue mining"
Cohesion: 0.12
Nodes (16): 0 · Why (user directive), 1 · Verified bug diagnoses (2026-07-10, against real code — not reports), 2 · Design principles (unchanged bets, now enforced deeper), 3 · C0 — Scoped compile: `isidore compile --only <sel>[,<sel>…]`, 4 · C1+C2 — Change-driven compile: `isidore compile --changed [--since <ref>]`, 5 · C3 — Impact detection: `isidore impact [--since <ref>] [--md] [--check]` (new, **0 LLM always**), 6 · C4+C5+C6 — Correctness fixes (the right ones), 7 · C7 — Residue mining (all 0-LLM; the "squeeze everything" layer) (+8 more)

### Community 18 - "git_repo.py"
Cohesion: 0.23
Nodes (14): all_connectors(), Connector, get(), IngestResult, _load_plugins(), missing_env(), Protocol, Connector protocol + registry (ADR-0032 F1).  A connector ingests raw items from (+6 more)

### Community 19 - "VerifyContext"
Cohesion: 0.20
Nodes (13): _cmd_contracts(), Lane B (part 2) — claim->contract graduation + `isidore contracts`. (T-8dfc)  A, Check every promoted contract against the current graph. Pure, 0-LLM., Add `isidore contracts` (promote / list / check)., Command implementation for `isidore contracts`., register_cli(), verify_contracts(), Contract (+5 more)

### Community 20 - "IngestOptions"
Cohesion: 0.13
Nodes (18): IngestOptions, Caps and scoping for a run. All limits live here (in code), never in a prompt., GitRepoConnector, Run a git command; return stdout or None on any failure (never raises)., (item, None) for a changed repo, (None, None) if HEAD is unchanged, (None, warni, iso_now(), _git(), _head() (+10 more)

### Community 21 - "pipeline.py"
Cohesion: 0.11
Nodes (23): coverage_gap_candidates(), Module pages with no inbound link from any test-looking module., isidore — compile an agent-oriented wiki from your codebase's structure graph., CompileResult, context_hash(), _match_only(), PageSpec, prompt_for() (+15 more)

### Community 22 - "mcp.py"
Cohesion: 0.16
Nodes (12): _allowed(), _JsonRpcClient, McpConnector, Any, Minimal read-only MCP connector (ADR-0032 F3).  The implementation deliberately, Map tool name -> its MCP annotations via tools/list (paginated). Empty if the se, Current state, or a fresh default if missing OR corrupt (I13-style recovery, nev, Prepend a run summary, keeping the last 20 (newest first). (+4 more)

### Community 23 - "test_pcp_pipeline.py"
Cohesion: 0.29
Nodes (10): _compile(), _fake_generator(), _fake_generator_with_a_lie(), Path, P-INT gate — the pipeline wiring ties all five PCP lanes together end to end: a, test_compile_writes_a_certificate_with_typed_verdicts(), test_deterministic_mark_forces_the_banner_despite_calm_prose(), test_refuted_claim_is_quarantined_not_published() (+2 more)

### Community 24 - "knowledge.py"
Cohesion: 0.14
Nodes (23): is_negative_existential(), True for statements asserting existential/definitional ABSENCE (unanchorable). C, Pages owning at least one stale/orphan claim — they must regenerate even if thei, stale_pages(), parse_findings_block(), Split a generated page into (clean page, findings rows). Tolerant of malformed l, mkdir -p with restrictive mode, best-effort — never raises on a perms/FS quirk., safe_mkdir() (+15 more)

### Community 25 - "plan_pages"
Cohesion: 0.16
Nodes (16): Counter, _match_seed(), module_dep_edges(), plan_flows(), plan_pages(), Cross-module dependency edges (src_module, dst_module) -> link count. Shared by, Module pages from the graph: top-K modules holding at least min_symbols code sym, Cross-cutting flow pages: BFS over the graph from user-declared seeds.      Conf (+8 more)

### Community 26 - "pcp.py"
Cohesion: 0.13
Nodes (20): get_verifier(), parse_predicate(), Predicate, Protocol, Proof-Carrying Prose (PCP) — the frozen seam shared by every PCP lane.  This mod, A predicate verifier. MUST be deterministic and 0-LLM. Returns UNDECIDABLE, neve, Dispatch one predicate to its registered verifier. No verifier -> UNDECIDABLE (f, A decidable assertion parsed from a claim's third field. Frozen: predicates are (+12 more)

### Community 27 - "_tool_read_only"
Cohesion: 0.16
Nodes (12): _name_looks_mutating(), Fallback heuristic ONLY (not exhaustive): does the tool name contain a mutating, (allowed, reason). Authority order: explicit readOnlyHint/destructiveHint > name, _tool_read_only(), _FakeClient, MCP connector read-only barrier (ADR-0032 F3). Regression for the review of T-db, Stands in for _JsonRpcClient: a server exposing one read tool, one write tool (a, test_destructive_hint_rejects() (+4 more)

### Community 28 - "PCP_SEAMS — the frozen interface for Proof-Carrying Prose (ADR-0033, phase P0)"
Cohesion: 0.15
Nodes (12): Certificate (`<page>.md` → `<page>.md.cert.json`, alongside the page), CLI, Contracts (`contracts.json` in the wiki dir), File ownership matrix (nobody edits another lane's files), How each lane starts (all depend ONLY on P0 = T-1dc9), Marks (lane C output; also the golden `marks.json`), PCP_SEAMS — the frozen interface for Proof-Carrying Prose (ADR-0033, phase P0), Pipeline hooks (lane A wires; signatures frozen) (+4 more)

### Community 29 - "encode"
Cohesion: 0.15
Nodes (18): append_run(), Compile journal + per-page changelog — residue mining, all zero-LLM.  Every comp, Map each `## heading` to its body text (content before the first heading is keye, (H2 headings whose content changed / were added / removed, new_line_count - old_, Append an H2-level changelog entry to a page's state (capped). No-op if the pros, record_page_change(), section_diff(), _sections() (+10 more)

### Community 30 - "Mark"
Cohesion: 0.19
Nodes (12): Files reachable from an auth/secret/crypto root via imports (BFS, file-level). 0, _topology_marks(), format_mark(), generate_security_banner(), Mark, A deterministic security-relevant flag raised BEFORE the LLM call (lane C)., Lane B (part 1) — the reconciler: the model's own outputs cross-checked, 0 LLM., Helper to split file:line into (file, line). (+4 more)

### Community 31 - "write_items"
Cohesion: 0.25
Nodes (9): create_run_id(), Sortable, collision-resistant run id (UTC second + millis)., Append items as JSONL to `raw/<run_id>/items.jsonl`; stamp each with its `chash`, write_items(), Algorithmically suggest topics from ingested raw items (0-LLM, term frequency ba, suggest_topics(), test_compile_topics(), test_filter_findings_with_src() (+1 more)

### Community 32 - "isidore"
Cohesion: 0.17
Nodes (11): Bring your own graph, Config (`isidore.json`, optional), Design rules, isidore, Languages, License, Proof-carrying prose — how to read a certified page, Quickstart (+3 more)

### Community 33 - "auth.py"
Cohesion: 0.29
Nodes (6): authenticate(), Auth service fixture for PCP lane tests. Line numbers are load-bearing: the gold, Verify the caller's JWT and enforce the attempt ceiling., Token service fixture for PCP lane tests. verify_jwt is defined on L5 (cited by, Return the decoded claims if the token's signature checks out, else None., verify_jwt()

### Community 35 - "scan"
Cohesion: 0.38
Nodes (9): Run all three detector families over the repo -> deterministic marks. Pure, 0-LL, scan(), _ctx(), Lane C gate — deterministic detectors flag by facts, are specific, and don't cra, test_determinism(), test_entropy_flags_the_backdoor_token(), test_specificity_no_false_positive_on_ordinary_strings(), test_topology_reaches_tokens_from_auth() (+1 more)

### Community 36 - "assemble_context"
Cohesion: 0.22
Nodes (10): assemble_context(), git_log_for(), lint_cited_paths(), Path, Gather one page's facts. Returns (context, truncation-warnings)., File-looking paths cited in the prose that do NOT exist in the repo., save_state(), test_assemble_context_includes_docs_excerpts_deps_and_budget_warning() (+2 more)

### Community 37 - "GenerationError"
Cohesion: 0.28
Nodes (8): Request, build_request(), generate(), GenerationError, RuntimeError, Single-provider LLM client (OpenAI-compatible), fail-closed by design.  One mode, The provider failed. No retry with a different model — fail closed., test_build_request_openai_compat_temperature_zero_and_bearer()

### Community 38 - "ClaimVerdict"
Cohesion: 0.28
Nodes (9): ClaimVerdict, One claim's line in a certificate: the anchored claim + its typed verdict (if an, _claim_symbols(), classify_mass(), The code identifiers a claim is about: its predicate args (last dotted component, Per-sentence confidence, 0-LLM: green if a sentence mentions a symbol from a cla, _sentence_split(), test_contracts_cli_promote_and_list() (+1 more)

### Community 39 - "test_wiki_dir_env.py"
Cohesion: 0.31
Nodes (7): ISIDORE_WIKI_DIR redirects the compiled-wiki output directory.  WIKI_DIRNAME is, A nested WIKI_DIRNAME (e.g. doc/isidore) must create its parents, not crash., _reload_render(), test_save_state_creates_nested_wiki_dir(), test_wiki_dirname_blank_env_falls_back(), test_wiki_dirname_defaults_to_wiki(), test_wiki_dirname_honors_env()

### Community 40 - "test_reconcile.py"
Cohesion: 0.25
Nodes (3): Ensure reconcile.py does not import pipeline, claims, or verify (frozen boundary, test_pure_reconcile_imports_constraint(), test_reconcile_mark_uncovered()

### Community 41 - "test_humanpack.py"
Cohesion: 0.29
Nodes (6): Lane E gate — the human pack renders from golden artifacts, is deterministic, an, I12: the renderer must be 0-LLM. Guard it at the source level., test_humanpack_does_not_import_llm(), test_pdf_flag_writes_print_html(), test_render_pack_content(), test_render_pack_is_deterministic()

### Community 42 - "src-isidore.md"
Cohesion: 0.33
Nodes (5): Architecture, Dependencies, How to change safely, Key entry points, Purpose

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

## Knowledge Gaps
- **81 isolated node(s):** `isidore-wiki`, `Wiki (isidore)`, `Why`, `Quickstart`, `What you get` (+76 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **5 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `VerifyContext` connect `VerifyContext` to `compile_wiki`, `scan`, `detectors.py`, `verify.py`, `read_certificate`, `whatsnew.py`, `build_certificate`, `pyramid.py`, `pipeline.py`, `pcp.py`, `Mark`?**
  _High betweenness centrality (0.115) - this node is a cross-community bridge._
- **Why does `compile_wiki()` connect `compile_wiki` to `cli.py`, `graph.py`, `scan`, `read_certificate`, `GenerationError`, `assemble_context`, `findings.py`, `module_of`, `test_claims.py`, `whatsnew.py`, `build_certificate`, `VerifyContext`, `pipeline.py`, `test_pcp_pipeline.py`, `knowledge.py`, `plan_pages`, `encode`, `Mark`?**
  _High betweenness centrality (0.103) - this node is a cross-community bridge._
- **Why does `IngestOptions` connect `IngestOptions` to `cli.py`, `git_repo.py`, `_tool_read_only`, `mcp.py`?**
  _High betweenness centrality (0.088) - this node is a cross-community bridge._
- **Are the 30 inferred relationships involving `compile_wiki()` (e.g. with `test_compile_stores_claims_and_writes_claims_toon()` and `test_dry_run_still_detects_stale_claims_for_free()`) actually correct?**
  _`compile_wiki()` has 30 INFERRED edges - model-reasoned connections that need verification._
- **Are the 12 inferred relationships involving `VerifyContext` (e.g. with `CompileResult` and `PageSpec`) actually correct?**
  _`VerifyContext` has 12 INFERRED edges - model-reasoned connections that need verification._
- **Are the 10 inferred relationships involving `run_whatsnew()` (e.g. with `test_a_false_predicate_is_kept_in_the_certificate_but_never_published()` and `test_a_phantom_path_earns_one_repair_attempt_then_a_visible_quarantine()`) actually correct?**
  _`run_whatsnew()` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Are the 8 inferred relationships involving `load_graph()` (e.g. with `_ctx_for()` and `_ctx()`) actually correct?**
  _`load_graph()` has 8 INFERRED edges - model-reasoned connections that need verification._