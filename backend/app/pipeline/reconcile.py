# Placeholder for Phase 3 Step 15 (reconciliation rules).
# Blends capacity and behavioral scores, dialing back toward the more
# conservative score when loss aversion is high, so the pipeline is
# exercisable end-to-end before the real rules exist.


def reconcile(
    capacity_score: float, behavioral_score: float, loss_aversion_score: float
) -> tuple[float, str]:
    loss_aversion_weight = loss_aversion_score / 100
    reconciled_score = (
        capacity_score * (1 - loss_aversion_weight)
        + behavioral_score * loss_aversion_weight
    )
    reconciled_score = round(reconciled_score, 1)

    if capacity_score - behavioral_score > 15:
        explanation = (
            "Your finances could support a more aggressive portfolio, but your "
            "answers suggest a strong reaction to losses, so we've dialed back "
            "the risk to reduce the chance of panic-selling."
        )
    elif behavioral_score - capacity_score > 15:
        explanation = (
            "You're comfortable with more risk than your finances may "
            "comfortably support, so we've moderated the recommendation."
        )
    else:
        explanation = (
            "Your financial capacity and behavioral tolerance are well "
            "aligned, so this recommendation reflects both directly."
        )

    return reconciled_score, explanation
