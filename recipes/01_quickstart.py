"""Quickstart: your first Sugra API call.

What this shows:
- public system endpoint (no key) vs data endpoint (x-api-key header)
- the standard envelope: {"data": ..., "meta": {...}}
- reading your rate-limit state from the response headers

Run:
    export SUGRA_API_KEY=sugra_...
    python recipes/01_quickstart.py
"""
import os

import requests

BASE = "https://sugra.ai"
KEY = os.environ["SUGRA_API_KEY"]

# 1. System endpoints are public - no key needed.
health = requests.get(f"{BASE}/health", timeout=30)
print("health:", health.json())

# 2. Data endpoints take the key in the x-api-key header.
r = requests.get(
    f"{BASE}/api/v1/etf/sectors/relative-strength",
    headers={"x-api-key": KEY},
    params={"window": "1m"},
    timeout=30,
)
r.raise_for_status()

# 3. Every response uses the same envelope: data + meta.
body = r.json()
print("endpoint:", body["meta"]["endpoint"])
print("data_time:", body["meta"]["data_time"])
print("leader:", body["data"]["leader"])

# 4. Rate-limit state rides on every response.
print("quota:", r.headers.get("X-RateLimit-Limit"))
print("remaining:", r.headers.get("X-RateLimit-Remaining"))
print("resets:", r.headers.get("X-RateLimit-Reset"))
