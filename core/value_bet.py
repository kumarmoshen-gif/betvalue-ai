def implied_probability(odd):
    """
    Convertit une cote décimale en probabilité implicite bookmaker.
    Exemple : cote 2.00 = 50 %
    """

    if odd <= 1:
        return 0

    return round((1 / odd) * 100, 2)


def compute_value_bet(ai_probability, odd):
    """
    Compare la probabilité IA avec la probabilité bookmaker.
    """

    bookmaker_probability = implied_probability(odd)
    value = round(ai_probability - bookmaker_probability, 2)

    if value >= 10:
        decision = "🟢 VALUE FORTE"
    elif value >= 5:
        decision = "🟡 VALUE"
    else:
        decision = "🔴 PAS DE VALUE"

    return {
        "odd": odd,
        "ai_probability": ai_probability,
        "bookmaker_probability": bookmaker_probability,
        "value": value,
        "decision": decision,
    }