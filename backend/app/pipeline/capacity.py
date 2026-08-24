from app.schemas import FinancialProfile

# Placeholder for Phase 3 Step 13 (trained risk capacity model).
# Returns a deterministic 0-100 score from a simple heuristic so the
# pipeline is exercisable end-to-end before the real model exists.


def score_capacity(financial_profile: FinancialProfile) -> float:
    age_factor = max(0.0, 1 - (financial_profile.age - 25) / 60)
    experience_factor = {"none": 0.3, "some": 0.6, "experienced": 1.0}.get(
        financial_profile.experience_level, 0.5
    )
    score = 50 * age_factor + 50 * experience_factor
    return round(min(max(score, 0), 100), 1)
