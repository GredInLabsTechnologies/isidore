## Purpose

`src/isidore/plain.py` is the plain-language gate: it answers whether a reader who has never seen code can use a sentence (`src/isidore/plain.py:1`). Isidore writes a layer for people who are not programmers, and a "plain" summary that still says "the method's parameter is now optional" is worse than none, because it looks like an answer and isn't — so that layer needs a gate (`src/isidore/plain.py:3-L6`).

The gate deliberately does not score readability. ISO 24495-1:2023 judges plain language by whether a reader can find, understand and use a document, not by readability formulas, which rate "the daemon instantiates a mutex" as easy (`src/isidore/plain.py:8-L13`). Instead it works like a prose linter: every check is a named rule of a declared kind, so a rejection can be reported, argued with and extended (`src/isidore/plain.py:15-L20`).

## Architecture

- **Rules.** `PlainRule` is one named check with a `kind` — `vocabulary` or `structure` — a pattern and a reason (`src/isidore/plain.py:66-L71`). `RULES` holds them: `jargon-term` for engineer vocabulary, and structural rules for `snake-case`, `camel-case`, file names, line references and code punctuation (`src/isidore/plain.py:81-L95`).
- **Vocabulary.** `_vocabulary` compiles the jargon list case-insensitively, longest term first (`src/isidore/plain.py:74-L75`). The list grew from real failures: a live overview passed the gate while opening with "compiles a structured wiki from your codebase, so agents can understand it" (`src/isidore/plain.py:45-L50`). Case-insensitivity is scoped to this one rule; applied to the whole set, the camel-case pattern would match any two letters and reject every sentence — a bug the gate shipped with until a live run exposed it (`src/isidore/plain.py:78-L80`).
- **Accepted terms.** `ACCEPTED_TERMS` (GitHub, JavaScript, iPhone, …) are removed before the structural rules run, because the camel-case pattern would otherwise flag ordinary words (`src/isidore/plain.py:54-L62`).
- **Checking.** `check` strips accepted terms and returns the names of every rule the text breaks (`src/isidore/plain.py:98-L105`); `is_plain` is its negation (`src/isidore/plain.py:108-L109`); `explain` turns rule names into a readable reason for the run summary and the journal (`src/isidore/plain.py:112-L115`).

The gate is one-sided: it can prove a sentence is not plain, never that it is. It is a floor under the prompt, and when it fires the caller drops the sentence rather than publishing it with a warning (`src/isidore/plain.py:22-L25`, `src/isidore/plain.py:101-L102`).

## Key entry points

- `check(text)` — names of the rules broken; empty means nothing disqualifying was found (`src/isidore/plain.py:98`).
- `is_plain(text)` — the boolean form (`src/isidore/plain.py:108`).
- `explain(names)` — the reason, for humans (`src/isidore/plain.py:112`).
- `RULES`, `PlainRule`, `JARGON_TERMS` — the rule set itself (`src/isidore/plain.py:118`).

## Dependencies

It imports nothing from the rest of Isidore. It is used by `src/isidore/pyramid.py` (the product overview) and `src/isidore/whatsnew.py`, and tested by `tests/test_plain.py`.

## How to change safely

1. Do not add a readability score; the module explains why it is the wrong tool (`src/isidore/plain.py:12-L13`).
2. Add a failure as a named rule or a vocabulary term, never as an anonymous pattern, so rejections stay explainable.
3. Keep case-insensitivity scoped to the vocabulary rule (`src/isidore/plain.py:78-L80`).
4. When a structural rule catches an ordinary word, add it to `ACCEPTED_TERMS` rather than weakening the rule.
