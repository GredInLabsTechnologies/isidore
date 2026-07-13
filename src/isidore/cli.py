"""isidore — compile an agent-oriented wiki from your codebase's structure graph.

Subcommands:
  scan           build a structure graph for a repo in ANY language (zero-dep) -> .isidore/graph.json
  compile        compile/refresh the wiki (dry-run by default; --execute to generate)
  ask            answer one question over the compiled wiki + graph (one LLM call)
  suggest-flows  print the heaviest cross-module bridges as flow candidates for isidore.json
  claims         zero-LLM staleness audit of every claim (--check: exit 1 if any is stale)
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .graph import GraphError, find_graph, load_graph, write_scan
from .llm import GenerationError, default_generator
from .pipeline import (
    DEFAULT_MAX_CALLS,
    DEFAULT_MAX_PROMPT_CHARS,
    DEFAULT_MIN_SYMBOLS,
    DEFAULT_MODULE_DEPTH,
    DEFAULT_TOP_K_PAGES,
    compile_wiki,
    load_config,
    suggest_flows,
)
from .qa import ask


def _setting(args_value, config: dict, key: str, default):
    """Precedence: explicit CLI arg > isidore.json > built-in default."""
    if args_value is not None:
        return args_value
    return config.get(key, default)


def _cmd_scan(args) -> int:
    out_path = write_scan(args.repo)
    nodes, links, _ = load_graph(out_path)
    print(f"[isidore] scanned {args.repo} -> {out_path} ({len(nodes)} nodes, {len(links)} links)")
    return 0


def _cmd_compile(args) -> int:
    config = load_config(args.repo)
    graph_path = find_graph(args.repo, args.graph)
    try:
        result = compile_wiki(
            args.repo,
            graph_path=graph_path,
            execute=args.execute,
            module_depth=_setting(args.module_depth, config, "module_depth", DEFAULT_MODULE_DEPTH),
            top_k=_setting(args.top_k, config, "top_k", DEFAULT_TOP_K_PAGES),
            min_symbols=_setting(args.min_symbols, config, "min_symbols", DEFAULT_MIN_SYMBOLS),
            max_calls=_setting(args.max_calls, config, "max_calls", DEFAULT_MAX_CALLS),
            max_prompt_chars=_setting(args.max_prompt_chars, config, "max_prompt_chars",
                                      DEFAULT_MAX_PROMPT_CHARS),
            flows_config=config.get("flows", []),
            only=[s for s in (args.only or "").split(",") if s.strip()] or None,
            changed=args.changed,
            since=args.since,
            affected_depth=args.affected_depth,
        )
    except (FileNotFoundError, GraphError, GenerationError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    print(f"[isidore] plan: {result.planned} pages · dirty: {len(result.dirty)} · "
          f"generated: {len(result.generated)} · retries: {result.retries} · "
          f"quarantined: {len(result.quarantined)} · pruned: {len(result.pruned)} · "
          f"findings kept/dropped/absence: {result.findings_kept}/{result.findings_dropped}/"
          f"{result.findings_dropped_negative} · "
          f"claims new/repaired/dropped/absence: {result.claims_total}/{result.claims_repaired}/"
          f"{result.claims_dropped}/{result.claims_dropped_negative}")
    if result.certificates:
        m = result.verified_mass
        print(f"[isidore] certificates: {len(result.certificates)} · verified mass "
              f"{m['green']} proved / {m['yellow']} anchored / {m['gray']} narrative · "
              f"marks: {result.marks_raised} · reconciler flags: {result.reconcile_violations} · "
              f"refuted (model errors quarantined, not published): {result.claims_refuted}")
    if result.claims_stale_pages:
        print(f"[isidore] stale claims forced regeneration of: "
              f"{', '.join(result.claims_stale_pages)}")
    if result.security_flagged:
        print(f"[isidore] ⚠ SECURITY banner forced on {len(result.security_flagged)} page(s): "
              f"{', '.join(result.security_flagged)}", file=sys.stderr)
    quarantined = set(result.quarantined)
    generated = set(result.generated)
    skipped = set(result.skipped_by_cap)
    for name in result.dirty:
        mark = ("QRT " if name in quarantined else "GEN " if name in generated
                else "CAP " if name in skipped else "dry ")
        print(f"  {mark}{name}")
    for name, missing in result.lint_findings.items():
        print(f"[isidore] QUARANTINE {name}: cited paths not found after retry: "
              f"{', '.join(missing)}", file=sys.stderr)
    for warning in result.warnings:
        print(f"[isidore] warning: {warning}", file=sys.stderr)
    if not args.execute:
        print("[isidore] DRY-RUN — 0 LLM calls. Pass --execute to compile.", file=sys.stderr)
    if args.strict and result.quarantined:
        print(f"[isidore] STRICT: {len(result.quarantined)} page(s) quarantined "
              f"(cited nonexistent paths) — failing.", file=sys.stderr)
        return 3
    return 0


def _cmd_ask(args) -> int:
    if args.offline:
        # 0-LLM path: answer from verified claims. No graph or endpoint required.
        print(ask(args.repo, args.question, graph_path=Path("."), generator=None, offline=True, knowledge=args.knowledge))
        return 0
    graph_path = find_graph(args.repo, args.graph)
    if graph_path is None and not args.knowledge:
        print("ERROR: no structure graph — run `isidore scan` first", file=sys.stderr)
        return 2
    try:
        answer = ask(args.repo, args.question, graph_path=graph_path or Path("."),
                     generator=default_generator(), knowledge=args.knowledge)
    except GenerationError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    print(answer)
    return 0


def _cmd_suggest_flows(args) -> int:
    graph_path = find_graph(args.repo, args.graph)
    if graph_path is None:
        print("ERROR: no structure graph — run `isidore scan` first", file=sys.stderr)
        return 2
    nodes, links, _ = load_graph(graph_path)
    candidates = suggest_flows(nodes, links)
    if not candidates:
        print("[isidore] no cross-module bridges found")
        return 0
    print("[isidore] flow candidates (add the ones that matter to isidore.json -> \"flows\"):")
    print(json.dumps({"flows": candidates}, indent=2))
    return 0


def _cmd_impact(args) -> int:
    from .impact import build_impact, render_impact
    graph_path = find_graph(args.repo, args.graph)
    if graph_path is None:
        print("ERROR: no structure graph — run `isidore scan` first", file=sys.stderr)
        return 2
    config = load_config(args.repo)
    report = build_impact(
        args.repo, graph_path=graph_path, since=args.since, affected_depth=args.affected_depth,
        module_depth=_setting(None, config, "module_depth", DEFAULT_MODULE_DEPTH),
        min_symbols=_setting(None, config, "min_symbols", DEFAULT_MIN_SYMBOLS),
        top_k=_setting(None, config, "top_k", DEFAULT_TOP_K_PAGES))
    print(render_impact(report, md=args.md))
    if args.check and report.has_signal():
        print(f"[isidore] impact --check: {len(report.dirty_pages)} page(s) would regenerate, "
              f"{len(report.claims_at_risk)} claim(s) at risk — failing.", file=sys.stderr)
        return 1
    return 0


def _cmd_claims(args) -> int:
    from .claims import check_claims, claims_for_file, claims_grep
    from .pipeline import WIKI_DIRNAME, load_state

    if getattr(args, "home", False):
        from .knowledge import load_knowledge_state
        pages = load_knowledge_state().get("pages", {})
        repo = Path(".")
    else:
        state = load_state(args.repo / WIKI_DIRNAME)
        pages = state.get("pages", {})
        repo = args.repo

    if getattr(args, "by_file", None):
        rows = claims_for_file(repo, pages, args.by_file)
        print(f"[isidore] {len(rows)} claim(s) anchored to {args.by_file} (0 LLM calls)")
        for r in rows:
            print(f"  {r['state'].upper()} {r['page']}: {r['statement']} [{r['evidence']}]")
        return 0
    if getattr(args, "grep", None):
        rows = claims_grep(repo, pages, args.grep)
        print(f"[isidore] {len(rows)} claim(s) matching {args.grep!r} (0 LLM calls)")
        for r in rows:
            print(f"  {r['state'].upper()} {r['page']}: {r['statement']} [{r['evidence']}]")
        return 0
    rows = check_claims(repo, pages)
    if not rows:
        print("[isidore] no anchored claims yet — run `isidore compile --execute` first")
        return 0
    bad = [r for r in rows if r["state"] != "ok"]
    print(f"[isidore] {len(rows)} claims · {len(bad)} stale/orphan/superseded (0 LLM calls)")
    for r in bad:
        print(f"  {r['state'].upper()} {r['page']} {r['id']}: {r['statement']} [{r['evidence']}]")
    return 1 if (bad and args.check) else 0


def _cmd_export_agora(args) -> int:
    from .export import build_cards, write_cards
    cards = build_cards(args.repo, domain=args.domain, min_claims=args.min_claims,
                        include_stale=args.include_stale)
    if not cards:
        print("[isidore] no cards to export — no compiled OK claims yet "
              "(run `isidore compile --execute` first)")
        return 0
    written = write_cards(cards, args.out)
    print(f"[isidore] wrote {len(written)} draft card(s) to {args.out} (DRAFTS — review, never "
          f"auto-posted). Each carries verify_cmd `isidore claims --check` for `agora lib audit`.")
    for path in written:
        print(f"  {path}")
    return 0


def _cmd_stats(args) -> int:
    from .journal import render_stats
    from .pipeline import WIKI_DIRNAME, load_state
    print(render_stats(load_state(args.repo / WIKI_DIRNAME)))
    return 0


def _cmd_findings(args) -> int:
    if getattr(args, "action", None) == "resolve":
        if not getattr(args, "finding_id", None):
            print("ERROR: resolve action requires a finding ID", file=sys.stderr)
            return 2
        from .findings import resolve_finding
        return resolve_finding(args.repo, args.finding_id, args.actor or "human", args.reason or "")

    from .findings import findings_new
    from .pipeline import WIKI_DIRNAME, load_state

    state = load_state(args.repo / WIKI_DIRNAME)
    ref = args.since or state.get("commit")
    if not ref:
        print("ERROR: no baseline commit — run `isidore compile --execute` first, or pass --since",
              file=sys.stderr)
        return 2
    llm, todos = findings_new(args.repo, state.get("pages", {}), ref)
    print(f"[isidore] findings in files changed since {ref[:12]}: "
          f"{len(llm)} model finding(s), {len(todos)} TODO/FIXME (0 LLM calls)")
    for f in llm:
        print(f"  {f.get('kind', '?')} {f.get('where', '')}: {f.get('note', '')}")
    for t in todos:
        print(f"  {t['marker']} {t['file']}:{t['line']}: {t['note']}")
    return 0


def _cmd_sync(args) -> int:
    from .knowledge import compile_topics
    from .connectors.base import all_connectors, missing_env, IngestOptions

    # 1. Ingest enabled connectors
    print("[isidore] running ingestion connectors...")
    for conn in all_connectors():
        if missing_env(conn):
            print(f"[isidore] connector '{conn.id}' skipped: missing required env vars: {conn.required_env}", file=sys.stderr)
            continue
        try:
            options = IngestOptions(limit=args.limit)
            res = conn.ingest(options)
            print(f"  {conn.id}: {res.status} ({res.counts.get('items', 0)} item(s) ingested)")
        except Exception as exc:
            print(f"[isidore] connector '{conn.id}' failed: {exc}", file=sys.stderr)

    # 2. Recompile stale topics
    print("[isidore] compiling knowledge topics...")
    try:
        res = compile_topics(execute=args.execute, max_calls=args.max_calls)
    except Exception as exc:
        print(f"ERROR compiling topics: {exc}", file=sys.stderr)
        return 2

    print(f"[isidore] plan: {res.planned} topics · dirty: {len(res.dirty)} · "
          f"generated: {len(res.generated)} · skipped: {len(res.skipped_by_cap)}")
    for name in res.dirty:
        mark = "GEN " if name in res.generated else "CAP " if name in res.skipped_by_cap else "dry "
        print(f"  {mark}{name}")

    if not args.execute:
        print("[isidore] DRY-RUN — 0 LLM calls. Pass --execute to sync.", file=sys.stderr)

    # 3. Claims check
    from .claims import check_claims
    from .knowledge import load_knowledge_state
    pages = load_knowledge_state().get("pages", {})
    rows = check_claims(Path("."), pages)
    bad = [r for r in rows if r["state"] != "ok"]
    print(f"[isidore] {len(rows)} claims · {len(bad)} stale/orphan/superseded (0 LLM calls)")
    for r in bad:
        print(f"  {r['state'].upper()} {r['page']} {r['id']}: {r['statement']} [{r['evidence']}]")

    return 0



def main(argv: list[str] | None = None) -> int:
    # Windows consoles default to cp1252; model output routinely carries characters outside it
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")

    parser = argparse.ArgumentParser(prog="isidore", description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)

    p_scan = sub.add_parser("scan", help="build a structure graph for any language (zero-dep)")
    p_scan.add_argument("--repo", type=Path, default=Path("."))
    p_scan.set_defaults(func=_cmd_scan)

    p_compile = sub.add_parser("compile", help="compile/refresh the wiki (dry-run by default)")
    p_compile.add_argument("--repo", type=Path, default=Path("."))
    p_compile.add_argument("--graph", type=Path, default=None)
    p_compile.add_argument("--execute", action="store_true")
    p_compile.add_argument("--top-k", type=int, default=None)
    p_compile.add_argument("--min-symbols", type=int, default=None)
    p_compile.add_argument("--module-depth", type=int, default=None)
    p_compile.add_argument("--max-calls", type=int, default=None,
                           help="max LLM calls this run (0 = unlimited); default 12. Retries count.")
    p_compile.add_argument("--max-prompt-chars", type=int, default=None)
    p_compile.add_argument("--strict", action="store_true",
                           help="exit nonzero if any page is quarantined (cited nonexistent paths)")
    p_compile.add_argument("--only", default=None,
                           help="scope to pages matching these selectors (comma-separated module "
                                "path prefixes or page filenames); prune is disabled under scope")
    p_compile.add_argument("--changed", action="store_true",
                           help="scope to the blast radius of git changes since --since (default: "
                                "the last compiled commit): changed modules + their dependents")
    p_compile.add_argument("--since", default=None,
                           help="git ref baseline for --changed (default: the last compiled commit)")
    p_compile.add_argument("--affected-depth", type=int, default=1,
                           help="--changed: how many fan-in hops of dependents to include (default 1)")
    p_compile.set_defaults(func=_cmd_compile)

    p_ask = sub.add_parser("ask", help="answer one question (one LLM call)")
    p_ask.add_argument("question")
    p_ask.add_argument("--repo", type=Path, default=Path("."))
    p_ask.add_argument("--graph", type=Path, default=None)
    p_ask.add_argument("--offline", action="store_true",
                        help="answer from verified claims only, 0 LLM calls (or refuse honestly)")
    p_ask.add_argument("--knowledge", action="store_true",
                        help="QA over the knowledge base instead of the repository wiki")
    p_ask.set_defaults(func=_cmd_ask)

    p_flows = sub.add_parser("suggest-flows", help="print flow candidates for isidore.json")
    p_flows.add_argument("--repo", type=Path, default=Path("."))
    p_flows.add_argument("--graph", type=Path, default=None)
    p_flows.set_defaults(func=_cmd_suggest_flows)

    p_impact = sub.add_parser("impact", help="zero-LLM emergent-interaction report for a change-set")
    p_impact.add_argument("--repo", type=Path, default=Path("."))
    p_impact.add_argument("--graph", type=Path, default=None)
    p_impact.add_argument("--since", default=None,
                          help="git ref baseline (default: the last compiled commit)")
    p_impact.add_argument("--affected-depth", type=int, default=1,
                          help="how many fan-in hops of dependents to include (default 1)")
    p_impact.add_argument("--md", action="store_true", help="Markdown output instead of TOON")
    p_impact.add_argument("--check", action="store_true",
                          help="exit 1 if any page would regenerate or any claim is at risk")
    p_impact.set_defaults(func=_cmd_impact)

    p_export = sub.add_parser("export-agora",
                              help="zero-LLM: render verified claims as Living-Library card DRAFTS")
    p_export.add_argument("--repo", type=Path, default=Path("."))
    p_export.add_argument("--out", type=Path, default=Path("agora-cards"),
                          help="output directory for the draft cards (default: ./agora-cards)")
    p_export.add_argument("--domain", default="code", help="card domain field (default: code)")
    p_export.add_argument("--min-claims", type=int, default=1,
                          help="minimum OK claims a page needs to become a card (default 1)")
    p_export.add_argument("--include-stale", action="store_true",
                          help="also export stale/orphan claims (default: verified OK claims only)")
    p_export.set_defaults(func=_cmd_export_agora)

    p_stats = sub.add_parser("stats", help="zero-LLM compile telemetry + most-unstable pages")
    p_stats.add_argument("--repo", type=Path, default=Path("."))
    p_stats.set_defaults(func=_cmd_stats)

    p_findings = sub.add_parser("findings", help="zero-LLM: findings/TODOs in files changed since a ref")
    p_findings.add_argument("--repo", type=Path, default=Path("."))
    p_findings.add_argument("--new", action="store_true", help="only findings in the changed files")
    p_findings.add_argument("--since", default=None, help="git ref baseline (default: last compiled commit)")
    p_findings.add_argument("action", nargs="?", choices=["resolve"], help="action to perform (e.g. resolve)")
    p_findings.add_argument("finding_id", nargs="?", help="ID of the finding to resolve")
    p_findings.add_argument("--actor", help="actor resolving the finding")
    p_findings.add_argument("--reason", help="reason for resolution")
    p_findings.set_defaults(func=_cmd_findings)

    p_claims = sub.add_parser("claims", help="zero-LLM staleness audit of anchored claims")
    p_claims.add_argument("--repo", type=Path, default=Path("."))
    p_claims.add_argument("--by-file", default=None,
                          help="show the claims anchored to this file (its documentation contract)")
    p_claims.add_argument("--grep", default=None, help="search claims by statement/evidence text")
    p_claims.add_argument("--check", action="store_true",
                          help="exit 1 if any claim is stale/orphan (CI gate)")
    p_claims.add_argument("--home", action="store_true",
                          help="audit claims from the knowledge home instead of the repository")
    p_claims.set_defaults(func=_cmd_claims)

    p_sync = sub.add_parser("sync", help="ingest enabled connectors -> compile dirty topics -> claims check")
    p_sync.add_argument("--execute", action="store_true",
                        help="execute compiles (default dry-run)")
    p_sync.add_argument("--limit", type=int, default=None,
                        help="limit number of ingested items per connector")
    p_sync.add_argument("--max-calls", type=int, default=10,
                        help="max LLM calls for compiling topic pages")
    p_sync.set_defaults(func=_cmd_sync)


    # PCP (ADR-0033): each lane module exposes register_cli(sub) and owns its subcommand. This loop
    # is written ONCE (P0) so no lane ever edits cli.py again — verify (A), contracts (B),
    # pyramid (D), render (E). Lane C has no CLI (its marks flow through the pipeline).
    from . import contracts as _contracts, humanpack as _humanpack, pyramid as _pyramid, verify as _verify
    for _mod in (_verify, _contracts, _pyramid, _humanpack):
        _mod.register_cli(sub)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
