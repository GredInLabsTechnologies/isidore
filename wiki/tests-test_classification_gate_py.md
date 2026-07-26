## Purpose
The `tests/test_classification_gate.py` module tests the classification and trust mechanisms that prevent internal or sensitive content from being sent to external APIs. The module verifies that items marked as `internal` or `secret` are correctly filtered out of prompts, ensuring compliance with the invariant that internal content is never used as someone else's training input. It also tests the exact-word requirement for trust declarations, ensuring that only the literal string `"yes"` (case-insensitive, trimmed) enables trusted behavior.

## Architecture
The module uses pytest fixtures and helper functions to simulate storage and classification scenarios. The `home` fixture sets up a temporary environment, `_store` writes test items to a mock store, and `_item` constructs test items with optional classifications. The tests validate:
1. Classification precedence: metadata labels take priority over document content.
2. Trust declarations: only the exact string `"yes"` (case-insensitive, trimmed) enables trusted behavior.
3. The classification gate: restricted items are excluded from prompts by default.

## Key entry points
- `test_the_label_comes_from_meta_first_then_the_document_itself()`: Verifies classification precedence.
- `test_the_trust_declaration_takes_an_exact_word()`: Ensures trust is only granted for the exact string `"yes"`.
- `test_restricted_items_never_reach_the_prompt_by_default()`: Confirms restricted items are filtered out.

## Dependencies
The module depends on:
- `isidore.connectors.store`: For storage operations like `create_run_id`, `write_items`, and `read_state`.
- `isidore.knowledge`: For classification and trust logic, including `item_classification` and `provider_is_trusted`.

## How to change safely
When modifying this module:
1. Preserve the exact-word requirement for trust declarations (`"yes"` only) to avoid breaking existing assumptions.
2. Maintain the classification precedence order (metadata > document content) to ensure consistent behavior.
3. Test all classification scenarios, including edge cases like mixed-case or whitespace-padded trust declarations.
