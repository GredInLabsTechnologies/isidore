"""Lane D — the pyramid: hierarchical synthesis with wiki:// claim chains. (T-af65 / fixed in T-5726)

Levels: N1 module pages (exist today) -> N2 subsystem pages compiled FROM N1 pages+claims -> N3
product manual citing N2. A higher-level claim cites `wiki://<page>#<claim-id>` IN ITS EVIDENCE
field; the verifier registered here checks the cited claim exists, is non-stale, and is TRUE — its
truth comes from the cited page's CERTIFICATE (the verdict lives there, not in pages_state). Certs
compose, so the manual has integrity rooted down to the code lines. Staleness propagates UPWARD, 0 LLM.

Original lane-D draft (chatgpt) was returned in review: the auto-seed read node['path'/'file'/'name']
(fields the isidore graph doesn't have — it uses 'source_file'), ignored `links`, and the wikichain
crashed on None. Rewritten by claude-agora with those three fixed + tests.
"""
from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path
from pathlib import PurePosixPath

from .pcp import (
    FALSE,
    ORACLE_WIKI,
    TRUE,
    WIKI_SCHEME,
    WIKI_VERIFIER_KIND,
    Predicate,
    Verdict,
    VerifyContext,
    parse_wiki_uri,
    register_verifier,
    undecidable,
)


# ---------------------------------------------------------------- wiki:// chain verifier


def _claim_verdict(ctx: VerifyContext, page: str, claim_id: str) -> tuple[str, str] | None:
    """Resolve (verdict, state) for a cited claim. Truth comes from the page's certificate; fall back
    to pages_state if the pipeline populated verdicts there. Returns None if the claim isn't found."""
    # 1) the certificate is the source of truth for a claim's verdict
    from .pcp import CERT_SUFFIX, read_certificate
    from .pipeline import WIKI_DIRNAME
    cert_path = ctx.repo / WIKI_DIRNAME / (page + CERT_SUFFIX)
    if cert_path.is_file():
        try:
            cert = read_certificate(cert_path)
        except ValueError:
            cert = None
        if cert is not None:
            for cv in cert.claims:
                if cv.id == claim_id:
                    return cv.verdict, "ok"
    # 2) fall back to pages_state (its claims may carry a verdict/state once the pipeline wires it)
    entry = ctx.pages_state.get(page)
    if isinstance(entry, dict):
        raw = entry.get("claims", [])
        if isinstance(raw, dict):
            raw = [dict(v, id=k) for k, v in raw.items()]
        for claim in raw:
            if claim.get("id") == claim_id:
                state = claim.get("state", entry.get("state", "ok"))
                verdict = claim.get("verdict", claim.get("value", ""))
                return verdict or "", "stale" if claim.get("stale") else state
    return None


def _wikichain_verifier(predicate: Predicate | None, ctx: VerifyContext) -> Verdict:
    """Resolve a wiki:// chain. Fail-closed: None/invalid/missing -> not TRUE, never crashes."""
    if predicate is None or len(predicate.args) != 1:
        return undecidable("wikichain expects one wiki:// URI")
    parsed = parse_wiki_uri(predicate.args[0])
    if parsed is None:
        return Verdict(FALSE, ORACLE_WIKI, "invalid wiki:// URI")
    page, claim_id = parsed
    found = _claim_verdict(ctx, page, claim_id)
    if found is None:
        return Verdict(FALSE, ORACLE_WIKI, f"cited claim not found: {page}#{claim_id}")  # quarantine
    verdict, state = found
    if state != "ok":
        return Verdict(FALSE, ORACLE_WIKI, f"cited claim is stale ({state})")
    if verdict == TRUE:
        return Verdict(TRUE, ORACLE_WIKI, "cited claim proved TRUE")
    if verdict == FALSE:
        return Verdict(FALSE, ORACLE_WIKI, "cited claim is FALSE")
    return undecidable("cited claim has no TRUE verdict")


register_verifier(WIKI_VERIFIER_KIND, _wikichain_verifier)


# ---------------------------------------------------------------- deterministic planning


def _top_dir(source_file: str) -> str:
    parts = PurePosixPath(source_file.replace("\\", "/")).parts
    return parts[0] if parts else source_file


