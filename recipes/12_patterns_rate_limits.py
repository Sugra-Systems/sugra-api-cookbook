"""Pattern: respect rate limits without guesswork.

Every Sugra API response carries your quota state in headers, and a 429 tells
you exactly when the window resets (UTC midnight). So a polite client needs no
heuristics: read the headers, back off on 429, resume at the reset time.

Run:
    python recipes/12_patterns_rate_limits.py
"""
import os
import time

import requests

H = {"x-api-key": os.environ["SUGRA_API_KEY"]}
URL = "https://sugra.ai/api/v1/etf/sectors/relative-strength"


def get_with_limit_awareness(url: str, **kwargs) -> requests.Response:
    """GET that reports quota state and handles the 429 case explicitly."""
    r = requests.get(url, headers=H, timeout=30, **kwargs)

    remaining = r.headers.get("X-RateLimit-Remaining")
    if remaining is not None and int(remaining) < 10:
        print(f"warning: only {remaining} requests left today "
              f"(resets {r.headers.get('X-RateLimit-Reset')})")

    if r.status_code == 429:
        # The daily counter resets at UTC midnight; the header says when.
        reset_at = r.headers.get("X-RateLimit-Reset")
        raise RuntimeError(f"daily quota exhausted; resets at {reset_at}")

    r.raise_for_status()
    return r


def get_with_retry(url: str, attempts: int = 3, **kwargs) -> requests.Response:
    """Retry transient upstream errors (5xx) with backoff; never retry 4xx."""
    for attempt in range(1, attempts + 1):
        r = requests.get(url, headers=H, timeout=30, **kwargs)
        if r.status_code < 500:
            r.raise_for_status()
            return r
        if attempt < attempts:
            sleep_s = 2 ** attempt
            print(f"upstream {r.status_code}, retry {attempt}/{attempts - 1} in {sleep_s}s")
            time.sleep(sleep_s)
    r.raise_for_status()
    return r


resp = get_with_limit_awareness(URL, params={"window": "1m"})
print("leader:", resp.json()["data"]["leader"]["sector_canonical"])
