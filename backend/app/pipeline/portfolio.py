from app.schemas import Portfolio

# Placeholder for Phase 3 Step 17 (PyPortfolioOpt + yfinance efficient
# frontier optimizer). Interpolates between four fixed model portfolios by
# reconciled_score so the pipeline is exercisable end-to-end before the
# real optimizer exists.

_MODEL_PORTFOLIOS = [
    # (score_ceiling, weights, expected_return, expected_volatility, sharpe)
    (25, {"VTI": 0.20, "VXUS": 0.05, "BND": 0.65, "VNQ": 0.10}, 0.045, 0.06, 0.48),
    (50, {"VTI": 0.35, "VXUS": 0.10, "BND": 0.45, "VNQ": 0.10}, 0.058, 0.085, 0.51),
    (75, {"VTI": 0.45, "VXUS": 0.15, "BND": 0.30, "VNQ": 0.10}, 0.071, 0.11, 0.52),
    (100, {"VTI": 0.55, "VXUS": 0.25, "BND": 0.10, "VNQ": 0.10}, 0.084, 0.145, 0.5),
]


def build_portfolio(reconciled_score: float) -> Portfolio:
    for ceiling, weights, expected_return, expected_volatility, sharpe in _MODEL_PORTFOLIOS:
        if reconciled_score <= ceiling:
            return Portfolio(
                asset_weights=weights,
                expected_return=expected_return,
                expected_volatility=expected_volatility,
                sharpe_ratio=sharpe,
            )

    ceiling, weights, expected_return, expected_volatility, sharpe = _MODEL_PORTFOLIOS[-1]
    return Portfolio(
        asset_weights=weights,
        expected_return=expected_return,
        expected_volatility=expected_volatility,
        sharpe_ratio=sharpe,
    )
