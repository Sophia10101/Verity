# Phase 3 Steps 18-19: Monte Carlo simulation.
#
# Simulates N independent monthly return paths over the goal timeframe,
# starting from $0 and building up purely through monthly contributions
# plus market growth (no "current savings" input exists yet, that's a
# reasonable future field to add).
#
# Disciplined and reactive investors are simulated as a PAIR on each path,
# using the exact same random monthly return each month for both. That's
# deliberate: it isolates the "behavior gap" to be purely about behavior,
# not about the reactive investor coincidentally hitting worse market luck.
#
# The reactive investor's panic-selling model (Step 19): each month they're
# invested, track their portfolio's drawdown from its running peak. If that
# drawdown is at least DRAWDOWN_THRESHOLD, there's a chance each month they
# panic-sell, move to cash for CASH_OUT_MONTHS, then re-enter, missing
# whatever recovery happened while they were out (the actual "buy high,
# sell low" mechanism). loss_aversion_score scales that monthly panic
# probability linearly: 0 means they never panic (and so are mathematically
# identical to the disciplined investor), 100 means the full base rate.

from __future__ import annotations

import numpy as np

from app.schemas import Percentiles, Portfolio, Simulation

N_SIMULATIONS = 5000
MONTHS_PER_YEAR = 12

DRAWDOWN_THRESHOLD = 0.15  # 15% off the peak counts as a "scary" drawdown
BASE_MONTHLY_PANIC_PROB = 0.15  # per-month panic chance at loss_aversion_score=100
CASH_OUT_MONTHS = 6  # how long a panicked investor sits out before re-entering
CASH_RETURN_MONTHLY = 0.02 / MONTHS_PER_YEAR  # near risk-free while sitting out


def _run_paths(
    portfolio: Portfolio,
    months: int,
    monthly_contribution: float,
    loss_aversion_score: float,
    rng: np.random.Generator,
) -> tuple[np.ndarray, np.ndarray]:
    monthly_mean = (1 + portfolio.expected_return) ** (1 / MONTHS_PER_YEAR) - 1
    monthly_std = portfolio.expected_volatility / np.sqrt(MONTHS_PER_YEAR)
    panic_prob = (loss_aversion_score / 100) * BASE_MONTHLY_PANIC_PROB

    returns = rng.normal(monthly_mean, monthly_std, size=(N_SIMULATIONS, months))
    panic_rolls = rng.random(size=(N_SIMULATIONS, months))

    disciplined = np.zeros(N_SIMULATIONS)
    reactive = np.zeros(N_SIMULATIONS)
    reactive_peak = np.zeros(N_SIMULATIONS)
    months_in_cash = np.zeros(N_SIMULATIONS, dtype=int)

    for month in range(months):
        r = returns[:, month]

        disciplined += monthly_contribution
        disciplined *= 1 + r

        reactive += monthly_contribution
        in_cash = months_in_cash > 0
        invested = ~in_cash

        reactive[in_cash] *= 1 + CASH_RETURN_MONTHLY
        reactive[invested] *= 1 + r[invested]
        months_in_cash[in_cash] -= 1

        reactive_peak[invested] = np.maximum(reactive_peak[invested], reactive[invested])
        has_peak = invested & (reactive_peak > 0)
        drawdown = np.zeros(N_SIMULATIONS)
        drawdown[has_peak] = 1 - reactive[has_peak] / reactive_peak[has_peak]

        panics_now = has_peak & (drawdown >= DRAWDOWN_THRESHOLD) & (
            panic_rolls[:, month] < panic_prob
        )
        months_in_cash[panics_now] = CASH_OUT_MONTHS
        reactive_peak[panics_now] = 0.0

    return disciplined, reactive


def simulate(
    portfolio: Portfolio,
    goal_amount: float,
    time_horizon_years: int,
    loss_aversion_score: float,
    monthly_contribution: float,
    rng: np.random.Generator | None = None,
) -> Simulation:
    rng = rng or np.random.default_rng()
    months = time_horizon_years * MONTHS_PER_YEAR

    disciplined, reactive = _run_paths(
        portfolio, months, monthly_contribution, loss_aversion_score, rng
    )

    disciplined_percentiles = Percentiles(
        p10=round(float(np.percentile(disciplined, 10)), 2),
        p50=round(float(np.percentile(disciplined, 50)), 2),
        p90=round(float(np.percentile(disciplined, 90)), 2),
    )
    reactive_percentiles = Percentiles(
        p10=round(float(np.percentile(reactive, 10)), 2),
        p50=round(float(np.percentile(reactive, 50)), 2),
        p90=round(float(np.percentile(reactive, 90)), 2),
    )

    disciplined_success_prob = round(float(np.mean(disciplined >= goal_amount)), 2)
    reactive_success_prob = round(float(np.mean(reactive >= goal_amount)), 2)

    behavior_gap_dollars = round(
        disciplined_percentiles.p50 - reactive_percentiles.p50, 2
    )

    return Simulation(
        disciplined_percentiles=disciplined_percentiles,
        reactive_percentiles=reactive_percentiles,
        disciplined_success_prob=disciplined_success_prob,
        reactive_success_prob=reactive_success_prob,
        behavior_gap_dollars=behavior_gap_dollars,
    )
