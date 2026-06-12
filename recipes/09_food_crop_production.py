"""Food and agriculture: crop and livestock production (FAOSTAT).

Production quantities for 245+ countries back to 1961. Codes follow the
FAOSTAT conventions: area is M49 (840 = USA), item is the FAOSTAT item code
(15 = Wheat, 27 = Rice).

Run:
    python recipes/09_food_crop_production.py
"""
import os

import requests

r = requests.get(
    "https://sugra.ai/api/v1/faostat/production",
    headers={"x-api-key": os.environ["SUGRA_API_KEY"]},
    params={"area": "840", "item": "15", "year": "2023"},  # US wheat, 2023
    timeout=60,
)
r.raise_for_status()

for row in r.json()["data"]["records"][:10]:
    print(row)
