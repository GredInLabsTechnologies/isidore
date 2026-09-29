"""Incremental page updates: change only what changed, keep the rest byte for byte.

Before this, a page was "dirty" when the sha256 of its WHOLE prompt moved, and a dirty page was
rewritten from nothing by a prompt that did not even contain the previous version. The prompt carries
things that say nothing about what the page should say — the module's `git log`, link COUNTS and
symbol degrees, and the prompt template itself — so a commit that fixed a comment, a new test that
imported the module, or an upgrade of isidore re-wrote whole pages. Measured on isidore's own wiki:
5 to 12 of 40 pages rewritten per commit, one page seven times in fifteen runs.

Two separate decisions, two separate fixes:

- WHETHER a page changed is decided by a semantic fingerprint (`facts_record`): the dependency SETS,
  the symbol inventory, and a hash of each source excerpt's CODE (not its line numbers). No git log,
  no counts, no template. A line shift, a new caller elsewhere, a new commit message: not a change.
- WHAT is rewritten is only the affected sections. A dirty page that already exists gets a revision
  prompt — its current text plus the DELTA of facts — and the model returns only the `##` sections
  that must change (or NO-CHANGES). `splice` replaces those and keeps every other section verbatim.
  Claims whose anchored line is still there are carried over at 0 LLM (`carry_claims`); the model
  adds claims only for what is new. The result then goes through the ordinary pipeline: lint,
  quarantine, anchoring, certificate — a revised page earns no more trust than a fresh one.

`--rewrite` (compile/handoff) restores the full regeneration when that is what is wanted.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

NO_CHANGES = "NO-CHANGES"
MODE_FULL = "full"
MODE_REVISE = "revise"

_EXCERPT_LINE = re.compile(r"^\d+: ", re.M)
_H2 = re.compile(r"^## +(.+?)\s*$")


def _h(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def _excerpt_code(excerpt: str) -> str:
    """An excerpt's code without its header and line-number gutter: what the page is ABOUT, so
    lines inserted above the symbol do not count as a change to it."""
    body = excerpt.split("\n", 1)[1] if excerpt.startswith("--- excerpt ") else excerpt
    return _EXCERPT_LINE.sub("", body)


def facts_record(repo: Path, spec, read_excerpt) -> dict:
    """The facts a page's CONTENT depends on, in a comparable shape. `read_excerpt` is injected so
    this module stays independent of pipeline.py (which imports it)."""
    rec: dict = {"kind": spec.kind, "name": spec.name}
    if spec.kind == "flow":
        rec["modules"] = sorted(spec.modules)
        rec["edges"] = sorted(f"{a} --{rel}--> {b}" for a, rel, b in spec.flow_edges)
    else:
        rec["files"] = spec.files
        rec["symbols"] = spec.symbols
        rec["deps_out"] = sorted(m for m, _c in spec.deps_out)
        rec["deps_in"] = sorted(m for m, _c in spec.deps_in)
        docs = {}
        for doc in spec.doc_files:
            path = repo / doc
            if path.is_file():
                head = "\n".join(path.read_text(encoding="utf-8", errors="replace").splitlines()[:150])
                docs[doc] = _h(head)
        rec["docs"] = docs
    excerpts = {}
    for label, f, loc, _deg in spec.hot_symbols:
        text = read_excerpt(repo, f, loc)
        if text:
            excerpts[f"{f}::{label}"] = _h(_excerpt_code(text))
    rec["excerpts"] = excerpts
    return rec


# Kept in the record (a revision shows them) but never a reason on their own to call the model:
# - the COUNTS: a new test function that is not among the page's excerpts moved `symbols`, gave the
#   model nothing to document, and bought a NO-CHANGES reply — found on the first real incremental run;
# - who depends on this module (`deps_in`): a new consumer does not change what the module does, it is
#   documented on the consumer's own page — and the list is the top few by link count, so one new
#   consumer pushed another off it and a module nobody touched came back "changed".
_NOT_A_CHANGE = frozenset({"files", "symbols", "deps_in"})


def facts_fingerprint(record: dict) -> str:
    """Identity of what a page describes. ALWAYS compared by recomputing it from both stored and
    current records with THIS rule: a change to the rule then never dirties every page at once, which
    is the very stampede this module exists to end."""
    kept = {k: v for k, v in record.items() if k not in _NOT_A_CHANGE}
    return hashlib.sha256(json.dumps(kept, sort_keys=True).encode("utf-8")).hexdigest()


def facts_delta(old: dict, new: dict, repo: Path, spec, read_excerpt) -> str:
    """What changed between two fact records, as FACTS the model can cite: new excerpts are given in
    full (with line numbers), removals are named. Empty string when nothing semantic changed."""
    out: list[str] = []

    def _set_change(key: str, label: str) -> None:
        before, after = set(old.get(key, [])), set(new.get(key, []))
        if after - before:
            out.append(f"{label} — added: " + ", ".join(sorted(after - before)))
        if before - after:
            out.append(f"{label} — removed: " + ", ".join(sorted(before - after)))

    for key in ("files", "symbols"):
        if old.get(key) != new.get(key):
            out.append(f"{key} count: {old.get(key)} -> {new.get(key)}")
    _set_change("deps_out", "depends on")
    _set_change("deps_in", "depended on by")
    _set_change("modules", "modules involved")
    _set_change("edges", "graph edges")
    old_docs, new_docs = old.get("docs", {}), new.get("docs", {})
    for doc in sorted(set(old_docs) | set(new_docs)):
        if old_docs.get(doc) != new_docs.get(doc):
            path = repo / doc
            if doc in new_docs and path.is_file():
                head = "\n".join(path.read_text(encoding="utf-8", errors="replace").splitlines()[:150])
                out.append(f"--- doc {doc} (changed; first lines) ---\n{head}")
            else:
                out.append(f"doc removed: {doc}")
    old_ex, new_ex = old.get("excerpts", {}), new.get("excerpts", {})
    removed = sorted(set(old_ex) - set(new_ex))
    if removed:
        out.append("symbols no longer among this page's evidence: "
                   + ", ".join(k.replace("::", " ") for k in removed))
    by_key = {f"{f}::{label}": (f, loc) for label, f, loc, _d in spec.hot_symbols}
    for key in sorted(new_ex):
        if old_ex.get(key) == new_ex[key]:
            continue
        f, loc = by_key[key]
        tag = "NEW symbol" if key not in old_ex else "CHANGED code"
        out.append(f"{tag}: {key.replace('::', ' ')}\n{read_excerpt(repo, f, loc)}")
    return "\n\n".join(out)


REVISE_PROMPT = """You are UPDATING one existing page of an internal wiki that coding agents read before
touching a repository. The page is about the {kind} `{name}`. Below is the CURRENT PAGE, followed by
{what}. Most of the page is still right: change only what the facts below make wrong or incomplete.

