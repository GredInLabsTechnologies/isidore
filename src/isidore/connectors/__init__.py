"""Connectors: deterministic, zero-LLM ingest of external evidence into the knowledge home.

Importing this package registers the built-in connectors. Third-party connectors (e.g. the private
Ágora connector) register via the `isidore.connectors` entry-point group — see base._load_plugins.
"""
from __future__ import annotations

from . import git_repo  # noqa: F401  (import for its self-registration side effect)
from . import mcp  # noqa: F401  (import for its self-registration side effect)
from .base import (
    Connector,
    IngestOptions,
    IngestResult,
    all_connectors,
    get,
    missing_env,
    register,
)

__all__ = [
    "Connector",
    "IngestOptions",
    "IngestResult",
    "all_connectors",
    "get",
    "missing_env",
    "register",
]
