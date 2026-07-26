"""RSS / Atom connector (ADR-0032 F4). stdlib `xml.etree` + `urllib`, no dependencies.

One stream per configured feed; one item per entry, keyed by its guid (falling back to its link, then
to a hash of title+date — a feed with no stable id must still be idempotent). Only what the feed
itself hands over is stored: fetching the linked article and parsing its HTML is explicitly out of
scope for this phase.

Configure with:
    isidore connect rss --configure --set feeds=https://example.com/feed.xml \\
                                    --set feeds=https://other.dev/atom.xml
"""
from __future__ import annotations

import hashlib
import xml.etree.ElementTree as ET
from urllib.parse import urlsplit

from .base import IngestOptions, IngestResult, register, stored_config
from .http import DEFAULT_MAX_BYTES, FetchError, fetch
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
MAX_ENTRIES_PER_FEED = 50          # a cap in code, always applied (I2)
MAX_CONTENT_CHARS = 4000           # per entry; the summary a feed gives, not an article

# Atom lives in a namespace; RSS 2.0 does not. Both go through one parser by matching on the LOCAL
# tag name, instead of two nearly-identical parsers plus a namespace table to keep in sync.


def _local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def _text(el, *names: str) -> str:
    """First non-empty child whose local tag is one of `names`, stripped."""
    for child in el:
        if _local(child.tag) in names:
            value = "".join(child.itertext()).strip()
            if value:
                return value
    return ""


def _link(el) -> str:
    """RSS puts the URL in <link>'s text; Atom puts it in <link href=...>, sometimes several."""
    fallback = ""
    for child in el:
        if _local(child.tag) != "link":
            continue
        href = child.get("href")
        rel = child.get("rel", "alternate")
        if href and rel == "alternate":
            return href.strip()
        if href and not fallback:
            fallback = href.strip()
        text = (child.text or "").strip()
        if text and not fallback:
            fallback = text
    return fallback


def parse_feed(xml_text: str) -> tuple[str, list[dict]]:
    """(feed title, entries) from RSS 2.0 or Atom. Raises ValueError on XML that will not parse.

    Entries are dicts of plain strings: `id, title, link, published, summary, author`. Nothing here
    reaches the network, so a stored feed body can be re-parsed offline (I7).
    """
    try:
        root = ET.fromstring(xml_text)              # noqa: S314 - stdlib parser, no external entities
    except ET.ParseError as exc:
        raise ValueError(f"not parseable as RSS or Atom: {exc}") from exc

    channel = root.find("channel")                  # RSS 2.0
    container = channel if channel is not None else root
    title = _text(container, "title") or "(untitled feed)"

    entries = []
    for el in container:
        if _local(el.tag) not in ("item", "entry"):
            continue
        summary = _text(el, "description", "summary", "content", "encoded")
        entries.append({
            "id": _text(el, "guid", "id"),
            "title": _text(el, "title"),
            "link": _link(el),
            "published": _text(el, "pubDate", "published", "updated", "date"),
            "summary": summary[:MAX_CONTENT_CHARS],
            "author": _text(el, "author", "creator"),
        })
        if len(entries) >= MAX_ENTRIES_PER_FEED:
            break
    return title, entries


def entry_id(entry: dict) -> str:
    """A stable id, so re-ingesting an unchanged feed produces nothing.

    guid, else link, else a hash of title+date. The last resort is what makes a badly-behaved feed
    idempotent instead of duplicating every entry on every run.
    """
    for key in ("id", "link"):
        value = (entry.get(key) or "").strip()
        if value:
            return value
    seed = f"{entry.get('title', '')}|{entry.get('published', '')}"
    return "sha1:" + hashlib.sha1(seed.encode("utf-8")).hexdigest()[:16]   # noqa: S324 - an id, not a MAC


def stream_name(feed_url: str) -> str:
    """A short, stable stream name for a feed URL (its host, which is what a reader recognises)."""
    host = urlsplit(feed_url).netloc.lower()
    return host[4:] if host.startswith("www.") else host or feed_url


def _render(entry: dict, feed_title: str) -> str:
    lines = [f"Feed: {feed_title}", f"Title: {entry.get('title') or '(untitled)'}"]
    if entry.get("author"):
        lines.append(f"Author: {entry['author']}")
    if entry.get("published"):
        lines.append(f"Published: {entry['published']}")
    if entry.get("link"):
        lines.append(f"Link: {entry['link']}")
    if entry.get("summary"):
        lines += ["Summary:", entry["summary"]]
    return "\n".join(lines)


class RssConnector:
    id = "rss"
    backend = "direct-api"
    required_env: list[str] = []          # public feeds; no credential to fail closed on

    def ingest(self, options: IngestOptions) -> IngestResult:
        config = options.config or stored_config(self.id, _INSTANCE)
        feeds = config.get("feeds") or []
        if isinstance(feeds, str):
            feeds = [feeds]
        run_id = create_run_id()
        if not feeds:
            return IngestResult(self.id, "skipped", warnings=["no feeds configured"], run_id=run_id)

        state = read_state(self.id, _INSTANCE)
        cursors = state.setdefault("cursors", {})
        seen: dict = state.setdefault("seen", {})
        wanted = set(options.streams or ())
        max_bytes = options.max_bytes or DEFAULT_MAX_BYTES
        new_items: list[dict] = []
        warnings: list[str] = []
        reached = failed = 0

        for url in feeds:
            stream = stream_name(url)
            if wanted and stream not in wanted:
                continue
            try:
                xml_text, truncated = fetch(url, max_bytes=max_bytes)
                if truncated:
                    # Truncated XML never parses, and letting it through reported "not parseable as
                    # RSS" — blaming the feed for our own cap. Measured on hnrss.org at 4000 bytes.
                    raise FetchError(f"feed is larger than the {max_bytes}-byte cap; not read "
                                     f"(raise --max-bytes to accept it)")
                feed_title, entries = parse_feed(xml_text)
            except (FetchError, ValueError) as exc:
                # I6: this feed contributed nothing and its cursor is untouched. Next run retries it.
                failed += 1
                warnings.append(f"{stream}: {exc}")
                continue
            reached += 1

            known = set(seen.get(stream) or [])
            fresh = []
            for entry in entries:
                eid = entry_id(entry)
                if eid in known:
                    continue
                if options.limit is not None and len(new_items) + len(fresh) >= options.limit:
                    warnings.append(f"{stream}: stopped at --limit {options.limit}; "
                                    f"older entries were left for the next run")
                    break
                fresh.append((eid, entry))
            for eid, entry in fresh:
                new_items.append({"id": safe_item_id(stream, eid), "stream": stream,
                                  "ts": iso_now(),
                                  "content": _render(entry, feed_title),
                                  "meta": {"feed": url, "link": entry.get("link", ""),
                                           "published": entry.get("published", ""),
                                           "entry_id": eid}})
            if fresh:
                # Remember ids, not a timestamp: feeds reorder and backfill, and a date watermark
                # would skip an entry that appears late with an older date.
                seen[stream] = ([eid for eid, _e in fresh] + list(known))[:MAX_ENTRIES_PER_FEED * 4]
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
                            {"feeds": reached, "failed": failed, "items": len(new_items)}, run_id)


register(RssConnector())
