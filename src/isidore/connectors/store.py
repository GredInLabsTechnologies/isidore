"""The raw store: immutable ingested items + per-connector cursor state (ADR-0032 F1).

Each item is `{id, stream, ts, content, meta, chash}` where `chash = _hash(_normalize(content))`
reuses claims.py's fingerprint — the SAME primitive that anchors code claims now anchors external
evidence (`src://<cid>/<instance>/<item-id>`). Items are append-only and never rewritten, so a claim
anchored to one is stable; staleness for knowledge is detected by stream watermark, not by content
change (that is F2's job, and `resolve_uri` here is the anchor it will use).
"""
from __future__ import annotations

import json
import os
import shutil
import time
from collections.abc import Iterable, Iterator

from ..claims import _hash, _normalize
from ..home import connector_dir, raw_dir, safe_chmod, safe_mkdir, state_path

_DEFAULT_STATE = {"version": 1, "cursors": {}, "runs": []}


def create_run_id() -> str:
    """Sortable, collision-resistant run id (UTC second + millis)."""
    now = time.time()
    return time.strftime("%Y%m%dT%H%M%S", time.gmtime(now)) + f"{int(now * 1000) % 1000:03d}"


def iso_now() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def chash(content: str) -> str:
    return _hash(_normalize(content))


def write_items(cid: str, instance: str | None, run_id: str, items: Iterable[dict]) -> str:
    """Append items as JSONL to `raw/<run_id>/items.jsonl`; stamp each with its `chash`. Does NOT
    mutate the caller's dicts. Returns the file path."""
    out_dir = raw_dir(cid, instance, run_id)
    safe_mkdir(out_dir)
    out_file = out_dir / "items.jsonl"
    with open(out_file, "w", encoding="utf-8") as fh:
        for item in items:
            stamped = {**item, "chash": chash(item.get("content", ""))}
            fh.write(json.dumps(stamped, ensure_ascii=False) + "\n")
    safe_chmod(out_file, 0o600)
    return str(out_file)


def read_state(cid: str, instance: str | None = None) -> dict:
    """Current state, or a fresh default if missing OR corrupt (I13-style recovery, never a crash)."""
    path = state_path(cid, instance)
    if not path.exists():
        return json.loads(json.dumps(_DEFAULT_STATE))
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return json.loads(json.dumps(_DEFAULT_STATE))
    if not isinstance(data, dict) or data.get("version") != 1:
        return json.loads(json.dumps(_DEFAULT_STATE))
    data.setdefault("cursors", {})
    data.setdefault("runs", [])
    return data


def write_state(cid: str, instance: str | None, state: dict) -> None:
    """Atomic write (tmp + os.replace) so a crash mid-write never corrupts the live state."""
    path = state_path(cid, instance)
    safe_mkdir(path.parent)
    tmp = path.with_name(path.name + f".tmp{os.getpid()}")
    tmp.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
    safe_chmod(tmp, 0o600)
    os.replace(tmp, path)


def update_cursor(state: dict, stream: str, last_id: str) -> None:
    state.setdefault("cursors", {})[stream] = last_id


def record_run(state: dict, run_summary: dict) -> None:
    """Prepend a run summary, keeping the last 20 (newest first)."""
    runs = state.setdefault("runs", [])
    runs.insert(0, run_summary)
    del runs[20:]


def iter_items(cid: str, instance: str | None = None, stream: str | None = None) -> Iterator[dict]:
    """Yield stored items, newest run first. A corrupt/half-written JSONL line is skipped, not fatal."""
    for run_id in _run_ids_newest_first(cid, instance):
        items_file = connector_dir(cid, instance) / "raw" / run_id / "items.jsonl"
        if not items_file.exists():
            continue
        try:
            lines = items_file.read_text(encoding="utf-8").splitlines()
        except OSError:
            continue
        for line in lines:
            if not line.strip():
                continue
            try:
                item = json.loads(line)
            except ValueError:
                continue
            if isinstance(item, dict) and (stream is None or item.get("stream") == stream):
                yield item


def _run_ids_newest_first(cid: str, instance: str | None) -> list[str]:
    """Run ids from state (already newest-first); fall back to sorting the raw dir if state is thin."""
    state = read_state(cid, instance)
    ids = [r.get("run_id") for r in state.get("runs", []) if r.get("run_id")]
    if ids:
        return ids
    raw_root = connector_dir(cid, instance) / "raw"
    if not raw_root.is_dir():
        return []
    return sorted((p.name for p in raw_root.iterdir() if p.is_dir()), reverse=True)


def resolve_uri(uri: str) -> dict | None:
    """`src://<cid>/<instance>/<item-id>` or `src://<cid>/<item-id>` -> the raw item, or None.

    Never raises on a malformed URI. F2's claim anchoring resolves external evidence through here.
    """
    if not uri.startswith("src://"):
        return None
    parts = uri[len("src://"):].split("/")
    if len(parts) == 2:
        cid, instance, item_id = parts[0], None, parts[1]
    elif len(parts) == 3:
        cid, instance, item_id = parts[0], parts[1], parts[2]
    else:
        return None
    if not cid or not item_id:
        return None
    for item in iter_items(cid, instance):
        if item.get("id") == item_id:
            return item
    return None


def prune_runs(cid: str, instance: str | None, keep: int) -> None:
    """Drop all but the newest `keep` runs, deleting their raw dirs and trimming state."""
    state = read_state(cid, instance)
    runs = state.get("runs", [])
    if len(runs) <= keep:
        return
    for run in runs[keep:]:
        rid = run.get("run_id")
        if rid:
            shutil.rmtree(connector_dir(cid, instance) / "raw" / rid, ignore_errors=True)
    del runs[keep:]
    write_state(cid, instance, state)