def _seed_subsystems(nodes: list[dict], links: list[dict]) -> list[dict]:
    """0-LLM subsystem suggester: group files by top directory (the isidore graph uses `source_file`),
    then use the `imports` edges to record inter-subsystem dependencies (cohesion signal for N3)."""
    groups: dict[str, set[str]] = defaultdict(set)
    file_to_sub: dict[str, str] = {}
    for n in nodes:
        sf = n.get("source_file")
        if sf:
            sub = _top_dir(sf)
            groups[sub].add(_norm(sf))
            file_to_sub[_norm(sf)] = sub
    # map graph node ids -> subsystem, so imports edges can be attributed to subsystems
    id_to_sub = {n["id"]: file_to_sub.get(_norm(n.get("source_file", "")))
                 for n in nodes if n.get("id") and n.get("source_file")}
    deps: dict[str, set[str]] = defaultdict(set)
    for link in links:
        if link.get("relation") != "imports":
            continue
        a, b = id_to_sub.get(link.get("source")), id_to_sub.get(link.get("target"))
        if a and b and a != b:
            deps[a].add(b)
    return [{"name": sub, "modules": sorted(files), "globs": [f"{sub}/**"],
             "depends_on": sorted(deps.get(sub, set()))}
            for sub, files in sorted(groups.items())]


def _norm(path: str) -> str:
    return path.replace("\\", "/").lstrip("./")


def plan_pyramid(nodes: list[dict], links: list[dict], config: dict) -> list[dict]:
    """Plan deterministic N2 subsystem + N3 product pages. 0 LLM.

    Explicit `pyramid.subsystems` config is authoritative; absent, subsystems are seeded from the
    graph by top directory of `source_file`, with `imports` edges giving inter-subsystem deps.
    """
    pyramid = config.get("pyramid", config) if isinstance(config, dict) else {}
    subsystems = pyramid.get("subsystems", []) or _seed_subsystems(nodes, links)
    specs: list[dict] = []
    for item in subsystems:
        specs.append({"level": 2, "name": item.get("name", "subsystem"), "kind": "subsystem",
                      "modules": list(item.get("modules", [])),
                      "globs": list(item.get("globs", [])),
                      "depends_on": list(item.get("depends_on", [])),
                      "sources": sorted(set(item.get("modules", [])))})
    for item in pyramid.get("product_pages", []):
        refs = list(item.get("subsystems", [s["name"] for s in specs]))
        specs.append({"level": 3, "name": item.get("name", "overview"),
                      "kind": item.get("kind", "overview"), "subsystems": refs, "sources": refs})
    return specs


# ---------------------------------------------------------------- N2: subsystem pages

SUBSYSTEM_PREFIX = "subsystem-"

# A subsystem page is a page about an AREA, so it is bounded by how much of an area a reader can hold
# at once, not by how much material exists.
_MAX_SUBSYSTEM_CLAIMS = 24
_MAX_SUBSYSTEM_PAGES = 20


def subsystem_page_name(name: str) -> str:
    slug = name.replace("/", "-").replace("\\", "-").replace(".", "_").replace(" ", "-")
    return f"{SUBSYSTEM_PREFIX}{slug}.md"


def _module_pages_of(repo: Path, subsystem: str) -> dict[str, dict]:
    """The compiled module pages that belong to one subsystem, keyed by page file name."""
    from .pipeline import load_state
    from .render import WIKI_DIRNAME

    state = load_state(repo / WIKI_DIRNAME)
    return {page: entry for page, entry in (state.get("pages") or {}).items()
            if isinstance(entry, dict) and entry.get("kind") == "module"
            and _top_dir(entry.get("name", "")) == subsystem}


def _page_purpose(repo: Path, page: str) -> str:
    """The first sentence of a module page's `## Purpose` — what that module says it is FOR."""
    from .render import WIKI_DIRNAME

    path = repo / WIKI_DIRNAME / page
    if not path.is_file():
        return ""
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    for index, line in enumerate(lines):
        if line.strip().lower().startswith("## purpose"):
            for body in lines[index + 1:]:
                if body.strip() and not body.startswith("#"):
                    return body.strip().split(". ")[0].rstrip(".") + "."
            break
    return ""


