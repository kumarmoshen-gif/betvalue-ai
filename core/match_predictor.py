from core.team_strength import compute_team_strength


def predict_match_probabilities(home_stats, away_stats, home_form=None, away_form=None):
    home_strength = compute_team_strength(home_stats)
    away_strength = compute_team_strength(away_stats)

    # Ajout de la forme récente
    if home_form:
        home_strength += home_form["form_score"] * 0.15

    if away_form:
        away_strength += away_form["form_score"] * 0.15

    # Avantage domicile
    home_strength += 5

    total_strength = home_strength + away_strength

    if total_strength == 0:
        return {
            "home": 33.33,
            "draw": 33.33,
            "away": 33.33,
        }

    draw_probability = 25
    remaining = 100 - draw_probability

    home_probability = (home_strength / total_strength) * remaining
    away_probability = (away_strength / total_strength) * remaining

    return {
        "home": round(home_probability, 2),
        "draw": round(draw_probability, 2),
        "away": round(away_probability, 2),
    }