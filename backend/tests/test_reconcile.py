from app.pipeline.reconcile import reconcile


def test_baseline_is_the_minimum_not_an_average():
    # capacity=80, behavioral=40, neutral loss aversion (50 -> no penalty)
    reconciled_score, _ = reconcile(80, 40, 50)
    assert reconciled_score == 40.0  # min(80, 40), not the average (60)

    reconciled_score, _ = reconcile(40, 80, 50)
    assert reconciled_score == 40.0  # min still wins regardless of which side is lower


def test_loss_aversion_only_penalizes_never_boosts():
    # Below-neutral loss aversion should apply no penalty at all.
    reconciled_score, _ = reconcile(60, 60, 0)
    assert reconciled_score == 60.0

    reconciled_score, _ = reconcile(60, 60, 50)
    assert reconciled_score == 60.0

    # Max loss aversion (100) applies the full 30% cut.
    reconciled_score, _ = reconcile(60, 60, 100)
    assert reconciled_score == 42.0  # 60 * 0.7


def test_reconciled_score_never_exceeds_baseline():
    # Regardless of loss aversion, reconciled_score should never exceed
    # min(capacity, behavioral).
    for loss_aversion in (0, 25, 50, 75, 100):
        reconciled_score, _ = reconcile(70, 55, loss_aversion)
        assert reconciled_score <= 55.0


def test_explanation_capacity_exceeds_behavioral():
    _, explanation = reconcile(80, 50, 40)  # divergence=30, loss aversion normal
    assert "steadier approach" in explanation

    _, explanation = reconcile(80, 50, 80)  # divergence=30, loss aversion elevated
    assert "prone to reacting to losses" in explanation


def test_explanation_behavioral_exceeds_capacity():
    _, explanation = reconcile(40, 80, 40)  # divergence=-40, loss aversion normal
    assert "capped this recommendation at what your finances can handle" in explanation

    _, explanation = reconcile(40, 80, 80)  # divergence=-40, loss aversion elevated
    assert "dialed back further given how you tend to react to losses" in explanation


def test_explanation_aligned():
    _, explanation = reconcile(60, 55, 40)  # divergence=5, loss aversion normal
    assert "reflects that directly" in explanation

    _, explanation = reconcile(60, 55, 80)  # divergence=5, loss aversion elevated
    assert "dialing back further to help you stay invested" in explanation


def test_divergence_threshold_boundary():
    # Exactly at the threshold (15) should still count as "aligned", not
    # diverged, since the check is a strict >.
    _, explanation = reconcile(65, 50, 40)  # divergence == 15 exactly
    assert "reflects that directly" in explanation
