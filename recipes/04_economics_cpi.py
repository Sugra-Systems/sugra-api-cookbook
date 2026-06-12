"""Economics: long-run consumer-price series for any of 63 countries.

Sourced from the BIS long-run CPI dataset - index level and year-over-year
change per observation. Same key, same envelope as every other domain.

Run:
    python recipes/04_economics_cpi.py
"""
import os

import requests

r = requests.get(
    "https://sugra.ai/api/v1/bis/cpi",
    headers={"x-api-key": os.environ["SUGRA_API_KEY"]},
    params={"country": "us", "last_n": 12},  # 2-letter code, last N observations
    timeout=30,
)
r.raise_for_status()

for row in r.json()["data"]:
    print(row)
