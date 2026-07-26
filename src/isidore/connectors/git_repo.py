"""git-repo connector (ADR-0032 F1): local repositories as a knowledge source. No network.

Emits ONE item per repo — a compact manifest (branch, HEAD, dirty status, recent commits). The item
id is `<repo-name>@<head-sha>`, so a repo whose HEAD hasn't moved since the stored cursor produces
ZERO new items on re-ingest. That idempotency is the F1 gate, and it only works because this
connector reads the REAL persisted state and writes items + cursor back through the store — the piece
the first draft omitted.
"""
from __future__ import annotations

import subprocess
import time
from pathlib import Path

from .base import IngestOptions, IngestResult, register, stored_config
from .store import (
    create_run_id,
    iso_now,
    read_state,
    record_run,
    safe_item_id,
    write_items,
    write_state,
)

_INSTANCE = ""  # git-repo is a single-instance connector
_GIT_TIMEOUT = 30
_TRUNCATION_MARK = "\n[truncated by --max-bytes]"


def _window_floor(window_hours: int | None) -> tuple[int | None, str | None]:
    """Epoch second a commit must reach to be inside the window, or (None, note) if unbounded.

    The window is applied to git's OUTPUT, not handed to `git log --since`, for two measured reasons:
      - `--since=<N> hours ago` collapses silently. On git 2.53 a window of 999999 hours returns ZERO
        commits with exit status 0 (approxidate gives up), so "the last 114 years" is
        indistinguishable from "this repo has no commits".
      - `--since` is a revision-LIMITING option: it prunes the walk at the first commit older than the
        cutoff. A history whose dates run out of order — a rebase, a cherry-pick keeping its date,
        imported history — therefore loses every commit BEHIND the old one, silently. Measured: a repo
        whose HEAD is back-dated returns nothing at all for a 24h window, including the commit made
        seconds ago.
    Filtering the (already count-capped) output has neither failure mode.
    """
    if window_hours is None:
        return None, None
    if window_hours <= 0:
        return None, (f"window_hours={window_hours} is not a window; ignored, "
                      f"the full commit list was read")
    floor = time.time() - window_hours * 3600
    if floor <= 0:
        return None, (f"window_hours={window_hours} reaches before the epoch; ignored, "
                      f"the full commit list was read")
    return int(floor), None


def _cap_content(item: dict, max_bytes: int) -> tuple[dict, str | None]:
    """Cap an item's content to `max_bytes` UTF-8 bytes, cutting on a character boundary.

    Returns (item, note). The note is the caller's warning: a reader who asked for a cap must be told
    it bit, or a manifest that lost its last commits reads exactly like a repo that has none. The
    item's `meta` records the original size so the loss is measurable, not just mentioned.
    """
    raw = item.get("content", "").encode("utf-8")
    if len(raw) <= max_bytes:
        return item, None
    kept = raw[:max_bytes].decode("utf-8", errors="ignore")
    capped = {**item, "content": kept + _TRUNCATION_MARK,
              "meta": {**item.get("meta", {}), "truncated": True, "content_bytes": len(raw)}}
    return capped, (f"{item.get('stream', '?')}: content truncated to {max_bytes} of "
                    f"{len(raw)} bytes (--max-bytes)")


class GitRepoConnector:
    id = "git-repo"
    backend = "local-git"
    required_env: list[str] = []

    def ingest(self, options: IngestOptions) -> IngestResult:
        config = options.config or stored_config(self.id, _INSTANCE)
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

        floor, floor_note = _window_floor(options.window_hours)
        if floor_note:
            warnings.append(floor_note)
        wanted = set(options.streams or ())
        for repo in repos:
            if options.limit is not None and processed >= options.limit:
                break
            if wanted and (Path(repo).name or repo) not in wanted:
                continue                      # out of the requested streams: not read, not touched
            processed += 1
            item, warning = self._manifest(repo, cursors, floor, options.window_hours)
            if warning:
                warnings.append(warning)
                continue
            ok += 1
            if item is not None:  # None == HEAD unchanged since cursor
                if options.max_bytes is not None:
                    item, note = _cap_content(item, options.max_bytes)
                    if note:
                        warnings.append(note)   # truncation is REPORTED, never silent
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

    def _manifest(self, repo: str, cursors: dict, floor: int | None = None,
                  window_hours: int | None = None) -> tuple[dict | None, str | None]:
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
        commits = self._commits(repo, floor)

        lines = [f"Repository: {name}", f"Branch: {branch}", f"HEAD: {head}",
                 f"Dirty files: {len(dirty)}"]
        if floor is not None:
            # Say the window out loud. Without it, "Recent commits:" followed by nothing reads as a
            # repo with no history rather than one with nothing inside the window asked for.
            lines.append(f"Commit window: last {window_hours} hour(s)")
        lines.append("Recent commits:" if commits else "Recent commits: (none in range)")
        lines += [f"  {c['sha'][:8]} {c['ts']} {c['author']}: {c['subject']}" for c in commits]
        content = "\n".join(lines)

        item = {
            "id": safe_item_id(name, head),
            "stream": name,
            "ts": iso_now(),
            "content": content,
            "meta": {"repo": repo, "branch": branch, "head_sha": head,
                     "dirty": len(dirty), "commits": len(commits),
                     **({"window_hours": window_hours} if floor is not None else {})},
        }
        return item, None

    def _commits(self, repo: str, floor: int | None = None) -> list[dict]:
        # Bounded by COUNT here and by TIME below, on git's output rather than through `--since`
        # (see _window_floor for the two ways that option loses commits without saying so).
        out = self._git(repo, "log", "-n", "20", "--pretty=%H%x1f%an%x1f%at%x1f%s")
        if not out:
            return []
        commits = []
        for line in out.splitlines():
            parts = line.split("\x1f")
            if len(parts) != 4:
                continue
            try:
                epoch = int(parts[2])
            except ValueError:
                ts = "?"
            else:
                if floor is not None and epoch < floor:
                    continue                     # outside the requested window
                ts = time.strftime("%Y-%m-%d", time.gmtime(epoch))
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
