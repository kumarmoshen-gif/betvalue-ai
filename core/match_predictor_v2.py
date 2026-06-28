from core.team_rating import compute_team_rating
from core.probability_engine import ratings_to_probabilities


def predict_match_v2(home_stats, away_stats, home_form=None, away_form=None):
    home_rating = compute_team_rating(
        home_stats,
        home_form,
        is_home=True
    )

    away_rating = compute_team_rating(
        away_stats,
        away_form,
        is_home=False
    )

    probabilities = ratings_to_probabilities(
        home_rating["rating"],
        away_rating["rating"]
    )

    return {
        "home": probabilities["home"],
        "draw": probabilities["draw"],
        "away": probabilities["away"],
        "diff": probabilities["diff"],
        "home_rating": home_rating,
        "away_rating": away_rating,
    }