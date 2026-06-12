"""Entity: screen a name against the sanctions corpus (Sugra Entity).

POST /entity/screen returns a screening signal - `clear`, `review` or `hit` -
with matched records and list-freshness metadata. Screening is fail-closed:
if the underlying list is stale, results are downgraded to `review` instead
of pretending certainty.

Run:
    python recipes/07_entity_sanctions_screening.py
"""
import os

import requests

r = requests.post(
    "https://sugra.ai/api/v1/entity/screen",
    headers={"x-api-key": os.environ["SUGRA_API_KEY"]},
    json={
        "name": "Acme Trading LLC",
        # optional context to sharpen matching:
        # "country": "DE", "dob": "1980-01-01",
        # tune sensitivity (defaults: hit >= 0.90, review >= 0.70):
        # "threshold_hit": 0.90, "threshold_review": 0.70,
    },
    timeout=30,
)
r.raise_for_status()
body = r.json()

print("status:", body["data"]["status"])
for match in body["data"].get("matches", []):
    print("match:", match)

# Inspect which lists are loaded and how fresh they are:
src = requests.get(
    "https://sugra.ai/api/v1/entity/sources",
    headers={"x-api-key": os.environ["SUGRA_API_KEY"]},
    timeout=30,
)
for entry in src.json()["data"]["lists"]:
    print(f"  {entry['key']}: loaded={entry['loaded']} stale={entry['stale']}")
