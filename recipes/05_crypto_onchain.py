"""Crypto: live Bitcoin network stats in one request.

Hash rate, difficulty, mempool, block height - on-chain fundamentals without
a separate crypto SDK or an extra key.

Run:
    python recipes/05_crypto_onchain.py
"""
import os

import requests

r = requests.get(
    "https://sugra.ai/api/v1/blockchain/stats",
    headers={"x-api-key": os.environ["SUGRA_API_KEY"]},
    timeout=30,
)
r.raise_for_status()

for key, value in r.json()["data"].items():
    print(f"{key}: {value}")
