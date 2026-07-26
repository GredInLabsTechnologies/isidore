"""`isidore recertify` — re-run the claim oracles over unchanged prose and rewrite the certificate.

The gap this closes (T-e46b, found while making GIMO's living documentation green): `isidore verify`
fails a page whose recorded verdicts no longer match the current graph, but `isidore compile`
computes dirtiness from (context changed) OR (claim stale) OR (page missing) — a stale CERTIFICATE
is in none of those sets. The two commands disagreed and there was no supported way out; the
workaround was deleting the page so "missing" forced regeneration, at one LLM call each.

Most of that drift is the documentation being MORE right than its certificate: a module-level
constant an older extractor could not see is now proved by the current one, so a claim recorded
FALSE verifies TRUE. Nothing a model wrote is wrong — only the record of what could be proved. That
is repaired by re-running the oracles, which costs nothing.

The one direction this refuses to touch is TRUE -> FALSE. A claim only reaches the published prose
once it verified TRUE, so that move means a sentence a reader can see is now contradicted by the
code. Rewriting the certificate there would turn a wrong page green — the page needs new prose, and
this command hands it to `compile` instead of hiding it.
"""
from __future__ import annotations

from dataclasses import dataclass, field, replace
from pathlib import Path

from .pcp import CERT_SUFFIX, WIKI_VERIFIER_KIND, Certificate, parse_stored_predicate, parse_wiki_uri, write_certificate
from .verify import (
    CERT_DRIFTED,
    CERT_MISSING,
    CERT_OK,
    CERT_TAMPERED,
    CERT_UNREADABLE,
    CertStatus,
    _ctx_for,
    certificate_status,
    classify_mass,
    verify_predicate_ctx,
)

# What recertify decided to do with a page. `refuted` and `tampered` are the two it will not fix.
ACT_OK = "ok"                  # certificate already matches the graph — nothing to do
ACT_RECERTIFY = "recertify"    # drift the oracles can restate honestly, 0 LLM
ACT_REFUTED = "refuted"        # a published claim is now FALSE — needs new prose, not a new cert
ACT_TAMPERED = "tampered"      # the prose was edited after compile — the cert describes other text
ACT_NO_CERT = "no-cert"        # never certified (or unreadable): compile's job, not this one


@dataclass
class PageRecert:
    page: str
    action: str
    drift: tuple[tuple[str, str, str], ...] = ()
    children_moved: tuple[str, ...] = ()

    @property
    def needs_prose(self) -> bool:
        return self.action in (ACT_REFUTED, ACT_TAMPERED)


@dataclass
class RecertifyResult:
    pages: list[PageRecert] = field(default_factory=list)
    written: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def of(self, action: str) -> list[PageRecert]:
        return [p for p in self.pages if p.action == action]


def _level(name: str) -> int:
    """Pyramid level, so children are recertified before the pages that cite them.

    A `wikichain` claim reads the child's certificate live off disk, so recertifying a parent first
    would compose the child's OLD verdict and then be stale the moment the child is rewritten.
    """
    from .pyramid import OVERVIEW_PAGE, SUBSYSTEM_PREFIX
    if name == OVERVIEW_PAGE:
        return 3
    return 2 if name.startswith(SUBSYSTEM_PREFIX) else 1


def _child_digest(repo: Path, uri: str) -> tuple[str, str] | None:
    """(child page, sha256 of its certificate) for a wiki:// URI, or None if there is no child cert."""
    import hashlib

    from .pipeline import WIKI_DIRNAME
    parsed = parse_wiki_uri(uri)
    if parsed is None:
        return None
    page, _claim = parsed
    child = repo / WIKI_DIRNAME / f"{page}{CERT_SUFFIX}"
    if not child.is_file():
        return None
    return page, hashlib.sha256(child.read_bytes()).hexdigest()


def rebuild_certificate(repo: Path, page_path: Path, st: CertStatus, ctx) -> Certificate:
    """The recorded certificate with every re-runnable verdict recomputed. Prose is never touched.

    `prose_sha256` is carried over deliberately: the caller has already established that the page
    still hashes to it, so re-deriving it would only invite the day someone recertifies a page they
    also edited. Marks and violations are carried over too — they were produced by scans that ran
    BEFORE the model call, and a danger mark is answered in the prose, which is not being rewritten.
    """
    cert = st.cert
    assert cert is not None                     # callers only reach here on ok/drifted
    from .claims import parse_claims_block
    clean, _rows = parse_claims_block(page_path.read_text(encoding="utf-8"))

    claims = []
    child_hashes: dict[str, str] = {}
    chained = False
    for cv in cert.claims:
        pred = parse_stored_predicate(cv.predicate)
        if pred is None:
            claims.append(cv)                   # existence-anchored: no oracle to re-run
            continue
        v = verify_predicate_ctx(pred, ctx)
        ehash = cv.ehash
        if pred.kind == WIKI_VERIFIER_KIND and pred.args:
            chained = True
            found = _child_digest(repo, pred.args[0])
            if found is not None:
                child_page, digest = found
                child_hashes[child_page] = digest
                ehash = digest[:12]             # composed integrity, refreshed with the child
        claims.append(replace(cv, verdict=v.value, oracle=v.oracle, detail=v.detail, ehash=ehash))

    # For a chained page the recomputed set is authoritative EVEN IF empty — a child whose
    # certificate was deleted must drop out, or the stale entry survives every repair and the page
    # never converges. A page with no chain keeps whatever it recorded.
    return Certificate(
        page=cert.page, graph_commit=ctx.commit, prose_sha256=cert.prose_sha256, claims=claims,
        marks=list(cert.marks), violations=list(cert.violations),
        mass=classify_mass(clean, claims),
        child_cert_hashes=child_hashes if chained else dict(cert.child_cert_hashes))


