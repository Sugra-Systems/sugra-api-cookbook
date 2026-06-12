"""Commodities: latest monthly prices for 18 commodities (World Bank Pink Sheet).

Energy, metals and agricultural products in one response - plus a catalog
endpoint that documents units, frequency and source per commodity.

Run:
    python recipes/11_commodities_prices.py
"""
import os

import requests

BASE = "https://sugra.ai/api/v1/commodities"
H = {"x-api-key": os.environ["SUGRA_API_KEY"]}

catalog = requests.get(f"{BASE}/catalog", headers=H, timeout=30)
catalog.raise_for_status()
print("available commodities:")
for c in catalog.json()["data"][:6]:
    print(" ", c)

prices = requests.get(f"{BASE}/prices", headers=H, timeout=30)
prices.raise_for_status()
print("\nlatest prices:")
print(prices.json()["data"])
