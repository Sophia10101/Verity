# Phase 3 Step 14: behavioral questionnaire scoring rubric.
#
# Produces two scores from the 17-item questionnaire (see
# frontend/src/lib/questionnaire.ts for exact wording):
#   - behavioral_score: general psychological risk tolerance, independent
#     of finances (can they stomach risk in principle?)
#   - loss_aversion_score: specifically how prone they are to panic-react
#     to a loss (will they actually stay the course when it gets real?)
#
# These are kept as separate constructs on purpose: someone can score high
# on general risk tolerance while also scoring high on loss aversion, which
# is exactly the "tension" reconcile() is meant to catch and explain.
#
# Each item maps to at most one construct, with a direction (agreeing may
# raise or lower that construct) and a weight. The three most direct,
# validated-style items (q11, q13, q16) get double weight; the indirect
# psychological probes (q1-q10) are smaller corroborating signals. This is
# a reasoned starting rubric, not one calibrated against real outcome data,
# and is expected to be refined once real user data exists.

# weight, reverse-scored (True means agreeing lowers the construct)
BEHAVIORAL_ITEMS: dict[str, tuple[float, bool]] = {
    "q7": (1, False),  # enjoys risk/unpredictability
    "q11": (2, False),  # general willingness to take financial risk (anchor)
    "q14": (1, True),  # prefers a guaranteed smaller gain (reverse: less risk tolerant)
    "q15": (1, False),  # confident in beating the market (overconfidence -> more risk-taking)
}

LOSS_AVERSION_ITEMS: dict[str, tuple[float, bool]] = {
    "q1": (1, False),  # spur-of-the-moment decisions
    "q2": (1, False),  # abandons plans under pressure
    "q3": (1, True),  # regrets actions more than inactions (disposition effect: reverse)
    "q4": (1, False),  # uncomfortable without a clear outcome
    "q5": (1, False),  # not knowing is worse than bad news
    "q6": (1, False),  # trusts gut over analysis
    "q8": (1, False),  # herding: assumes the crowd is right
    "q9": (1, False),  # herding: comfort once others have decided
    "q10": (1, True),  # sticks with commitment when uncomfortable (protective: reverse)
    "q12": (1, True),  # researches thoroughly before investing (protective: reverse)
    "q13": (2, False),  # likely to sell after a 20% loss (anchor)
    "q16": (2, False),  # losing hurts more than an equal gain feels good (anchor)
    "q17": (1, False),  # checks accounts more often when values drop
}


def _weighted_score(
    raw_answers: dict[str, int], items: dict[str, tuple[float, bool]]
) -> float:
    total = 0.0
    total_weight = 0.0

    for item_id, (weight, reverse) in items.items():
        if item_id not in raw_answers:
            continue
        normalized = (raw_answers[item_id] - 1) / 4  # 1-5 Likert -> 0-1
        if reverse:
            normalized = 1 - normalized
        total += weight * normalized
        total_weight += weight

    if total_weight == 0:
        return 50.0

    return round(total / total_weight * 100, 1)


def score_behavioral(raw_answers: dict[str, int]) -> tuple[float, float]:
    if not raw_answers:
        return 50.0, 50.0

    behavioral_score = _weighted_score(raw_answers, BEHAVIORAL_ITEMS)
    loss_aversion_score = _weighted_score(raw_answers, LOSS_AVERSION_ITEMS)

    return behavioral_score, loss_aversion_score
