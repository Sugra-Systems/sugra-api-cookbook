"""Network: who runs an IP - ASN, geo and privacy signal (Sugra Net Atlas).

Three small lookups against the same IP. Note: the network domain returns its
payload directly (with an inline `_meta` quality block) rather than the
standard envelope - it is built for high-volume per-IP lookups.

Run:
    python recipes/06_network_ip_intelligence.py
"""
import os

import requests

BASE = "https://sugra.ai/api/v1/network"
H = {"x-api-key": os.environ["SUGRA_API_KEY"]}
IP = "1.1.1.1"

# 1. ASN + organization
asn = requests.get(f"{BASE}/ip/{IP}/asn", headers=H, timeout=30).json()
print("asn:", asn.get("asn"))

# 2. Geo (country, city, timezone)
geo = requests.get(f"{BASE}/ip/{IP}/geo", headers=H, timeout=30).json()
print("geo:", {k: geo.get(k) for k in ("country", "city", "timezone")})

# 3. Composite privacy signal (VPN / proxy / hosting)
privacy = requests.get(f"{BASE}/ip/{IP}/privacy", headers=H, timeout=30).json()
print("privacy:", privacy.get("privacy"))