def subsystem_facts(repo: Path, spec: dict) -> dict:
    """What one subsystem page is written from: its module pages, what each says it is FOR, and the
    claims they PROVED. 0 LLM.

    The purposes matter as much as the claims. A proven claim is a narrow fact — "this file defines
    that symbol" — and a page given only narrow facts has to guess what the area is FOR from the file
    names it can see. Measured here: fed claims alone, the model read `detectors.py` and `claims.py`
    and opened with "this area analyzes code for security issues and correlates them with known
    vulnerabilities", about a documentation compiler. Framing has to come from the layer below too,
    not be re-derived at each level.
    """
    pages = _module_pages_of(repo, spec["name"])
    claims = [c for c in verified_claims(repo) if c["page"] in pages][:_MAX_SUBSYSTEM_CLAIMS]
    return {
        "name": spec["name"],
        "pages": [{"page": page, "module": entry.get("name", page),
                   "purpose": _page_purpose(repo, page)}
                  for page, entry in sorted(pages.items())],
        "depends_on": list(spec.get("depends_on", [])),
        "claims": claims,
    }


SUBSYSTEM_PROMPT = """You are writing the page for ONE AREA of a codebase: the level between a
single module and the whole product. Your reader knows how to program but does not know THIS area —
a developer joining it, a reviewer touching it for the first time, an agent orienting itself.

AREA: {name}

THE MODULES IN IT, each with what its own page says it is FOR. This is what the area DOES — read it
before anything else, and do not re-derive the area's purpose from the file names:
{pages}

AREAS THIS ONE DEPENDS ON: {depends_on}

PROVEN FACTS about these modules. Each was verified against the code by machine. To use one, cite
its URI exactly as given:
{claims}

Write Markdown with EXACTLY these headings:

## What this area is responsible for
Two or three sentences. The job this area does for the rest of the system — its responsibility, not
its contents.

## How the work is divided
One short paragraph or a few bullets: how the modules split that responsibility between them, and
WHY the split falls where it does. A reader should finish knowing which module to open for what.

## What it depends on, and what depends on it
Two or three sentences about the boundary: what this area needs from elsewhere and what it promises
to the rest.

## Where to start reading
2-4 bullets naming the module page to open first for the most common tasks in this area.

RULES:
- Build ONLY on the proven facts and the module list above. Never invent a module, a behaviour or a
  dependency that is not there.
- Describe the area, not each module in turn. A page that walks the list one by one has added
  nothing that the list did not already say — it is the failure mode here.
- Never state that something does NOT exist: your facts are a selection, so absence is not provable.
- Max ~450 words. No preamble, no closing remarks.

End with a fenced block citing the proven facts your sentences rest on, one per line:

```isidore-claims
<the sentence you wrote> | <the wiki:// URI, exactly as given above> |
```
Leave the third field empty. Every claim must use a URI from the list above, verbatim. The `wiki://`
form belongs ONLY in this block — in your prose, name a page as `its-file-name.md`, never as a link
to `wiki://`, which resolves to nothing for a reader.
"""


