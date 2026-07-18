# Sugra API Cookbook

Runnable recipes for the [Sugra API](https://sugra.ai) - intelligence infrastructure for the decisions that matter.

One API key, one envelope, 1,500+ endpoints across 160+ primary sources and 36 data domains: markets, economics, news, crypto, network intelligence, entity screening and more. Every recipe in this cookbook is a small, self-contained Python script you can run as-is.

## Setup

```bash
pip install requests
export SUGRA_API_KEY=sugra_...   # get a free key at https://sugra.ai (50 requests/day)
```

Every data endpoint authenticates with the `x-api-key` header. System endpoints (`/health`, `/about`, `/services`, `/sources`) are public.

## The envelope

Every response is wrapped in the same shape, so one parser works for every domain:

```json
{
  "data": { },
  "meta": {
    "endpoint": "/api/v1/...",
    "data_time": "2026-06-12T19:30:00Z",
    "response_time": "2026-06-12T19:30:01Z",
    "provider": "Sugra API"
  }
}
```

Rate-limit state rides on every response as headers: `X-RateLimit-Limit` (daily quota), `X-RateLimit-Remaining`, `X-RateLimit-Reset` (ISO 8601, UTC).

## Recipes

| # | Recipe | Domain | What it shows |
|---|--------|--------|---------------|
| 01 | [quickstart.py](recipes/01_quickstart.py) | - | First call, envelope parsing, rate-limit headers |
| 02 | [markets_sector_momentum.py](recipes/02_markets_sector_momentum.py) | Markets | Rank US sectors by momentum in one call |
| 03 | [news_global_flow.py](recipes/03_news_global_flow.py) | News | Search global news, trending themes |
| 04 | [economics_cpi.py](recipes/04_economics_cpi.py) | Economics | Long-run CPI for any of 63 countries |
| 05 | [crypto_onchain.py](recipes/05_crypto_onchain.py) | Crypto | Live Bitcoin network stats |
| 06 | [network_ip_intelligence.py](recipes/06_network_ip_intelligence.py) | Network | Who runs an IP: ASN, geo, privacy signal |
| 07 | [entity_sanctions_screening.py](recipes/07_entity_sanctions_screening.py) | Entity | Screen a name against the sanctions corpus |
| 08 | [aviation_airport_search.py](recipes/08_aviation_airport_search.py) | Aviation | Search 85,000+ airports by country, type, code |
| 09 | [food_crop_production.py](recipes/09_food_crop_production.py) | Food | Crop and livestock production, 245+ countries |
| 10 | [forex_usd_rates.py](recipes/10_forex_usd_rates.py) | Forex | USD exchange rates, 147 currencies |
| 11 | [commodities_prices.py](recipes/11_commodities_prices.py) | Commodities | Monthly prices for 18 commodities |
| 12 | [patterns_rate_limits.py](recipes/12_patterns_rate_limits.py) | Patterns | Quota awareness, 429 handling, 5xx backoff |
| 13 | [patterns_pagination.py](recipes/13_patterns_pagination.py) | Patterns | Offset pagination over large result sets |
| 14 | [agent_anthropic_mcp.py](recipes/14_agent_anthropic_mcp.py) | Agents | Claude drives the API via hosted MCP |
| 15 | [markets_post_earnings_moves.py](recipes/15_markets_post_earnings_moves.py) | Markets | Join earnings surprise with prices for post-quarter moves |
| 16 | [markets_sector_universe.py](recipes/16_markets_sector_universe.py) | Markets | The canonical US sector map: 11 SPDR ETFs, symbol to sector to name |

Run any of them:

```bash
python recipes/01_quickstart.py
```

## AI agents

Your agent can drive the whole catalog through MCP - discovery included, no per-endpoint wiring. See [agents/mcp.md](agents/mcp.md) for Claude Desktop, Claude Code and the hosted endpoint. The flagship MCP server lives at [github.com/Sugra-Systems/sugra-api-mcp](https://github.com/Sugra-Systems/sugra-api-mcp).

## Plans

All endpoints are available on every plan - gating is volume-only. Free $0 (50 requests/day), Dev $25 (5K), Pro $59 (50K), Enterprise custom. Details: [sugra.ai](https://sugra.ai).

## License

MIT. The data each endpoint serves carries its own upstream terms; see `/sources` and the per-response `meta`.
