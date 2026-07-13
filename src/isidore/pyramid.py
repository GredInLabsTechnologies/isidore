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
from collections import defaultdict
from pathlib import Path
from pathlib import PurePosixPath

from .pcp import (
    FALSE,
    ORACLE_WIKI,
    TRUE,
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


def register_cli(sub) -> None:
    """Add `isidore pyramid` (plan/preview the hierarchical pages)."""
    p = sub.add_parser("pyramid", help="plan the subsystem/product pyramid pages (0 LLM)")
    p.add_argument("--repo", type=Path, default=Path("."))
    p.add_argument("--graph", type=Path, default=None)
    p.set_defaults(func=_cmd_pyramid)


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
