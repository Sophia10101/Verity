# Phase 3 Step 15: reconciliation rules.
#
# Principle: the lower of capacity_score and behavioral_score always wins,
# never an average. Recommending more risk than someone's finances can
# support is bad advice regardless of how they feel about it; recommending
# more risk than someone is behaviorally comfortable with just sets up the
# exact panic-selling this product exists to prevent. So the baseline is a
# hard ceiling from two independent constraints:
#
#     baseline = min(capacity_score, behavioral_score)
#
# loss_aversion_score can only dial further DOWN from that baseline, never
# back up. It's drawn partly from indirect psychological items (impulsivity,
# need for certainty, herding), so it can reveal someone is more panic-prone
# than their own stated risk comfort (behavioral_score) suggests, which is
# the actual mismatch the product is built to catch. Being unusually
# composed (low loss aversion) doesn't unlock exceeding a ceiling that's
# already set by money and stated preference.

DIVERGENCE_THRESHOLD = 15  # |capacity - behavioral| below this counts as "aligned"
LOSS_AVERSION_ELEVATED_THRESHOLD = 60  # above this, call it out in the explanation
MAX_LOSS_AVERSION_PENALTY = 0.3  # loss_aversion_score of 100 -> 30% further cut


def reconcile(
    capacity_score: float, behavioral_score: float, loss_aversion_score: float
) -> tuple[float, str]:
    baseline = min(capacity_score, behavioral_score)
    loss_aversion_penalty = (
        max(0.0, loss_aversion_score - 50) / 50 * MAX_LOSS_AVERSION_PENALTY
    )
    reconciled_score = round(baseline * (1 - loss_aversion_penalty), 1)

    divergence = capacity_score - behavioral_score
    loss_averse = loss_aversion_score > LOSS_AVERSION_ELEVATED_THRESHOLD

    if divergence > DIVERGENCE_THRESHOLD:
        # Finances could support more than they're behaviorally comfortable with.
        if loss_averse:
            explanation = (
                "Your finances could support more risk, but you're not fully "
                "comfortable with it and prone to reacting to losses, so we've "
                "built this around your comfort level and dialed back further."
            )
        else:
            explanation = (
                "Your finances could support more risk, but you've told us "
                "you're more comfortable with a steadier approach, so this "
                "recommendation reflects that."
            )
    elif divergence < -DIVERGENCE_THRESHOLD:
        # They're comfortable with more risk than their finances can prudently
        # support, capacity is the binding constraint here regardless of loss
        # aversion.
        if loss_averse:
            explanation = (
                "You're comfortable with more risk than your finances can "
                "prudently support right now, so we've capped this at what "
                "your finances can handle, and dialed back further given how "
                "you tend to react to losses."
            )
        else:
            explanation = (
                "You're comfortable with more risk than your finances can "
                "prudently support right now, so we've capped this "
                "recommendation at what your finances can handle."
            )
    else:
        # Capacity and behavioral tolerance are aligned.
        if loss_averse:
            explanation = (
                "Your financial capacity and general comfort with risk are "
                "well aligned, but your reaction to losses specifically "
                "suggests dialing back further to help you stay invested."
            )
        else:
            explanation = (
                "Your financial capacity, risk comfort, and reaction to "
                "losses are all well aligned, so this recommendation "
                "reflects that directly."
            )

    return reconciled_score, explanation
