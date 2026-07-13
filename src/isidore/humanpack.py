"""Lane E — the human pack: `isidore render`, self-contained HTML + PDF, 0 LLM. (T-b046)

Named humanpack.py, NOT render.py — render.py already exists (quickstart/index.toon/AGENTS block)
and lane E must not collide with it. The CLI command is `isidore render`.

Renders a beautiful, consumable onboarding pack from ALREADY-COMPILED artifacts (pages + claims +
*.cert.json + graph.json + contracts.json): cover, SVG architecture map, reading path, per-sentence
confidence via a verified-mass bar (green/yellow/gray), security banners, glossary, active contracts,
and an Ágora task-board placeholder. Deterministic: same input -> same output. MUST NOT import llm.py
(I12; a test guards this). PDF is print-CSS off the same HTML — no hard dependency on a binary.

Drafted by the pool (qwen3-coder:480b, T-b046) against the frozen seam; reviewed and integrated by
claude-agora (import fix, dead-import cleanup, CLI preservation, anchor ids, honest PDF note).
"""
from __future__ import annotations

import html
from pathlib import Path

from .graph import load_graph
from .pcp import (
    GRAY,
    GREEN,
    YELLOW,
    Certificate,
    ClaimVerdict,
    Contract,
    Mark,
    VerifiedMass,
    read_certificate,
    read_contracts,
)


def _esc(text: str) -> str:
    """HTML-escape untrusted content (statements, reasons, labels) so a page can't inject markup."""
    return html.escape(text or "")


def minimal_markdown_to_html(md_text: str) -> str:
    """Deterministic, dependency-free markdown subset: headings, code fences, lists, paragraphs."""
    lines = md_text.splitlines()
    out: list[str] = []
    in_code = False
    in_list = False
    for line in lines:
        if line.startswith("```"):
            if in_list:
                out.append("</ul>")
                in_list = False
            out.append("</code></pre>" if in_code else "<pre><code>")
            in_code = not in_code
            continue
        if in_code:
            out.append(_esc(line))
            continue
        if line.startswith("# "):
            out.append(f"<h1>{_esc(line[2:])}</h1>")
        elif line.startswith("## "):
            out.append(f"<h2>{_esc(line[3:])}</h2>")
        elif line.startswith("### "):
            out.append(f"<h3>{_esc(line[4:])}</h3>")
        elif line.startswith("- "):
            if not in_list:
                out.append("<ul>")
                in_list = True
            out.append(f"<li>{_esc(line[2:])}</li>")
        else:
            if in_list:
                out.append("</ul>")
                in_list = False
            if line.strip():
                out.append(f"<p>{_esc(line)}</p>")
    if in_list:
        out.append("</ul>")
    if in_code:
        out.append("</code></pre>")
    return "".join(out)


def _verdict_color(verdict: str) -> str:
    if verdict == "TRUE":
        return GREEN
    if verdict == "FALSE":
        return "red"
    return GRAY


def format_mark(mark: Mark) -> str:
    return f"{_esc(mark.file)}:{mark.line} — {_esc(mark.reason)}"


def generate_security_banner(marks: list[Mark]) -> str:
    danger = [m for m in marks if m.severity == "danger"]
    if not danger:
        return ""
    items = "".join(f"<li>{format_mark(m)}</li>" for m in danger)
    return (f'<div class="security-banner"><h3>Security marks — verify before trusting</h3>'
            f'<ul>{items}</ul></div>')


def generate_mass_bar(mass: VerifiedMass) -> str:
    total = mass.total
    if total == 0:
        return '<div class="mass-bar"><div class="segment gray" style="width:100%"></div></div>'
    seg = []
    for cls, n in ((GREEN, mass.green), (YELLOW, mass.yellow), (GRAY, mass.gray)):
        if n:
            seg.append(f'<div class="segment {cls}" style="width:{round(n / total * 100, 2)}%"></div>')
    return f'<div class="mass-bar">{"".join(seg)}</div>'


def generate_claims_table(claims: list[ClaimVerdict]) -> str:
    if not claims:
        return "<p>No claims verified for this page.</p>"
    rows = []
    for c in claims:
        dot = f'<span class="dot {_verdict_color(c.verdict)}"></span>'
        rows.append(f"<tr><td>{dot}</td><td>{_esc(c.statement)}</td><td>{_esc(c.verdict)}</td>"
                    f"<td><code>{_esc(c.evidence)}</code></td></tr>")
    return ('<table class="claims-table"><thead><tr><th>status</th><th>statement</th>'
            f'<th>verdict</th><th>evidence</th></tr></thead><tbody>{"".join(rows)}</tbody></table>')


