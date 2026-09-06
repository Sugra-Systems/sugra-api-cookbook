"""Forex: price a 99 USD item on the official daily book.

Sugra Finance already carries the central-bank FX shelf. One request
lists 151 ISO codes. Convert reads that same book. This is orientation
for a storefront, not a trade.

Run:
    python recipes/17_forex_shop_convert.py
"""
import os

import requests

H = {"x-api-key": os.environ["SUGRA_API_KEY"]}
BASE = "https://sugra.ai/api/v1/forex"
NAMES = {
    "bdi": "Banca d'Italia",
    "cbu": "Central Bank of Uzbekistan",
    "ecb": "ECB",
    "nbp": "Narodowy Bank Polski",
}

book = requests.get(
    f"{BASE}/rates",
    headers=H,
    params={"base": "USD"},
    timeout=30,
)
book.raise_for_status()
panel = book.json()["data"]
print("base", panel["base"], "count", panel["count"])

amount = 99
for dst in ("EUR", "JPY", "GEL", "UZS"):
    r = requests.get(
        f"{BASE}/convert",
        headers=H,
        params={"from": "USD", "to": dst, "amount": amount},
        timeout=30,
    )
    r.raise_for_status()
    row = r.json()["data"]
    src = NAMES.get(row["path"].split("-")[0], row["path"])
    value = row["result"]
    if dst in {"JPY", "UZS"}:
        shown = f"{value:,.0f}"
    else:
        shown = f"{value:,.2f}"
    print(
        f"{amount} USD -> {shown} {dst}  "
        f"{src}  as_of {row['date']}  "
        f"{row['basis']}"
    )
