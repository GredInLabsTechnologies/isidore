> [!WARNING]
> **SECURITY — unverified suspect(s) flagged automatically while compiling this page.**
> Detected from the evidence, not from a security scan. Treat as review items to VERIFY, never as intended features to preserve:
>
> - `tests/fixtures/pcp/repo/svc/auth.py:23` — security risk: hardcoded credential literal in auth path

## Purpose
The `tests/fixtures/pcp` module provides a test fixture for Proof-Carrying Prose (PCP), a system where typed claims about code are verified against the code itself and bundled into tamper-evident certificates. The fixture includes an authentication service (`auth.py`) and a token verification service (`tokens.py`), along with supporting JSON files that define the system's structure and contracts.

## Architecture
The module consists of:
- `auth.py`: The authentication service that verifies JWT tokens and enforces an attempt ceiling.
- `tokens.py`: The token verification service that checks token signatures using HMAC.
- JSON files (`contracts.json`, `graph.json`, `marks.json`, `pyramid_config.json`): These define the system's contracts, code structure, security marks, and configuration.

The system is designed to be self-verifying: the `graph.json` captures the exact relationships between code elements, and `contracts.json` defines claims that must hold true for the system to be valid.

## Key entry points
- `authenticate()` in `tests/fixtures/pcp/repo/svc/auth.py`: The main authentication function that verifies JWT tokens and enforces the attempt ceiling.
- `verify_jwt()` in `tests/fixtures/pcp/repo/svc/tokens.py`: The function that performs the actual token verification.

## Dependencies
The module has no external dependencies, as evidenced by the fact that it is not depended on by any other module in the repository.

## How to change safely
When modifying this module:
1. Ensure all changes are reflected in the golden files (`graph.json`, `contracts.json`, etc.) to maintain the system's self-verifying properties.
2. Update the documentation in `svc.md` to reflect any changes in behavior or constraints.
3. Verify that all claims in `contracts.json` continue to hold true after changes.
