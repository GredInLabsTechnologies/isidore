"""Lane B (part 2) — claim->contract graduation + `isidore contracts`. (T-8dfc)

A typed claim a human promotes becomes an invariant that `isidore verify --contracts` enforces in
CI. This module owns promotion, the gate, and the CLI.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path
from datetime import datetime, timezone

from . import pcp
from .pcp import (
    Contract,
    VerifyContext,
    Verdict,
    undecidable,
)
from .toon import encode


def verify_contracts(contracts: list[Contract], ctx: VerifyContext) -> list[tuple[Contract, Verdict]]:
    """Check every promoted contract against the current graph. Pure, 0-LLM."""
    results: list[tuple[Contract, Verdict]] = []
    for c in contracts:
        pred = pcp.parse_predicate(c.predicate)
        if pred is None:
            results.append((c, undecidable(f"malformed predicate: {c.predicate}")))
        else:
            verdict = pcp.verify_predicate(pred, ctx)
            results.append((c, verdict))
    return results


def register_cli(sub) -> None:
    """Add `isidore contracts` (promote / list / check)."""
    p = sub.add_parser("contracts", help="promote a claim to a CI-enforced invariant, or list them")
    p.add_argument("--repo", type=Path, default=Path("."))
    p.add_argument("--promote", default=None, metavar="CLAIM_ID",
                   help="promote the claim with this id to a contract (human, audited)")
    p.add_argument("--list", action="store_true", help="list promoted contracts")
    p.set_defaults(func=_cmd_contracts)


def _cmd_contracts(args) -> int:
    """Command implementation for `isidore contracts`."""
    wiki_dir = args.repo / "wiki"

    if args.promote:
        claim_id = args.promote.strip()
        # Scan cert files in wiki/ to find the claim
        certs = list(wiki_dir.glob("**/*.cert.json"))
        target_claim = None
        for path in certs:
            try:
                cert = pcp.read_certificate(path)
                for c in cert.claims:
                    if c.id == claim_id:
                        target_claim = c
                        break
            except Exception:
                continue
            if target_claim:
                break

        if not target_claim:
            print(f"ERROR: claim '{claim_id}' not found in any certificate in '{wiki_dir}'", file=sys.stderr)
            return 1

        # Load existing contracts
        contracts_path = wiki_dir / pcp.CONTRACTS_FILENAME
        try:
            contracts = pcp.read_contracts(contracts_path)
        except Exception as exc:
            print(f"ERROR: loading contracts failed: {exc}", file=sys.stderr)
            return 1

        # Check if already promoted
        if any(c.id == claim_id for c in contracts):
            print(f"Contract '{claim_id}' is already promoted.")
            return 0

        # Promote claim
        new_contract = Contract(
            id=target_claim.id,
            predicate=target_claim.predicate,
            evidence=target_claim.evidence,
            promoted_by=os.environ.get("AGORA_ACTOR", "human"),
            promoted_at=datetime.now(timezone.utc).isoformat(),
            note=target_claim.statement
        )
        contracts.append(new_contract)

        try:
            wiki_dir.mkdir(parents=True, exist_ok=True)
            pcp.write_contracts(contracts, contracts_path)
            print(f"ACCEPTED contract.promote {claim_id} · promoted to contracts.json")
            return 0
        except Exception as exc:
            print(f"ERROR: writing contracts failed: {exc}", file=sys.stderr)
            return 1

    if args.list:
        contracts_path = wiki_dir / pcp.CONTRACTS_FILENAME
        try:
            contracts = pcp.read_contracts(contracts_path)
        except Exception as exc:
            print(f"ERROR: loading contracts failed: {exc}", file=sys.stderr)
            return 1

        if not contracts:
            print("[isidore] no contracts promoted yet.")
            return 0

        rows = []
        for c in contracts:
            rows.append({
                "id": c.id,
                "predicate": c.predicate,
                "evidence": c.evidence,
                "promoted_by": c.promoted_by,
                "promoted_at": c.promoted_at
            })
        print(encode(("contracts", ["id", "predicate", "evidence", "promoted_by", "promoted_at"], rows)))
        return 0

    print("ERROR: specify either --promote <id> or --list", file=sys.stderr)
    return 0
