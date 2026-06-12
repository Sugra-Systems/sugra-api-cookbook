"""Markets: rank every US sector by momentum in one call.

The common way to answer "which sectors lead this month?" is pulling 11 sector
ETFs and computing returns client-side. On Sugra it is precomputed: one call
returns the ranked leaderboard with leader, laggard, spread and breadth.

Run:
    python recipes/02_markets_sector_momentum.py
"""
import os

import requests

KEY = os.environ["SUGRA_API_KEY"]

r = requests.get(
    "https://sugra.ai/api/v1/etf/sectors/relative-strength",
    headers={"x-api-key": KEY},
    params={"window": "1m"},  # also: 1w, 3m, ...
    timeout=30,
)
r.raise_for_status()
d = r.json()["data"]

leader, laggard = d["leader"], d["laggard"]
print(f"leader:  {leader['sector_canonical']:24s} {leader['return_pct']:+.2f}%")
print(f"laggard: {laggard['sector_canonical']:24s} {laggard['return_pct']:+.2f}%")

print("\nfull leaderboard:")
for row in d["sectors"]:
    print(f"  {row['sector_canonical']:24s} {row['return_pct']:+.2f}%")
