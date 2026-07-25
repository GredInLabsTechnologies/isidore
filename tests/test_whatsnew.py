"""isidore whatsnew: the typed surface delta, its artifact, and the verification discipline of the
prose tier. Real git repositories in tmp_path; the LLM is always injected and counted."""
from __future__ import annotations

import json
import shutil
import subprocess

import pytest

from isidore.render import WIKI_DIRNAME
from isidore.whatsnew import (
    FILE_ADDED,
    FILE_REMOVED,
    FILE_RENAMED,
    SIGNATURE_CHANGED,
    SYMBOL_ADDED,
    WhatsnewError,
    build_delta,
    impact_summary,
    parse_plain_block,
    render_whatsnew_md,
    render_whatsnew_toon,
    run_whatsnew,
    strip_inline_claim_rows,
    surface_verify_ctx,
)

PAGE = """Bullets about the change.

- `GICSClient.put_many_conditional` is new — see `client.py:5`.

```isidore-claims
client.py defines put_many_conditional | client.py:5 | defines:client.py;put_many_conditional
```
"""


def _git(path, *args):
    subprocess.run(["git", *args], cwd=path, check=True, capture_output=True)


def _commit(repo, message):
    _git(repo, "add", "-A")
    _git(repo, "-c", "user.email=t@t", "-c", "user.name=t", "commit", "-m", message, "--no-gpg-sign")
    out = subprocess.run(["git", "rev-parse", "HEAD"], cwd=repo, check=True, capture_output=True,
                         encoding="utf-8")
    return out.stdout.strip()


@pytest.fixture()
def repo(tmp_path):
    """A repository mirroring the shape of the change that motivated this command: a method added to
    an existing class (Python AND TypeScript), a brand-new file, a changed signature, a deletion and
    a rename."""
    if shutil.which("git") is None:
        pytest.skip("git not available")
    root = tmp_path / "proj"
    root.mkdir()
    _git(root, "init", "-q")

    (root / "client.py").write_text(
        "class GICSClient:\n"
        "    def put(self, key):\n"
        "        return key\n",
        encoding="utf-8")
    (root / "node.ts").write_text(
        "export class NodeClient {\n"
        "    async put(key: string): Promise<void> {}\n"
        "}\n",
        encoding="utf-8")
    (root / "old.py").write_text("def gone():\n    pass\n", encoding="utf-8")
    (root / "util.py").write_text("def helper(a):\n    return a\n", encoding="utf-8")
    base = _commit(root, "base")

    (root / "client.py").write_text(
        "class GICSClient:\n"
        "    def put(self, key, verify=False):\n"
        "        return key\n"
        "\n"
        "    def put_many_conditional(self, conditions, records):\n"
        "        return None\n",
        encoding="utf-8")
    (root / "node.ts").write_text(
        "export class NodeClient {\n"
        "    async put(key: string): Promise<void> {}\n"
        "\n"
        "    async putManyConditional(\n"
        "        conditions: Condition[],\n"
        "        options: Options = {},\n"
        "    ): Promise<Result> {\n"
        "        return this.rpc('putManyConditional');\n"
        "    }\n"
        "}\n",
        encoding="utf-8")
    (root / "version.py").write_text("VERSION = '1.5.2'\n", encoding="utf-8")
    (root / "old.py").unlink()
    _git(root, "mv", "util.py", "helpers.py")
    head = _commit(root, "feat: conditional batch")
    return root, base, head


# ------------------------------------------------------------------ the delta (0 LLM)

def test_delta_reports_exactly_the_real_changes_and_invents_nothing(repo):
    root, base, _head = repo
    delta = build_delta(root, base)
    found = {(e.kind, e.qualname or e.file) for e in delta.entries}

    assert (SYMBOL_ADDED, "GICSClient.put_many_conditional") in found
    assert (SYMBOL_ADDED, "NodeClient.putManyConditional") in found
    assert (FILE_ADDED, "version.py") in found
    assert (SYMBOL_ADDED, "VERSION") in found
    assert (SIGNATURE_CHANGED, "GICSClient.put") in found
    assert (FILE_REMOVED, "old.py") in found
    assert (FILE_RENAMED, "helpers.py") in found

    # Anti-invention: every reported symbol belongs to a file that really changed.
    assert {e.file for e in delta.entries} <= set(delta.changed_files)
    # An untouched symbol is never reported.
    assert not [e for e in delta.entries if e.qualname == "NodeClient.put"]