def compile_subsystems(repo: Path, nodes: list[dict], links: list[dict], config: dict, *,
                       execute: bool = False, generator=None, max_calls: int = 0) -> list[dict]:
    """Compile the N2 layer: one bounded call per area, each page chained to its module pages.

    This is the level that makes the pyramid worth having. Without it the product page cites module
    claims directly, which verifies fine and reads badly: "the guide can be trusted" resting on a
    claim from a test module is a true chain and a poor argument. An area page is the natural place
    for a claim a product statement can honestly lean on.
    """
    from .claims import parse_claims_block
    from .pcp import CERT_SUFFIX, VerifyContext, write_certificate
    from .render import WIKI_DIRNAME
    from .verify import build_certificate, classify_mass

    specs = [s for s in plan_pyramid(nodes, links, config) if s.get("level") == 2]
    specs = [s for s in specs if _module_pages_of(repo, s["name"])][:_MAX_SUBSYSTEM_PAGES]
    results = [{"name": s["name"], "page": subsystem_page_name(s["name"]),
                "facts": subsystem_facts(repo, s), "calls": 0, "proved": 0, "written": False}
               for s in specs]
    if not execute:
        return results

    if generator is None:
        from .llm import default_generator
        from .pipeline import assert_may_send_source
        assert_may_send_source(f"facts drawn from {len(results)} subsystem(s) of this repository")
        generator = default_generator()

    ctx = VerifyContext(repo=repo, nodes=nodes, links=links)
    wiki = repo / WIKI_DIRNAME
    wiki.mkdir(parents=True, exist_ok=True)
    calls = 0
    for result in results:
        if max_calls and calls >= max_calls:
            break
        facts = result["facts"]
        if not facts["claims"]:
            # Nothing proven underneath: an area page here could only paraphrase the module list.
            result["skipped"] = "no proven claims in this area yet"
            continue
        prompt = SUBSYSTEM_PROMPT.format(
            name=facts["name"],
            pages="\n".join(f"- {p['module']} ({p['page']})"
                            + (f": {p['purpose']}" if p["purpose"] else "")
                            for p in facts["pages"]),
            depends_on=", ".join(facts["depends_on"]) or "(none recorded)",
            claims="\n".join(f"- {c['statement']} -> {c['uri']}" for c in facts["claims"]),
        )
        raw = generator(prompt)
        calls += 1
        result["calls"] = 1

        markdown, raw_claims = parse_claims_block(raw)
        wiki_rows = [c for c in raw_claims if (c.get("evidence") or "").startswith(WIKI_SCHEME)]
        cert = build_certificate(result["page"], markdown, [], ctx)
        cert.claims.extend(_chain_verdicts(repo, wiki_rows, ctx, cert))
        cert.mass = classify_mass(markdown, cert.claims)
        proved = [c for c in cert.claims if c.verdict == TRUE]
        result["proved"] = len(proved)

        if not proved:
            markdown = (f"# {facts['name']}\n\n> This area page was not published: none of its "
                        "statements could be traced back to a proven fact. See the module pages.\n")
            cert = build_certificate(result["page"], markdown, [], ctx)
        else:
            # Rewrite the reader-facing links AFTER certifying, so the certificate's prose hash
            # covers exactly the bytes on disk.
            markdown = relink_wiki_uris(markdown)
            cert = build_certificate(result["page"], markdown, [], ctx)
            cert.claims.extend(_chain_verdicts(repo, wiki_rows, ctx, cert))
            cert.mass = classify_mass(markdown, cert.claims)
        (wiki / result["page"]).write_text(markdown, encoding="utf-8")
        write_certificate(cert, wiki / f"{result['page']}{CERT_SUFFIX}")
        result["written"] = bool(proved)
    return results


# ---------------------------------------------------------------- N3: the product overview

OVERVIEW_PAGE = "overview.md"

# How many proven claims and modules the model is shown. The overview is a page a person reads in a
# minute; feeding it the whole repository would produce an inventory, which is the failure mode.
_MAX_CLAIMS = 40
_MAX_MODULES = 12
_README_LINES = 40


def verified_claims(repo: Path, *, prefer_level: int = 0) -> list[dict]:
    """Every claim the pages below PROVED, as citable `wiki://page#id` facts.

    This is the whole point of building upward: the raw material is not the code and not the model's
    memory, but statements a deterministic oracle already judged TRUE. A sentence up here can inherit
    its truth from a certificate further down instead of asserting anything new.

    `prefer_level=2` returns subsystem claims when any exist. It matters for the product page: a
    module claim verifies exactly as well, but "the guide can be trusted" resting on a fact from a
    test module is a valid chain and a poor argument. Citing the layer directly below keeps each
    step of the pyramid a short, defensible one.
    """
    from .pcp import CERT_SUFFIX, TRUE, read_certificate
    from .render import WIKI_DIRNAME

    wiki = repo / WIKI_DIRNAME
    if not wiki.is_dir():
        return []
    out: list[dict] = []
    for cert_path in sorted(wiki.glob(f"*.md{CERT_SUFFIX}")):
        try:
            cert = read_certificate(cert_path)
        except ValueError:
            continue
        page = cert_path.name[: -len(CERT_SUFFIX)]
        if page == OVERVIEW_PAGE:
            continue                      # the product page never cites itself
        for claim in cert.claims:
            if claim.verdict == TRUE:
                out.append({"page": page, "id": claim.id, "statement": claim.statement,
                            "evidence": claim.evidence, "level": 2 if
                            page.startswith(SUBSYSTEM_PREFIX) else 1,
                            "uri": f"{WIKI_SCHEME}{page}#{claim.id}"})
    if prefer_level == 2:
        subsystem = [c for c in out if c["level"] == 2]
        if subsystem:
            return subsystem
    return out


