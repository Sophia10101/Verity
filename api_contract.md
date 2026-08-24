# API Contract — Behavior-Aware Portfolio Advisor

## Design note
Rather than one HTTP endpoint per pipeline stage, the pipeline stages are implemented as separate, testable functions *inside* the backend, called by a small number of consolidated endpoints. This keeps the frontend simple (fewer network round-trips) while preserving clean separation for testing and understanding.

---

## Endpoints

### `POST /onboarding/submit`
Runs the full pipeline: scores capacity, scores behavioral profile, reconciles them, builds the portfolio, runs both Monte Carlo simulations, and saves everything to Supabase. Called once after a user finishes both forms (or retakes them).

**Request body**
```json
{
  "user_id": "uuid",
  "financial_profile": {
    "age": 29,
    "income_range": "$50,000–$75,000",
    "goal_amount_range": "$100,000–$500,000",
    "goal_timeframe_range": "10–20 years",
    "experience_level": "some"
  },
  "behavioral_responses": {
    "q1": 3, "q2": 5, "q3": 2
  }
}
```

**Response body**
```json
{
  "risk_scores": {
    "capacity_score": 72,
    "behavioral_score": 45,
    "loss_aversion_score": 68,
    "reconciled_score": 58,
    "explanation_text": "Your finances could support a more aggressive portfolio, but your answers suggest a strong reaction to losses, so we've dialed back the risk to reduce the chance of panic-selling."
  },
  "portfolio": {
    "asset_weights": { "VTI": 0.45, "VXUS": 0.15, "BND": 0.30, "VNQ": 0.10 },
    "expected_return": 0.071,
    "expected_volatility": 0.11,
    "sharpe_ratio": 0.52
  },
  "simulation": {
    "disciplined_percentiles": { "p10": 210000, "p50": 340000, "p90": 510000 },
    "reactive_percentiles": { "p10": 150000, "p50": 260000, "p90": 400000 },
    "disciplined_success_prob": 0.74,
    "reactive_success_prob": 0.51,
    "behavior_gap_dollars": 82000
  }
}
```

### `GET /results`
For returning users — fetches the most recent saved risk score, portfolio, and simulation results (joined) to populate the dashboard on login, without recomputing anything. Response shape matches `/onboarding/submit` above, pulled straight from the database.

### `POST /onboarding/retake` *(optional)*
If someone's situation changes, re-runs the whole pipeline and creates fresh rows (history over overwrite — see database_schema.md). Functionally identical to `/onboarding/submit`; a separate endpoint isn't strictly necessary.

---

## Internal backend structure
Not exposed as separate endpoints — these are separate functions/files called by `/onboarding/submit`:

```
score_capacity(financial_profile) -> capacity_score
score_behavioral(raw_answers) -> behavioral_score, loss_aversion_score
reconcile(capacity_score, behavioral_score, loss_aversion_score) -> reconciled_score, explanation_text
build_portfolio(reconciled_score) -> asset_weights, expected_return, expected_volatility, sharpe_ratio
simulate(portfolio, goal_amount, time_horizon, loss_aversion_score) -> disciplined + reactive results
```

Keeping these as clean, separate, testable functions means each stage can be unit tested individually, even though the frontend only ever calls one endpoint.
