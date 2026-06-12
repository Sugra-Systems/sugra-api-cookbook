"""Forex: USD exchange rates for 192 countries, 147 currencies (BIS).

Long-run official exchange-rate series vs the US dollar - same call shape as
the CPI recipe, because the envelope never changes between domains.

Run:
    python recipes/10_forex_usd_rates.py
"""
import os

import requests

H = {"x-api-key": os.environ["SUGRA_API_KEY"]}

for country in ("jp", "ch", "gb"):
    r = requests.get(
        "https://sugra.ai/api/v1/bis/fx",
        headers=H,
        params={"country": country, "last_n": 1},
        timeout=30,
    )
    r.raise_for_status()
    for row in r.json()["data"]:
        print(country.upper(), row)