def _readme_context(repo: Path) -> str:
    """The project's own words about itself — CONTEXT, never evidence (see OVERVIEW_PROMPT)."""
    for name in ("README.md", "README.rst", "README.txt", "readme.md"):
        path = repo / name
        if path.is_file():
            lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
            return "\n".join(lines[:_README_LINES])
    return ""


def overview_facts(repo: Path, nodes: list[dict], links: list[dict], config: dict) -> dict:
    """Everything the overview is allowed to be written from. 0 LLM."""
    from .graph import module_of

    counts: dict[str, int] = defaultdict(int)
    for node in nodes:
        if node.get("file_type") == "code" and node.get("source_file"):
            counts[module_of(node["source_file"], 2)] += 1
    modules = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))[:_MAX_MODULES]
    return {
        "name": repo.resolve().name,
        "readme": _readme_context(repo),
        "subsystems": [s for s in plan_pyramid(nodes, links, config) if s.get("level") == 2],
        "modules": [{"name": name, "symbols": n} for name, n in modules],
        "claims": verified_claims(repo, prefer_level=2)[:_MAX_CLAIMS],
    }


OVERVIEW_PROMPT = """You are writing the front page of a product's documentation, for someone who
will never read its code: a manager, a customer, a new colleague from another department.

THE PROJECT CALLS ITSELF THIS (context only — it is marketing prose written by a human, NOT evidence.
Use it to understand the intent, never to state a fact):
{readme}

WHAT THE SOFTWARE IS MADE OF (mechanically extracted):
{modules}

PROVEN FACTS you may build on. Each was already verified against the code by machine. To use one,
cite its URI exactly as given:
{claims}

Write Markdown with EXACTLY these headings and nothing else:

## What this is
Two or three sentences. What problem does this software solve, and for whom? Lead with the problem,
not the technology.

## What you can do with it
3-6 bullets. Each bullet is one capability, described as an OUTCOME for the person using it.

## How the pieces fit together
Two or three sentences telling the story of how work flows through it. A story, not an inventory —
never list components, never describe structure for its own sake.

RULES, and the first one outranks everything else:
- Write for someone who has never seen code and never will. BANNED WORDS, no exceptions: method,
  class, function, parameter, argument, API, endpoint, payload, constant, variable, module, library,
  daemon, server, addon, binary, runtime, instance, protocol, schema, snapshot, interface, struct,
  callback, async, repository, repo, commit, refactor, compile, compiler, cache, buffer, thread,
  lock, mutex, hash, serialise, LLM, agent, codebase, token, graph, parse, crawl, syntax, metadata,
  backend, frontend, config.
- Name the technology by what it DOES, not by what it is. "Reads the project and writes its
  documentation" — not "compiles a wiki from the codebase".
- No file names, no line numbers, no CamelCase or snake_case names, no code punctuation.
- Say only what the PROVEN FACTS and the project's own description support. Never invent a feature,
  a user, a benefit or a number.
- If you cannot say something without a banned word, say less. A short honest page beats a long one.

CITATIONS ARE MANDATORY. A page nobody can check is worth nothing here. End with a fenced block in
which EVERY bullet under "What you can do with it" appears, each resting on a proven fact:

```isidore-claims
<the sentence you wrote, in plain words> | <the wiki:// URI, exactly as given above> |
```
Use the URI verbatim from the PROVEN FACTS list. Leave the third field empty. If a sentence you
wrote cannot cite one of those facts, delete that sentence — do not cite a fact that does not
support it.
"""

