# isidore

**Compile an agent-oriented wiki from your codebase's structure graph — one bounded LLM call
per page, deterministic everything else.**

Named after Isidore of Seville, whose *Etymologiae* (~630 AD) compiled the knowledge of the
ancient world instead of re-deriving it.

## Why

Coding agents work better when they understand the repository. Existing doc agents solve this
by letting an LLM agent *crawl* your repo — a shell-equipped loop that decides what to read,
spawns subagents, and retries with bigger models. That loop is where all the money goes, and
none of its limits live in code.

isidore's bet: **if a structure graph already answers WHAT exists and WHERE, the wiki can be
compiled, not crawled.**

| stage | how | cost |
|---|---|---|
| Page planning | top modules from the graph | code, free |
| Context assembly | exact `file:line` excerpts + READMEs + git log | code, free |
| Prose | **one** bounded call per page, temperature 0 | 1 LLM call |
| Refresh | content-hash cache (make-style): unchanged context → | **0 calls** |
| Hallucination lint | every cited path checked against the repo | code, free |

Hard limits are code, not prompt suggestions: `--max-calls` per run (skips reported, never
silent), a per-prompt character budget (truncation reported), **one single model** (failure >
silent escalation to a pricier one), one timeout per call. No shell access, no subagents.

## Quickstart

```bash
pip install isidore-wiki

cd your-repo
isidore scan                      # build a structure graph — ANY language, zero dependencies
isidore compile                   # dry-run: shows the plan, 0 LLM calls

# point at ANY OpenAI-compatible endpoint — local server or hosted API
export ISIDORE_BASE_URL=http://localhost:11434/v1   # or an OpenAI/OpenRouter/vLLM/... URL
export ISIDORE_MODEL=<model-id-your-endpoint-exposes>
export ISIDORE_API_KEY=<token>                      # only if your endpoint needs one
isidore compile --execute         # compiles wiki/ (quickstart.md, module pages, index.toon)

isidore ask "how does the auth flow handle expired tokens?"   # one call, cited answer
isidore claims --check            # CI gate: exit 1 if any claim's evidence went stale (0 LLM calls)
```

Provider: any OpenAI-compatible endpoint via `ISIDORE_BASE_URL`, `ISIDORE_MODEL`, optional
`ISIDORE_API_KEY`. Isidore has no preferred provider; the default base URL is just the
conventional local-server port. A small or free-tier model is usually plenty — the prompt
already contains verified facts, so the model only writes prose.

## What you get

