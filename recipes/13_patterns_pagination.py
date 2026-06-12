"""Pattern: offset pagination on large result sets.

Example: all ASNs allocated to a country (a large country has thousands).
The endpoint takes limit + offset and reports full totals, so the loop knows
exactly when to stop.

Run:
    python recipes/13_patterns_pagination.py
"""
import os

import requests

H = {"x-api-key": os.environ["SUGRA_API_KEY"]}
URL = "https://sugra.ai/api/v1/network/asn"

LIMIT = 1000
offset = 0
asns = []

while True:
    r = requests.get(
        URL,
        headers=H,
        params={"country": "NL", "limit": LIMIT, "offset": offset},
        timeout=60,
    )
    r.raise_for_status()
    page = r.json()  # network domain returns the payload directly (no envelope)
    batch = page["asns"]
    asns.extend(batch)
    total = page["asn_count"]
    print(f"fetched {len(asns)}/{total}")
    if len(batch) < LIMIT or len(asns) >= total:
        break
    offset += LIMIT

print(f"\n{len(asns)} ASNs allocated to NL; first ten: {asns[:10]}")