OVERVIEW_REPAIR = """

Your previous answer used wording a non-technical reader cannot follow. These rules were broken:
{broken}
Rewrite it saying the same thing without those words or shapes. If a SENTENCE cannot survive the
rewrite, drop that sentence. Keep ALL THREE headings and the claims block: dropping a whole section
is not a fix, it is a smaller page with the same problem.
"""

# The headings the product page promises its reader. Checked deterministically, because a repair pass
# that drops a whole section rather than rewording it produces a page that reads fine and quietly
# answers less — observed on the first GICS run, where "How the pieces fit together" simply vanished.
OVERVIEW_SECTIONS = ("What this is", "What you can do with it", "How the pieces fit together")


def missing_sections(markdown: str, expected: tuple[str, ...] = OVERVIEW_SECTIONS) -> list[str]:
    """Required headings the page does not have. 0 LLM."""
    present = {line[3:].strip().lower() for line in markdown.splitlines() if line.startswith("## ")}
    return [name for name in expected if name.lower() not in present]


def relink_wiki_uris(markdown: str) -> str:
    """Turn `wiki://page` into `page` in PROSE, so the links a reader clicks actually resolve.

    The scheme is machine-facing: it is how a claim names its evidence, and lane D's verifier is what
    reads it. In a sentence it is a dead link — `[page](wiki://page)` opens nothing. Dropping the
    scheme leaves a working relative link in the `[text](page)` form and a readable file name in the
    bare `(wiki://page)` form, which are the two shapes models actually produce here.
    """
    return markdown.replace(WIKI_SCHEME, "")


def _plain_violations(markdown: str) -> list[str]:
    """Rule names broken by the PROSE (fenced blocks excluded — those are machine-facing)."""
    from .plain import check

    body = re.sub(r"```.*?```", "", markdown, flags=re.DOTALL)
    broken: list[str] = []
    for name in check(body):
        if name not in broken:
            broken.append(name)
    return broken