- `wiki/quickstart.md` — deterministic catalog (0 LLM calls), entry point for humans.
- `wiki/index.toon` — the same catalog in [TOON](https://github.com/toon-format/spec) tables:
  ~40% fewer tokens for agents to load.
- `wiki/<module>.md` — per-module pages: purpose, architecture, entry points, dependencies,
  how to change safely — with `path:line` citations that are mechanically verified.
- `wiki/flow-<name>.md` — cross-cutting flow pages ("how a request travels"), BFS-derived
  from seeds you declare in `isidore.json`. `isidore suggest-flows` prints candidates.
- `wiki/claims.toon` — the page's key facts as **evidence-anchored claims**: each is a single
  falsifiable statement bound to its `path:line` by a content hash of the cited lines. On every
  compile the hashes are re-checked with **zero LLM calls**, so a code change flags exactly the
  claims it invalidates and forces only their page to regenerate. `isidore claims --check` is a
  CI gate for documentation truth (exit 1 on any stale/orphan claim).
- `wiki/findings.toon` — **compilation residue**: since the model already read the excerpts,
  structured side-observations ride the same call at ~zero marginal cost — suspected bugs,
  doc/code drift, open questions (an *unverified triage queue*, never a report) — plus
  purely mechanical facts: TODO/FIXME harvest, orphan-file candidates, modules without test
  links, and risk hotspots (connection degree × git churn).
- A delimited, idempotent reference block in `AGENTS.md` pointing agents at the wiki.
- `wiki/<page>.md.cert.json` — a **re-verifiable certificate** for each page (see below).

## Proof-carrying prose — how to read a certified page

A model writes the prose, but it cannot *hide* a claim that the code contradicts. Each page ships a
certificate; every sentence carries one of three confidence levels:

- **green — proved.** The sentence rests on a *typed claim* the compiler checked against the code
  with zero LLM calls: `calls(a,b)`, `defines(file,sym)`, `imports(file,tgt)`, `value(name,literal)`,
  `signature(fn,args)`, `env(NAME)`. A green claim is TRUE against the current graph/AST.
- **yellow — anchored.** Cited to a real `path:line` (content-hashed) but not a decidable predicate.
  Its evidence exists; its meaning isn't machine-proved.
- **gray — narrative.** No citation: design rationale, judgement, opinion. Honestly un-load-bearing —
  the certificate never dresses it up as fact.

The certificate also records deterministic **security marks** (high-entropy secrets, dangerous sinks,
auth-reachable surface — 0 LLM) and a hash of the prose. Two guarantees follow:

- **Tamper-evident.** Edit a published page and `isidore verify` fails — the prose no longer matches
  its hash. A monotonic-escalation rule means a danger mark forces a loud banner the prose can't lower.
- **Offline & free.** `isidore verify` re-checks every claim and certificate with **no LLM calls**.

```bash
isidore verify                          # re-verify all pages offline (0 LLM); nonzero on tamper/FALSE
isidore verify --min-verified-mass 0.3  # CI gate: fail if <30% of sentences are green (proved)
isidore verify --fail-on-marks          # CI gate: fail on any unresolved danger-severity mark
isidore verify --contracts              # CI gate: fail if a promoted claim->contract is now FALSE
isidore contracts --promote <claim-id>  # graduate a proved claim to a CI-enforced invariant
```

The gates are **opt-in** (off by default). A ready-to-copy pre-commit / CI step:

```yaml
# .github/workflows/docs.yml (or a pre-commit hook)
- run: isidore claims --check                       # evidence still anchored (0 LLM)
- run: isidore verify --contracts --fail-on-marks   # certificates intact, invariants hold (0 LLM)
```

## Languages

`isidore scan` is **multi-language and zero-dependency** — no tree-sitter, no native wheels, no
external binary, so it runs anywhere Python does (including ARM Linux). One engine, driven by a
declarative table (`langspec.py`); adding a language is adding a row. Three honest tiers:

- **Python** — exact parse via the stdlib `ast` (functions, classes, imports, precise spans).
- **JS/TS, Java, Kotlin, Scala, Groovy, C, C++, C#, Go, Rust, Swift, PHP, Ruby, shell, Lua,
  Elixir, …** — top-level and one-level-nested symbols (functions, methods, types) with line
  spans, via a comment/string-sanitized, brace-depth-tracked scan.
- **Any other text file** — a bare file node, so it still appears in its module page.

It is intentionally structural, not a compiler: false positives are possible and tolerated. For
precise cross-language symbols and real call graphs, bring your own graph (below).

## Bring your own graph

For anything richer than the built-in scanner (precise call graphs, semantic edges), point
`--graph` at a JSON file in this tool-agnostic shape — extra fields are ignored, so existing
graph producers (e.g. Graphify) work as-is:

```json
{
  "nodes": [{"id": "pkg_mod_fn", "label": "fn()", "file_type": "code",
             "source_file": "pkg/mod.py", "source_location": "L42"}],
  "links": [{"source": "pkg_mod_fn", "target": "other_id", "relation": "calls"}],
  "built_at_commit": "abc123"
}
```

`file_type`: `code` | `document` | anything else. `source_location`: `L<line>`, 1-based.
By default isidore uses its own `.isidore/graph.json` (from `scan`), then falls back to a
`graphify-out/graph.json` if present. Any producer emitting the format above works via `--graph`.

## Config (`isidore.json`, optional)

```json
{
  "top_k": 24,
  "min_symbols": 10,
  "max_calls": 12,
  "flows": [
    {"name": "grant-issue", "seeds": ["grants.py", "cmd_grant"]}
  ]
}
```

CLI flags override config; config overrides defaults.

## Design rules

1. **Compile, don't crawl.** The LLM never decides what to read; the graph already knows.
2. **The no-op is actually free.** Unchanged context hash → zero calls, zero writes.
3. **No silent anything.** Caps, truncations and skips are always reported.
4. **Fail closed.** No model fallback, no retry-with-bigger-model. If the provider fails,
   the run fails.
5. **Trust nothing generated.** Cited paths are lint-checked mechanically; model
   side-observations are quarantined in `findings.toon` as unverified.

## License

MIT © Gred In Labs
