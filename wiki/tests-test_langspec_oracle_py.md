## Purpose
The `tests/test_langspec_oracle.py` module tests the `isidore.verify` subsystem's ability to decide whether a code element's signature or value matches a claim. It focuses on two key functions: `parameter_names()` (reading parameter names from signatures) and `literal_value()` (extracting comparable literals from declarations). The tests verify that these functions correctly parse and validate code elements in various languages (TypeScript, Go, Rust, Java, C) and refuse to answer when the input is malformed or unsupported.

## Architecture
The module uses a helper function `_ctx()` to create a `VerifyContext` with a temporary file containing test code. The test cases are organized into sections:
1. **Reading parameters**: Tests for `parameter_names()` that verify correct parsing of parameter names from signatures and refusal to answer for unsupported cases.
2. **Literal values**: Tests for `literal_value()` that check extraction of comparable literals and refusal to answer for non-literal or complex declarations.
3. **Verifiers**: Tests for `v_value()` and `v_signature()` that verify the oracle's ability to decide claims about values and signatures.

## Key entry points
- `_ctx()`: Creates a test context with a temporary file and `VerifyContext`.
- `test_parameter_names_are_read_where_the_name_comes_first()`: Tests successful parameter name extraction.
- `test_a_language_whose_parameter_order_is_not_modelled_refuses_to_answer()`: Tests refusal for unsupported languages.
- `test_a_truncated_declaration_refuses_to_answer()`: Tests refusal for malformed signatures.
- `test_a_parameter_that_is_not_a_plain_name_refuses_to_answer()`: Tests refusal for complex parameters.
- `test_literal_value_reads_only_comparable_literals()`: Tests successful literal extraction.
- `test_value_now_decides_for_a_typescript_constant()`: Tests the oracle's ability to decide value claims.

## Dependencies
The module depends on:
- `isidore.pcp`: For `Predicate`, `VerifyContext`, and decision constants (`TRUE`, `FALSE`, etc.).
- `isidore.surface`: For `literal_value()` and `parameter_names()`.
- `isidore.verify`: For `v_signature()` and `v_value()`.
- `pathlib.Path`: For file operations.

## How to change safely
To modify this module:
1. **Add new tests**: Follow the existing pattern of testing both success and refusal cases.
2. **Update test data**: Modify the `TS`, `JAVA`, and other language examples to reflect new language features or edge cases.
3. **Refactor helpers**: Ensure `_ctx()` remains consistent with the `VerifyContext` requirements.
4. **Document new behavior**: Add comments to explain new test cases or edge cases.