def compile_overview(repo: Path, nodes: list[dict], links: list[dict], config: dict, *,
                     execute: bool = False, generator=None) -> dict:
    """Compile the plain-language product page (N3). One LLM call, plus at most one repair.

    Unlike a module page, this one is gated on being READABLE, not only on being true: a page for
    non-technical readers that comes back full of jargon has failed at its only job, so the model
    gets one bounded chance to rewrite it before the offending prose is refused.
    """
    from .claims import anchor_claims, parse_claims_block
    from .pcp import CERT_SUFFIX, VerifyContext, write_certificate
    from .plain import explain
    from .render import WIKI_DIRNAME
    from .verify import build_certificate, classify_mass

    facts = overview_facts(repo, nodes, links, config)
    result = {"page": OVERVIEW_PAGE, "calls": 0, "claims": 0, "plain_broken": [], "written": False,
              "facts": facts}
    if not execute:
        return result

    if generator is None:
        from .llm import default_generator
        from .pipeline import assert_may_send_source
        assert_may_send_source("this repository's README and its module inventory")
        generator = default_generator()

    prompt = OVERVIEW_PROMPT.format(
        readme=facts["readme"] or "(no README)",
        modules="\n".join(f"- {m['name']} ({m['symbols']} symbols)" for m in facts["modules"])
                or "- (none)",
        claims="\n".join(f"- {c['statement']} -> {c['uri']}" for c in facts["claims"]) or "- (none)",
    )
    raw = generator(prompt)
    result["calls"] = 1

    broken = _plain_violations(raw)
    if broken:
        raw = generator(prompt + OVERVIEW_REPAIR.format(broken=explain(broken)))
        result["calls"] = 2
        broken = _plain_violations(raw)
    result["plain_broken"] = broken

    markdown, raw_claims = parse_claims_block(raw)
    # The page still speaks to engineers. Publishing it would defeat the point of having it, so the
    # prose is refused and the reader is told plainly why — the same discipline the claim verifier
    # applies to truth, applied to readability.
    refusal = (f"could not be written in plain language ({explain(broken)}). Nothing is published "
               "rather than publishing a page a non-technical reader cannot use") if broken else ""
    if broken:
        raw_claims = []

    ctx = VerifyContext(repo=repo, nodes=nodes, links=links)
    # A `wiki://` claim is anchored by its CHAIN, not by a file: `anchor_claims` would try to hash the
    # URI as a path, fail, and drop it — which is why lane D's verifier, registered since P0, had
    # never actually decided a single claim. Split them out and resolve them through the registry.
    wiki_rows = [c for c in raw_claims if (c.get("evidence") or "").startswith(WIKI_SCHEME)]
    file_rows = [c for c in raw_claims if not (c.get("evidence") or "").startswith(WIKI_SCHEME)]
    markdown = relink_wiki_uris(markdown)
    anchored, _dropped, _repaired = anchor_claims(repo, file_rows, None)
    cert = build_certificate(OVERVIEW_PAGE, markdown, anchored, ctx)
    cert.claims.extend(_chain_verdicts(repo, wiki_rows, ctx, cert))
    cert.mass = classify_mass(markdown, cert.claims)

    proved = [c for c in cert.claims if c.verdict == TRUE]
    result["claims"] = len(cert.claims)
    result["proved"] = len(proved)
    result["missing_sections"] = missing_sections(markdown) if not refusal else []
    if not proved and not refusal:
        # A product page resting on nothing is precisely the artifact this tool exists to replace:
        # fluent, plausible, unverifiable. Refuse it rather than publish it.
        refusal = ("was not published: none of its statements could be traced back to a proven fact "
                   "about the code")
    if refusal:
        # Language comes first when both are wrong: "rewrite it in plain words" is the actionable
        # instruction, and the missing citations are a consequence of refusing the prose, not a
        # separate failure to report.
        markdown = (f"# {facts['name']}\n\n> This overview {refusal}. See the module pages for the "
                    "technical view.\n")
        cert = build_certificate(OVERVIEW_PAGE, markdown, [], ctx)

    wiki = repo / WIKI_DIRNAME
    wiki.mkdir(parents=True, exist_ok=True)
    (wiki / OVERVIEW_PAGE).write_text(markdown, encoding="utf-8")
    write_certificate(cert, wiki / f"{OVERVIEW_PAGE}{CERT_SUFFIX}")
    result["written"] = bool(proved)
    return result


def _chain_verdicts(repo: Path, rows: list[dict], ctx: VerifyContext, cert) -> list:
    """Resolve `wiki://` claims through lane D's verifier and compose the child certificates.

    Each cited child certificate is hashed into `child_cert_hashes`, so the overview's integrity is
    rooted in the pages it rests on: edit a module page and its certificate hash moves, which is
    visible here without re-running a single model call.
    """
    import hashlib

    from .claims import claim_id
    from .pcp import CERT_SUFFIX, ClaimVerdict, Predicate, verify_predicate
    from .render import WIKI_DIRNAME

    out = []
    for row in rows:
        uri = row["evidence"]
        predicate = Predicate(kind=WIKI_VERIFIER_KIND, args=(uri,))
        verdict = verify_predicate(predicate, ctx)
        parsed = parse_wiki_uri(uri)
        ehash = ""
        if parsed is not None:
            page, _claim = parsed
            child = repo / WIKI_DIRNAME / f"{page}{CERT_SUFFIX}"
            if child.is_file():
                digest = hashlib.sha256(child.read_bytes()).hexdigest()
                cert.child_cert_hashes[page] = digest
                ehash = digest[:12]
        out.append(ClaimVerdict(
            id=claim_id(row["statement"], uri), statement=row["statement"], evidence=uri,
            ehash=ehash, predicate=predicate.serialize(), verdict=verdict.value,
            oracle=verdict.oracle, detail=verdict.detail))
    return out


