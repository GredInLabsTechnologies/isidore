"""Web-search connector (ADR-0032 F4): any Tavily-compatible endpoint, named by env var.

Provider-agnostic on purpose. The endpoint and the key are `ISIDORE_WEBSEARCH_URL` and
`ISIDORE_WEBSEARCH_KEY`; the config holds the QUERIES and never a credential (I9). With no key set the
connector is skipped with a message that says so — a search nobody ran is reported as not run, never
as zero results.

Configure with:
    isidore connect websearch --configure --set queries="documentation staleness detection"
    setx ISIDORE_WEBSEARCH_URL https://api.tavily.com/search   # or any compatible endpoint
"""
from __future__ import annotations

import json
import os

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
ENV_URL = "ISIDORE_WEBSEARCH_URL"
ENV_KEY = "ISIDORE_WEBSEARCH_KEY"
MAX_RESULTS = 10                    # a cap in code (I2)
MAX_CONTENT_CHARS = 4000


def parse_results(payload: object) -> list[dict]:
    """The `results` array of a Tavily-shaped response, or ValueError.

    Accepts the two shapes compatible providers actually return: `{"results": [...]}` and a bare
    list. Anything else is malformed and must be an error — a provider that changed its schema is not
    a provider that found nothing (I6).
    """
    rows = payload.get("results") if isinstance(payload, dict) else payload
    if not isinstance(rows, list):
        raise ValueError("response has no 'results' array")
    return [r for r in rows if isinstance(r, dict)]


def result_id(result: dict) -> str:
    """The URL is the identity of a web result: the same page found again is the same item."""
    return (result.get("url") or result.get("link") or "").strip()


def _render(result: dict, query: str) -> str:
    lines = [f"Query: {query}", f"Title: {result.get('title') or '(untitled)'}"]
    if result_id(result):
        lines.append(f"Link: {result_id(result)}")
    if result.get("published_date"):
        lines.append(f"Published: {result['published_date']}")
    if result.get("score") is not None:
        lines.append(f"Provider score: {result['score']}")
    body = (result.get("content") or result.get("snippet") or "").strip()
    if body:
        lines += ["Extract:", body[:MAX_CONTENT_CHARS]]
    return "\n".join(lines)


class WebSearchConnector:
    id = "websearch"
    backend = "direct-api"
    required_env = [ENV_URL, ENV_KEY]     # absent -> skipped before any network call (I6)

    def ingest(self, options: IngestOptions) -> IngestResult:
        config = options.config or stored_config(self.id, _INSTANCE)
        queries = config.get("queries") or []
        if isinstance(queries, str):
            queries = [queries]
        run_id = create_run_id()
        if not queries:
            return IngestResult(self.id, "skipped", warnings=["no queries configured"],
                                run_id=run_id)
        url, key = os.environ.get(ENV_URL), os.environ.get(ENV_KEY)
        if not url or not key:
            missing = ", ".join(n for n in (ENV_URL, ENV_KEY) if not os.environ.get(n))
            return IngestResult(self.id, "skipped",
                                warnings=[f"no search provider configured (missing {missing}); "
                                          f"no query was run"], run_id=run_id)

        state = read_state(self.id, _INSTANCE)
        cursors = state.setdefault("cursors", {})
        seen: dict = state.setdefault("seen", {})
        wanted = set(options.streams or ())
        max_bytes = options.max_bytes or DEFAULT_MAX_BYTES
        limit = min(options.limit or MAX_RESULTS, MAX_RESULTS)
        new_items: list[dict] = []
        warnings: list[str] = []
        reached = failed = 0

        for query in queries:
            stream = f"search:{query}"
            if wanted and stream not in wanted:
                continue
            body = json.dumps({"api_key": key, "query": query, "max_results": limit,
                               "search_depth": "basic"}).encode("utf-8")
            try:
                text, truncated = fetch(url, data=body, max_bytes=max_bytes,
                                        headers={"Content-Type": "application/json",
                                                 "Authorization": f"Bearer {key}"})
                if truncated:
                    # A half-read JSON document is malformed; parsing it would invent results.
                    raise FetchError(f"response exceeded {max_bytes} bytes; refusing to parse a "
                                     f"partial JSON document (raise --max-bytes to accept it)")
                results = parse_results(json.loads(text))
            except (FetchError, ValueError) as exc:
                failed += 1
                warnings.append(f"{stream}: {_scrub(str(exc), key)}")
                continue
            reached += 1

            known = set(seen.get(stream) or [])
            fresh = []
            for result in results:
                rid = result_id(result)
                if not rid or rid in known:
                    continue
                if len(new_items) + len(fresh) >= limit:
                    break
                fresh.append((rid, result))
            for rid, result in fresh:
                new_items.append({"id": safe_item_id(stream, rid), "stream": stream,
                                  "ts": iso_now(),
                                  "content": _render(result, query),
                                  "meta": {"url": rid, "query": query,
                                           "score": result.get("score")}})
            if fresh:
                seen[stream] = ([r for r, _x in fresh] + list(known))[:MAX_RESULTS * 20]
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
                            {"queries": reached, "failed": failed, "items": len(new_items)}, run_id)


def _scrub(message: str, key: str) -> str:
    """Never let the key reach a warning, a run record, or a terminal (I9).

    Providers echo the request URL in error messages, and a key-in-query provider would put the
    secret in ours. Cheap to strip; impossible to un-log.
    """
    return message.replace(key, "<redacted>") if key else message


register(WebSearchConnector())
