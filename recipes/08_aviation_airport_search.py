"""Aviation: search 85,000+ airports worldwide.

Filter by name, country, type, ICAO/IATA code or scheduled service. The same
record shape whether you query a hub or a heliport.

Run:
    python recipes/08_aviation_airport_search.py
"""
import os

import requests

BASE = "https://sugra.ai/api/v1/airports"
H = {"x-api-key": os.environ["SUGRA_API_KEY"]}

# Large airports with scheduled service in Japan
r = requests.get(
    f"{BASE}/search",
    headers=H,
    params={"country": "jp", "type": "large_airport", "scheduled_only": True},
    timeout=30,
)
r.raise_for_status()
for a in r.json()["data"]["airports"]:
    print(f"{a.get('iata_code') or '---'}  {a.get('name')}")

# Or resolve one code directly
r = requests.get(f"{BASE}/code/JFK", headers=H, timeout=30)
print("\nJFK:", r.json()["data"].get("name"))
