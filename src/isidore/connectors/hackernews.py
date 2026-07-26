"""Hacker News connector (ADR-0032 F4): public front-page tags and Algolia searches. No auth.

Everything comes from Algolia's public HN API, which answers a whole page or a whole search in ONE
request — the Firebase API would need one call per story, which is a rate-limit problem dressed as an
architecture. Item id is HN's own `objectID`, so re-ingesting an unchanged search yields nothing.

Configure with:
    isidore connect hackernews --configure --set queries="code documentation staleness" \\
                                          --set feeds=front_page
"""
from __future__ import annotations

import time
from urllib.parse import quote

from .base import IngestOptions, IngestResult, register, stored_config
from .http import DEFAULT_MAX_BYTES, FetchError, fetch_json
from .store import (
    create_run_id,
    iso_now,
    read_state,
    record_run,
    safe_item_id,
    write_items,
    write_state,
)

_INSTANCE = ""
API = "https://hn.algolia.com/api/v1"
HITS_PER_REQUEST = 20               # a cap in code (I2); Algolia's own default is 20
MAX_TEXT_CHARS = 4000

# The tags Algolia exposes as browsable listings. Anything else is a search.
FEED_TAGS = {"front_page": "front_page", "show_hn": "show_hn", "ask_hn": "ask_hn",
             "story": "story", "poll": "poll"}


def search_url(query: str, hits: int = HITS_PER_REQUEST) -> str:
    """Algolia URL for a text search, newest-first so a cursor means something."""
    return f"{API}/search_by_date?query={quote(query)}&tags=story&hitsPerPage={hits}"


def feed_url(tag: str, hits: int = HITS_PER_REQUEST) -> str:
    """Algolia URL for a listing tag (front_page, show_hn, ...)."""
    return f"{API}/search?tags={quote(FEED_TAGS.get(tag, tag))}&hitsPerPage={hits}"


def with_window(url: str, window_hours: int | None) -> str:
    """Append Algolia's own time filter. Applied server-side, so the cap costs no extra bytes.

    A non-positive window, or one reaching past the epoch, adds NO filter rather than one that matches
    nothing — the rule the git connector had to learn the hard way: a cap that cannot be expressed
    must not quietly come back empty.
    """
    if not window_hours or window_hours <= 0:
        return url
    floor = int(time.time() - window_hours * 3600)
    return f"{url}&numericFilters=created_at_i>{floor}" if floor > 0 else url


def _render(hit: dict) -> str:
    lines = [f"Title: {hit.get('title') or hit.get('story_title') or '(untitled)'}"]
    for label, key in (("Author", "author"), ("Points", "points"),
                       ("Comments", "num_comments"), ("Posted", "created_at")):
        if hit.get(key) not in (None, ""):
            lines.append(f"{label}: {hit[key]}")
    if hit.get("url"):
        lines.append(f"Link: {hit['url']}")
    if hit.get("objectID"):
        lines.append(f"Discussion: https://news.ycombinator.com/item?id={hit['objectID']}")
    text = (hit.get("story_text") or hit.get("comment_text") or "").strip()
    if text:
        lines += ["Text:", text[:MAX_TEXT_CHARS]]
    return "\n".join(lines)


def parse_hits(payload: object) -> list[dict]:
    """The `hits` array, or ValueError. A payload without one is malformed, not empty (I6): reporting
    "0 new items" for a response we failed to understand is the lie this refuses to tell."""
    if not isinstance(payload, dict) or not isinstance(payload.get("hits"), list):
        raise ValueError("response has no 'hits' array")
    return [h for h in payload["hits"] if isinstance(h, dict)]


class HackerNewsConnector:
    id = "hackernews"
    backend = "direct-api"
    required_env: list[str] = []          # the Algolia HN API is public

    def ingest(self, options: IngestOptions) -> IngestResult:
        config = options.config or stored_config(self.id, _INSTANCE)
        targets = _targets(config)
        run_id = create_run_id()
        if not targets:
            return IngestResult(self.id, "skipped",
                                warnings=["no queries or feeds configured"], run_id=run_id)

        state = read_state(self.id, _INSTANCE)
        cursors = state.setdefault("cursors", {})
        seen: dict = state.setdefault("seen", {})
        wanted = set(options.streams or ())
        max_bytes = options.max_bytes or DEFAULT_MAX_BYTES
        new_items: list[dict] = []
        warnings: list[str] = []
        reached = failed = 0

        for stream, url in targets:
            if wanted and stream not in wanted:
                continue
            try:
                payload, _t = fetch_json(with_window(url, options.window_hours),
                                         max_bytes=max_bytes)
                hits = parse_hits(payload)
            except (FetchError, ValueError) as exc:
                failed += 1
                warnings.append(f"{stream}: {exc}")      # state untouched for this stream (I6)
                continue
            reached += 1

            known = set(seen.get(stream) or [])
            fresh = []
            for hit in hits:
                oid = str(hit.get("objectID") or "").strip()
                if not oid or oid in known:
                    continue
                if options.limit is not None and len(new_items) + len(fresh) >= options.limit:
                    warnings.append(f"{stream}: stopped at --limit {options.limit}; "
                                    f"the rest of the page was left for the next run")
                    break
                fresh.append((oid, hit))
            for oid, hit in fresh:
                new_items.append({"id": safe_item_id(stream, oid), "stream": stream,
                                  "ts": iso_now(),
                                  "content": _render(hit),
                                  "meta": {"object_id": oid, "url": hit.get("url") or "",
                                           "points": hit.get("points"),
                                           "created_at": hit.get("created_at") or ""}})
            if fresh:
                seen[stream] = ([o for o, _h in fresh] + list(known))[:HITS_PER_REQUEST * 10]
                cursors[stream] = fresh[0][0]

        raw_files: list[str] = []
        if new_items:
            raw_files.append(write_items(self.id, _INSTANCE, run_id, new_items))
        # I6, per F4's card: a target that failed to fetch or returned a payload we could not
        # parse makes the RUN an error, even when other targets delivered. The items that did arrive
        # are still stored and counted — but a caller checking `status == "success"` must never be
        # told all was well while a source was unreachable. (git-repo keeps F1's laxer rule: a
        # missing local path is a permanent config mistake, not a transport failure.)
        status = "error" if failed else "success"
        record_run(state, {"run_id": run_id, "at": iso_now(), "status": status,
                           "raw_files": raw_files, "items": len(new_items)})
        write_state(self.id, _INSTANCE, state)
        return IngestResult(self.id, status, raw_files, warnings,
                            {"targets": reached, "failed": failed, "items": len(new_items)}, run_id)


def _targets(config: dict) -> list[tuple[str, str]]:
    """(stream, url) for every configured search and listing. Streams are named for what they are, so
    a claim citing one reads as evidence rather than as an opaque id."""
    out: list[tuple[str, str]] = []
    for tag in _as_list(config.get("feeds")):
        out.append((f"feed:{tag}", feed_url(tag)))
    for query in _as_list(config.get("queries")):
        out.append((f"search:{query}", search_url(query)))
    return out


def _as_list(value) -> list[str]:
    if not value:
        return []
    return [str(value)] if isinstance(value, str) else [str(v) for v in value]


register(HackerNewsConnector())
