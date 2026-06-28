def compute_defense_score(stats):
    """
    Calcule un score défensif sur 100.
    Moins l'équipe encaisse de buts, meilleur est le score.
    """

    if stats is None:
        return 50

    played = stats["fixtures"]["played"]["total"]

    if played == 0:
        return 50

    goals_against = stats["goals"]["against"]["total"]["total"]
    goals_against_per_match = goals_against / played

    score = 100 - (goals_against_per_match * 35)

    return max(0, min(100, round(score, 1)))