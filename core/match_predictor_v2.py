from core.team_rating import compute_team_rating
from core.probability_engine import ratings_to_probabilities


def predict_match_v2(home_stats, away_stats, home_form=None, away_form=None):
    home_rating = compute_team_rating(home_stats, home_form)
    away_rating = compute_team_rating(away_stats, away_form)

    # Avantage domicile
    adjusted_home_rating = home_rating["rating"] + 5
    adjusted_away_rating = away_rating["rating"]

    probabilities = ratings_to_probabilities(
        adjusted_home_rating,
        adjusted_away_rating
    )

    return {
        "home": probabilities["home"],
        "draw": probabilities["draw"],
        "away": probabilities["away"],
        "diff": probabilities["diff"],
        "home_rating": home_rating,
        "away_rating": away_rating,
    }