def generate_glossary(nodes: list[dict]) -> str:
    symbols = {}
    for n in nodes:
        label, src = n.get("label", ""), n.get("source_file", "")
        loc = (n.get("source_location") or "").lstrip("L").split("-")[0]
        if label and src:
            symbols[label] = f"{src}:{loc}" if loc else src
    if not symbols:
        return "<p>No symbols found.</p>"
    rows = "".join(f"<tr><td><code>{_esc(k)}</code></td><td>{_esc(v)}</td></tr>"
                   for k, v in sorted(symbols.items()))
    return f'<table class="glossary"><thead><tr><th>symbol</th><th>location</th></tr></thead><tbody>{rows}</tbody></table>'


def generate_contracts_section(contracts: list[Contract]) -> str:
    if not contracts:
        return "<p>No contracts promoted yet.</p>"
    rows = "".join(
        f"<tr><td><code>{_esc(c.id)}</code></td><td><code>{_esc(c.predicate)}</code></td>"
        f"<td><code>{_esc(c.evidence)}</code></td><td>{_esc(c.promoted_by)}</td></tr>"
        for c in contracts)
    return ('<table class="contracts-table"><thead><tr><th>id</th><th>predicate</th>'
            f'<th>evidence</th><th>promoted by</th></tr></thead><tbody>{rows}</tbody></table>')


