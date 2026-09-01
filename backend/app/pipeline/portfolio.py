# Phase 3 Step 17: portfolio optimizer.
#
# Two decisions happen here, in order:
#
# 1. SELECTION: which 6-8 of the 21 tickers actually go into this person's
#    portfolio. Not every ticker is used for every person; that's the point
#    of having 21 to choose from.
#      - Foundation funds and how many satellite stock slots exist scale
#        with reconciled_score (see foundation_and_satellite_count): a
#        conservative profile gets a fund-heavy foundation with a couple of
#        satellites, an aggressive one drops bonds entirely and leans into
#        more individual stocks.
#      - Satellite stocks are picked from whichever industries the user
#        said they're interested in (or the full stock universe if they're
#        open to anything), ranked by how well each stock's own historical
#        risk/return profile matches this person's risk level (see
#        per_stock_match_scores), not just by raw performance. A stock
#        that returned well but is far more volatile than someone's
#        risk tolerance is not a "good match" for them even if it's a
#        good stock in the abstract.
#
# 2. ALLOCATION: once the subset is picked, standard Modern Portfolio
#    Theory decides how much of each. We compute the minimum-volatility and
#    max-Sharpe portfolios on that subset as anchors, linearly map
#    reconciled_score onto a target volatility between them, and solve for
#    the exact efficient-frontier portfolio at that risk level.
#
# Historical prices are fetched once per process (not per-request) and
# cached at module level; PyPortfolioOpt/yfinance failures fall back to a
# small static lookup table so the endpoint still responds.

from __future__ import annotations

import logging

import numpy as np
import pandas as pd
import yfinance as yf
from pypfopt import EfficientFrontier, expected_returns, risk_models

from app.schemas import Portfolio

logger = logging.getLogger(__name__)

FUND_TICKERS = ["VTI", "VOO", "VXUS", "VB", "BND", "VNQ", "GLD"]

# Sector tags match the INDUSTRY_OPTIONS values on the frontend financial
# profile form exactly, so a user's industry_interests can be compared
# directly against these.
STOCK_SECTORS: dict[str, str] = {
    "NVDA": "Technology",
    "TSM": "Technology",
    "AAPL": "Technology",
    "MSFT": "Technology",
    "JNJ": "Healthcare",
    "UNH": "Healthcare",
    "JPM": "Financials",
    "XOM": "Energy",
    "AMZN": "Consumer / Retail",
    "COST": "Consumer / Retail",
    "PG": "Consumer / Retail",
    "GOOGL": "Communication / Media",
    "DIS": "Communication / Media",
    "NEE": "Utilities",
}

ALL_TICKERS = FUND_TICKERS + list(STOCK_SECTORS)

RISK_FREE_RATE = 0.02
LOOKBACK = "10y"

# Weights for combining a stock's raw historical return with how well its
# volatility matches the user's target risk level (both z-scored first, see
# per_stock_match_scores). Fit is weighted twice as heavily as raw return on
# purpose: a stock with an extreme historical return (NVDA's 10-year return
# is ~65% annualized, dwarfing everything else in the universe) shouldn't
# get recommended to a conservative user just because the number is big.
# Matching the person is the point, not chasing the best historical return.
RETURN_WEIGHT = 1.0
FIT_WEIGHT = 2.0

FOUNDATION_WEIGHT_BOUNDS = (0.05, 0.60)
SATELLITE_WEIGHT_BOUNDS = (0.05, 0.15)


def _fetch_market_data() -> tuple[pd.Series, pd.DataFrame]:
    prices = yf.download(
        ALL_TICKERS, period=LOOKBACK, auto_adjust=True, progress=False
    )["Close"]
    prices = prices.dropna(axis=0, how="any")
    mu = expected_returns.mean_historical_return(prices)
    cov = risk_models.CovarianceShrinkage(prices).ledoit_wolf()
    return mu, cov


try:
    MU, COV = _fetch_market_data()
except Exception:
    logger.exception(
        "Failed to fetch market data from yfinance; build_portfolio will use "
        "the static fallback until the process restarts."
    )
    MU, COV = None, None


def foundation_and_satellite_count(reconciled_score: float) -> tuple[list[str], int]:
    if reconciled_score < 35:
        return ["VTI", "VXUS", "BND", "GLD"], 2
    if reconciled_score < 65:
        diversifier = "GLD" if reconciled_score < 50 else "VNQ"
        return ["VTI", "VXUS", "BND", diversifier], 3
    return ["VTI", "VXUS", "VNQ"], 5


def per_stock_match_scores(
    mu: pd.Series, cov: pd.DataFrame, reconciled_score: float
) -> dict[str, float]:
    stock_tickers = list(STOCK_SECTORS)
    mu_values = np.array([float(mu[t]) for t in stock_tickers])
    vol_values = np.array([float(np.sqrt(cov.loc[t, t])) for t in stock_tickers])

    min_vol, max_vol = vol_values.min(), vol_values.max()
    target_vol = min_vol + (reconciled_score / 100) * (max_vol - min_vol)
    fit = -((vol_values - target_vol) ** 2)

    # z-score both components so a stock with an outlier-large historical
    # return (in absolute terms) doesn't automatically dominate the ranking
    # regardless of how badly its volatility fits the user's risk level.
    mu_z = (mu_values - mu_values.mean()) / mu_values.std()
    fit_z = (fit - fit.mean()) / fit.std()
    combined = RETURN_WEIGHT * mu_z + FIT_WEIGHT * fit_z

    return {t: float(combined[i]) for i, t in enumerate(stock_tickers)}


