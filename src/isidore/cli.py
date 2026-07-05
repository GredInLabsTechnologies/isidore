"""isidore — compile an agent-oriented wiki from your codebase's structure graph.

Subcommands:
  scan           build a structure graph for a Python repo (stdlib ast) -> .isidore/graph.json
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
        )
    except (FileNotFoundError, GraphError, GenerationError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    print(f"[isidore] plan: {result.planned} pages · dirty: {len(result.dirty)} · "
          f"generated: {len(result.generated)} · pruned: {len(result.pruned)} · "
          f"findings kept/dropped: {result.findings_kept}/{result.findings_dropped} · "
          f"claims new/dropped: {result.claims_total}/{result.claims_dropped}")
    if result.claims_stale_pages:
        print(f"[isidore] stale claims forced regeneration of: "
              f"{', '.join(result.claims_stale_pages)}")
    for name in result.dirty:
        mark = "GEN " if name in result.generated else ("CAP " if name in result.skipped_by_cap
                                                        else "dry ")
        print(f"  {mark}{name}")
    for name, missing in result.lint_findings.items():
        print(f"[isidore] LINT {name}: cited paths not found: {', '.join(missing)}",
              file=sys.stderr)
    for warning in result.warnings:
        print(f"[isidore] warning: {warning}", file=sys.stderr)
    if not args.execute:
        print("[isidore] DRY-RUN — 0 LLM calls. Pass --execute to compile.", file=sys.stderr)
    return 0


def _cmd_ask(args) -> int:
    graph_path = find_graph(args.repo, args.graph)
    if graph_path is None:
        print("ERROR: no structure graph — run `isidore scan` first", file=sys.stderr)
        return 2
    try:
        answer = ask(args.repo, args.question, graph_path=graph_path,
                     generator=default_generator())
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


def _cmd_claims(args) -> int:
    from .claims import check_claims
    from .pipeline import WIKI_DIRNAME, load_state

    state = load_state(args.repo / WIKI_DIRNAME)
    rows = check_claims(args.repo, state.get("pages", {}))
    if not rows:
        print("[isidore] no anchored claims yet — run `isidore compile --execute` first")
        return 0
    bad = [r for r in rows if r["state"] != "ok"]
    print(f"[isidore] {len(rows)} claims · {len(bad)} stale/orphan (0 LLM calls)")
    for r in bad:
        print(f"  {r['state'].upper()} {r['page']} {r['id']}: {r['statement']} [{r['evidence']}]")
    return 1 if (bad and args.check) else 0


def main(argv: list[str] | None = None) -> int:
    # Windows consoles default to cp1252; model output routinely carries characters outside it
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")

    parser = argparse.ArgumentParser(prog="isidore", description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)

    p_scan = sub.add_parser("scan", help="build a structure graph (Python repos, stdlib ast)")
    p_scan.add_argument("--repo", type=Path, default=Path("."))
    p_scan.set_defaults(func=_cmd_scan)

    p_compile = sub.add_parser("compile", help="compile/refresh the wiki (dry-run by default)")
    p_compile.add_argument("--repo", type=Path, default=Path("."))
    p_compile.add_argument("--graph", type=Path, default=None)
    p_compile.add_argument("--execute", action="store_true")
    p_compile.add_argument("--top-k", type=int, default=None)
    p_compile.add_argument("--min-symbols", type=int, default=None)
    p_compile.add_argument("--module-depth", type=int, default=None)
    p_compile.add_argument("--max-calls", type=int, default=None)
    p_compile.add_argument("--max-prompt-chars", type=int, default=None)
    p_compile.set_defaults(func=_cmd_compile)

    p_ask = sub.add_parser("ask", help="answer one question (one LLM call)")
    p_ask.add_argument("question")
    p_ask.add_argument("--repo", type=Path, default=Path("."))
    p_ask.add_argument("--graph", type=Path, default=None)
    p_ask.set_defaults(func=_cmd_ask)

    p_flows = sub.add_parser("suggest-flows", help="print flow candidates for isidore.json")
    p_flows.add_argument("--repo", type=Path, default=Path("."))
    p_flows.add_argument("--graph", type=Path, default=None)
    p_flows.set_defaults(func=_cmd_suggest_flows)

    p_claims = sub.add_parser("claims", help="zero-LLM staleness audit of anchored claims")
    p_claims.add_argument("--repo", type=Path, default=Path("."))
    p_claims.add_argument("--check", action="store_true",
                          help="exit 1 if any claim is stale/orphan (CI gate)")
    p_claims.set_defaults(func=_cmd_claims)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
