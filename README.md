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
isidore recertify --write         # re-run the oracles over unchanged prose (0 LLM calls)

isidore whatsnew --since v1.2.0   # verifiable changelog of the API-surface delta (0 LLM calls)
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
- `wiki/whatsnew/<since>..<until>.md` — a **changelog you can re-verify**, from `isidore whatsnew`
  (see below).

## What's new — novelty, not just topology

A module page tells you what something *is*. It cannot tell you what just *changed*: a new method is
one more symbol in a module that already has dozens, so nothing in the page prompt has reason to
mention it. `isidore whatsnew` closes that gap, and its first tier is free:

```bash
isidore whatsnew --since v1.5.1                 # 0 LLM calls: the typed API-surface delta
isidore whatsnew --since v1.5.1 --execute       # + prose, one call per changed module
```

The delta is computed by extracting the API surface of every changed file **from both git blobs**
(no checkout, no worktree) and diffing them symbol by symbol: `symbol_added`, `symbol_removed`,
`signature_changed`, `file_added`, `file_removed`, `file_renamed`. It descends into classes, so a
method added to an existing type — the usual shape of a new API — is reported by name, with its
signature and its `path:line`. Rows are grouped as `api` / `internal` / `tests` / `docs`, so the
product's surface leads and test churn does not bury it.

### One range, three readers

The same delta is written out for three audiences, because they need different things:

| Reader | Where | What they get |
|---|---|---|
| **Anyone** | `## In plain words`, at the top of the page | Whether anything they rely on broke, and what became possible — no paths, no identifiers, no jargon |
| **Developer** | the rest of the page | Per-module bullets with `path:line` citations, then every change with its signature |
| **Agent** | `<range>.toon` beside the page | The same rows as TOON tables — no prose to parse |

The plain-words section leads with a **zero-LLM impact answer** ("2 were taken away; anything built
on top may need updating") — derivable from the delta alone, since a removed or reshaped public
symbol is exactly what breaks a caller. The descriptive sentences come from the model, which is told
to write for someone who has never seen code and given an explicit list of banned words; a summary
that comes back with jargon in it anyway is **dropped, not shown**, and counted in the run summary.
Silence beats a "plain" summary a non-programmer still cannot read.

With `--execute`, the model receives **only that structured delta** (never a raw diff) plus commit
subjects marked explicitly as context-not-evidence, and writes under the same certificate discipline
as any page: claims anchored by content hash, verified against a deterministic oracle, and refuted
claims kept in the certificate but never published. Two properties keep it honest:

- **Removals are never written by the model.** "X was removed" cannot be anchored to the new tree —
  there is nothing to cite — so deletions are reported by the deterministic tier only.
- **Commit messages are never evidence.** They are a human's prose about the change; the code delta
  is the ground truth. If a hint contradicts the surface rows, the rows win.

`--execute` requires `--until` to be HEAD, because claims anchor to the working tree. The artifact
is a photograph of a range, so it stays out of the staleness loop that governs living pages.

## The pyramid — three levels, each resting on the one below

A module page is written for whoever is about to change that module. That is what it is for, and it
is why a tech lead, a manager or a customer cannot use it. Two more levels are compiled **from the
pages already certified below them**, so each step up inherits its truth instead of asserting
anything new:

```bash
isidore compile --execute         # N1: module pages (for whoever changes the code)
isidore subsystems --execute      # N2: area pages   (for whoever must understand an area)
isidore overview --execute        # N3: the product page (for anyone at all)
isidore llms                      # llms.txt: the whole thing indexed for agents (0 LLM)
```

`llms.txt` follows the [convention](https://llmstxt.org/) coding agents fetch when they need a
project's documentation: the product page becomes the summary, areas come before modules because
they orient, and anything an agent can skip when its context is short sits under the reserved
`## Optional` heading. It is a second index over files that already exist — deterministic, free, and
nothing extra to keep true.

Every sentence up here cites `wiki://<page>#<claim-id>`; the verdict comes from the cited page's
**certificate**, and each cited certificate is hashed into `child_cert_hashes`. Edit a module page
and the composition above it breaks — detectable with no model call at all. Run each level after the
one below; a page that can prove nothing is refused rather than published.

The middle level is what makes the top one honest. Without it the product page reaches straight down
to module claims, which verifies exactly as well and argues badly: *"the guide can be trusted"*
resting on a fact from a test module is a valid chain and a poor reason. An area page is where a
claim a product statement can lean on actually lives.

`isidore overview` is the level anyone can read:

It is built from the claims the module pages already **proved**, and its own sentences cite them as
`wiki://<page>#<claim-id>`. The verdict comes from the child page's certificate, so the overview
inherits its truth instead of asserting anything new, and each cited certificate is hashed into
`child_cert_hashes` — edit a module page and the composition breaks, with no model call needed to
notice.

Two refusals guard it, and both publish nothing rather than something misleading:

- **It must be readable.** The prose is checked against named plain-language rules (`plain.py`); the
  model gets one rewrite naming the rules it broke, and if it still writes for engineers the page is
  refused. Silence beats a "plain" page a non-programmer cannot use.
- **It must be provable.** A page whose statements cannot be traced to a proven fact is refused —
  fluent, plausible and unverifiable is exactly the artifact this tool exists to replace.

The gate deliberately carries **no readability score**. [ISO 24495-1:2023](https://www.iso.org/standard/78907.html)
judges plain language by whether the reader can find, understand and use the document, not by
mechanical formulas — and the formulas would mislead here: *"the daemon instantiates a mutex"* scores
as easy, while a longer, genuinely clearer sentence scores as hard.

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

### When a certificate falls behind the code

A page can be *more* right than its certificate. Improve an extractor and a claim it once recorded
FALSE now verifies TRUE: nothing the model wrote is wrong, only the record of what could be proved —
but `verify` fails the page all the same. That repair costs nothing, so it should never cost a call:

```bash
isidore recertify           # report which certificates the oracles can restate (0 LLM)
isidore recertify --write   # re-run them and rewrite the certificates; the prose is never touched
```

It refuses two cases on purpose, and both are honest refusals rather than silent repairs:

- **A published claim that is now FALSE.** A claim only reaches the prose once it verified TRUE, so
  this means a sentence a reader can see is contradicted by the code. Re-certifying would turn a
  wrong page green. `compile` treats exactly this as dirty — the page needs new prose, one call.
- **A page edited after compile.** The certificate describes different text; recertifying it would
  certify an edit no verifier ever read.

So every `verify` failure has an owner: free if the oracles moved, one call if the page is wrong.

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
