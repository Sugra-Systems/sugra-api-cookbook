"""Markets: how a stock moved after each of its recent earnings quarters.

A common research question - "does this name tend to run up after it reports?" -
usually means stitching two datasets together by hand. Here it is two Sugra calls
and a client-side join:

  - /quotes/{symbol}/earnings-history  -> per-quarter EPS surprise
  - /quotes/{symbol}/historical        -> daily closes (one call spans them all)

For each recent fiscal quarter, the recipe pairs the EPS surprise with the stock's
close-to-close move over the WINDOW days after the quarter closed.

Note on anchoring: earnings-history anchors on the fiscal QUARTER timestamp, not the
exact announcement day (the API does not expose historical announcement dates). The
move below is measured from the quarter close forward, so it captures the run into
and out of the report, not an announcement-day gap. For the next (upcoming)
announcement date, use /quotes/{symbol}/calendar.

Run:
    python recipes/15_markets_post_earnings_moves.py
"""
import os
from datetime import datetime, timedelta, timezone

import requests

KEY = os.environ["SUGRA_API_KEY"]
BASE = "https://sugra.ai/api/v2"
SYMBOL = "AAPL"
WINDOW = 30  # calendar days after the quarter close to measure the move


def get(path, **params):
    r = requests.get(f"{BASE}{path}", headers={"x-api-key": KEY}, params=params, timeout=30)
    r.raise_for_status()
    return r.json()["data"]


def day(ts, plus=0):
    return (datetime.fromtimestamp(ts, timezone.utc) + timedelta(days=plus)).strftime("%Y-%m-%d")


# 1. EPS surprise per quarter.
quarters = [q for q in get(f"/quotes/{SYMBOL}/earnings-history", limit=8) if q.get("quarter")]
if not quarters:
    raise SystemExit(f"no earnings history for {SYMBOL}")

# 2. Daily closes spanning every quarter, in ONE call.
q_ts = [q["quarter"] for q in quarters]
bars = get(
    f"/quotes/{SYMBOL}/historical",
    start=day(min(q_ts)),
    end=day(max(q_ts), WINDOW + 7),
    interval="1d",
)["data"]
closes = {b["date"]: b["close"] for b in bars}
trading_days = sorted(closes)


def close_on_or_after(d):
    # Prices exist only on trading days; take the first close at or after d.
    hit = next((td for td in trading_days if td >= d), None)
    return closes[hit] if hit else None


# 3. Client-side join: surprise vs the move that followed.
print(f"{SYMBOL}: EPS surprise vs {WINDOW}-day move after each quarter close\n")
print(f"{'quarter close':14s}{'EPS surprise':>14s}{'move':>10s}")
for q in quarters:
    c0 = close_on_or_after(day(q["quarter"]))
    c1 = close_on_or_after(day(q["quarter"], WINDOW))
    if not (c0 and c1):
        continue  # window runs past the latest available price
    surprise = q.get("surprise_percent")
    surprise_s = f"{surprise * 100:+.1f}%" if surprise is not None else "n/a"
    move = (c1 / c0 - 1) * 100
    print(f"{day(q['quarter']):14s}{surprise_s:>14s}{move:>+9.2f}%")
