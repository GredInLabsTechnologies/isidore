# Graph Report - .  (2026-07-13)

## Corpus Check
- 82 files · ~55,496 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 810 nodes · 2064 edges · 35 communities (34 shown, 1 thin omitted)
- Extraction: 84% EXTRACTED · 16% INFERRED · 0% AMBIGUOUS · INFERRED: 326 edges (avg confidence: 0.77)
- Token cost: 23,561 input · 1,918 output

## Community Hubs (Navigation)
- Community 0
- Community 1
- Community 2
- Community 3
- Community 4
- Community 5
- Community 6
- Community 7
- Community 8
- Community 9
- Community 10
- Community 11
- Community 12
- Community 13
- Community 14
- Community 15
- Community 16
- Community 17
- Community 18
- Community 19
- Community 20
- Community 21
- Community 22
- Community 23
- Community 24
- Community 25
- Community 26
- Community 27
- Community 28
- Community 29
- Community 30
- Community 31
- Community 32
- Community 33
- Community 34

## God Nodes (most connected - your core abstractions)
1. `compile_wiki()` - 80 edges
2. `VerifyContext` - 44 edges
3. `_make_repo()` - 31 edges
4. `load_graph()` - 25 edges
5. `Predicate` - 22 edges
6. `IngestOptions` - 21 edges
7. `check_claims()` - 20 edges
8. `compile_topics()` - 20 edges
9. `build_impact()` - 19 edges
10. `Verdict` - 19 edges

## Surprising Connections (you probably didn't know these)
- `test_pcp_subcommands_are_registered()` --calls--> `main()`  [INFERRED]
  tests/test_pcp_seams.py → src/isidore/cli.py
- `test_filter_findings_drops_hallucinated_paths()` --calls--> `filter_findings()`  [INFERRED]
  tests/test_units.py → src/isidore/findings.py
- `test_golden_graph_loads()` --calls--> `load_graph()`  [INFERRED]
  tests/test_pcp_seams.py → src/isidore/graph.py
- `test_home_env_override()` --calls--> `home()`  [INFERRED]
  tests/test_connectors_f1.py → src/isidore/home.py
- `test_predicate_rejects_absent_or_unknown()` --calls--> `parse_predicate()`  [INFERRED]
  tests/test_pcp_seams.py → src/isidore/pcp.py

## Import Cycles
- 1-file cycle: `src/isidore/connectors/__init__.py -> src/isidore/connectors/__init__.py`

## Hyperedges (group relationships)
- **Proof-Carrying Prose Lanes** — src_isidore_verify, src_isidore_reconcile, src_isidore_detectors, src_isidore_pyramid, src_isidore_humanpack [EXTRACTED 1.00]
- **Isidore Compilation Flow** — src_isidore_pipeline, src_isidore_graph, src_isidore_claims, src_isidore_findings [EXTRACTED 1.00]

## Communities (35 total, 1 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.06
Nodes (69): Request, claims_grep(), Free-text search over verified atomic facts — answers many questions with 0 LLM, _cmd_ask(), _cmd_claims(), _cmd_compile(), _cmd_export_agora(), _cmd_impact() (+61 more)

### Community 1 - "Community 1"
Cohesion: 0.06
Nodes (61): Pattern, git_head(), git_listed_files(), _is_binary(), _iter_source_files(), _node_id(), _norm_source_file(), Path (+53 more)

### Community 2 - "Community 2"
Cohesion: 0.08
Nodes (61): Counter, assemble_context(), compile_wiki(), context_hash(), git_log_for(), lint_cited_paths(), module_dep_edges(), PageSpec (+53 more)

### Community 3 - "Community 3"
Cohesion: 0.07
Nodes (39): PCP Seams Contract, Certificate, certificate_from_dict(), certificate_to_dict(), Contract, get_verifier(), parse_wiki_uri(), Path (+31 more)