def generate_architecture_map(nodes: list[dict], links: list[dict]) -> str:
    """Deterministic inline SVG: modules (top dir of source_file) as boxes, imports as lines."""
    modules: dict[str, list[dict]] = {}
    for n in nodes:
        src = n.get("source_file", "")
        if src:
            top = src.split("/")[0] if "/" in src else src
            modules.setdefault(top, []).append(n)
    if not modules:
        return "<p>No architecture data available.</p>"
    id_to_module = {n["id"]: top for top, ns in modules.items() for n in ns if "id" in n}
    box_w, box_h, gap = 200, 90, 60
    pos: dict[str, tuple[int, int]] = {}
    boxes = []
    for i, (name, ns) in enumerate(modules.items()):
        x = 30 + (i % 3) * (box_w + gap)
        y = 30 + (i // 3) * (box_h + gap)
        pos[name] = (x + box_w // 2, y + box_h // 2)
        boxes.append(
            f'<rect x="{x}" y="{y}" width="{box_w}" height="{box_h}" rx="6" class="mod-box"/>'
            f'<text x="{x + 10}" y="{y + 24}" class="mod-title">{_esc(name)}</text>'
            f'<text x="{x + 10}" y="{y + 46}" class="mod-sub">{len(ns)} symbol(s)</text>')
    seen = set()
    lines = []
    for link in links:
        if link.get("relation") != "imports":
            continue
        a, b = id_to_module.get(link.get("source")), id_to_module.get(link.get("target"))
        if a and b and a != b and (key := tuple(sorted((a, b)))) not in seen:
            seen.add(key)
            (x1, y1), (x2, y2) = pos[a], pos[b]
            lines.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" class="mod-link"/>')
    rows = (len(modules) + 2) // 3
    height = 60 + rows * (box_h + gap)
    return (f'<svg viewBox="0 0 720 {height}" class="arch-map" xmlns="http://www.w3.org/2000/svg">'
            f'{"".join(lines)}{"".join(boxes)}</svg>')


def render_page(cert: Certificate, md_content: str) -> str:
    return (f'<section class="page" id="{_esc(cert.page)}"><h2>{_esc(cert.page)}</h2>'
            f'{generate_security_banner(cert.marks)}{generate_mass_bar(cert.mass)}'
            f'<div class="content">{minimal_markdown_to_html(md_content)}</div>'
            f'<h3>Verified claims</h3>{generate_claims_table(cert.claims)}</section>')


_CSS = """
:root{--bg:#fff;--fg:#1a1a1a;--muted:#666;--bd:#ddd;--green:#1D9E75;--yellow:#EF9F27;--gray:#9e9e9e;--danger:#A32D2D}
@media(prefers-color-scheme:dark){:root{--bg:#121212;--fg:#eaeaea;--muted:#aaa;--bd:#333}}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:var(--bg);color:var(--fg);margin:0;padding:24px;line-height:1.6;max-width:900px;margin:0 auto}
.cover{text-align:center;padding:32px 0;border-bottom:1px solid var(--bd);margin-bottom:24px}
.legend{background:rgba(128,128,128,.08);padding:16px;border-radius:8px;margin:16px 0}
.legend-item{margin:6px 0}
.security-banner{background:var(--danger);color:#fff;padding:14px;border-radius:8px;margin:14px 0}
.mass-bar{display:flex;height:14px;border:1px solid var(--bd);border-radius:4px;overflow:hidden;margin:12px 0}
.segment{height:100%}.segment.green{background:var(--green)}.segment.yellow{background:var(--yellow)}.segment.gray{background:var(--gray)}
.dot{display:inline-block;width:11px;height:11px;border-radius:50%;margin-right:6px;vertical-align:middle}
.dot.green{background:var(--green)}.dot.yellow{background:var(--yellow)}.dot.gray{background:var(--gray)}.dot.red{background:var(--danger)}
table{width:100%;border-collapse:collapse;margin:12px 0}th,td{text-align:left;padding:8px;border-bottom:1px solid var(--bd);font-size:14px}
pre{background:rgba(128,128,128,.08);padding:12px;border-radius:6px;overflow-x:auto}code{font-family:Consolas,Menlo,monospace;font-size:13px}
a{color:var(--green)}.page{margin:28px 0;padding-top:8px;border-top:1px solid var(--bd)}
.arch-map{width:100%;height:auto;border:1px solid var(--bd);border-radius:8px;margin:16px 0}
.mod-box{fill:rgba(29,158,117,.12);stroke:var(--green);stroke-width:1}.mod-title{font:600 14px sans-serif;fill:var(--fg)}.mod-sub{font:12px sans-serif;fill:var(--muted)}
.mod-link{stroke:var(--muted);stroke-width:1.5}
@media print{body{padding:0;max-width:none}@page{margin:2cm}.page{break-inside:avoid}}
"""


def render_pack(artifacts_dir: Path, out_dir: Path, *, pdf: bool = False) -> Path:
    """Render the human pack from compiled artifacts into out_dir. Returns the path to index.html.

    Deterministic, 0-LLM. `pdf=True` writes print-optimized HTML (the @page CSS is always present);
    a real PDF needs an external print engine, so we emit print-ready HTML and note it honestly.
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    pages = []
    for md_file in sorted(artifacts_dir.glob("*.md")):
        cert_file = md_file.parent / (md_file.name + ".cert.json")
        if cert_file.is_file():
            try:
                pages.append((md_file, read_certificate(cert_file)))
            except ValueError:
                continue

    def _key(item):
        name = item[0].stem.lower()
        return (0, name) if name in ("readme", "overview", "product", "index") else (1, name)
    pages.sort(key=_key)

    contracts_file = artifacts_dir / "contracts.json"
    contracts = read_contracts(contracts_file) if contracts_file.is_file() else []

    graph_path = artifacts_dir.parent / ".isidore" / "graph.json"
    try:
        nodes, links, commit = load_graph(graph_path) if graph_path.is_file() else ([], [], None)
    except Exception:
        nodes, links, commit = [], [], None

    g = y = gr = 0
    page_html = []
    for md_file, cert in pages:
        page_html.append(render_page(cert, md_file.read_text(encoding="utf-8")))
        g, y, gr = g + cert.mass.green, y + cert.mass.yellow, gr + cert.mass.gray

    reading = "".join(f'<li><a href="#{_esc(c.page)}">{_esc(c.page)}</a></li>' for _f, c in pages)
    repo_name = artifacts_dir.parent.name
    doc = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{_esc(repo_name)} — isidore pack</title><style>{_CSS}</style></head><body>
<div class="cover"><h1>{_esc(repo_name)}</h1><p>isidore onboarding pack</p>
<p>graph commit <code>{_esc((commit or "?")[:12])}</code> · {g + y + gr} claims
(<span style="color:var(--green)">{g} proved</span> ·
<span style="color:var(--yellow)">{y} anchored</span> · {gr} narrative)</p></div>
<div class="legend"><h3>How to read this</h3>
<div class="legend-item"><span class="dot green"></span> green — proved against the code</div>
<div class="legend-item"><span class="dot yellow"></span> yellow — anchored (existence)</div>
<div class="legend-item"><span class="dot gray"></span> gray — narrative, not load-bearing</div></div>
<h2>Reading path</h2><ul>{reading}</ul>
{"".join(page_html)}
<h2>Active contracts</h2><p>The rules of this house — CI enforces them.</p>{generate_contracts_section(contracts)}
<h2>Architecture map</h2>{generate_architecture_map(nodes, links)}
<h2>Glossary</h2>{generate_glossary(nodes)}
<h2>Ágora task board</h2><p>No task-board data in this pack (Ágora connector not wired here).</p>
</body></html>
"""
    index = out_dir / "index.html"
    index.write_text(doc, encoding="utf-8", newline="\n")
    if pdf:
        (out_dir / "print.html").write_text(doc, encoding="utf-8", newline="\n")
    return index


def register_cli(sub) -> None:
    """Add `isidore render` (build the human onboarding pack)."""
    p = sub.add_parser("render", help="build a self-contained human onboarding pack (HTML/PDF, 0 LLM)")
    p.add_argument("--repo", type=Path, default=Path("."))
    p.add_argument("--out", type=Path, default=Path("isidore-pack"),
                   help="output directory for the pack (default: ./isidore-pack)")
    p.add_argument("--pdf", action="store_true", help="also emit print-ready HTML (print CSS)")
    p.set_defaults(func=_cmd_render)


def _cmd_render(args) -> int:
    from .pipeline import WIKI_DIRNAME
    wiki = args.repo / WIKI_DIRNAME
    if not wiki.is_dir():
        print(f"[isidore] no wiki at {wiki} — run `isidore compile --execute` first")
        return 2
    index = render_pack(wiki, args.out, pdf=args.pdf)
    print(f"[isidore] wrote human pack to {index}")
    return 0
