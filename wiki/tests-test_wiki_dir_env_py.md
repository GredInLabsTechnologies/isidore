## Purpose
The `tests/test_wiki_dir_env.py` module verifies the behavior of the `WIKI_DIRNAME` constant in the `isidore.render` module, which determines the output directory for compiled wiki content. The tests ensure that `WIKI_DIRNAME` correctly resolves from the `ISIDORE_WIKI_DIR` environment variable, defaults to `"wiki"` when unset, and handles nested directory paths properly. This is critical for maintaining consistent wiki output locations across different environments and configurations.

## Architecture
The module uses pytest fixtures and environment patching to test `WIKI_DIRNAME` resolution. The key function `_reload_render()` forces a reload of the `render` module to reflect environment changes, while the test cases verify different scenarios:
- Default resolution when `ISIDORE_WIKI_DIR` is unset (`test_wiki_dirname_defaults_to_wiki`)
- Explicit resolution from `ISIDORE_WIKI_DIR` (`test_wiki_dirname_honors_env`)
- Fallback to default when `ISIDORE_WIKI_DIR` is blank (`test_wiki_dirname_blank_env_falls_back`)
- Directory creation for nested paths (`test_save_state_creates_nested_wiki_dir`)

A `teardown_module` hook ensures the default binding is restored after tests.

## Key entry points
- `_reload_render()`: Reloads the `render` module to apply environment changes.
- `test_wiki_dirname_defaults_to_wiki`: Verifies the default `"wiki"` directory.
- `test_wiki_dirname_honors_env`: Confirms `ISIDORE_WIKI_DIR` overrides the default.
- `test_wiki_dirname_blank_env_falls_back`: Ensures blank env vars fall back to default.
- `test_save_state_creates_nested_wiki_dir`: Validates nested directory creation.

## Dependencies
The module depends on:
- `isidore.render`: For the `WIKI_DIRNAME` constant and module reloading.
- `isidore.pipeline`: For `save_state` and `STATE_FILENAME` in nested directory testing.
- `pytest`: For fixtures like `monkeypatch` and `tmp_path`.

## How to change safely
1. **Environment variable handling**: Modify `_reload_render()` if the module reloading logic changes.
2. **Default value**: Update the default in `test_wiki_dirname_defaults_to_wiki` if the default path changes.
3. **Nested directory logic**: Adjust `test_save_state_creates_nested_wiki_dir` if directory creation behavior changes.
4. **Teardown**: Ensure `teardown_module` remains to restore the default binding.