### Community 4 - "Community 4"
Cohesion: 0.07
Nodes (34): _looks_like_secret(), Path, Lane C — deterministic security detectors: entropy, sinks, topology. 0 LLM. (T-e, Files reachable from an auth/secret/crypto root via imports (BFS, file-level). 0, Run all three detector families over the repo -> deterministic marks. Pure, 0-LL, Shannon entropy per character (bits). Stdlib only., Return a reason if the literal is credential-shaped, else None., Repo-relative source files to scan: the graph's, or a bounded walk if the graph (+26 more)

### Community 5 - "Community 5"
Cohesion: 0.13
Nodes (35): AST, AsyncFunctionDef, FunctionDef, Module, Everything a verifier needs, assembled once per page/verify run. Read-only to ve, VerifyContext, _ast_of(), _file_nodes() (+27 more)

### Community 6 - "Community 6"
Cohesion: 0.12
Nodes (28): _cmd_render(), _esc(), format_mark(), generate_architecture_map(), generate_claims_table(), generate_contracts_section(), generate_glossary(), generate_mass_bar() (+20 more)

### Community 7 - "Community 7"
Cohesion: 0.14
Nodes (27): isidore — compile an agent-oriented wiki from your codebase's structure graph., load_knowledge_state(), CompileResult, answer_knowledge_offline(), answer_offline(), ask(), ask_knowledge(), gather_claims() (+19 more)

### Community 8 - "Community 8"
Cohesion: 0.09
Nodes (27): insert_security_banner(), is_security_finding(), True if a suspect reads as a security risk (hardcoded secret, auth bypass, injec, A prominent, deterministic banner listing this page's security suspects — meant, Place the banner right under the page's H1 (or at the very top if there is none), security_banner(), security_suspects(), Verify that negation patterns do not trigger false positive security findings (6 (+19 more)

### Community 9 - "Community 9"
Cohesion: 0.12
Nodes (25): affected_modules(), changed_lines(), changed_symbols(), _git_diff(), _module_fan_in(), modules_of(), Path, Change-set detection: which graph symbols a git diff touched, and which modules (+17 more)

### Community 10 - "Community 10"
Cohesion: 0.13
Nodes (26): anchor_claims(), claim_id(), parse_claims_block(), Split a generated page into (clean page, raw claim rows). Tolerant of malformed, Deterministic, ledger-friendly id: stable across runs for the same (statement, e, Repair a shortened citation to a real file, or None if it can't be resolved uniq, Quarantine filter + anchoring. Returns (anchored claims, dropped, repaired)., resolve_citation() (+18 more)

### Community 11 - "Community 11"
Cohesion: 0.17
Nodes (22): _hash(), _normalize(), Collapse all whitespace runs to single spaces and trim — so re-indentation, trai, chash(), prune_runs(), The raw store: immutable ingested items + per-connector cursor state (ADR-0032 F, Drop all but the newest `keep` runs, deleting their raw dirs and trimming state., Atomic write (tmp + os.replace) so a crash mid-write never corrupts the live sta (+14 more)

### Community 12 - "Community 12"
Cohesion: 0.14
Nodes (21): _cmd_findings(), _churn(), coverage_gap_candidates(), filter_findings(), finding_id(), findings_new(), is_finding_resolved(), orphan_file_candidates() (+13 more)

### Community 13 - "Community 13"
Cohesion: 0.15
Nodes (20): parse_predicate_field(), Parse a claim's optional third field into a pcp.Predicate (or None). PCP typed-c, ClaimVerdict, One claim's line in a certificate: the anchored claim + its typed verdict (if an, build_certificate(), _claim_symbols(), classify_mass(), The code identifiers a claim is about: its predicate args (last dotted component (+12 more)

### Community 14 - "Community 14"
Cohesion: 0.15
Nodes (18): _cmd_pyramid(), _norm(), plan_pyramid(), Lane D — the pyramid: hierarchical synthesis with wiki:// claim chains. (T-af65, 0-LLM subsystem suggester: group files by top directory (the isidore graph uses, Plan deterministic N2 subsystem + N3 product pages. 0 LLM.      Explicit `pyrami, Add `isidore pyramid` (plan/preview the hierarchical pages)., Print a deterministic JSON plan for humans and scripts. (+10 more)

### Community 15 - "Community 15"
Cohesion: 0.22
Nodes (18): check_claims(), claims_for_file(), evidence_hash(), evidence_state(), Path, Claims: the atomic, evidence-anchored form of wiki knowledge.  A claim is a sing, Fingerprint of the CITED LINE's normalized content (whole normalized file if no, ok" | "stale" | "orphan" | "superseded" — content-anchored, tolerant of line shi (+10 more)

### Community 16 - "Community 16"
Cohesion: 0.14
Nodes (18): harvest_todos(), TODO/FIXME/HACK/XXX with file:line — regex over the files the graph already know, _git_repo(), _qa_repo(), Unit tests: toon encoder, graph scanner, findings residue, QA retrieval, LLM req, A third-party graph (e.g. Graphify) that indexed a gitignored path gets cleaned, Init a minimal git repo at `path`; skip the test if git is unavailable., The reported GIMO bug: a gitignored build-artifact copy must NOT be indexed as s (+10 more)

### Community 17 - "Community 17"
Cohesion: 0.18
Nodes (11): GitRepoConnector, git-repo connector (ADR-0032 F1): local repositories as a knowledge source. No n, Run a git command; return stdout or None on any failure (never raises)., (item, None) for a changed repo, (None, None) if HEAD is unchanged, (None, warni, iso_now(), Current state, or a fresh default if missing OR corrupt (I13-style recovery, nev, Prepend a run summary, keeping the last 20 (newest first)., read_state() (+3 more)

### Community 18 - "Community 18"
Cohesion: 0.24
Nodes (14): _cmd_sync(), all_connectors(), Connector, get(), IngestResult, _load_plugins(), missing_env(), Protocol (+6 more)

### Community 19 - "Community 19"
Cohesion: 0.16
Nodes (16): _cmd_contracts(), Lane B (part 2) — claim->contract graduation + `isidore contracts`. (T-8dfc)  A, Check every promoted contract against the current graph. Pure, 0-LLM., Add `isidore contracts` (promote / list / check)., Command implementation for `isidore contracts`., register_cli(), verify_contracts(), The result of checking one predicate against an oracle. `value` is TRUE|FALSE|UN (+8 more)

### Community 20 - "Community 20"
Cohesion: 0.17
Nodes (11): _git(), _head(), _make_repo(), F1 (ADR-0032): knowledge home + raw store + git-repo connector.  The load-bearin, Regression: a real repo's commit messages carry UTF-8 (accents, emoji). On Windo, test_git_repo_handles_non_ascii_commit_messages(), test_git_repo_ingest_persists_and_is_idempotent(), test_git_repo_no_repos_skips() (+3 more)

### Community 21 - "Community 21"
Cohesion: 0.12
Nodes (15): Incremental Compilation Design, parse_findings_block(), Split a generated page into (clean page, findings rows). Tolerant of malformed l, render_findings(), annotate_unverified_paths(), _match_only(), _match_seed(), The compiler pipeline: plan -> assemble -> generate -> cache -> lint.  Everythin (+7 more)

### Community 22 - "Community 22"
Cohesion: 0.21
Nodes (9): RuntimeError, _allowed(), _JsonRpcClient, Any, Minimal read-only MCP connector (ADR-0032 F3).  The implementation deliberately, Map tool name -> its MCP annotations via tools/list (paginated). Empty if the se, create_run_id(), Sortable, collision-resistant run id (UTC second + millis). (+1 more)

### Community 23 - "Community 23"
Cohesion: 0.21
Nodes (13): Load a certificate from disk. Raises ValueError on malformed JSON (fail-closed f, read_certificate(), _compile(), _fake_generator(), _fake_generator_with_a_lie(), Path, P-INT gate — the pipeline wiring ties all five PCP lanes together end to end: a, test_compile_writes_a_certificate_with_typed_verdicts() (+5 more)

### Community 24 - "Community 24"
Cohesion: 0.23
Nodes (13): is_negative_existential(), True for statements asserting existential/definitional ABSENCE (unanchorable). C, assemble_topic_context(), compile_topics(), knowledge_dir(), load_topics(), Path, The knowledge core: user-defined topics compile + 0-LLM suggest topics (ADR-0032 (+5 more)

### Community 25 - "Community 25"
Cohesion: 0.23
Nodes (12): Deterministic outputs: quickstart.md, index.toon, and the AGENTS.md reference bl, render_quickstart(), render_toon_index(), encode(), encode_table(), _field(), Any, TOON (Token-Oriented Object Notation) serializer — tabular subset.  One declarat (+4 more)

### Community 26 - "Community 26"
Cohesion: 0.21
Nodes (12): parse_predicate(), Predicate, Dispatch one predicate to its registered verifier. No verifier -> UNDECIDABLE (f, A decidable assertion parsed from a claim's third field. Frozen: predicates are, Parse "<kind>:<a>;<b>" -> Predicate, or None if absent/malformed/unknown-kind., verify_predicate(), Dispatch through the registry (kept local so callers don't import pcp directly)., verify_predicate_ctx() (+4 more)

### Community 27 - "Community 27"
Cohesion: 0.29
Nodes (10): _name_looks_mutating(), Fallback heuristic ONLY (not exhaustive): does the tool name contain a mutating, (allowed, reason). Authority order: explicit readOnlyHint/destructiveHint > name, _tool_read_only(), MCP connector read-only barrier (ADR-0032 F3). Regression for the review of T-db, test_destructive_hint_rejects(), test_mutating_names_are_rejected_without_annotation(), test_read_names_pass_without_annotation() (+2 more)

### Community 28 - "Community 28"
Cohesion: 0.24
Nodes (6): IngestOptions, Caps and scoping for a run. All limits live here (in code), never in a prompt., McpConnector, _FakeClient, Stands in for _JsonRpcClient: a server exposing one read tool, one write tool (a, test_ingest_invokes_only_read_only_tools()

### Community 29 - "Community 29"
Cohesion: 0.24
Nodes (9): append_run(), Compile journal + per-page changelog — residue mining, all zero-LLM.  Every comp, Map each `## heading` to its body text (content before the first heading is keye, (H2 headings whose content changed / were added / removed, new_line_count - old_, Append an H2-level changelog entry to a page's state (capped). No-op if the pros, record_page_change(), section_diff(), _sections() (+1 more)

### Community 30 - "Community 30"
Cohesion: 0.29
Nodes (10): prose_hash(), The tamper-evidence anchor: sha256 of the page prose (full hex, this is a machin, _cmd_verify(), _ctx_for(), Path, Re-verify a page against its sidecar certificate, offline, 0 LLM (invariant I11), Add `isidore verify` (called once from cli.main via the registrar loop — P0 owns, register_cli() (+2 more)

### Community 31 - "Community 31"
Cohesion: 0.28
Nodes (7): Append items as JSONL to `raw/<run_id>/items.jsonl`; stamp each with its `chash`, write_items(), Algorithmically suggest topics from ingested raw items (0-LLM, term frequency ba, suggest_topics(), test_compile_topics(), test_filter_findings_with_src(), test_suggest_topics()

### Community 32 - "Community 32"
Cohesion: 0.50
Nodes (4): iter_items(), Run ids from state (already newest-first); fall back to sorting the raw dir if s, Yield stored items, newest run first. A corrupt/half-written JSONL line is skipp, _run_ids_newest_first()

### Community 33 - "Community 33"
Cohesion: 0.50
Nodes (3): authenticate(), Auth service fixture for PCP lane tests. Line numbers are load-bearing: the gold, Verify the caller's JWT and enforce the attempt ceiling.

## Knowledge Gaps
- **6 isolated node(s):** `isidore-wiki`, `Index (TOON)`, `Claims (TOON)`, `Findings (TOON)`, `Incremental Compilation Design` (+1 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **1 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `IngestOptions` connect `Community 28` to `Community 0`, `Community 17`, `Community 18`, `Community 20`, `Community 22`?**
  _High betweenness centrality (0.124) - this node is a cross-community bridge._
- **Why does `compile_wiki()` connect `Community 2` to `Community 0`, `Community 1`, `Community 3`, `Community 4`, `Community 5`, `Community 7`, `Community 8`, `Community 9`, `Community 10`, `Community 12`, `Community 13`, `Community 15`, `Community 16`, `Community 21`, `Community 23`, `Community 25`, `Community 29`?**
  _High betweenness centrality (0.114) - this node is a cross-community bridge._
- **Why does `VerifyContext` connect `Community 5` to `Community 2`, `Community 3`, `Community 4`, `Community 7`, `Community 13`, `Community 14`, `Community 19`, `Community 21`, `Community 26`, `Community 30`?**
  _High betweenness centrality (0.060) - this node is a cross-community bridge._
- **Are the 30 inferred relationships involving `compile_wiki()` (e.g. with `test_compile_stores_claims_and_writes_claims_toon()` and `test_dry_run_still_detects_stale_claims_for_free()`) actually correct?**
  _`compile_wiki()` has 30 INFERRED edges - model-reasoned connections that need verification._
- **Are the 8 inferred relationships involving `VerifyContext` (e.g. with `CompileResult` and `PageSpec`) actually correct?**
  _`VerifyContext` has 8 INFERRED edges - model-reasoned connections that need verification._
- **Are the 8 inferred relationships involving `load_graph()` (e.g. with `_ctx_for()` and `_ctx()`) actually correct?**
  _`load_graph()` has 8 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `Predicate` (e.g. with `test_predicate_parse_and_serialize_round_trip()` and `test_registry_has_every_kind_and_is_fail_closed()`) actually correct?**
  _`Predicate` has 4 INFERRED edges - model-reasoned connections that need verification._