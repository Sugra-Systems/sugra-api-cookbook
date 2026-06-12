"""News: search the global news flow and read trending themes.

Backed by GDELT: 250K+ sources, 100+ languages, time windows down to 15
minutes. Two calls here:
1. /gdelt/articles  - free-text search with phrase support
2. /gdelt/themes/trending - what the world's news is about right now

Run:
    python recipes/03_news_global_flow.py
"""
import os

import requests

BASE = "https://sugra.ai/api/v1"
H = {"x-api-key": os.environ["SUGRA_API_KEY"]}

# 1. Search articles. Query syntax supports "exact phrase", OR, -, domain: etc.
r = requests.get(
    f"{BASE}/gdelt/articles",
    headers=H,
    params={"q": '"artificial intelligence"', "timespan": "1h", "max_records": 10},
    timeout=30,
)
r.raise_for_status()
d = r.json()["data"]
print(f"{d['count']} articles in the last hour:")
for a in d["articles"][:5]:
    print(f"  [{a['language']}] {a['domain']}: {a['title'][:70]}")

# 2. Trending themes across the global flow (period: 1h, 6h or 24h).
r = requests.get(
    f"{BASE}/gdelt/themes/trending",
    headers=H,
    params={"period": "1h", "limit": 5},
    timeout=30,
)
r.raise_for_status()
print("\ntop themes right now:")
for t in r.json()["data"]["themes"]:
    print(f"  {t['theme']}: {t['count']}")
