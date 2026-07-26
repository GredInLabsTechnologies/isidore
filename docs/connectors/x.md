# X (Twitter) — deferred to 1.2, and here is exactly why

**Status: not shipped.** No `connectors/x.py` exists, and none is being written for 1.1. This page
says so plainly instead of leaving a gap someone has to discover.

## The reason is money, not effort

The MCP layer is free; the API underneath it is not. On **6 February 2026** X replaced its tiered
plans with pay-per-use as the default for new developers: there is no free tier and no way for a new
customer to sign up for Basic or Pro. Reads are billed at **$0.005 per post** (capped at 2M/month),
and free access survives only as case-by-case grants for "for-good public utility" apps.

So an X connector is not a connector you can turn on. It is a meter. Every other source in Isidore is
free to read — local git, RSS, the public HN API, an MCP server you already pay for in some other
currency — and shipping one that quietly bills per item would break the property that makes `ingest`
safe to run on a schedule.

## What it would take

An API key on a paid account. If you have one:

1. Point the MCP connector at any X MCP server that speaks read-only search, exactly as in
   [gmail.md](gmail.md) — same instance shape, same allowlist, same read-only barrier. Nothing in
   Isidore needs to change.
2. Keep the token in your secret store and name it in the environment, never in the config file.
3. Set a hard `--limit`, and know what each run costs before you schedule it.

There is no recipe block here with a concrete server in it, because recommending one for a paid API
neither of us has tested would be a guess dressed as documentation. The MCP directory listings change
faster than a page like this does; pick one, check `tools/list` against it, and treat that as the
source of truth — the same instruction the Slack recipe gives, for the same reason.

## Revisit in 1.2

Worth reopening if any of these change: X restores a usable free read tier, the collective acquires a
paid key with a budget attached, or a mirrored/aggregated source makes the same content reachable
without per-post billing.

## Sources

- [X API pricing 2026 — pay-per-use replaces the tiers](https://postproxy.dev/blog/x-api-pricing-2026/)
- [Can you use the X API for free?](https://twitterapi.io/blog/can-you-use-x-api-for-free)
- [X (Twitter) MCP server guide](https://mcp.directory/blog/x-twitter-mcp-server) — the MCP layer is free, the API is not.
