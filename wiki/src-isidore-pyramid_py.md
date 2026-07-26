## Purpose
The `src/isidore/pyramid.py` module implements Lane D of the architecture, a hierarchical synthesis system that creates tamper-evident documentation with wiki:// claim chains. It enables multi-level documentation (N1 module pages → N2 subsystem pages → N3 product manuals) where higher-level claims cite lower-level claims via `wiki://<page>#<claim-id>`. The verifier checks that cited claims exist, are non-stale, and are TRUE, with truth rooted in certificates that compose upward from code lines.

## Architecture
The module consists of three main components:
1. A wiki:// chain verifier (`_wikichain_verifier`) that resolves claims by checking certificates first, then falling back to pages_state
2. A subsystem suggester (`_seed_subsystems`) that groups files by top directory and records inter-subsystem dependencies
3. A pyramid planner (`plan_pyramid`) that generates N2 subsystem and N3 product page specifications

## Key entry points
- `_wikichain_verifier`: The verifier function registered for `WIKI_VERIFIER_KIND` that resolves wiki:// claims
- `_seed_subsystems`: Groups files into subsystems based on top directory and import relationships
- `plan_pyramid`: Generates specifications for N2 subsystem and N3 product pages

## Dependencies
The module depends on `src/isidore/pcp.py` for:
- Verdict constants (TRUE, FALSE)
- Verification infrastructure (Predicate, Verdict, VerifyContext)
- Certificate handling (CERT_SUFFIX, read_certificate)
- URI parsing (parse_wiki_uri)
- Verifier registration (register_verifier)

## How to change safely
1. When modifying the verifier logic:
   - Maintain the fail-closed behavior (invalid/missing claims should never crash)
   - Preserve the certificate-first resolution strategy
   - Keep the state handling consistent (ok/stale/quarantine)

2. For subsystem grouping:
   - The top directory heuristic is hardcoded - consider whether this should be configurable
   - The import relationship analysis is based on the graph's `imports` edges

3. When extending the pyramid planning:
   - Maintain the 0-LLM requirement
   - Preserve the existing configuration hierarchy
   - Keep the level 2/3 distinction clear
