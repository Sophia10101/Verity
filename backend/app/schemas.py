from pydantic import BaseModel


class FinancialProfile(BaseModel):
    age: int
    income_range: str
    goal_amount_range: str
    goal_timeframe_range: str
    experience_level: str
    industry_interests: list[str] = []
    monthly_contribution_range: str | None = None


class OnboardingSubmitRequest(BaseModel):
    user_id: str
    financial_profile: FinancialProfile
    behavioral_responses: dict[str, int]


class RiskScores(BaseModel):
    capacity_score: float
    behavioral_score: float
    loss_aversion_score: float
    reconciled_score: float
    explanation_text: str


class Portfolio(BaseModel):
    asset_weights: dict[str, float]
    expected_return: float
    expected_volatility: float
    sharpe_ratio: float


class Percentiles(BaseModel):
    p10: float
    p50: float
    p90: float


class Simulation(BaseModel):
    disciplined_percentiles: Percentiles
    reactive_percentiles: Percentiles
    disciplined_success_prob: float
    reactive_success_prob: float
    behavior_gap_dollars: float


class OnboardingSubmitResponse(BaseModel):
    risk_scores: RiskScores
    portfolio: Portfolio
    simulation: Simulation