def test_signature_change_records_both_sides(repo):
    root, base, _head = repo
    changed = [e for e in build_delta(root, base).entries if e.kind == SIGNATURE_CHANGED]
    entry = next(e for e in changed if e.qualname == "GICSClient.put")
    assert "verify=False" in entry.sig
    assert "verify=False" not in entry.old_sig


def test_multiline_typescript_signature_is_cited_at_its_declaration(repo):
    root, base, _head = repo
    entry = next(e for e in build_delta(root, base).entries
                 if e.qualname == "NodeClient.putManyConditional")
    line = (root / "node.ts").read_text(encoding="utf-8").splitlines()[entry.line - 1]
    assert line.strip().startswith("async putManyConditional")
    assert "Options = {}" in entry.sig          # brace-bearing default must not defeat the matcher


def test_rename_maps_to_the_new_path(repo):
    root, base, _head = repo
    entry = next(e for e in build_delta(root, base).entries if e.kind == FILE_RENAMED)
    assert entry.file == "helpers.py" and entry.old_file == "util.py"


def test_deleted_file_is_reported_but_carries_no_line_to_cite(repo):
    root, base, _head = repo
    entry = next(e for e in build_delta(root, base).entries if e.kind == FILE_REMOVED)
    assert entry.file == "old.py"
    assert entry.evidence == "old.py"          # no `:line` — there is nothing to point at anymore


def test_empty_range_is_valid_and_not_an_error(repo):
    root, _base, head = repo
    delta = build_delta(root, head, head)
    assert delta.entries == []
    assert "Nothing changed" in render_whatsnew_md(delta)


# ------------------------------------------------------------------ readable by anyone

def test_impact_summary_answers_do_i_have_to_do_anything_without_jargon(repo):
    root, base, _head = repo
    lines = " ".join(impact_summary(build_delta(root, base)))

    # The range removes `gone()` and reshapes `GICSClient.put`, so the honest answer is "yes".
    assert "taken away" in lines or "differently" in lines
    assert "may need updating" in lines
    # A non-technical reader must not meet a single identifier, path or programming term here.
    for jargon in ("()", ".py", ":", "method", "class", "parameter", "signature", "symbol"):
        assert jargon not in lines


def test_impact_summary_says_so_when_nothing_can_break(tmp_path):
    if shutil.which("git") is None:
        pytest.skip("git not available")
    root, base = _one_file_repo(tmp_path)          # this fixture only ADDS a method
    lines = " ".join(impact_summary(build_delta(root, base)))
    assert "Nothing was taken away" in lines
    assert "keeps working as before" in lines


def test_page_is_layered_so_a_non_technical_reader_can_stop_after_the_top(repo):
    root, base, _head = repo
    page = render_whatsnew_md(build_delta(root, base))
    plain_at = page.index("## In plain words")
    detail_at = page.index("## Every change, in detail")

    assert plain_at < detail_at                     # plain words lead; paths and signatures follow
    assert ".py:" not in page[plain_at:detail_at]   # nothing technical leaks into the top section
    assert "checked against the code by machine" in page    # how to trust it, in plain words


def test_plain_language_block_is_dropped_when_it_comes_back_as_jargon():
    _rest, plain, broken = parse_plain_block(
        "```isidore-plain\nThe method's parameter is now optional.\n```")
    # Silence beats a "plain" summary a non-programmer still cannot read — and the rejection says
    # WHICH rule caught it, so the failure can be argued with instead of just observed.
    assert plain == ""
    assert "jargon-term" in broken

    _rest, good, none_broken = parse_plain_block(
        "```isidore-plain\nSaving a batch of records can now be made conditional, so two people "
        "editing at once no longer overwrite each other.\n```")
    assert good.startswith("Saving a batch")
    assert none_broken == []


