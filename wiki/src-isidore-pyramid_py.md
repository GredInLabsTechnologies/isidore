## Purpose
The `src/isidore/pyramid.py` module implements a hierarchical synthesis system for documentation, treating wiki pages as a "pyramid" of claims that compose to form higher-level truths. It enables tamper-evident documentation by verifying claims against certificates and ensuring staleness propagates upward. The module also provides deterministic planning for subsystem and product page generation, using the codebase structure to seed initial subsystem definitions.

## Architecture
The module consists of three main components:
1. A wiki:// chain verifier that resolves claims by checking certificates and fallbacks to pages_state
2. A subsystem suggester that groups files by top directory and records inter-subsystem dependencies
3. A pyramid planner that generates N2 subsystem and N3 product page specifications

The verifier follows a fail-closed approach, treating any invalid or missing claim as FALSE. The subsystem suggester operates with zero LLM calls, using only the code structure. The planner supports both explicit configuration and automatic seeding from the codebase.

## Key entry points
- `_wikichain_verifier`: The main verifier function registered with `WIKI_VERIFIER_KIND`
- `_seed_subsystems`: Generates initial subsystem definitions from the code graph
- `plan_pyramid`: The main entry point for generating pyramid specifications

## Dependencies
The module depends on `src/isidore/pcp.py` for:
- Verdict constants (TRUE, FALSE)
- Verification infrastructure (Predicate, Verdict, VerifyContext)
- URI parsing and verifier registration

## How to change safely
1. When modifying the verifier logic:
   - Maintain the fail-closed behavior
   - Preserve the certificate-first resolution order
   - Keep the staleness propagation rules consistent

2. For subsystem planning changes:
   - Ensure the 0-LLM constraint is maintained
   - Preserve the existing configuration precedence rules
   - Keep the glob pattern format consistent

3. When adding new verifier kinds:
   - Follow the same registration pattern as `WIKI_VERIFIER_KIND`
   - Maintain the same fail-closed behavior
   - Document the new verifier kind in the module docstring
