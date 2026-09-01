import numpy as np
import pandas as pd

from app.pipeline.portfolio import (
    STOCK_SECTORS,
    foundation_and_satellite_count,
    optimize_subset,
    per_stock_match_scores,
    select_satellites,
)


def test_foundation_and_satellite_count_conservative():
    foundation, satellite_count = foundation_and_satellite_count(20)
    assert foundation == ["VTI", "VXUS", "BND", "GLD"]
    assert satellite_count == 2


def test_foundation_and_satellite_count_moderate_low_and_high():
    foundation, satellite_count = foundation_and_satellite_count(40)
    assert foundation == ["VTI", "VXUS", "BND", "GLD"]
    assert satellite_count == 3

    foundation, satellite_count = foundation_and_satellite_count(60)
    assert foundation == ["VTI", "VXUS", "BND", "VNQ"]
    assert satellite_count == 3


def test_foundation_and_satellite_count_aggressive_drops_bonds():
    foundation, satellite_count = foundation_and_satellite_count(80)
    assert foundation == ["VTI", "VXUS", "VNQ"]
    assert "BND" not in foundation
    assert satellite_count == 5


def test_foundation_and_satellite_count_boundaries():
    # 35 and 65 are the first values in the next band up, matching the < checks.
    assert foundation_and_satellite_count(34)[1] == 2
    assert foundation_and_satellite_count(35)[1] == 3
    assert foundation_and_satellite_count(64)[1] == 3
    assert foundation_and_satellite_count(65)[1] == 5


def test_select_satellites_filters_by_industry():
    # All scores equal, so the industry filter is the only thing that matters.
    match_scores = {t: 1.0 for t in STOCK_SECTORS}
    selected = select_satellites(["Technology"], 3, match_scores)
    assert all(STOCK_SECTORS[t] == "Technology" for t in selected)
    assert len(selected) == 3


def test_select_satellites_open_to_anything_ignores_sector():
    match_scores = {t: float(i) for i, t in enumerate(STOCK_SECTORS)}
    selected = select_satellites([], 3, match_scores)
    # Should pick the 3 highest-scoring tickers regardless of sector.
    expected = sorted(STOCK_SECTORS, key=lambda t: match_scores[t], reverse=True)[:3]
    assert selected == expected


def test_select_satellites_backfills_thin_industry():
    # Utilities only has one stock (NEE); asking for 3 satellites should pull
    # the other 2 from the best-scoring remainder rather than only returning 1.
    match_scores = {t: float(i) for i, t in enumerate(STOCK_SECTORS)}
    selected = select_satellites(["Utilities"], 3, match_scores)
    assert len(selected) == 3
    assert "NEE" in selected  # the one real Utilities match is still included


def test_match_scores_favor_low_volatility_for_conservative_profile():
    # One outlier stock with an extreme historical return AND extreme
    # volatility (modeling something like NVDA's real 10-year numbers),
    # against several modest, low-volatility stocks.
    tickers = list(STOCK_SECTORS)
    outlier = tickers[0]
    others = tickers[1:]

    mu = pd.Series({outlier: 0.65, **{t: 0.12 for t in others}})
    variances = {outlier: 0.5**2, **{t: 0.18**2 for t in others}}
    cov = pd.DataFrame(np.diag(list(variances.values())), index=tickers, columns=tickers)

    conservative_scores = per_stock_match_scores(mu, cov, reconciled_score=0)
    top_pick = max(conservative_scores, key=conservative_scores.get)

    # The outlier's extreme return shouldn't win out over a much better
    # volatility fit for a fully conservative target.
    assert top_pick != outlier


def test_match_scores_favor_high_return_for_aggressive_profile():
    tickers = list(STOCK_SECTORS)
    outlier = tickers[0]
    others = tickers[1:]

    mu = pd.Series({outlier: 0.65, **{t: 0.12 for t in others}})
    variances = {outlier: 0.5**2, **{t: 0.18**2 for t in others}}
    cov = pd.DataFrame(np.diag(list(variances.values())), index=tickers, columns=tickers)

    aggressive_scores = per_stock_match_scores(mu, cov, reconciled_score=100)
    top_pick = max(aggressive_scores, key=aggressive_scores.get)

    # At the aggressive end, the outlier's high volatility is exactly what's
    # being targeted, so its huge return advantage should win.
    assert top_pick == outlier


def test_optimize_subset_respects_weight_bounds_and_sums_to_one():
    foundation = ["F1", "F2"]
    satellites = ["S1", "S2"]
    tickers = foundation + satellites

    mu = pd.Series({"F1": 0.05, "F2": 0.07, "S1": 0.15, "S2": 0.20})
    variances = {"F1": 0.05**2, "F2": 0.08**2, "S1": 0.25**2, "S2": 0.30**2}
    cov = pd.DataFrame(np.diag(list(variances.values())), index=tickers, columns=tickers)

    portfolio = optimize_subset(foundation, satellites, mu, cov, reconciled_score=50)

    assert abs(sum(portfolio.asset_weights.values()) - 1.0) < 1e-3
    for ticker, weight in portfolio.asset_weights.items():
        if ticker in foundation:
            assert weight <= 0.60 + 1e-6
        else:
            assert weight <= 0.15 + 1e-6


def test_optimize_subset_higher_score_means_higher_volatility():
    foundation = ["F1", "F2"]
    satellites = ["S1", "S2"]
    tickers = foundation + satellites

    mu = pd.Series({"F1": 0.05, "F2": 0.07, "S1": 0.15, "S2": 0.20})
    variances = {"F1": 0.05**2, "F2": 0.08**2, "S1": 0.25**2, "S2": 0.30**2}
    cov = pd.DataFrame(np.diag(list(variances.values())), index=tickers, columns=tickers)

    conservative = optimize_subset(foundation, satellites, mu, cov, reconciled_score=0)
    aggressive = optimize_subset(foundation, satellites, mu, cov, reconciled_score=100)

    assert aggressive.expected_volatility > conservative.expected_volatility