def test_plain_language_summary_reaches_the_page_and_the_rejection_is_counted(tmp_path):
    if shutil.which("git") is None:
        pytest.skip("git not available")
    root, base = _one_file_repo(tmp_path)
    answer = (
        "```isidore-plain\n"
        "Records can now be saved as a group only when the data still looks as expected.\n"
        "```\n\n- Added `put_many_conditional` — `client.py:5`.\n"
    )
    result = run_whatsnew(root, base, execute=True, generator=lambda p: answer)
    page = result.page_path.read_text(encoding="utf-8")

    assert "Records can now be saved as a group" in page
    assert page.index("Records can now be saved") < page.index("## Every change, in detail")
    assert result.plain_rejected == 0

    jargon = "```isidore-plain\nThe class exposes a new method parameter.\n```\n\n- a bullet\n"
    assert run_whatsnew(root, base, execute=True, generator=lambda p: jargon).plain_rejected == 1


def test_agents_get_the_same_delta_as_a_toon_sidecar(repo):
    root, base, _head = repo
    result = run_whatsnew(root, base)
    toon = result.toon_path.read_text(encoding="utf-8")

    # Same facts, machine shape: an agent should never have to parse the prose to recover the rows.
    assert "api[" in toon and "GICSClient.put_many_conditional" in toon
    assert result.toon_path.suffix == ".toon"


def test_unresolvable_ref_fails_closed(repo):
    root, _base, _head = repo
    with pytest.raises(WhatsnewError):
        build_delta(root, "no-such-ref")


def test_generated_wiki_and_docs_are_not_mistaken_for_source(repo):
    root, base, _head = repo
    (root / WIKI_DIRNAME).mkdir(exist_ok=True)
    (root / WIKI_DIRNAME / "page.md").write_text("# generated\n", encoding="utf-8")
    (root / "notes.md").write_text("# notes\n", encoding="utf-8")
    _commit(root, "docs + wiki")

    delta = build_delta(root, base)
    assert not [e for e in delta.entries if e.file.startswith(f"{WIKI_DIRNAME}/")]
    assert [e for e in delta.entries if e.file == "notes.md" and e.area == "docs"]


def test_paths_with_spaces_and_unicode_survive_the_nul_parse(repo):
    root, base, _head = repo
    (root / "módulo con espacio.py").write_text("def añadido():\n    pass\n", encoding="utf-8")
    _commit(root, "unicode path")

    delta = build_delta(root, base)
    assert any(e.file == "módulo con espacio.py" and e.qualname == "añadido"
               for e in delta.entries)


def test_test_files_are_reported_in_their_own_area(repo):
    root, base, _head = repo
    (root / "tests").mkdir()
    (root / "tests" / "test_thing.py").write_text("def test_thing():\n    pass\n", encoding="utf-8")
    _commit(root, "tests")

    delta = build_delta(root, base)
    assert all(e.area == "tests" for e in delta.entries if e.file.startswith("tests/"))
    assert "test_thing" not in render_whatsnew_toon(delta, public_only=True)


# ------------------------------------------------------------------ artifact + certificate

def test_run_writes_a_deterministic_page_and_certificate_without_calling_the_model(repo):
    root, base, _head = repo
    result = run_whatsnew(root, base, generator=lambda p: pytest.fail("must not call the LLM"))

    assert result.page_path.is_file() and result.cert_path.is_file()
    assert result.calls == 0
    first = result.page_path.read_bytes()

    page = first.decode("utf-8")
    assert "put_many_conditional" in page and "version.py" in page

    run_whatsnew(root, base, generator=lambda p: pytest.fail("must not call the LLM"))
    assert result.page_path.read_bytes() == first      # no wall-clock -> byte-identical re-runs

    cert = json.loads(result.cert_path.read_text(encoding="utf-8"))
    assert cert["graph_commit"] == subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=root, check=True, capture_output=True,
        encoding="utf-8").stdout.strip()
    assert cert["prose_sha256"]


