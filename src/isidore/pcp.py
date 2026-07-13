"""Proof-Carrying Prose (PCP) — the frozen seam shared by every PCP lane.

This module is the SINGLE point of coupling for ADR-0033. It owns the types, the predicate
grammar, the certificate shape, and the verifier registry that lanes A–E all import. **Lanes never
redefine these types** — they import them here and fill in behaviour in their own modules:

    A (verify.py)      registers verifiers, builds/reads certificates
    B (reconcile.py,   the reconciler + contracts, as PURE functions with the frozen signatures
       contracts.py)
    C (detectors.py)   scan(root, ctx) -> list[Mark]
    D (pyramid.py)     registers the wiki:// verifier, plans levels
    E (humanpack.py)   renders the human pack from compiled artifacts (0 LLM)

Design rules baked into this seam (see design/PCP_SEAMS.md for the full contract):

- Two oracles, declared. The internal scanner only emits `contains`/`imports` edges (see graph.py),
  so `calls(A,B)` is NOT decidable from the graph alone — a verifier may reparse the cited file's
  AST. Every Verdict records WHICH oracle decided it. A predicate with no verifier for the cited
  language returns UNDECIDABLE — it NEVER masquerades as TRUE (fail-closed, invariant of P1).

- Certificates are read by a MACHINE (`isidore verify`), not an LLM, so they persist as JSON
  (re-parseable with the stdlib), not TOON. TOON stays the LLM-facing format; JSON is the
  machine-facing one. A human-readable TOON view of a cert is a render concern, not storage.

- Monotonic escalation (I10): a Mark's `disposition` is filled AFTER the LLM call, but the mark is
  never removed by the model. Clearing a mark is an audited human action, recorded elsewhere.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Callable, Protocol

PCP_VERSION = "pcp-1"
CERT_SUFFIX = ".cert.json"          # <page>.md -> <page>.md.cert.json alongside the page
CONTRACTS_FILENAME = "contracts.json"

# Verdict values — the only three a verifier may return. UNDECIDABLE is a first-class citizen:
# it is what keeps the system honest when the oracle cannot reach a decision for a language.
TRUE = "TRUE"
FALSE = "FALSE"
UNDECIDABLE = "UNDECIDABLE"

# Oracle tags — which deterministic source decided a verdict. Recorded in the certificate so an
# auditor sees HOW each claim was checked, and so lanes can tell graph-backed from AST-backed facts.
ORACLE_GRAPH = "graph"        # decided from graph.json nodes/edges
ORACLE_AST = "ast"            # decided by reparsing the cited file (Python stdlib ast, etc.)
ORACLE_LANGSPEC = "langspec"  # decided by the declarative multi-language engine
ORACLE_GREP = "grep"          # decided by a deterministic textual scan (e.g. env(NAME))
ORACLE_WIKI = "wiki"          # decided by resolving a wiki:// chain (lane D)
ORACLE_NONE = "none"          # no oracle could decide -> UNDECIDABLE

# Predicate kinds — the decidable grammar. args semantics (positional) are frozen here:
#   calls      [caller_symbol, callee_symbol]      caller has a call to callee in its body
#   defines    [file, symbol]                      file defines a top-level symbol of that name
#   exports    [file, symbol]                      file exports symbol (language-dependent)
#   imports    [file, module_or_file]              file imports that module/file
#   value      [symbol_or_name, literal]           a const/assignment equals the literal
#   signature  [fn, arg1, arg2, ...]               fn's parameter list equals these names (order)
#   route      [method_and_path, handler]          e.g. "GET /admin", "adminHandler"
#   env        [NAME]                               the env var NAME is read somewhere
PREDICATE_KINDS = frozenset(
    {"calls", "defines", "exports", "imports", "value", "signature", "route", "env"})

# Serialized predicate grammar (fits inside one TOON/pipe field — NO commas, they break TOON):
#   "<kind>:<arg1>;<arg2>;..."      e.g.  "calls:authMiddleware;supabase.auth.getUser"
# An empty/absent predicate means the claim is existence-anchored only (a "yellow" claim, the
# pre-PCP behaviour). This is what keeps lane A backwards compatible with today's claims.
_PRED_SEP = ":"
_ARG_SEP = ";"


@dataclass(frozen=True)
class Predicate:
    """A decidable assertion parsed from a claim's third field. Frozen: predicates are values."""
    kind: str
    args: tuple[str, ...]

    def serialize(self) -> str:
        return f"{self.kind}{_PRED_SEP}{_ARG_SEP.join(self.args)}" if self.kind else ""


