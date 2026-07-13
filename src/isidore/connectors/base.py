"""Connector protocol + registry (ADR-0032 F1).

A connector ingests raw items from ONE source into the knowledge home's raw store, deterministically
and with zero LLM calls. The registry is populated by built-in connectors (which register on import)
and by third-party plugins discovered via the `isidore.connectors` entry-point group — so the private
Ágora connector can plug in without ever touching this public repo.
"""
from __future__ import annotations

import importlib.metadata
import os
import sys
from dataclasses import dataclass, field
from typing import Literal, Protocol, runtime_checkable

IngestStatus = Literal["success", "skipped", "error"]
Backend = Literal["direct-api", "local-git", "mcp-http", "mcp-stdio"]


@dataclass
class IngestResult:
    """Outcome of one ingest run. `raw_files` are the JSONL files written this run."""
    connector_id: str
    status: IngestStatus
    raw_files: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    counts: dict[str, int] = field(default_factory=dict)
    run_id: str = ""


@dataclass
class IngestOptions:
    """Caps and scoping for a run. All limits live here (in code), never in a prompt."""
    limit: int | None = None
    window_hours: int | None = None
    max_bytes: int | None = None
    streams: list[str] | None = None
    config: dict | None = None


@runtime_checkable
class Connector(Protocol):
    id: str
    backend: Backend
    required_env: list[str]

    def ingest(self, options: IngestOptions) -> IngestResult: ...


_CONNECTORS: dict[str, Connector] = {}
_PLUGINS_LOADED = False


def register(connector: Connector) -> None:
    _CONNECTORS[connector.id] = connector


def get(cid: str) -> Connector | None:
    _load_plugins()
    return _CONNECTORS.get(cid)


def all_connectors() -> list[Connector]:
    _load_plugins()
    return list(_CONNECTORS.values())


def _load_plugins() -> None:
    """Discover third-party connectors once. A broken entry-point warns and is skipped — one bad
    plugin never blocks the built-ins."""
    global _PLUGINS_LOADED
    if _PLUGINS_LOADED:
        return
    _PLUGINS_LOADED = True
    try:
        eps = importlib.metadata.entry_points(group="isidore.connectors")
    except Exception as exc:  # metadata layout varies across Python/pip versions
        print(f"[isidore] connector plugin discovery failed: {exc}", file=sys.stderr)
        return
    for ep in eps:
        try:
            register(ep.load()())
        except Exception as exc:
            print(f"[isidore] connector plugin '{ep.name}' failed to load: {exc}", file=sys.stderr)


def missing_env(conn: Connector) -> list[str]:
    """Names of required env vars that are absent — for failing closed. Returns NAMES only; never
    reads a secret's value."""
    return [name for name in conn.required_env if name not in os.environ]
