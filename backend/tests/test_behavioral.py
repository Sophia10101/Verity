from app.pipeline.behavioral import score_behavioral


def test_empty_answers_returns_neutral_defaults():
    assert score_behavioral({}) == (50.0, 50.0)


def test_all_neutral_answers_returns_50_50():
    neutral = {f"q{i}": 3 for i in range(1, 18)}
    assert score_behavioral(neutral) == (50.0, 50.0)


def test_all_max_agreement():
    # Reverse-scored items (q14 behavioral; q3, q10, q12 loss aversion) pull
    # the score down even though every raw answer is a 5, since agreeing
    # with them means LOWER risk tolerance / LOWER panic tendency.
    high = {f"q{i}": 5 for i in range(1, 18)}
    assert score_behavioral(high) == (80.0, 80.0)


def test_all_min_agreement():
    # Mirror image of the all-5s case: linear normalization means the two
    # extremes sum to exactly 100 for each construct.
    low = {f"q{i}": 1 for i in range(1, 18)}
    behavioral_score, loss_aversion_score = score_behavioral(low)
    assert behavioral_score == 20.0
    assert loss_aversion_score == 20.0


def test_reverse_scored_item_flips_direction():
    # q14 ("prefers a guaranteed smaller gain") is reverse-scored for
    # behavioral_score: strongly agreeing should read as LOW risk tolerance.
    behavioral_score, _ = score_behavioral({"q14": 5})
    assert behavioral_score == 0.0

    behavioral_score, _ = score_behavioral({"q14": 1})
    assert behavioral_score == 100.0

    # q3 ("regrets actions more than inactions", the disposition effect) is
    # reverse-scored for loss_aversion_score: agreeing predicts holding, not
    # panic-selling.
    _, loss_aversion_score = score_behavioral({"q3": 5})
    assert loss_aversion_score == 0.0


def test_anchor_items_carry_more_weight():
    # q11 is a double-weighted anchor; q7 is a single-weight item. Pitted
    # against the same reverse-scored q14=5 (which alone would pull the
    # score to 0), the anchor should win out by more.
    with_anchor, _ = score_behavioral({"q11": 5, "q14": 5})
    with_non_anchor, _ = score_behavioral({"q7": 5, "q14": 5})

    assert with_non_anchor == 50.0  # equal weights cancel out to the midpoint
    assert with_anchor == 66.7  # anchor (weight 2) outweighs q14 (weight 1)
    assert with_anchor > with_non_anchor


def test_missing_construct_items_falls_back_to_50():
    # Only a loss-aversion item is supplied; behavioral_score has nothing to
    # compute from and should fall back to the neutral default.
    behavioral_score, loss_aversion_score = score_behavioral({"q13": 5})
    assert behavioral_score == 50.0
    assert loss_aversion_score == 100.0


def test_scores_are_independent():
    # Supplying only behavioral items shouldn't move loss_aversion_score,
    # and vice versa, since the two item sets don't overlap.
    behavioral_score, loss_aversion_score = score_behavioral({"q11": 5, "q15": 5})
    assert behavioral_score > 50.0
    assert loss_aversion_score == 50.0

    behavioral_score, loss_aversion_score = score_behavioral({"q16": 5, "q17": 5})
    assert behavioral_score == 50.0
    assert loss_aversion_score > 50.0
