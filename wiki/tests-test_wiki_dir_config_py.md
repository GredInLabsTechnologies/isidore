> [!WARNING]
> **SECURITY — deterministic detectors flagged this code (0 LLM). Verify; never document as an intended feature.**
>
> - `tests/test_wiki_dir_config.py:115` — high-entropy literal (>=24 chars, >=3.5 bits/char)
## Purpose
`tests/test_wiki_dir_config.py` tests the repository-level wiki directory configuration — a `wiki_dir` key in a `.isidore.json` file that travels with the repo instead of depending on the operator remembering to export `ISIDORE_WIKI_DIR`. Before this, forgetting the env var once caused the toolchain to guard a nonexistent directory while indexing the real wiki as source — a 13 MB certificate documenting the documentation (`tests/test_wiki_dir_config.py:1-L6`).

## Architecture
The module uses a `no_env` fixture (`tests/test_wiki_dir_config.py:23-L25`) that strips the `WIKI_DIR_ENV` variable so every test starts from a clean state. The helper `_config()` (`tests/test_wiki_dir_config.py:28-L30`) writes a `.isidore.json` with a `wiki_dir` key (or an empty object for `None`). All test functions use `@pytest.mark.usefixtures("no_env")` to guarantee isolation.

## Key entry points
- `no_env()`: Pytest fixture that deletes `WIKI_DIR_ENV` via `monkeypatch` (`tests/test_wiki_dir_config.py:23-L25`).
- `_config()`: Writes a `.isidore.json` with the given `wiki_dir` value (`tests/test_wiki_dir_config.py:28-L30`).
- `test_a_repo_without_a_setting_gets_the_default()`: Asserts `configured_wiki_dirname` returns `DEFAULT_WIKI_DIRNAME` when no config exists (`tests/test_wiki_dir_config.py:34-L35`).
- `test_a_repo_says_where_its_docs_live()`: Asserts setting `wiki_dir: "doc/isidore"` is returned by `configured_wiki_dirname` (`tests/test_wiki_dir_config.py:39-L41`).
- `test_the_setting_is_found_from_a_subdirectory()`: Asserts the config is found by walking up from `src/pkg/inner/` — the case where forgetting the env var used to change the answer (`tests/test_wiki_dir_config.py:45-L51`).
- `test_the_environment_still_wins()`: Asserts `ISIDORE_WIKI_DIR` overrides the repo config, keeping a one-off override possible (`tests/test_wiki_dir_config.py:54-L58`).
- `test_a_config_without_a_usable_value_settles_on_the_default()`: Parametrized over `""`, `"   "`, `None`, `42` — asserts the default is used and a parent repo's setting does not leak into a nested repo (`tests/test_wiki_dir_config.py:63-L70`).

## Dependencies
The module depends on two cross-module imports:
- `src/isidore/render.py` (1 link) — for `CONFIG_FILENAME`, `DEFAULT_WIKI_DIRNAME`, `WIKI_DIR_ENV`, `configured_wiki_dirname` (`tests/test_wiki_dir_config.py:14-L19`).
- `src/isidore/cli.py` (1 link) — imported by the test module.

## How to change safely
1. The `no_env` fixture must strip `WIKI_DIR_ENV` — if new config keys are added, strip their env equivalents there too.
2. `_config()` writes a minimal JSON payload; if the config schema grows, update this helper.
3. The walk-up behavior tested in `test_the_setting_is_found_from_a_subdirectory` is the critical invariant — any change to config lookup must preserve it.