def register_cli(sub) -> None:
    """Add `isidore pyramid` (plan/preview) and `isidore overview` (the N3 product page)."""
    p = sub.add_parser("pyramid", help="plan the subsystem/product pyramid pages (0 LLM)")
    p.add_argument("--repo", type=Path, default=Path("."))
    p.add_argument("--graph", type=Path, default=None)
    p.set_defaults(func=_cmd_pyramid)

    s = sub.add_parser("subsystems", help="compile the area pages (N2) from the module pages below")
    s.add_argument("--repo", type=Path, default=Path("."))
    s.add_argument("--graph", type=Path, default=None)
    s.add_argument("--execute", action="store_true", help="write the pages (1 LLM call per area)")
    s.add_argument("--max-calls", type=int, default=0, help="0 = no cap")
    s.set_defaults(func=_cmd_subsystems)

    o = sub.add_parser("overview", help="compile the plain-language product page from proven claims")
    o.add_argument("--repo", type=Path, default=Path("."))
    o.add_argument("--graph", type=Path, default=None)
    o.add_argument("--execute", action="store_true", help="write the page (1 LLM call, +1 repair)")
    o.set_defaults(func=_cmd_overview)


def _cmd_subsystems(args) -> int:
    nodes, links, config = _load_graph_for(args)
    results = compile_subsystems(args.repo, nodes, links, config, execute=args.execute,
                                 max_calls=args.max_calls)
    if not results:
        print("[isidore] no areas with compiled module pages — run `isidore compile --execute` first")
        return 1
    if not args.execute:
        for item in results:
            print(f"[isidore] {item['name']}: {len(item['facts']['pages'])} module page(s), "
                  f"{len(item['facts']['claims'])} proven claim(s)")
        print(f"[isidore] {len(results)} area page(s) planned — 0 LLM calls made; "
              "run with --execute to compile")
        return 0
    written = [r for r in results if r["written"]]
    for item in results:
        if item["written"]:
            print(f"  OK   {item['page']}  ({item['proved']} claim(s) chained)")
        elif item.get("skipped"):
            print(f"  SKIP {item['page']}  ({item['skipped']})")
        else:
            print(f"  REFUSED {item['page']}  (nothing traceable to a proven fact)")
    print(f"[isidore] {len(written)}/{len(results)} area page(s) written · "
          f"{sum(r['calls'] for r in results)} call(s)")
    return 0 if written else 1


def _load_graph_for(args) -> tuple[list[dict], list[dict], dict]:
    from .graph import find_graph, load_graph
    graph_path = args.graph or find_graph(args.repo)
    if graph_path and Path(graph_path).is_file():
        nodes, links, _commit = load_graph(Path(graph_path))
    else:
        nodes, links = [], []
    config_path = args.repo / "pyramid_config.json"
    config = json.loads(config_path.read_text(encoding="utf-8")) if config_path.is_file() else {}
    return nodes, links, config


def _cmd_overview(args) -> int:
    from .plain import explain

    nodes, links, config = _load_graph_for(args)
    result = compile_overview(args.repo, nodes, links, config, execute=args.execute)
    facts = result["facts"]
    if not args.execute:
        print(f"[isidore] overview would be built from {len(facts['claims'])} proven claim(s) "
              f"across {len(facts['modules'])} module(s) — 0 LLM calls made")
        print("[isidore] run with --execute to compile it (1 call, +1 if a plain-language repair "
              "is needed)")
        return 0
    if result["plain_broken"]:
        print(f"[isidore] REFUSED: the overview could not be written in plain language "
              f"({explain(result['plain_broken'])})")
        return 1
    print(f"[isidore] wrote {args.repo / 'wiki' / OVERVIEW_PAGE} · {result['claims']} claim(s) "
          f"chained to module certificates · {result['calls']} call(s)")
    if result["missing_sections"]:
        print(f"[isidore] warning: the page is missing {', '.join(result['missing_sections'])} — "
              "it answers less than it promises")
    return 0


def _cmd_pyramid(args) -> int:
    """Print a deterministic JSON plan for humans and scripts."""
    from .graph import find_graph, load_graph
    graph_path = args.graph or find_graph(args.repo)
    if graph_path and Path(graph_path).is_file():
        nodes, links, _commit = load_graph(Path(graph_path))
    else:
        nodes, links = [], []
    config_path = args.repo / "pyramid_config.json"
    config = json.loads(config_path.read_text(encoding="utf-8")) if config_path.is_file() else {}
    print(json.dumps(plan_pyramid(nodes, links, config), indent=2))
    return 0