def parse_predicate(raw: str | None) -> Predicate | None:
    """Parse "<kind>:<a>;<b>" -> Predicate, or None if absent/malformed/unknown-kind.

    Tolerant by design (a malformed predicate degrades the claim to existence-anchored, it never
    raises): unknown kinds and empty payloads return None so the claim stays 'yellow'.
    """
    if not raw or _PRED_SEP not in raw:
        return None
    kind, _sep, payload = raw.strip().partition(_PRED_SEP)
    kind = kind.strip().lower()
    if kind not in PREDICATE_KINDS:
        return None
    args = tuple(a.strip() for a in payload.split(_ARG_SEP) if a.strip())
    if not args:
        return None
    return Predicate(kind=kind, args=args)


@dataclass
class Verdict:
    """The result of checking one predicate against an oracle. `value` is TRUE|FALSE|UNDECIDABLE."""
    value: str
    oracle: str = ORACLE_NONE
    detail: str = ""            # short human reason, for the certificate's audit trail


# UNDECIDABLE is the safe default a stub or a language-blind verifier returns.
def undecidable(detail: str = "") -> Verdict:
    return Verdict(value=UNDECIDABLE, oracle=ORACLE_NONE, detail=detail)


@dataclass
class VerifyContext:
    """Everything a verifier needs, assembled once per page/verify run. Read-only to verifiers."""
    repo: Path
    nodes: list[dict] = field(default_factory=list)
    links: list[dict] = field(default_factory=list)
    commit: str | None = None
    # lane D populates this so the wiki:// verifier can resolve chains without importing the pipeline
    pages_state: dict = field(default_factory=dict)


class Verifier(Protocol):
    """A predicate verifier. MUST be deterministic and 0-LLM. Returns UNDECIDABLE, never guesses."""
    def __call__(self, predicate: Predicate, ctx: VerifyContext) -> Verdict: ...


# The registry. Lane A fills it (calls/defines/imports/exports/value/signature/route/env); lane D
# adds the wiki:// resolver keyed on a reserved kind. register() is idempotent-overwrite so a lane
# owns its kinds without racing another. get() returns None for an unregistered kind (=> UNDECIDABLE).
VERIFIERS: dict[str, Verifier] = {}


def register_verifier(kind: str, fn: Verifier) -> None:
    VERIFIERS[kind] = fn


def get_verifier(kind: str) -> Verifier | None:
    return VERIFIERS.get(kind)


def verify_predicate(predicate: Predicate | None, ctx: VerifyContext) -> Verdict:
    """Dispatch one predicate to its registered verifier. No verifier -> UNDECIDABLE (fail-closed)."""
    if predicate is None:
        return undecidable("no predicate (existence-anchored only)")
    fn = get_verifier(predicate.kind)
    if fn is None:
        return undecidable(f"no verifier registered for '{predicate.kind}'")
    return fn(predicate, ctx)


# ---------------------------------------------------------------- certificate

@dataclass
class ClaimVerdict:
    """One claim's line in a certificate: the anchored claim + its typed verdict (if any)."""
    id: str
    statement: str
    evidence: str
    ehash: str
    predicate: str = ""          # serialized Predicate, "" for existence-anchored claims
    verdict: str = UNDECIDABLE   # TRUE|FALSE|UNDECIDABLE
    oracle: str = ORACLE_NONE
    detail: str = ""


# Sentence-confidence classes for "verified mass" (lane A). Deterministic mapping sentence->class.
GREEN = "green"     # sentence cites a typed claim proved TRUE
YELLOW = "yellow"   # sentence cites an existence-anchored (or UNDECIDABLE-typed) claim
GRAY = "gray"       # sentence carries no citation — narrative, honestly un-load-bearing


@dataclass
class VerifiedMass:
    green: int = 0
    yellow: int = 0
    gray: int = 0

    @property
    def total(self) -> int:
        return self.green + self.yellow + self.gray


@dataclass
class Mark:
    """A deterministic security-relevant flag raised BEFORE the LLM call (lane C).

    `disposition` is filled AFTER the call (the schema forces the model to address every mark), but
    the mark itself is immutable evidence: monotonic escalation (I10) means the model annotates,
    never erases. Clearing a mark is an audited human action (`isidore findings resolve`).
    """
    family: str          # "entropy" | "sink" | "topology"
    file: str
    line: int
    reason: str
    severity: str = "warn"       # "info" | "warn" | "danger"
    disposition: str = ""        # model's explanation, added post-call; NEVER removes the mark


@dataclass
class Violation:
    """A reconciler finding (lane B): the model's own outputs contradict each other. 0-LLM."""
    kind: str            # "prose-omits-finding" | "prose-contradicts-finding" | "mark-uncovered"
    where: str
    detail: str