def test_artifact_lives_outside_the_page_state_and_the_verify_glob(repo):
    root, base, _head = repo
    result = run_whatsnew(root, base)
    # `isidore verify` globs wiki/*.md non-recursively; a range snapshot must not join that loop,
    # nor the staleness loop that would slowly mark it stale as the code moves past the range.
    assert result.page_path.parent.name == "whatsnew"
    assert not (root / WIKI_DIRNAME / ".isidore-state.json").exists()


def test_verify_context_knows_methods_that_the_repository_graph_cannot_see(repo):
    root, base, _head = repo
    ctx = surface_verify_ctx(root, build_delta(root, base))
    labels = {n["label"] for n in ctx.nodes if n.get("source_file") == "client.py"}
    # The repo scanner only emits top-level symbols; without these synthesised nodes a claim about
    # a class method would be judged FALSE and wrongly refuted.
    assert "put_many_conditional()" in labels


# ------------------------------------------------------------------ prose tier (--execute)

def test_execute_publishes_a_verified_claim(tmp_path):
    if shutil.which("git") is None:
        pytest.skip("git not available")
    root = tmp_path / "p"
    root.mkdir()
    _git(root, "init", "-q")
    (root / "client.py").write_text("class C:\n    def old(self):\n        pass\n", encoding="utf-8")
    base = _commit(root, "base")
    (root / "client.py").write_text(
        "class C:\n"
        "    def old(self):\n"
        "        pass\n"
        "\n"
        "    def put_many_conditional(self, conditions):\n"
        "        return None\n", encoding="utf-8")
    _commit(root, "add method")

    result = run_whatsnew(root, base, execute=True, generator=lambda p: PAGE)
    assert result.calls == 1
    assert result.claims_published == 1
    assert result.claims_refuted == 0

    cert = json.loads(result.cert_path.read_text(encoding="utf-8"))
    claim = cert["claims"][0]
    assert claim["verdict"] == "TRUE"
    assert claim["evidence"].startswith("client.py:")


def _one_file_repo(tmp_path):
    root = tmp_path / "p"
    root.mkdir()
    _git(root, "init", "-q")
    (root / "client.py").write_text("class C:\n    def old(self):\n        pass\n", encoding="utf-8")
    base = _commit(root, "base")
    (root / "client.py").write_text(
        "class C:\n    def old(self):\n        pass\n\n"
        "    def put_many_conditional(self, conditions):\n        return None\n", encoding="utf-8")
    _commit(root, "add method")
    return root, base


def test_a_false_predicate_is_kept_in_the_certificate_but_never_published(tmp_path):
    if shutil.which("git") is None:
        pytest.skip("git not available")
    root, base = _one_file_repo(tmp_path)
    wrong = PAGE.replace("defines:client.py;put_many_conditional",
                         "defines:client.py;method_that_does_not_exist")
    result = run_whatsnew(root, base, execute=True, generator=lambda p: wrong)

    assert result.claims_refuted == 1
    assert result.claims_published == 0
    cert = json.loads(result.cert_path.read_text(encoding="utf-8"))
    assert cert["claims"][0]["verdict"] == "FALSE"        # audit trail survives; the claim does not


def test_a_phantom_path_earns_one_repair_attempt_then_a_visible_quarantine(tmp_path):
    if shutil.which("git") is None:
        pytest.skip("git not available")
    root, base = _one_file_repo(tmp_path)
    ghost = "See `does/not/exist.py:1` for details.\n"
    prompts: list[str] = []

    def generator(prompt):
        prompts.append(prompt)
        return ghost

    result = run_whatsnew(root, base, execute=True, generator=generator)
    assert len(prompts) == 2
    assert "does/not/exist.py" in prompts[1]              # the repair names the phantom path
    assert result.retries == 1
    assert result.quarantined is True
    assert "isidore: path not found" in result.page_path.read_text(encoding="utf-8")


