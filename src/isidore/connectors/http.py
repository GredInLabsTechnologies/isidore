"""Bounded HTTP for the direct-API connectors (ADR-0032 F4). stdlib urllib, no dependencies.

Every network read in Isidore goes through here, and it is only ever reached from `ingest`
(invariant I7). The caps are in code, never in a prompt (I2), and a response that is not a 200 with
a parseable body is an ERROR that leaves the connector's state untouched (I6) — never a partial
success that silently advances a cursor past items nobody read.
"""
from __future__ import annotations

import json
import urllib.error
import urllib.request
from urllib.parse import urlsplit

USER_AGENT = "isidore-knowledge/1.1 (+https://github.com/GredInLabsTechnologies/isidore)"
DEFAULT_TIMEOUT = 20
DEFAULT_MAX_BYTES = 2_000_000        # a feed larger than this is truncated, and SAID to be
ALLOWED_SCHEMES = ("http", "https")


class FetchError(Exception):
    """A fetch that did not produce a usable body. Carries a reason fit to show a user."""


def _check_url(url: str) -> None:
    """Refuse anything that is not plain http(s).

    urllib will happily open `file://` and `ftp://`, and a configured URL is not necessarily one the
    user typed — it can arrive from a redirect. A connector reading the local filesystem through what
    looks like a feed is not a feature.
    """
    parts = urlsplit(url)
    if parts.scheme not in ALLOWED_SCHEMES:
        raise FetchError(f"refusing non-http(s) URL scheme {parts.scheme!r}")
    if not parts.netloc:
        raise FetchError(f"URL has no host: {url!r}")


def fetch(url: str, *, timeout: int = DEFAULT_TIMEOUT, max_bytes: int = DEFAULT_MAX_BYTES,
          headers: dict[str, str] | None = None, data: bytes | None = None) -> tuple[str, bool]:
    """GET (or POST when `data` is given) -> (text, truncated). Raises FetchError on anything else.

    `truncated` is returned rather than logged so the caller can put it in an IngestResult warning:
    a body cut at the cap must reach the user as a fact, not vanish.
    """
    _check_url(url)
    req = urllib.request.Request(url, data=data, method="POST" if data else "GET")
    req.add_header("User-Agent", USER_AGENT)
    req.add_header("Accept-Encoding", "identity")   # no gzip: the byte cap must mean bytes of body
    for key, value in (headers or {}).items():
        req.add_header(key, value)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:   # noqa: S310 - scheme checked
            _check_url(resp.geturl())                # a redirect must not escape http(s) either
            if resp.status != 200:
                raise FetchError(f"HTTP {resp.status} from {url}")
            raw = resp.read(max_bytes + 1)
    except urllib.error.HTTPError as exc:
        raise FetchError(f"HTTP {exc.code} from {url}") from exc
    except urllib.error.URLError as exc:
        raise FetchError(f"could not reach {url}: {exc.reason}") from exc
    except (TimeoutError, OSError) as exc:
        raise FetchError(f"could not reach {url}: {exc}") from exc

    truncated = len(raw) > max_bytes
    if truncated:
        raw = raw[:max_bytes]
    return raw.decode("utf-8", errors="replace"), truncated


def fetch_json(url: str, **kwargs) -> tuple[object, bool]:
    """`fetch` + strict JSON parse. A truncated body is NOT parsed: half a document is malformed, and
    guessing at it is how a connector reports success for data it never received (I6)."""
    text, truncated = fetch(url, **kwargs)
    if truncated:
        raise FetchError(f"response from {url} exceeded the byte cap; refusing to parse a partial "
                         f"JSON document (raise --max-bytes to accept it)")
    try:
        return json.loads(text), truncated
    except ValueError as exc:
        raise FetchError(f"malformed JSON from {url}: {exc}") from exc


__all__ = ["DEFAULT_MAX_BYTES", "DEFAULT_TIMEOUT", "FetchError", "USER_AGENT", "fetch", "fetch_json"]
