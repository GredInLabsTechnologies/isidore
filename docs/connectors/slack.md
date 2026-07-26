# Slack — instance recipe for the MCP connector

Isidore reads Slack through **Slack's own MCP server**. Same rule as Gmail: no OAuth code here, no
token in any config file, read-only or nothing.

## What you get

Channel history and thread replies as ingested items, each addressable as `src://mcp/slack/<item-id>`,
so a knowledge page can cite the message where a decision was actually made.

## Setup

1. In your Slack app's **OAuth & Permissions**, add ONLY read scopes:
   `channels:read`, `channels:history`, `users:read`, and `search:read` if you want search.
   **Do not add `chat:write`.** Most Slack MCP walkthroughs include it because they assume you want a
   bot that answers; Isidore never posts, so granting it buys nothing and risks everything.
2. Install the app to the workspace and keep the token in your secret store.
3. Export the variable NAME Isidore should read it from: `ISIDORE_SLACK_TOKEN`.
4. Invite the app to the channels you want read. A channel it is not in is a channel it cannot see —
   that is the access model doing its job, not a misconfiguration.

## The config

`~/.isidore/connectors/mcp/slack/config.json`:

```json
{
  "instance": "slack",
  "transport": {
    "type": "http",
    "url": "https://mcp.slack.com/mcp",
    "auth_env": "ISIDORE_SLACK_TOKEN"
  },
  "allowed": [
    { "tool": "conversations_history", "arguments": { "channel": "C0123456789", "limit": 50 } },
    { "tool": "conversations_replies", "arguments": { "channel": "C0123456789", "ts": "" } }
  ]
}
```

### Confirm the tool names before you trust this block

Slack publishes its tool definitions at runtime and says so: `tools/list` against the authenticated
endpoint is the source of truth, and names change. Check yours:

```bash
isidore connect mcp --instance slack
```

If a name has moved, the run reports it rather than silently reading nothing. Adjust the allowlist.

### Where the caps live

In the arguments — `limit` on the history call, and a channel per entry. As with Gmail, Isidore does
not translate `--window-hours` into a server-specific parameter it would have to guess. List the
channels you actually want; a workspace-wide read is neither useful as knowledge nor kind to your
rate limit.

## The part you should actually worry about

**A Slack message is untrusted text from whoever can post in that channel** — which, in any shared or
connect channel, is more people than you think. The defence is the same as for mail and it is
mechanical, not a matter of trusting the model: items are stored verbatim as evidence, fenced with a
per-assembly nonce when they reach a prompt so a message cannot forge a second source, any forgery
attempt is marked and reported, and the prompt states that excerpts may be phrased as commands and
are never to be obeyed. The connector's read-only barrier means a successful injection still has no
tool to reach for.

Prefer channels whose membership you know. `#eng-decisions` is a good knowledge source; a public
connect channel is a stranger's keyboard.

## Verifying it works

```bash
isidore connect mcp --instance slack
isidore ingest --connector mcp
isidore claims --check
```

An expired or revoked token gives `status=error` with the server's message, nothing stored, no cursor
moved.

## Sources

- [Slack MCP server overview](https://docs.slack.dev/ai/slack-mcp-server/) — endpoint, auth, and the statement that `tools/list` is authoritative.
- [Guide to the Slack MCP server](https://slack.com/help/articles/48855576908307-Guide-to-the-Slack-MCP-server) — what the read tools cover.