def recertify(repo: Path, *, only: list[str] | None = None, write: bool = False) -> RecertifyResult:
    """Re-run the oracles over every certified page. 0 LLM. Writes only with `write=True`."""
    from .pipeline import WIKI_DIRNAME
    result = RecertifyResult()
    wiki = repo / WIKI_DIRNAME
    if not wiki.is_dir():
        result.warnings.append(f"no wiki at {wiki} — run `isidore compile --execute` first")
        return result
    ctx = _ctx_for(repo)
    if ctx is None:
        result.warnings.append("no structure graph — run `isidore scan` first")
        return result

    wanted = set(only or [])
    pages = sorted((p for p in wiki.glob("*.md") if not wanted or p.name in wanted),
                   key=lambda p: (_level(p.name), p.name))
    for page in pages:
        st = certificate_status(repo, page, ctx)
        if st.status in (CERT_MISSING, CERT_UNREADABLE):
            result.pages.append(PageRecert(page.name, ACT_NO_CERT))
            continue
        if st.status == CERT_TAMPERED:
            result.pages.append(PageRecert(page.name, ACT_TAMPERED))
            continue
        if st.status == CERT_OK:
            result.pages.append(PageRecert(page.name, ACT_OK))
            continue
        if st.status != CERT_DRIFTED:            # no-graph is impossible: ctx was built above
            result.warnings.append(f"{page.name}: unexpected status {st.status}")
            continue
        if st.refuted:
            result.pages.append(PageRecert(page.name, ACT_REFUTED, st.refuted))
            continue
        result.pages.append(PageRecert(page.name, ACT_RECERTIFY, st.drift, st.children_moved))
        if write:
            write_certificate(rebuild_certificate(repo, page, st, ctx),
                              page.parent / f"{page.name}{CERT_SUFFIX}")
            result.written.append(page.name)
    return result


# ---------------------------------------------------------------- CLI


def register_cli(sub) -> None:
    """Add `isidore recertify` (called once from cli.main via the registrar loop)."""
    p = sub.add_parser("recertify",
                       help="re-run the claim oracles and rewrite stale certificates (0 LLM)")
    p.add_argument("--repo", type=Path, default=Path("."))
    p.add_argument("--only", nargs="*", metavar="PAGE", help="restrict to these page filenames")
    p.add_argument("--write", action="store_true",
                   help="write the rebuilt certificates (default: report what would change)")
    p.set_defaults(func=_cmd_recertify)


def _cmd_recertify(args) -> int:
    result = recertify(args.repo, only=args.only, write=args.write)
    for w in result.warnings:
        print(f"[isidore] {w}")
    if result.warnings and not result.pages:
        return 2

    repairable = result.of(ACT_RECERTIFY)
    for p in repairable:
        moves = [f"{cid} {was}->{now}" for cid, was, now in p.drift]
        moves += [f"child {c} moved" for c in p.children_moved]
        print(f"  {'WROTE ' if args.write else 'STALE '} {p.page}  ({', '.join(moves)})")
    for p in result.of(ACT_REFUTED):
        moves = ", ".join(f"{cid}" for cid, _w, _n in p.drift)
        print(f"  REFUTED {p.page}  ({moves}) — published claim now FALSE, needs "
              f"`isidore compile --execute`")
    for p in result.of(ACT_TAMPERED):
        print(f"  EDITED  {p.page} — prose changed after compile; recertifying would certify an "
              f"unreviewed edit")

    ok = len(result.of(ACT_OK))
    blocked = [p for p in result.pages if p.needs_prose]
    print(f"[isidore] {ok} certificate(s) already current, {len(repairable)} "
          f"{'rewritten' if args.write else 'repairable at 0 LLM'}, {len(blocked)} need prose")
    if repairable and not args.write:
        print("[isidore] re-run with --write to apply")
    return 1 if blocked else 0


__all__ = ["ACT_NO_CERT", "ACT_OK", "ACT_RECERTIFY", "ACT_REFUTED", "ACT_TAMPERED", "PageRecert",
           "RecertifyResult", "rebuild_certificate", "recertify", "register_cli"]
