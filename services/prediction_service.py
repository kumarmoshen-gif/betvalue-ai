from providers.football_api import (
    get_team_id,
    get_team_statistics,
    get_last_matches,
)

from core.team_form import compute_team_form
from core.match_predictor_v2 import predict_match_v2
from core.value_bet import compute_value_bet


DEV_FALLBACK_ENABLED = True
DEMO_HOME_ODD = 2.10


def get_fake_stats(team_level="strong"):
    if team_level == "strong":
        return {
            "fixtures": {"played": {"total": 10}},
            "goals": {
                "for": {"total": {"total": 20}},
                "against": {"total": {"total": 10}},
            },
        }

    return {
        "fixtures": {"played": {"total": 10}},
        "goals": {
            "for": {"total": {"total": 15}},
            "against": {"total": {"total": 14}},
        },
    }


def get_fake_form(team_level="strong"):
    if team_level == "strong":
        return {
            "wins": 4,
            "draws": 0,
            "losses": 1,
            "goals_for": 10,
            "goals_against": 4,
            "points": 12,
            "form_score": 76,
        }

    return {
        "wins": 2,
        "draws": 1,
        "losses": 2,
        "goals_for": 6,
        "goals_against": 7,
        "points": 7,
        "form_score": 40,
    }


def get_ai_probability_for_bet(prediction, selected_bet, home_team, away_team):
    if selected_bet is None:
        return prediction["home"]

    bet = str(selected_bet).lower()

    if str(home_team).lower() in bet:
        return prediction["home"]

    if str(away_team).lower() in bet:
        return prediction["away"]

    if "draw" in bet or "nul" in bet:
        return prediction["draw"]

    return prediction["home"]


def enrich_with_value_bet(prediction, home_team, away_team, selected_bet=None, selected_odd=None):
    odd = selected_odd if selected_odd else DEMO_HOME_ODD

    ai_probability = get_ai_probability_for_bet(
        prediction,
        selected_bet,
        home_team,
        away_team
    )

    prediction["value_bet"] = compute_value_bet(
        ai_probability,
        odd
    )

    prediction["selected_bet"] = selected_bet
    prediction["selected_odd"] = odd

    return prediction


def get_fallback_prediction(home_team, away_team, selected_bet=None, selected_odd=None):
    prediction = predict_match_v2(
        get_fake_stats("strong"),
        get_fake_stats("medium"),
        get_fake_form("strong"),
        get_fake_form("medium"),
    )

    prediction["fallback"] = True
    prediction["message"] = "Données de démonstration utilisées car API-Football est indisponible."

    return enrich_with_value_bet(
        prediction,
        home_team,
        away_team,
        selected_bet,
        selected_odd
    )


def get_prediction_for_match(
    home_team,
    away_team,
    league_id=39,
    season=2024,
    selected_bet=None,
    selected_odd=None
):
    home_id = get_team_id(home_team)
    away_id = get_team_id(away_team)

    if home_id is None or away_id is None:
        if DEV_FALLBACK_ENABLED:
            return get_fallback_prediction(home_team, away_team, selected_bet, selected_odd)
        return None

    home_stats = get_team_statistics(home_id, league_id, season)
    away_stats = get_team_statistics(away_id, league_id, season)

    if home_stats is None or away_stats is None:
        if DEV_FALLBACK_ENABLED:
            return get_fallback_prediction(home_team, away_team, selected_bet, selected_odd)
        return None

    home_last_matches = get_last_matches(home_id, league_id, season)
    away_last_matches = get_last_matches(away_id, league_id, season)

    home_form = compute_team_form(home_last_matches, home_id)
    away_form = compute_team_form(away_last_matches, away_id)

    prediction = predict_match_v2(
        home_stats,
        away_stats,
        home_form,
        away_form,
    )

    prediction["fallback"] = False
    prediction["message"] = "Données réelles API-Football utilisées."

    return enrich_with_value_bet(
        prediction,
        home_team,
        away_team,
        selected_bet,
        selected_odd
    )