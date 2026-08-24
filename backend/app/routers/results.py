from fastapi import APIRouter, HTTPException

router = APIRouter(tags=["results"])


@router.get("/results")
def get_results(user_id: str):
    # TODO (Phase 3 Step 16): once /onboarding/submit persists to Supabase,
    # fetch and join the most recent risk_scores/portfolios/simulation_results
    # rows for user_id here, matching the OnboardingSubmitResponse shape.
    # Until then, the Next.js results page reads straight from Supabase.
    raise HTTPException(
        status_code=501,
        detail="Not implemented yet — results are read directly from Supabase for now.",
    )