How to answer:
- Return ONLY the sections that must change, each as a complete section starting with its `## `
  heading copied EXACTLY from the current page. A returned section replaces the old one entirely;
  every section you do not return is kept word for word.
- Keep the voice, structure and level of detail of the current page. Do not rewrite a section just
  to rephrase it.
- If nothing in the page needs to change, reply with exactly {no_changes} and nothing else (you may
  still append the blocks described below).
- Cite sources inline as `path:line` using ONLY paths that appear in the current page or the facts.
- Describe only what IS evidenced. NEVER state that something does not exist, is not used, or is
  not handled — the facts are excerpts, not the whole repo.
- No preamble, no closing remarks.

CURRENT PAGE
============
{page}

{facts_title}
{underline}
{facts}
"""

REVISE_CLAIMS_OVERRIDE = """
FOR THIS UPDATE the claims block holds ONLY NEW claims — about what the facts above changed (0-5
claims; omit the block if there are none). The page's existing claims are carried over and
re-verified mechanically; do not repeat them.
"""


def revise_prompt(spec, old_page: str, facts: str, *, delta: bool, addenda: str) -> str:
    title = "WHAT CHANGED IN THE FACTS" if delta else "CURRENT FACTS (the page predates change tracking)"
    what = ("only the facts that CHANGED since it was written" if delta
            else "the current facts it must agree with")
    return (REVISE_PROMPT.format(kind=spec.kind, name=spec.name, what=what, no_changes=NO_CHANGES,
                                 page=old_page.strip(), facts_title=title,
                                 underline="=" * len(title), facts=facts.strip())
            + addenda + REVISE_CLAIMS_OVERRIDE)


# ------------------------------------------------------------------ splice

def strip_security_banner(markdown: str) -> str:
    """Drop the deterministic SECURITY banner the pipeline prepends; it is rebuilt on every write,
    and keeping the old one would stack a second banner on top of it."""
    lines = markdown.split("\n")
    for i, line in enumerate(lines):
        if line.startswith("> [!WARNING]"):
            j = i
            while j < len(lines) and lines[j].startswith(">"):
                j += 1
            if j < len(lines) and not lines[j].strip():
                j += 1
            return "\n".join(lines[:i] + lines[j:])
        if line.startswith("## "):
            break
    return markdown


def _sections(markdown: str) -> tuple[str, list[tuple[str, str]]]:
    """(preamble, [(heading title, full section text)]) split on `## ` headings."""
    preamble: list[str] = []
    sections: list[tuple[str, list[str]]] = []
    for line in markdown.split("\n"):
        m = _H2.match(line)
        if m:
            sections.append((m.group(1), [line]))
        elif sections:
            sections[-1][1].append(line)
        else:
            preamble.append(line)
    return "\n".join(preamble), [(t, "\n".join(body).rstrip()) for t, body in sections]


def splice(old_page: str, reply: str) -> tuple[str, list[str]] | None:
    """Apply a revision reply to the old page. Returns (new page, titles of replaced/added sections),
    or None when the reply is neither NO-CHANGES nor a set of `##` sections (unusable: the caller keeps
    the page dirty rather than guess)."""
    text = reply.strip()
    if text == NO_CHANGES or text.startswith(NO_CHANGES + "\n"):
        return old_page, []
    _pre, new_secs = _sections(text)
    if not new_secs:
        return None
    old_pre, old_secs = _sections(old_page.strip("\n"))
    replacements = dict(new_secs)
    changed: list[str] = []
    merged: list[str] = []
    for title, body in old_secs:
        if title in replacements:
            merged.append(replacements.pop(title))
            changed.append(title)
        else:
            merged.append(body)
    for title, body in new_secs:                  # sections the page did not have, in reply order
        if title in replacements:
            merged.append(body)
            changed.append(title)
    head = old_pre.strip("\n")
    return (head + "\n\n" if head else "") + "\n\n".join(merged) + "\n", changed


def carry_claims(repo: Path, old_claims: list[dict]) -> list[dict]:
    """The previous compile's claims whose anchored content is still in place, re-pointed at where it
    moved. A claim about changed code is NOT carried: the model is asked for new claims instead."""
    from .claims import relocate_evidence
    rows: list[dict] = []
    for c in old_claims:
        if c.get("verdict") == "FALSE" or not c.get("ehash") or not c.get("evidence"):
            continue
        evidence = relocate_evidence(repo, c["evidence"], c["ehash"])
        if evidence is None:
            continue
        row = {"statement": c["statement"], "evidence": evidence}
        if c.get("id"):
            # Identity survives relocation: `wiki://page#<id>` chains above point at this id.
            # Found when the first real incremental run broke subsystem-src.md's chain to a claim
            # whose line had merely shifted by two.
            row["id"] = c["id"]
        if c.get("predicate"):
            row["predicate"] = c["predicate"]
        rows.append(row)
    return rows
