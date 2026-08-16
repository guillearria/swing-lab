"""Tunables + secrets for the research capture layer — one tiny place."""

import os
from dotenv import load_dotenv

load_dotenv()  # read .env (gitignored)

ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")

# Universe. Stocks + crypto (crypto trades 24/7 -> data on weekends too).
# Stocks <= 25 keeps daily news within the Alpha Vantage free tier (25/day).
WATCHLIST_STOCKS = [
    "AAPL", "MSFT", "NVDA", "AMD", "TSLA", "AMZN", "META", "GOOGL",
    "NFLX", "AVGO", "JPM", "XOM", "COIN", "PLTR", "SPY", "QQQ",
]
WATCHLIST_CRYPTO = ["BTC-USD", "ETH-USD", "SOL-USD", "XRP-USD", "DOGE-USD", "ADA-USD"]
WATCHLIST = WATCHLIST_STOCKS + WATCHLIST_CRYPTO


def is_crypto(symbol: str) -> bool:
    return symbol.endswith("-USD")


# Momentum signal (price + volume). Works for stocks and crypto.
LOOKBACK_DAYS = 20        # baseline window for average daily volume
TREND_DAYS = 5            # window for the recent % price move
REL_VOLUME_STRONG = 2.0   # latest volume >= 2x the baseline average
PCT_STRONG = 0.03         # AND price up >= 3% over the trend window

# News signal (Alpha Vantage, deterministic). Stocks only.
NEWS_RECENCY_HOURS = 48
NEWS_MIN_ARTICLES = 3
NEWS_SENTIMENT_STRONG = 0.35   # AV's own "bullish" threshold
NEWS_THROTTLE_SEC = 15         # free tier = 5 calls/min; pace to stay under it

# Outcome settlement — directly tests v1's fixed-% trade plan.
HORIZON_DAYS = 5          # trading days we track each snapshot forward
TP1_PCT = 0.10            # +10% target (= 2R on a 5% stop)
STOP_PCT = 0.05           # -5% stop

# Working orders (research/orders.py) — how far a real-money entry may chase, and how long the
# order stays live. THE one place these live; docs point at the command, never restate the number.
# Calibrated 2026-08-03 on the 40 taken movers with price history (FINDINGS same date):
# fill rate is FLAT at 87.5% across 1.0/1.5/2.0% bands while the median entry advantage over a
# blind close-chase decays +0.52% -> +0.35% -> +0.12%, so the tight end dominates on both axes.
ENTRY_BAND_MAX = 0.010    # never chase more than 1% past the reference close...
ENTRY_BAND_FRAC = 0.20    # ...nor more than 20% of the entry->stop distance, whichever is tighter
ORDER_EXPIRY_D = 3        # trading sessions an order stays live: 88% fill on session 1, 90% by 2,
                          # and sessions 3-10 add ONE name that had already run +19.8% on day 1
# RISK_PCT (the [ORDERS #2] per-trade risk unit) was deleted with the sizing logic [ARC 5 #12a]:
# counterfactual orders have no cash or equity to size against. Git history has the calibration.

# Bet admission — the liquidity floor [ARC 5 #12a]: a paper fill on a thin name is fantasy, so a
# bet that couldn't absorb real money never enters the pooled verdict's population. Fail-CLOSED:
# unverifiable liquidity refuses the bet (if prices are down the pre-market run is degraded anyway).
LIQ_FLOOR_USD = 5_000_000  # median daily dollar volume (close x volume) required to admit a bet
LIQ_WINDOW_D = 20          # ...measured over this many COMPLETED sessions

# Backtest — sweep this much daily history (yfinance, free).
BACKTEST_PERIOD = "5y"    # span multiple regimes (incl. the 2022 bear) for OOS checks
TREND_MA = 200            # trend filter: price vs its 200-day moving average
MR_DROP = -0.05           # mean-reversion: a 5-day drop of 5%+ = "oversold" (bounce test)
MR_MKT_DROP = -0.02       # if SPY also fell >=2% over the same 5d, the drop was market-wide (tantrum), not name-specific (knife)
COST_ROUNDTRIP = 0.002    # assumed round-trip cost (commission~0 + slippage); optimistic for illiquid

