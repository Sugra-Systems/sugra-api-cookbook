"""Markets: the canonical US sector map - 11 SPDR sector ETFs in one call.

Before you rank or rotate sectors you need the UNIVERSE: which ETF is which
sector. The 11 SPDR "Select Sector" ETFs are the market-standard proxy set (last
changed in 2018, when XLC split communication services out of tech). Rather than
hardcode the tickers and guess the sector names, pull the set from Sugra - one
call returns every sector ETF with its canonical sector and full name, so you can
join your own holdings to sectors with a stable, source-backed map.

(To rank this same universe by momentum, see recipe 02.)

Run:
    python recipes/16_markets_sector_universe.py
"""
import os

import requests

KEY = os.environ["SUGRA_API_KEY"]

r = requests.get(
    "https://sugra.ai/api/v1/etf/sectors/relative-strength",
    headers={"x-api-key": KEY},
    params={"window": "1m"},
    timeout=30,
)
r.raise_for_status()
d = r.json()["data"]

# the reusable sector map: ticker -> (canonical sector, full name)
sector_map = {s["symbol"]: (s["sector_canonical"], s["name"]) for s in d["sectors"]}

print(f"US sector universe - {d['covered']} ETFs (as of {d['as_of']}):\n")
print(f"  {'ETF':5s} {'sector':24s} name")
for sym in sorted(sector_map):
    sector, name = sector_map[sym]
    print(f"  {sym:5s} {sector:24s} {name}")

missing = d.get("missing_symbols") or []
if missing:
    print(f"\nuniverse gap: {missing} not covered right now")

# use it: map any ticker you hold to its sector in O(1)
holding = "XLK"
sector, name = sector_map.get(holding, ("unknown", "-"))
print(f"\nlookup: {holding} -> {sector} ({name})")
