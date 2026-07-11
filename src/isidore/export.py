"""export-agora — bridge isidore's verified claims into Living-Library card DRAFTS (0 LLM).

Each anchored claim is a machine-checked fact with a `path:line` anchor; a page's OK claims make a
draft card whose `verify_cmd` is `isidore claims --check`, so `agora lib audit` degrades the card
automatically when the code drifts. These are DRAFTS written to an output directory for human review
— nothing is ever posted into a notebook.
"""
from __future__ import annotations

from collections import defaultdict
from pathlib import Path

from .claims import check_claims
from .pipeline import WIKI_DIRNAME, load_state


def _slug(name: str) -> str:
    out = []
    for ch in name.replace("/", "-").replace("\\", "-").replace(".", "_"):
        out.append(ch if (ch.isalnum() or ch in "-_") else "-")
    return "".join(out).strip("-").lower() or "page"


def _yaml_str(s: str) -> str:
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def render_card(module: str, claims: list[dict], *, domain: str, commit: str | None) -> str:
    slug = _slug(module)
    tags = ", ".join(_yaml_str(t) for t in ("isidore", "compiled-claims", module))
    head = [
        "---",
        f"id: isidore-{slug}",
        f"title: {_yaml_str(f'{module} — facts compiled by isidore (draft)')}",
        f"domain: {domain}",
        "type: reference",
        "classification: internal",
        "confidence: verified",
        f"tags: [{tags}]",
        "cost_to_relearn: low",
        "verified_by: isidore",
        f"source_commit: {commit or '?'}",
        "verify_cmd: isidore claims --check --repo .",
        "claims:",
    ]
    for c in claims:
        head.append(f"  - statement: {_yaml_str(c['statement'])}")
        head.append(f"    evidence: {_yaml_str(c['evidence'])}")
    head.append("---")
    body = [
        f"# {module} — facts compiled by isidore (DRAFT — review before posting)",
        "",
        "Auto-extracted from the isidore wiki's anchored claims. Each is machine-checked against its",
        "evidence via `verify_cmd`, so `agora lib audit` degrades this card automatically when the",
        "cited code drifts. **This is a draft — a human curates it before it enters the notebook.**",
        "",
    ]
    body.extend(f"- {c['statement']} — `{c['evidence']}`" for c in claims)
    return "\n".join(head + body) + "\n"


def build_cards(repo: Path, *, domain: str = "code", min_claims: int = 1,
                include_stale: bool = False) -> list[tuple[str, str]]:
    """Return [(filename, content)] draft cards — one per wiki page with enough OK claims."""
    state = load_state(repo / WIKI_DIRNAME)
    pages_state = state.get("pages", {})
    by_page: dict[str, list[dict]] = defaultdict(list)
    for row in check_claims(repo, pages_state):
        if not include_stale and row["state"] != "ok":
            continue
        by_page[row["page"]].append(row)

    cards: list[tuple[str, str]] = []
    for page, claims in sorted(by_page.items()):
        if len(claims) < min_claims:
            continue
        module = pages_state.get(page, {}).get("name", page)
        cards.append((f"isidore-{_slug(module)}.md",
                      render_card(module, claims, domain=domain, commit=state.get("commit"))))
    return cards


def write_cards(cards: list[tuple[str, str]], out_dir: Path) -> list[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    for filename, content in cards:
        dest = out_dir / filename
        dest.write_text(content, encoding="utf-8", newline="\n")
        written.append(dest)
    return written
