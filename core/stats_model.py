def estimate_probability(home_stats, away_stats):
    """
    Estime la probabilité de victoire de l'équipe à domicile.
    Retourne une valeur comprise entre 10% et 90%.
    """

    # Buts marqués
    home_scored = home_stats["goals"]["for"]["total"]["total"]
    away_scored = away_stats["goals"]["for"]["total"]["total"]

    # Buts encaissés
    home_conceded = home_stats["goals"]["against"]["total"]["total"]
    away_conceded = away_stats["goals"]["against"]["total"]["total"]

    # Victoires
    home_wins = home_stats["fixtures"]["wins"]["total"]
    away_wins = away_stats["fixtures"]["wins"]["total"]

    # Matchs joués
    home_played = max(home_stats["fixtures"]["played"]["total"], 1)
    away_played = max(away_stats["fixtures"]["played"]["total"], 1)

    # Moyennes
    home_attack = home_scored / home_played
    away_attack = away_scored / away_played

    home_defense = home_conceded / home_played
    away_defense = away_conceded / away_played

    home_winrate = home_wins / home_played
    away_winrate = away_wins / away_played

    # Score de puissance
    home_strength = (
        home_attack * 45
        + home_winrate * 35
        + (3 - home_defense) * 20
    )

    away_strength = (
        away_attack * 45
        + away_winrate * 35
        + (3 - away_defense) * 20
    )

    total = home_strength + away_strength

    if total <= 0:
        return 50

    probability = (home_strength / total) * 100

    # Limites réalistes
    probability = max(10, min(90, probability))

    return round(probability, 2)