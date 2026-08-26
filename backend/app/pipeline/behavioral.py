# Placeholder for Phase 3 Step 14 (behavioral scoring rubric).
# Averages raw 1-5 Likert answers into a 0-100 behavioral score and a
# 0-100 loss-aversion score so the pipeline is exercisable end-to-end
# before the real rubric exists.


def score_behavioral(raw_answers: dict[str, int]) -> tuple[float, float]:
    if not raw_answers:
        return 50.0, 50.0

    values = list(raw_answers.values())
    mean = sum(values) / len(values)
    behavioral_score = round((mean - 1) / 4 * 100, 1)

    # Loss-aversion probe items (q13, q14, q16, q17 in the placeholder
    # questionnaire): falls back to the overall mean if absent.
    loss_aversion_ids = ["q13", "q14", "q16", "q17"]
    loss_values = [raw_answers[q] for q in loss_aversion_ids if q in raw_answers]
    loss_mean = sum(loss_values) / len(loss_values) if loss_values else mean
    loss_aversion_score = round((loss_mean - 1) / 4 * 100, 1)

    return behavioral_score, loss_aversion_score
