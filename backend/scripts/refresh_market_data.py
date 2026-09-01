"""Refreshes the bundled historical price data used by the portfolio
optimizer (app/pipeline/portfolio.py).

Run this locally whenever you want updated prices:

    python3 scripts/refresh_market_data.py

It fetches from Yahoo Finance directly, which works fine from a normal
residential/local connection but is unreliable from cloud hosts like
Render (Yahoo rate-limits or blocks the undocumented endpoint yfinance
relies on from datacenter IPs). So the deployed backend never calls
yfinance itself, it just reads the CSV this script writes.

yfinance isn't in requirements.txt since the deployed app doesn't need it,
only this script does. Install it locally first: pip install yfinance
"""

from pathlib import Path

import yfinance as yf

from app.pipeline.portfolio import ALL_TICKERS, LOOKBACK

DATA_PATH = Path(__file__).resolve().parent.parent / "app" / "data" / "market_prices.csv"


def main() -> None:
    print(f"Fetching {LOOKBACK} of daily prices for {len(ALL_TICKERS)} tickers...")
    prices = yf.download(
        ALL_TICKERS, period=LOOKBACK, auto_adjust=True, progress=False
    )["Close"]
    prices = prices.dropna(axis=0, how="any")

    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    prices.to_csv(DATA_PATH)
    print(f"Wrote {len(prices)} rows x {len(prices.columns)} tickers to {DATA_PATH}")


if __name__ == "__main__":
    main()
