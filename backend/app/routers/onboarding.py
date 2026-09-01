from fastapi import APIRouter

from app.buckets import GOAL_AMOUNT_BUCKETS, GOAL_TIMEFRAME_BUCKETS, midpoint_for
from app.pipeline.behavioral import score_behavioral
from app.pipeline.capacity import score_capacity
from app.pipeline.portfolio import build_portfolio
from app.pipeline.reconcile import reconcile
from app.pipeline.simulate import simulate
from app.schemas import (
    OnboardingSubmitRequest,
    OnboardingSubmitResponse,
    RiskScores,
)

router = APIRouter(prefix="/onboarding", tags=["onboarding"])


def _run_pipeline(payload: OnboardingSubmitRequest) -> OnboardingSubmitResponse:
    capacity_score = score_capacity(payload.financial_profile)
    behavioral_score, loss_aversion_score = score_behavioral(payload.behavioral_responses)
    reconciled_score, explanation_text = reconcile(
        capacity_score, behavioral_score, loss_aversion_score
    )

    portfolio = build_portfolio(
        reconciled_score, payload.financial_profile.industry_interests
    )

    goal_amount = midpoint_for(
        GOAL_AMOUNT_BUCKETS, payload.financial_profile.goal_amount_range
    )
    time_horizon_years = int(
        midpoint_for(
            GOAL_TIMEFRAME_BUCKETS, payload.financial_profile.goal_timeframe_range
        )
    )
    simulation = simulate(portfolio, goal_amount, time_horizon_years, loss_aversion_score)

    # TODO (Phase 3 Step 16): persist risk_scores/portfolios/simulation_results
    # to Supabase here using the service-role key, instead of only returning
    # the computed values.

    return OnboardingSubmitResponse(
        risk_scores=RiskScores(
            capacity_score=capacity_score,
            behavioral_score=behavioral_score,
            loss_aversion_score=loss_aversion_score,
            reconciled_score=reconciled_score,
            explanation_text=explanation_text,
        ),
        portfolio=portfolio,
        simulation=simulation,
    )


@router.post("/submit", response_model=OnboardingSubmitResponse)
def submit_onboarding(payload: OnboardingSubmitRequest) -> OnboardingSubmitResponse:
    return _run_pipeline(payload)


@router.post("/retake", response_model=OnboardingSubmitResponse)
def retake_onboarding(payload: OnboardingSubmitRequest) -> OnboardingSubmitResponse:
    return _run_pipeline(payload)
