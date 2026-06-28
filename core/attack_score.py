def compute_attack_score(stats):
    """
    Calcule un score offensif sur 100.
    """

    if stats is None:
        return 50

    played = stats["fixtures"]["played"]["total"]

    if played == 0:
        return 50

    goals_for = stats["goals"]["for"]["total"]["total"]
    goals_per_match = goals_for / played

    score = goals_per_match * 35

    return max(0, min(100, round(score, 1)))