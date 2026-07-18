# Sugra API for AI agents (MCP)

Your agent does not need per-endpoint wiring. The MCP server exposes the whole
Sugra API catalog with discovery built in: the agent searches for an operation,
inspects it, and calls it - on its own.

## The tools

| Tool | Purpose |
|---|---|
| `fetch_data` | One step: find the best endpoint for a natural-language query and call it |
| `search_endpoints` | Search the bundled endpoint catalog |
| `describe_endpoint` | Inspect an operation: parameters, required inputs, agent hints |
| `call_endpoint` | Call an operation by `operation_id` |
| `list_toolsets` | Catalog groups with endpoint counts |
| `list_sources` | Bundled catalog source metadata |
| `sugra_entity_screen` | Screen a name against sanctions and watchlists |
| `sugra_entity_lookup` | Composed entity lookup by `lei` or `vat` identifier |

`call_endpoint` and `fetch_data` support response shaping (`limit`, `fields`
with dotted paths, `include_raw`), and `describe_endpoint` returns
`agent_hints` (duration class, advisory concurrency ceiling) so the agent can
budget time before calling.

## Claude Desktop

Add to `claude_desktop_config.json` (macOS:
`~/Library/Application Support/Claude/claude_desktop_config.json`, Windows:
`%APPDATA%\Claude\claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "sugra": {
      "command": "sugra-api-mcp",
      "env": {
        "SUGRA_API_KEY": "sugra_..."
      }
    }
  }
}
```

```bash
pip install sugra-api-mcp
```

Restart Claude Desktop; the Sugra tools appear in the tools menu.

## Claude Code (CLI)

```bash
pip install sugra-api-mcp
claude mcp add sugra -- sugra-api-mcp
export SUGRA_API_KEY=sugra_...
```

## Hosted endpoint (no install)

Connect any MCP-capable client to:

```
https://app.sugra.ai/mcp
```

The hosted endpoint serves the same 8 tools plus three composed agent tools -
`resolve_entity`, `get_snapshot`, and `get_timeseries` - 11 tools in total,
with OAuth sign-in. Works with Anthropic and OpenAI clients.

## A typical agent flow

```
user:  which US sectors lead this month?
agent: search_endpoints("sector momentum")
agent: call_endpoint("etf_sectors_relative_strength", {"window": "1m"})
agent: Real estate leads, consumer cyclical lags.
```

One MCP server, every domain - markets, economics, news, crypto, network,
entity. Package source: [pypi.org/project/sugra-api-mcp](https://pypi.org/project/sugra-api-mcp/).
Server source: [github.com/Sugra-Systems/sugra-api-mcp](https://github.com/Sugra-Systems/sugra-api-mcp).
