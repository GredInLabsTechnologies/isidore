"""Plain-language gate: can a reader who has never seen code use this sentence?

Documentation that only a programmer can read serves only programmers, and most of the people
affected by a release are not programmers. Isidore's answer is a layer written for them — but a
generated "plain" summary that still says "the method's parameter is now optional" is worse than no
summary at all, because it looks like an answer and isn't. So the layer needs a gate.

**Why this gate does NOT score readability.** ISO 24495-1:2023, the plain-language standard, is
explicit that plain language is judged by whether the reader can find, understand and use the
document — NOT by mechanical readability formulas (Flesch-Kincaid and its relatives). Those formulas
measure word and sentence length, so "the daemon instantiates a mutex" scores as *easy* while a
longer, genuinely clearer sentence scores as *hard*. Scoring is the obvious idea here and it is the
wrong one; do not add it back.

**What it does instead** is what a prose linter does — Vale's model, where every check is a NAMED
rule of a declared kind rather than one opaque pattern. A named rule can be reported ("rejected by
`identifier`"), argued with, and extended, and the run summary can say which rule fires most often.
The vocabulary rule carries the words that betray writing aimed at engineers; the structural rules
carry the shapes — identifiers, file names, line references, code punctuation — that no sentence
written for a general reader ever contains.

The gate is deliberately one-sided: it can prove a sentence is NOT plain, never that it is. It is a
floor under the prompt, not a substitute for it — the prompt is what does the real work, and this
catches what slips through. When it fires, the caller drops the sentence rather than publishing it
with a warning a reader would have to decode.
"""
from __future__ import annotations

import re
from dataclasses import dataclass

# Words that mean "this was written for someone who builds software". Kept as a vocabulary list (a
# Vale `existence` rule over a term set) rather than folded into the structural patterns, because
# this is the part a team will want to tune per product — a database company may legitimately need
# "schema" in plain prose, and this is the one knob to turn.
JARGON_TERMS = (
    "method", "methods", "class", "classes", "function", "functions", "parameter", "parameters",
    "argument", "arguments", "api", "apis", "endpoint", "endpoints", "payload", "payloads",
    "constant", "constants", "variable", "variables", "module", "modules", "library", "libraries",
    "daemon", "daemons", "addon", "addons", "binary", "binaries", "runtime", "runtimes",
    "protocol", "protocols", "schema", "schemas", "snapshot", "snapshots", "interface",
    "interfaces", "struct", "callback", "callbacks", "async", "repository", "repositories",
    "refactor", "mutex", "boolean", "instantiate", "instantiates", "instantiated",
    "serialise", "serialize", "deserialise", "deserialize",
    # Added after a live overview passed the gate and still opened with "isidore compiles a
    # structured wiki from your codebase, so agents can understand it" — every one of these reads as
    # plain English to whoever wrote it and means nothing to the reader it was written for.
    "llm", "llms", "codebase", "codebases", "repo", "repos", "agent", "agents", "token", "tokens",
    "graph", "parse", "parses", "parsing", "compile", "compiles", "compiler", "crawl", "crawls",
    "crawling", "syntax", "metadata", "backend", "frontend", "middleware", "config",
)


@dataclass(frozen=True)
class PlainRule:
    """One named check. `kind` mirrors Vale's rule taxonomy so the intent of each is declared."""
    name: str
    kind: str            # "vocabulary" | "structure"
    pattern: re.Pattern
    why: str


def _vocabulary(terms: tuple[str, ...]) -> re.Pattern:
    return re.compile(r"(?i:\b(?:" + "|".join(sorted(terms, key=len, reverse=True)) + r")\b)")


# NOTE on the case-insensitive flag: it is SCOPED to the vocabulary rule. Applying `(?i)` across the
# whole set would turn the camelCase pattern `[a-z][A-Z]` into "any two letters", which rejects every
# sentence ever written — a bug this gate actually shipped with until a live run exposed it.
RULES: tuple[PlainRule, ...] = (
    PlainRule("jargon-term", "vocabulary", _vocabulary(JARGON_TERMS),
              "a word that only means something to someone who builds software"),
    PlainRule("snake-case", "structure", re.compile(r"[A-Za-z]+_[a-z]"),
              "an identifier copied out of the code"),
    PlainRule("camel-case", "structure", re.compile(r"[a-z][A-Z]"),
              "an identifier copied out of the code"),
    PlainRule("file-name", "structure",
              re.compile(r"[\w/]+\.(?:py|ts|js|go|rs|java|rb|md|json|toml|yaml|yml|rs|c|h|cpp)\b"),
              "a file name — a reader who does not open files cannot use it"),
    PlainRule("line-reference", "structure", re.compile(r":\d+\b"),
              "a line reference, which belongs in the developer layer"),
    PlainRule("code-syntax", "structure", re.compile(r"[{}]|\(\)|=>|::"),
              "punctuation that only appears in code"),
)


def check(text: str) -> list[str]:
    """Names of every rule the text breaks. Empty list = nothing disqualifying was found.

    One-sided by design: an empty list does NOT certify the text is plain, it only means this gate
    found nothing wrong. The prompt is what makes prose plain; this stops the worst from shipping.
    """
    return [rule.name for rule in RULES if rule.pattern.search(text or "")]


def is_plain(text: str) -> bool:
    return not check(text)


def explain(names: list[str]) -> str:
    """Human-readable reason for a rejection, for the run summary and the journal."""
    reasons = {rule.name: rule.why for rule in RULES}
    return "; ".join(f"{name} ({reasons.get(name, '?')})" for name in names)


__all__ = ["JARGON_TERMS", "RULES", "PlainRule", "check", "explain", "is_plain"]