def test_absence_and_out_of_range_claims_are_dropped_before_anchoring(tmp_path):
    if shutil.which("git") is None:
        pytest.skip("git not available")
    root, base = _one_file_repo(tmp_path)
    (root / "untouched.py").write_text("X = 1\n", encoding="utf-8")
    page = (
        "- something\n\n"
        "```isidore-claims\n"
        "there is no retry logic in the client | client.py:1 |\n"
        "untouched.py declares X | untouched.py:1 |\n"
        "```\n"
    )
    result = run_whatsnew(root, base, execute=True, generator=lambda p: page)
    # First is an absence claim (unanchorable); second cites a file outside the range, which this
    # artifact cannot prove either way.
    assert result.claims_dropped == 2
    assert result.claims_published == 0


def test_prose_never_sees_a_raw_diff_and_is_told_hints_are_not_evidence(tmp_path):
    if shutil.which("git") is None:
        pytest.skip("git not available")
    root, base = _one_file_repo(tmp_path)
    prompts: list[str] = []
    run_whatsnew(root, base, execute=True,
                 generator=lambda p: prompts.append(p) or "- a bullet\n")

    prompt = prompts[0]
    assert "SURFACE CHANGES" in prompt
    assert "NOT evidence" in prompt
    assert "add method" in prompt                        # the commit subject rides as a hint
    assert "@@" not in prompt and "+++ " not in prompt   # never a unified diff


def test_execute_refuses_a_range_that_does_not_end_at_head(repo):
    root, base, head = repo
    (root / "client.py").write_text("class GICSClient:\n    pass\n", encoding="utf-8")
    _commit(root, "later work")                          # HEAD has now moved past `head`
    # Claims anchor to the working tree, so prose about an older `--until` could not be verified.
    with pytest.raises(WhatsnewError, match="HEAD"):
        run_whatsnew(root, base, until=head, execute=True, generator=lambda p: PAGE)


def test_execute_refuses_an_off_head_range_even_when_it_is_empty(repo):
    root, _base, head = repo
    (root / "client.py").write_text("class GICSClient:\n    pass\n", encoding="utf-8")
    _commit(root, "later work")
    # An impossible request must fail on its own terms, not silently succeed because the range
    # happened to be empty.
    with pytest.raises(WhatsnewError, match="HEAD"):
        run_whatsnew(root, head, until=head, execute=True, generator=lambda p: PAGE)


def test_machine_syntax_never_leaks_into_the_page(tmp_path):
    if shutil.which("git") is None:
        pytest.skip("git not available")
    root, base = _one_file_repo(tmp_path)
    # Observed against a real provider: the model echoes the claim row inline after its own bullet.
    echoed = (
        "- Added `put_many_conditional` for conditional batches. | `client.py:5` | "
        "`defines:client.py;put_many_conditional`\n"
        "\n```isidore-claims\n"
        "client.py defines put_many_conditional | client.py:5 | defines:client.py;put_many_conditional\n"
        "```\n"
    )
    result = run_whatsnew(root, base, execute=True, generator=lambda p: echoed)
    page = result.page_path.read_text(encoding="utf-8")

    assert "Added `put_many_conditional` for conditional batches." in page
    assert "defines:client.py" not in page          # the predicate belongs in the certificate
    assert result.claims_published == 1             # ...where it still lives, verified


def test_a_bare_trailing_citation_is_stripped_too():
    # The second shape the same instinct produced on a later live run: one pipe, no predicate.
    cleaned = strip_inline_claim_rows("- Added instance handling. | gicsd-node/src/instance.rs:1")
    assert cleaned == "- Added instance handling."


def test_a_real_markdown_table_is_left_alone():
    table = "| symbol | where |\n|---|---|\n| `f` | `a.py:1` |"
    assert strip_inline_claim_rows(table) == table


def test_cli_smoke(repo, capsys):
    from isidore.cli import main
    root, base, _head = repo
    assert main(["whatsnew", "--since", base, "--repo", str(root)]) == 0
    assert "isidore whatsnew" in capsys.readouterr().out


def test_cli_reports_a_bad_ref_without_writing_an_artifact(repo, capsys):
    from isidore.cli import main
    root, _base, _head = repo
    assert main(["whatsnew", "--since", "nope", "--repo", str(root)]) == 2
    assert not (root / WIKI_DIRNAME / "whatsnew").exists()
