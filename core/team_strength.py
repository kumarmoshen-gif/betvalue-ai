def compute_team_strength(stats):
    """
    Retourne un score de force compris entre 0 et 100.
    """

    if stats is None:
        return 50

    played = stats["fixtures"]["played"]["total"]

    if played == 0:
        return 50

    wins = stats["fixtures"]["wins"]["total"]
    draws = stats["fixtures"]["draws"]["total"]
    losses = stats["fixtures"]["loses"]["total"]

    goals_for = stats["goals"]["for"]["total"]["total"]
    goals_against = stats["goals"]["against"]["total"]["total"]

    clean_sheets = stats["clean_sheet"]["total"]
    failed_to_score = stats["failed_to_score"]["total"]

    gf_per_match = goals_for / played
    ga_per_match = goals_against / played

    score = 50

    # Victoires
    score += wins * 1.2

    # Nuls
    score += draws * 0.3

    # Défaites
    score -= losses * 0.6

    # Attaque
    score += gf_per_match * 8

    # Défense
    score -= ga_per_match * 6

    # Clean sheets
    score += clean_sheets * 0.8

    # Matchs sans marquer
    score -= failed_to_score * 0.8

    score = max(0, min(100, round(score, 1)))

    return score