"""`isidore handoff` — let the CALLER be the model, instead of shipping the code to one.

Every other provider answers the same question the same way: whose machine does your source code end
up on. A hosted endpoint means someone else's; a FREE hosted endpoint usually means someone else's
training set (measured 2026-07-26: 87 prompts of private source to a free tier that trains by default).

This makes that question disappear. `emit` writes the exact prompts to disk and calls nothing. Whoever
is already reading the repository — the agent in your session, you, a local model — writes the answers
next to them. `apply` feeds those answers back through the ordinary pipeline: same claim parsing, same
quarantine, same certificate, same verification. Isidore never learns who wrote the prose, and the
prose gets no more trust for it.

    isidore handoff emit                 # 0 LLM, 0 network: prompts to wiki/.handoff/
    (something writes <page>.response.md beside each <page>.prompt.md)
    isidore handoff apply                # ingests them exactly as a provider's replies

Responses are matched to pages by a hash of the PROMPT, not by filename order: a stale response from
an earlier run, when the facts have since changed, is refused rather than silently certified.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from .graph import GraphError, find_graph
from .llm import GenerationError
from .pipeline import (
    DEFAULT_MAX_CALLS,
    CompileResult,
    DEFAULT_MAX_PROMPT_CHARS,
    DEFAULT_MIN_SYMBOLS,
    DEFAULT_MODULE_DEPTH,
    DEFAULT_TOP_K_PAGES,
    LINT_REPAIR_ADDENDUM,
    WIKI_DIRNAME,
    compile_wiki,
    load_config,
)

HANDOFF_DIRNAME = ".handoff"
MANIFEST = "manifest.json"
PROMPT_SUFFIX = ".prompt.md"
RESPONSE_SUFFIX = ".response.md"

# Derived, never retyped: the one line that tells a repair round apart from a changed prompt. If the
# gate's wording moves in pipeline.py, this moves with it instead of silently ceasing to match.
REPAIR_MARKER = LINT_REPAIR_ADDENDUM.strip().splitlines()[0]


def handoff_dir(repo: Path) -> Path:
    return repo / WIKI_DIRNAME / HANDOFF_DIRNAME


def prompt_id(prompt: str) -> str:
    """Content identity of a prompt. The pairing key, so a response can only answer the exact prompt
    it was written for."""
    return hashlib.sha256(prompt.encode("utf-8")).hexdigest()[:16]


def _plan(repo: Path, config: dict, args) -> CompileResult:
    """The dry-run plan: which pages are dirty and what prompt each would send. 0 LLM."""
    return compile_wiki(
        repo,
        graph_path=find_graph(repo, getattr(args, "graph", None)),
        execute=False,
        module_depth=config.get("module_depth", DEFAULT_MODULE_DEPTH),
        top_k=config.get("top_k", DEFAULT_TOP_K_PAGES),
        min_symbols=config.get("min_symbols", DEFAULT_MIN_SYMBOLS),
        max_calls=0,                       # plan them ALL; the cap belongs to whoever answers
        max_prompt_chars=config.get("max_prompt_chars", DEFAULT_MAX_PROMPT_CHARS),
        flows_config=config.get("flows", []),
        only=[s for s in (getattr(args, "only", "") or "").split(",") if s.strip()] or None,
    )


def emit(repo: Path, config: dict, args) -> tuple[int, list[str]]:
    """Write one prompt file per dirty page. Returns (count, page names)."""
    from .home import safe_mkdir
    result = _plan(repo, config, args)
    out = handoff_dir(repo)
    safe_mkdir(out)

    # Clear stale prompts: a page that is no longer dirty must not leave an answerable prompt lying
    # around, or the next `apply` certifies a page nobody asked for.
    for old in list(out.glob(f"*{PROMPT_SUFFIX}")) + list(out.glob(f"*{RESPONSE_SUFFIX}")):
        old.unlink()

    manifest = {}
    for name, prompt in result.prompts.items():
        (out / f"{name}{PROMPT_SUFFIX}").write_text(prompt, encoding="utf-8", newline="\n")
        manifest[prompt_id(prompt)] = name
    (out / MANIFEST).write_text(json.dumps(manifest, indent=2), encoding="utf-8", newline="\n")
    return len(manifest), sorted(manifest.values())


def response_generator(repo: Path):
    """A generator that answers from disk. Raises GenerationError when an answer is missing."""
    out = handoff_dir(repo)
    try:
        manifest = json.loads((out / MANIFEST).read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise GenerationError(
            f"no handoff manifest at {out} — run `isidore handoff emit` first") from exc

    def _lookup(prompt: str) -> str | None:
        """The emitted prompt this call is asking about, if any.

        Exact hash first. Failing that, the lint gate's repair round: it appends its correction
        addendum to the ORIGINAL prompt and calls again, so the text no longer hashes to anything.
        There is nobody to ask for a repair here — the answer was written before `apply` ran — so
        the same answer is served back, the gate re-lints it, and the page lands in quarantine with
        its bad citation annotated. Aborting instead would blame the repository for changing and
        take every other page down with it.

        The tail must be the repair addendum and nothing else. A bare prefix match would be a hole:
        facts appended to a page's context produce a longer prompt that still STARTS with the one
        that was answered, and a stale answer would be certified by the very check meant to catch it.
        """
        name = manifest.get(prompt_id(prompt))
        if name is not None:
            return name
        for key, candidate in manifest.items():
            original = out / f"{candidate}{PROMPT_SUFFIX}"
            try:
                text = original.read_text(encoding="utf-8")
            except OSError:
                continue
            if prompt_id(text) != key or not prompt.startswith(text):
                continue
            if prompt[len(text):].lstrip().startswith(REPAIR_MARKER):
                return candidate
        return None

    def _generate(prompt: str) -> str:
        name = _lookup(prompt)
        if name is None:
            # The prompt changed since emit: the facts moved under the answer. Refusing beats
            # certifying prose written against a repository that no longer looks like this.
            raise GenerationError(
                "this page's prompt is not in the handoff manifest — the repository changed since "
                "`handoff emit`. Re-run emit and answer the new prompts.")
        path = out / f"{name}{RESPONSE_SUFFIX}"
        if not path.is_file():
            raise GenerationError(f"no answer written for {name} (expected {path.name})")
        text = path.read_text(encoding="utf-8").strip()
        if not text:
            raise GenerationError(f"the answer for {name} is empty")
        return text

    return _generate


def apply(repo: Path, config: dict, args):
    """Compile using the written answers. Identical pipeline to any other provider."""
    return compile_wiki(
        repo,
        graph_path=find_graph(repo, getattr(args, "graph", None)),
        execute=True,
        generator=response_generator(repo),
        module_depth=config.get("module_depth", DEFAULT_MODULE_DEPTH),
        top_k=config.get("top_k", DEFAULT_TOP_K_PAGES),
        min_symbols=config.get("min_symbols", DEFAULT_MIN_SYMBOLS),
        max_calls=config.get("max_calls", DEFAULT_MAX_CALLS) or 0,
        max_prompt_chars=config.get("max_prompt_chars", DEFAULT_MAX_PROMPT_CHARS),
        flows_config=config.get("flows", []),
        only=[s for s in (getattr(args, "only", "") or "").split(",") if s.strip()] or None,
    )


# ---------------------------------------------------------------- CLI


def register_cli(sub) -> None:
    """Add `isidore handoff emit|apply` (registrar loop in cli.main)."""
    p = sub.add_parser("handoff", help="be the model yourself: emit prompts, answer them, apply (0 network)")
    p.add_argument("action", choices=("emit", "apply"))
    p.add_argument("--repo", type=Path, default=Path("."))
    p.add_argument("--graph", type=Path, default=None)
    p.add_argument("--only", default="", help="comma-separated page filenames to restrict to")
    p.set_defaults(func=_cmd_handoff)


def _cmd_handoff(args) -> int:
    config = load_config(args.repo)
    try:
        if args.action == "emit":
            count, names = emit(args.repo, config, args)
            out = handoff_dir(args.repo)
            if not count:
                print("[isidore] nothing dirty — no prompts written, nothing to answer.")
                return 0
            print(f"[isidore] wrote {count} prompt(s) to {out} (0 LLM, 0 network)")
            for name in names:
                print(f"  {name}{PROMPT_SUFFIX}  ->  answer in {name}{RESPONSE_SUFFIX}")
            print("[isidore] answer each one, then: isidore handoff apply")
            return 0

        result = apply(args.repo, config, args)
    except (FileNotFoundError, GraphError, GenerationError) as exc:
        print(f"ERROR: {exc}")
        return 2

    print(f"[isidore] applied {len(result.generated)} page(s) · "
          f"quarantined: {len(result.quarantined)} · "
          f"claims kept/dropped: {result.claims_total}/{result.claims_dropped}")
    for warning in result.warnings[:10]:
        print(f"  ! {warning}")
    return 0


__all__ = ["HANDOFF_DIRNAME", "apply", "emit", "handoff_dir", "prompt_id", "register_cli",
           "response_generator"]
