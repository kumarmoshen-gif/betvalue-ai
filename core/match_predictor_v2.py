from core.team_rating import compute_team_rating


def predict_match_v2(home_stats, away_stats, home_form=None, away_form=None):
    home_rating = compute_team_rating(home_stats, home_form)
    away_rating = compute_team_rating(away_stats, away_form)

    # Avantage domicile léger
    home_score = home_rating["rating"] + 5
    away_score = away_rating["rating"]

    total = home_score + away_score

    if total <= 0:
        return {
            "home": 33.3,
            "draw": 33.3,
            "away": 33.3,
            "home_rating": home_rating,
            "away_rating": away_rating,
        }

    draw_probability = 24
    remaining = 100 - draw_probability

    home_probability = (home_score / total) * remaining
    away_probability = (away_score / total) * remaining

    return {
        "home": round(home_probability, 1),
        "draw": draw_probability,
        "away": round(away_probability, 1),
        "home_rating": home_rating,
        "away_rating": away_rating,
    }