@dataclass
class Certificate:
    """The re-verifiable sidecar for one page. Persisted as JSON (machine-read). Tamper-evident via
    prose_sha256: editing the page after compile breaks `isidore verify`."""
    page: str
    version: str = PCP_VERSION
    graph_commit: str | None = None
    prose_sha256: str = ""
    claims: list[ClaimVerdict] = field(default_factory=list)
    marks: list[Mark] = field(default_factory=list)
    violations: list[Violation] = field(default_factory=list)
    mass: VerifiedMass = field(default_factory=VerifiedMass)
    # certs of the child pages this page's wiki:// claims depend on (lane D) -> composed integrity
    child_cert_hashes: dict[str, str] = field(default_factory=dict)


def prose_hash(markdown: str) -> str:
    """The tamper-evidence anchor: sha256 of the page prose (full hex, this is a machine check)."""
    return hashlib.sha256(markdown.encode("utf-8")).hexdigest()


def certificate_to_dict(cert: Certificate) -> dict:
    """Certificate -> plain dict (asdict handles the nested dataclasses). The JSON on disk."""
    return asdict(cert)


def certificate_from_dict(data: dict) -> Certificate:
    """Rebuild a Certificate from parsed JSON, reconstructing the nested dataclasses. Tolerant of
    missing keys (older/partial certs) so `isidore verify` degrades instead of crashing."""
    mass = data.get("mass") or {}
    return Certificate(
        page=data.get("page", ""),
        version=data.get("version", PCP_VERSION),
        graph_commit=data.get("graph_commit"),
        prose_sha256=data.get("prose_sha256", ""),
        claims=[ClaimVerdict(**c) for c in data.get("claims", [])],
        marks=[Mark(**m) for m in data.get("marks", [])],
        violations=[Violation(**v) for v in data.get("violations", [])],
        mass=VerifiedMass(green=mass.get("green", 0), yellow=mass.get("yellow", 0),
                          gray=mass.get("gray", 0)),
        child_cert_hashes=dict(data.get("child_cert_hashes", {})),
    )


def write_certificate(cert: Certificate, path: Path) -> None:
    """Persist a certificate as pretty JSON (stable key order for byte-deterministic diffs)."""
    path.write_text(json.dumps(certificate_to_dict(cert), indent=2, sort_keys=True) + "\n",
                    encoding="utf-8")


def read_certificate(path: Path) -> Certificate:
    """Load a certificate from disk. Raises ValueError on malformed JSON (fail-closed for verify)."""
    try:
        data = json.loads(path.read_text(encoding="utf-8", errors="replace"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"malformed certificate at {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError(f"certificate at {path} must be a JSON object")
    return certificate_from_dict(data)


def read_contracts(path: Path) -> list[Contract]:
    """Load promoted contracts (empty list if the file is absent). Malformed -> ValueError."""
    if not path.is_file():
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8", errors="replace"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"malformed contracts at {path}: {exc}") from exc
    return [Contract(**c) for c in data.get("contracts", [])]


def write_contracts(contracts: list[Contract], path: Path) -> None:
    """Persist contracts as JSON (machine-read gate input)."""
    path.write_text(
        json.dumps({"contracts": [asdict(c) for c in contracts]}, indent=2, sort_keys=True) + "\n",
        encoding="utf-8")


# ---------------------------------------------------------------- contracts

@dataclass
class Contract:
    """A typed claim a human promoted to an invariant. `isidore verify --contracts` fails CI if it
    turns FALSE against the current graph. Promotion and timestamp are supplied by the caller (no
    wall-clock here, so the seam stays pure/testable)."""
    id: str
    predicate: str       # serialized Predicate
    evidence: str
    promoted_by: str
    promoted_at: str = ""    # ISO 8601, passed in by the CLI
    note: str = ""


# ---------------------------------------------------------------- wiki:// (lane D)

WIKI_SCHEME = "wiki://"
WIKI_VERIFIER_KIND = "wikichain"   # reserved verifier kind lane D registers; not an LLM-facing kind


def parse_wiki_uri(uri: str) -> tuple[str, str] | None:
    """wiki://<page>#<claim-id> -> (page, claim_id), or None if it is not a wiki URI.

    A pyramid claim (level >= 2) cites this in its `evidence` field; lane D's verifier resolves it:
    the cited claim must exist, be non-stale, and carry verdict TRUE.
    """
    if not uri or not uri.startswith(WIKI_SCHEME):
        return None
    body = uri[len(WIKI_SCHEME):]
    page, sep, claim_id = body.partition("#")
    if not sep or not page or not claim_id:
        return None
    return page, claim_id


# ---------------------------------------------------------------- CLI registration seam

# Each lane module exposes `register_cli(subparsers)` to add its subcommand(s). cli.main() calls
# them in a loop (written ONCE in P0), so no lane ever edits cli.py again. A registrar takes the
# argparse subparsers object and calls add_parser(...).set_defaults(func=...). See cli.py.
CliRegistrar = Callable[[object], None]
