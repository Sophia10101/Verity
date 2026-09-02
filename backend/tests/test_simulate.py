import numpy as np

from app.pipeline.simulate import simulate
from app.schemas import Portfolio

PORTFOLIO = Portfolio(
    asset_weights={"VTI": 0.6, "BND": 0.4},
    expected_return=0.07,
    expected_volatility=0.12,
    sharpe_ratio=0.5,
)


def test_zero_loss_aversion_means_reactive_matches_disciplined_exactly():
    # At loss_aversion_score=0, panic_prob is exactly 0, so the reactive
    # investor never sits out and is mathematically identical to the
    # disciplined investor (same monthly returns applied both ways). This
    # should hold regardless of the random seed.
    result = simulate(
        PORTFOLIO,
        goal_amount=500_000,
        time_horizon_years=10,
        loss_aversion_score=0,
        monthly_contribution=500,
        rng=np.random.default_rng(42),
    )
    assert result.reactive_percentiles == result.disciplined_percentiles
    assert result.behavior_gap_dollars == 0.0
    assert result.reactive_success_prob == result.disciplined_success_prob


def test_higher_loss_aversion_produces_worse_reactive_outcomes():
    low = simulate(
        PORTFOLIO,
        goal_amount=500_000,
        time_horizon_years=15,
        loss_aversion_score=10,
        monthly_contribution=500,
        rng=np.random.default_rng(7),
    )
    high = simulate(
        PORTFOLIO,
        goal_amount=500_000,
        time_horizon_years=15,
        loss_aversion_score=90,
        monthly_contribution=500,
        rng=np.random.default_rng(7),
    )
    assert high.reactive_percentiles.p50 < low.reactive_percentiles.p50
    assert high.behavior_gap_dollars > low.behavior_gap_dollars


def test_percentiles_are_ordered():
    result = simulate(
        PORTFOLIO,
        goal_amount=300_000,
        time_horizon_years=20,
        loss_aversion_score=60,
        monthly_contribution=750,
        rng=np.random.default_rng(1),
    )
    assert result.disciplined_percentiles.p10 <= result.disciplined_percentiles.p50
    assert result.disciplined_percentiles.p50 <= result.disciplined_percentiles.p90
    assert result.reactive_percentiles.p10 <= result.reactive_percentiles.p50
    assert result.reactive_percentiles.p50 <= result.reactive_percentiles.p90


def test_success_probabilities_are_valid_fractions():
    result = simulate(
        PORTFOLIO,
        goal_amount=1_000_000,
        time_horizon_years=25,
        loss_aversion_score=50,
        monthly_contribution=1000,
        rng=np.random.default_rng(3),
    )
    assert 0.0 <= result.disciplined_success_prob <= 1.0
    assert 0.0 <= result.reactive_success_prob <= 1.0


def test_disciplined_never_worse_than_reactive_on_average():
    # The disciplined investor should never do worse on average, since the
    # reactive investor's only divergence (panicking) can only hurt, never
    # help, in this model.
    result = simulate(
        PORTFOLIO,
        goal_amount=500_000,
        time_horizon_years=15,
        loss_aversion_score=80,
        monthly_contribution=500,
        rng=np.random.default_rng(11),
    )
    assert result.disciplined_percentiles.p50 >= result.reactive_percentiles.p50
    assert result.disciplined_success_prob >= result.reactive_success_prob
