## What this is
Software projects need a guide that explains how they are built, and those guides go out of date the moment the work changes. This tool writes that guide for a software project and keeps it honest: every statement in it can be checked against the project itself, and the guide says so when something it claims is no longer true.

## What you can do with it
- **Know that each statement is backed.** Each claim in the guide points to the exact line of the project it rests on, so anyone can check it.
- **See what a change touched.** When the project changes, the tool works out which parts were affected, down to the individual pieces of work involved.
- **Get a guide that updates without starting over.** Each change is followed back to the lines it altered, so only the parts of the guide that depend on them need attention.
- **Trust the guide's pointers.** The places the guide points to are tracked the same way its claims are, so they keep pointing at the right spot as the project changes.

## How the pieces fit together
The tool first reads the project and draws a map of what exists and where. From that map it writes each page of the guide, and every claim on a page is tied to the line it came from. When the project changes, the tool compares the lines behind each claim, marks the ones that moved, and points to the pages that need a second look.
