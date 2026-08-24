from app.schemas import Percentiles, Portfolio, Simulation

# Placeholder for Phase 3 Steps 18-19 (Monte Carlo simulation, disciplined
# and reactive investor paths). Projects the goal amount forward using the
# portfolio's expected return/volatility with fixed percentile multipliers
# instead of actually running simulated paths, so the pipeline is
# exercisable end-to-end before the real simulation exists.


def simulate(
    portfolio: Portfolio,
    goal_amount: float,
    time_horizon_years: int,
    loss_aversion_score: float,
) -> Simulation:
    growth = (1 + portfolio.expected_return) ** time_horizon_years
    median = goal_amount * growth * 0.68

    disciplined_percentiles = Percentiles(
        p10=round(median * 0.62, 2),
        p50=round(median, 2),
        p90=round(median * 1.5, 2),
    )
    disciplined_success_prob = round(min(0.95, 0.5 + portfolio.sharpe_ratio / 2), 2)

    # Higher loss aversion -> more simulated panic-selling -> worse outcomes.
    behavior_drag = 0.15 + (loss_aversion_score / 100) * 0.25
    reactive_percentiles = Percentiles(
        p10=round(disciplined_percentiles.p10 * (1 - behavior_drag), 2),
        p50=round(disciplined_percentiles.p50 * (1 - behavior_drag), 2),
        p90=round(disciplined_percentiles.p90 * (1 - behavior_drag), 2),
    )
    reactive_success_prob = round(
        max(0.05, disciplined_success_prob - behavior_drag), 2
    )

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