def select_satellites(
    industry_interests: list[str], count: int, match_scores: dict[str, float]
) -> list[str]:
    pool = [
        ticker
        for ticker, sector in STOCK_SECTORS.items()
        if not industry_interests or sector in industry_interests
    ]
    ranked_pool = sorted(pool, key=lambda t: match_scores[t], reverse=True)
    selected = ranked_pool[:count]

    if len(selected) < count:
        remaining = [t for t in STOCK_SECTORS if t not in selected]
        ranked_remaining = sorted(remaining, key=lambda t: match_scores[t], reverse=True)
        selected += ranked_remaining[: count - len(selected)]

    return selected


def optimize_subset(
    foundation: list[str],
    satellites: list[str],
    mu: pd.Series,
    cov: pd.DataFrame,
    reconciled_score: float,
) -> Portfolio:
    selected = foundation + satellites
    mu_sub = mu.loc[selected]
    cov_sub = cov.loc[selected, selected]
    bounds = [
        FOUNDATION_WEIGHT_BOUNDS if t in foundation else SATELLITE_WEIGHT_BOUNDS
        for t in selected
    ]

    ef_min = EfficientFrontier(mu_sub, cov_sub, weight_bounds=bounds)
    ef_min.min_volatility()
    _, min_vol, _ = ef_min.portfolio_performance(risk_free_rate=RISK_FREE_RATE)

    ef_max = EfficientFrontier(mu_sub, cov_sub, weight_bounds=bounds)
    ef_max.max_sharpe(risk_free_rate=RISK_FREE_RATE)
    _, max_vol, _ = ef_max.portfolio_performance(risk_free_rate=RISK_FREE_RATE)

    target_vol = min_vol + (reconciled_score / 100) * (max_vol - min_vol)
    target_vol = max(min_vol, min(target_vol, max_vol))  # float-safety clamp

    ef_target = EfficientFrontier(mu_sub, cov_sub, weight_bounds=bounds)
    ef_target.efficient_risk(target_vol)
    weights = ef_target.clean_weights()
    expected_return, expected_volatility, sharpe_ratio = ef_target.portfolio_performance(
        risk_free_rate=RISK_FREE_RATE
    )

    asset_weights = {t: round(w, 4) for t, w in weights.items() if w > 0.0001}

    return Portfolio(
        asset_weights=asset_weights,
        expected_return=round(expected_return, 4),
        expected_volatility=round(expected_volatility, 4),
        sharpe_ratio=round(sharpe_ratio, 4),
    )


# Static fallback if the yfinance fetch failed at startup, so the endpoint
# still responds with something reasonable instead of erroring.
_FALLBACK_PORTFOLIOS = [
    (25, {"VTI": 0.20, "VXUS": 0.05, "BND": 0.65, "VNQ": 0.10}, 0.045, 0.06, 0.48),
    (50, {"VTI": 0.35, "VXUS": 0.10, "BND": 0.45, "VNQ": 0.10}, 0.058, 0.085, 0.51),
    (75, {"VTI": 0.45, "VXUS": 0.15, "BND": 0.30, "VNQ": 0.10}, 0.071, 0.11, 0.52),
    (100, {"VTI": 0.55, "VXUS": 0.25, "BND": 0.10, "VNQ": 0.10}, 0.084, 0.145, 0.5),
]


def _fallback_portfolio(reconciled_score: float) -> Portfolio:
    for ceiling, weights, expected_return, expected_volatility, sharpe in _FALLBACK_PORTFOLIOS:
        if reconciled_score <= ceiling:
            return Portfolio(
                asset_weights=weights,
                expected_return=expected_return,
                expected_volatility=expected_volatility,
                sharpe_ratio=sharpe,
            )

    ceiling, weights, expected_return, expected_volatility, sharpe = _FALLBACK_PORTFOLIOS[-1]
    return Portfolio(
        asset_weights=weights,
        expected_return=expected_return,
        expected_volatility=expected_volatility,
        sharpe_ratio=sharpe,
    )


def build_portfolio(
    reconciled_score: float, industry_interests: list[str] | None = None
) -> Portfolio:
    industry_interests = industry_interests or []

    if MU is None or COV is None:
        return _fallback_portfolio(reconciled_score)

    foundation, satellite_count = foundation_and_satellite_count(reconciled_score)
    match_scores = per_stock_match_scores(MU, COV, reconciled_score)
    satellites = select_satellites(industry_interests, satellite_count, match_scores)

    return optimize_subset(foundation, satellites, MU, COV, reconciled_score)
