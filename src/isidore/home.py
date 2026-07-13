"""The knowledge home (`~/.isidore`, override with `ISIDORE_HOME`).

Where connectors persist their raw ingested items, cursors, and the compiled knowledge wiki. Kept
separate from any repo: it is per-user, local-only, and (unlike the per-repo `.isidore/`) never
travels. Permissions are tightened best-effort — a no-op on Windows, never a crash anywhere.
"""
from __future__ import annotations

import os
from pathlib import Path


def home() -> Path:
    """`$ISIDORE_HOME` if set, else `~/.isidore`."""
    env = os.environ.get("ISIDORE_HOME")
    return Path(env).expanduser().resolve() if env else Path.home() / ".isidore"


def connector_dir(cid: str, instance: str | None = None) -> Path:
    base = home() / "connectors" / cid
    return base / instance if instance else base


def raw_dir(cid: str, instance: str | None, run_id: str) -> Path:
    return connector_dir(cid, instance) / "raw" / run_id


def config_path(cid: str, instance: str | None = None) -> Path:
    return connector_dir(cid, instance) / "config.json"


def state_path(cid: str, instance: str | None = None) -> Path:
    return connector_dir(cid, instance) / "state.json"


def knowledge_dir() -> Path:
    return home() / "knowledge"


def safe_chmod(path: Path, mode: int) -> None:
    """chmod that never raises; a no-op on Windows where POSIX modes don't apply."""
    if os.name == "nt":
        return
    try:
        path.chmod(mode)
    except OSError:
        pass


def safe_mkdir(path: Path, mode: int = 0o700) -> None:
    """mkdir -p with restrictive mode, best-effort — never raises on a perms/FS quirk."""
    try:
        path.mkdir(mode=mode, parents=True, exist_ok=True)
    except OSError:
        return
    safe_chmod(path, mode)
