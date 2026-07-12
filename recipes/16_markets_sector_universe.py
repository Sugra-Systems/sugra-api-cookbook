"""Markets: the canonical US sector map - 11 SPDR sector ETFs, one call.

Before you rank or rotate sectors you need the UNIVERSE: which ETF is which
sector. The 11 SPDR "Select Sector" ETFs are the market-standard proxy set and a
stable static list (last changed in 2018, when XLC split communication services
out of tech). This recipe pins that canonical list so the map is always COMPLETE,
then enriches each ticker with its Sugra canonical sector and full name - a
source-backed lookup for joining your own holdings to sectors.

(To rank this same universe by momentum, see recipe 02.)

Run:
    python recipes/16_markets_sector_universe.py
"""
import os

import requests

KEY = os.environ["SUGRA_API_KEY"]
WINDOW = "1m"

# The canonical universe is a stable static list, so we pin it: the map is ALWAYS
# these 11, for both the table and O(1) lookups. We seed every ticker, then overwrite
# with Sugra's live sector + name where available; a ticker the API cannot enrich this
# call keeps its placeholder and is flagged - never silently dropped.
SECTOR_ETFS = ["XLB", "XLC", "XLE", "XLF", "XLI", "XLK",
               "XLP", "XLRE", "XLU", "XLV", "XLY"]
UNENRICHED = ("(not enriched this call)", "")

r = requests.get(
    "https://sugra.ai/api/v1/etf/sectors/relative-strength",
    headers={"x-api-key": KEY},
    params={"window": WINDOW},
    timeout=30,
)
r.raise_for_status()
sectors = (r.json().get("data") or {}).get("sectors") or []

sector_map = {sym: UNENRICHED for sym in SECTOR_ETFS}
covered = set()
for s in sectors:
    sym = s.get("symbol")
    if sym in sector_map:
        sector_map[sym] = (s.get("sector_canonical") or "-", s.get("name") or "-")
        covered.add(sym)

print(f"US sector universe - {len(SECTOR_ETFS)} SPDR Select Sector ETFs:\n")
print(f"  {'ETF':5s} {'sector':24s} name")
for sym in SECTOR_ETFS:
    sector, name = sector_map[sym]
    print(f"  {sym:5s} {sector:24s} {name}")

uncovered = [sym for sym in SECTOR_ETFS if sym not in covered]
if uncovered:
    print(f"\nnot enriched this call (no {WINDOW} return): {', '.join(uncovered)}")

# use it: map any ticker you hold to its sector in O(1) - always resolves for the 11
holding = "XLK"
sector, _ = sector_map[holding]
print(f"\nlookup: {holding} -> {sector}")
