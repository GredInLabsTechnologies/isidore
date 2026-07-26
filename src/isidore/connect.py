"""`isidore connect` and `isidore ingest` — the CLI face of the connector layer (ADR-0032 F1).

F1 shipped the library (home, protocol, raw store, git-repo) and its tests, but neither command the
contract names. The only way to reach a connector was `isidore sync`, which bundles ingestion with
F2's topic compilation — so you could not ingest without entering an LLM path, and there was no
supported way to write a connector's config at all. That is why F1's gate (two real repos, cursors
advancing, an immediate re-ingest yielding nothing) had never been run.

Both commands are 0 LLM. `connect` never touches the network; `ingest` is the ONLY place a connector
may (invariant I7), and a connector missing a required env var fails closed before it can try (I6).
"""
from __future__ import annotations

import json
from pathlib import Path

from .connectors.base import IngestOptions, all_connectors, get, missing_env
from .connectors.store import iter_items, read_state
from .home import config_path, home, state_path
from .toon import encode_table


def load_config(cid: str, instance: str | None = None) -> dict:
    """A connector's stored config, or {} if absent/corrupt. Never raises."""
    path = config_path(cid, instance)
    if not path.is_file():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return data if isinstance(data, dict) else {}


def save_config(cid: str, instance: str | None, config: dict) -> Path:
    """Write a connector's config with the home's restrictive permissions."""
    from .home import safe_chmod, safe_mkdir
    path = config_path(cid, instance)
    safe_mkdir(path.parent)
    path.write_text(json.dumps(config, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    safe_chmod(path, 0o600)
    return path


def parse_setting(raw: str) -> tuple[str, object]:
    """`key=value` -> (key, value). A value that parses as JSON is stored as JSON, so numbers and
    booleans keep their type; everything else stays a string. Raises ValueError on a missing `=`."""
    if "=" not in raw:
        raise ValueError(f"expected key=value, got {raw!r}")
    key, _sep, value = raw.partition("=")
    key = key.strip()
    if not key:
        raise ValueError(f"empty key in {raw!r}")
    try:
        return key, json.loads(value)
    except ValueError:
        return key, value


def apply_settings(config: dict, settings: list[str]) -> tuple[dict, list[str]]:
    """Fold `key=value` settings into a config. Repeating a key ACCUMULATES into a list — that is how
    a plural setting (repos, feeds, queries) is built without inventing shell-quoting rules.

    Returns (config, refused). A value that looks like a credential is REFUSED, not stored: a
    connector's config holds the NAME of an env var, never its value (invariant I9).
    """
    from .detectors import _looks_like_secret
    refused: list[str] = []
    for raw in settings:
        key, value = parse_setting(raw)
        if isinstance(value, str) and _looks_like_secret(value):
            refused.append(key)
            continue
        if key in config:
            existing = config[key]
            if isinstance(existing, list):
                if value not in existing:
                    existing.append(value)
                continue
            if existing != value:
                config[key] = [existing, value]
                continue
        config[key] = value
    return config, refused


def connector_summary(conn) -> dict:
    """One row of `connect --list`: what it is, whether it can run, and what it has ingested."""
    cid = conn.id
    state = read_state(cid, "")
    runs = state.get("runs", [])
    missing = missing_env(conn)
    return {
        "id": cid,
        "backend": conn.backend,
        "ready": "no" if missing else "yes",
        "missing_env": ",".join(missing) or "-",
        "configured": "yes" if load_config(cid, "") else "no",
        "streams": len(state.get("cursors", {})),
        "last_run": (runs[0].get("at", "-") if runs else "-"),
        "last_status": (runs[0].get("status", "-") if runs else "-"),
    }


# ---------------------------------------------------------------- CLI


def register_cli(sub) -> None:
    """Add `isidore connect` and `isidore ingest` (registrar loop in cli.main)."""
    p = sub.add_parser("connect", help="list, inspect and configure knowledge connectors (0 LLM)")
    p.add_argument("connector", nargs="?", help="connector id (omit with --list)")
    p.add_argument("--list", action="store_true", help="list every connector and its readiness")
    p.add_argument("--status", action="store_true", help="show one connector's config and cursors")
    p.add_argument("--configure", action="store_true", help="write config from --set/--unset")
    p.add_argument("--set", action="append", default=[], metavar="KEY=VALUE",
                   help="set a config key; repeat the same key to build a list")
    p.add_argument("--unset", action="append", default=[], metavar="KEY",
                   help="remove a config key")
    p.add_argument("--instance", default="", help="instance name for multi-instance connectors")
    p.set_defaults(func=_cmd_connect)

    q = sub.add_parser("ingest", help="run connectors into the raw store (0 LLM, the only network step)")
    q.add_argument("--connector", action="append", default=[], metavar="ID",
                   help="restrict to this connector; repeat for several (default: all)")
    q.add_argument("--limit", type=int, default=None, help="max items per connector")
    q.add_argument("--window-hours", type=int, default=None, help="only items newer than H hours")
    q.add_argument("--max-bytes", type=int, default=None, help="max content bytes per item")
    q.add_argument("--streams", default=None, help="comma-separated streams to restrict to")
    q.add_argument("--instance", default="", help="instance name for multi-instance connectors")
    q.set_defaults(func=_cmd_ingest)


def _cmd_connect(args) -> int:
    if args.list or not args.connector:
        rows = [connector_summary(c) for c in sorted(all_connectors(), key=lambda c: c.id)]
        if not rows:
            print("[isidore] no connectors registered")
            return 0
        print(encode_table("connector", ["id", "backend", "ready", "missing_env",
                                         "configured", "streams", "last_run", "last_status"],
                           rows))
        print(f"[isidore] knowledge home: {home()}")
        return 0

    conn = get(args.connector)
    if conn is None:
        known = ", ".join(sorted(c.id for c in all_connectors())) or "(none)"
        print(f"[isidore] unknown connector '{args.connector}' — registered: {known}")
        return 2

    inst = args.instance
    if args.configure or args.set or args.unset:
        config = load_config(conn.id, inst)
        config, refused = apply_settings(config, args.set)
        for key in args.unset:
            config.pop(key, None)
        path = save_config(conn.id, inst, config)
        for key in refused:
            print(f"[isidore] REFUSED '{key}': the value looks like a credential. A connector's "
                  f"config holds the NAME of an env var, never its value.")
        print(f"[isidore] wrote {path}")
        print(json.dumps(config, ensure_ascii=False, indent=2))
        return 1 if refused else 0

    # --status (the default for a named connector)
    state = read_state(conn.id, inst)
    missing = missing_env(conn)
    print(f"  id         {conn.id}")
    print(f"  backend    {conn.backend}")
    print(f"  env        {', '.join(conn.required_env) or '(none required)'}"
          + (f"  MISSING: {', '.join(missing)}" if missing else ""))
    print(f"  config     {config_path(conn.id, inst)}")
    print(f"  state      {state_path(conn.id, inst)}")
    config = load_config(conn.id, inst)
    if config:
        print(json.dumps(config, ensure_ascii=False, indent=2))
    cursors = state.get("cursors", {})
    if cursors:
        print(encode_table("cursor", ["stream", "at"],
                           [{"stream": s, "at": str(v)[:16]} for s, v in sorted(cursors.items())]))
    runs = state.get("runs", [])
    if runs:
        print(encode_table("run", ["run_id", "at", "status", "items"],
                           [{"run_id": r.get("run_id", "?"), "at": r.get("at", "?"),
                             "status": r.get("status", "?"), "items": r.get("items", 0)}
                            for r in runs[:10]]))
    print(f"[isidore] {sum(1 for _ in iter_items(conn.id, inst))} item(s) stored")
    return 0


def _cmd_ingest(args) -> int:
    wanted = set(args.connector)
    conns = [c for c in sorted(all_connectors(), key=lambda c: c.id)
             if not wanted or c.id in wanted]
    unknown = wanted - {c.id for c in conns}
    if unknown:
        print(f"[isidore] unknown connector(s): {', '.join(sorted(unknown))}")
        return 2
    if not conns:
        print("[isidore] no connectors registered")
        return 0

    options = IngestOptions(
        limit=args.limit, window_hours=args.window_hours, max_bytes=args.max_bytes,
        streams=[s.strip() for s in args.streams.split(",") if s.strip()] if args.streams else None)

    rows, failed = [], False
    for conn in conns:
        missing = missing_env(conn)
        if missing:
            # Fail closed BEFORE any network call: a connector that cannot authenticate never runs.
            rows.append({"connector": conn.id, "status": "skipped", "items": 0,
                         "note": f"missing env: {','.join(missing)}"})
            continue
        cfg = load_config(conn.id, args.instance)
        try:
            res = conn.ingest(IngestOptions(**{**options.__dict__, "config": cfg or None}))
        except Exception as exc:                     # a broken connector must not kill the others
            failed = True
            rows.append({"connector": conn.id, "status": "error", "items": 0, "note": str(exc)[:120]})
            continue
        failed = failed or res.status == "error"
        rows.append({"connector": conn.id, "status": res.status,
                     "items": res.counts.get("items", 0),
                     "note": "; ".join(res.warnings)[:120] or "-"})
    print(encode_table("ingest", ["connector", "status", "items", "note"], rows))
    total = sum(r["items"] for r in rows)
    print(f"[isidore] {total} new item(s) into {home() / 'connectors'} (0 LLM calls)")
    return 1 if failed else 0


__all__ = ["apply_settings", "connector_summary", "load_config", "parse_setting", "register_cli",
           "save_config"]
