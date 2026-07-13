"""git-repo connector (ADR-0032 F1): local repositories as a knowledge source. No network.

Emits ONE item per repo — a compact manifest (branch, HEAD, dirty status, recent commits). The item
id is `<repo-name>@<head-sha>`, so a repo whose HEAD hasn't moved since the stored cursor produces
ZERO new items on re-ingest. That idempotency is the F1 gate, and it only works because this
connector reads the REAL persisted state and writes items + cursor back through the store — the piece
the first draft omitted.
"""
from __future__ import annotations

import json
import subprocess
import time
from pathlib import Path

from ..home import config_path
from .base import IngestOptions, IngestResult, register
from .store import create_run_id, iso_now, read_state, record_run, write_items, write_state

_INSTANCE = ""  # git-repo is a single-instance connector
_GIT_TIMEOUT = 30


class GitRepoConnector:
    id = "git-repo"
    backend = "local-git"
    required_env: list[str] = []

    def ingest(self, options: IngestOptions) -> IngestResult:
        config = options.config or self._load_config()
        repos = config.get("repos") or []
        run_id = create_run_id()
        if not repos:
            return IngestResult(self.id, "skipped", warnings=["no repositories configured"],
                                run_id=run_id)

        state = read_state(self.id, _INSTANCE)
        cursors = state.setdefault("cursors", {})
        new_items: list[dict] = []
        warnings: list[str] = []
        processed = ok = 0

        for repo in repos:
            if options.limit is not None and processed >= options.limit:
                break
            processed += 1
            item, warning = self._manifest(repo, cursors)
            if warning:
                warnings.append(warning)
                continue
            ok += 1
            if item is not None:  # None == HEAD unchanged since cursor
                new_items.append(item)
                cursors[item["stream"]] = item["meta"]["head_sha"]

        raw_files: list[str] = []
        if new_items:
            raw_files.append(write_items(self.id, _INSTANCE, run_id, new_items))

        status = "success" if ok else "error"
        record_run(state, {"run_id": run_id, "at": iso_now(), "status": status,
                           "raw_files": raw_files, "items": len(new_items)})
        write_state(self.id, _INSTANCE, state)
        return IngestResult(self.id, status, raw_files, warnings,
                            {"repos": ok, "items": len(new_items)}, run_id)

    def _load_config(self) -> dict:
        path = config_path(self.id, _INSTANCE)
        if not path.is_file():
            return {}
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return {}

    def _manifest(self, repo: str, cursors: dict) -> tuple[dict | None, str | None]:
        """(item, None) for a changed repo, (None, None) if HEAD is unchanged, (None, warning) on
        any git error. One bad path never aborts the run."""
        name = Path(repo).name or repo
        head = self._git(repo, "rev-parse", "HEAD")
        if head is None:
            return None, f"not a git repository or git failed: {repo}"
        if cursors.get(name) == head:
            return None, None

        branch = self._git(repo, "rev-parse", "--abbrev-ref", "HEAD") or "unknown"
        status = self._git(repo, "status", "--porcelain") or ""
        dirty = [ln for ln in status.splitlines() if ln.strip()]
        commits = self._commits(repo)

        lines = [f"Repository: {name}", f"Branch: {branch}", f"HEAD: {head}",
                 f"Dirty files: {len(dirty)}", "Recent commits:"]
        lines += [f"  {c['sha'][:8]} {c['ts']} {c['author']}: {c['subject']}" for c in commits]
        content = "\n".join(lines)

        item = {
            "id": f"{name}@{head}",
            "stream": name,
            "ts": iso_now(),
            "content": content,
            "meta": {"repo": repo, "branch": branch, "head_sha": head,
                     "dirty": len(dirty), "commits": len(commits)},
        }
        return item, None

    def _commits(self, repo: str) -> list[dict]:
        out = self._git(repo, "log", "-n", "20", "--pretty=%H%x1f%an%x1f%at%x1f%s")
        if not out:
            return []
        commits = []
        for line in out.splitlines():
            parts = line.split("\x1f")
            if len(parts) != 4:
                continue
            try:
                ts = time.strftime("%Y-%m-%d", time.gmtime(int(parts[2])))
            except ValueError:
                ts = "?"
            commits.append({"sha": parts[0], "author": parts[1], "ts": ts, "subject": parts[3]})
        return commits

    @staticmethod
    def _git(repo: str, *args: str) -> str | None:
        """Run a git command; return stdout or None on any failure (never raises)."""
        try:
            # git emits UTF-8; force it (Windows' default cp1252 decode raises on real commit
            # messages with accents/emoji — caught by the live run, invisible to ASCII tests).
            res = subprocess.run(["git", "-C", repo, *args], capture_output=True, text=True,
                                 encoding="utf-8", errors="replace", timeout=_GIT_TIMEOUT)
        except (OSError, subprocess.SubprocessError):
            return None
        if res.returncode != 0:
            return None
        return res.stdout.strip()


register(GitRepoConnector())
