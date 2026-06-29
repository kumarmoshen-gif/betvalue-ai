from providers.football_api import (
    get_team_id,
    get_team_statistics,
    get_last_matches,
)

from core.team_form import compute_team_form
from core.match_predictor_v2 import predict_match_v2
from core.value_bet import compute_value_bet
from database.repository import (
    load_team_form,
    save_prediction,
    save_team_form,
)

from config import (
    DEFAULT_LEAGUE,
    DEFAULT_SEASON,
    DEFAULT_ODD,
    SAVE_FALLBACK_PREDICTIONS,
)


DEV_FALLBACK_ENABLED = True


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


def get_predicted_result(prediction, home_team, away_team, selected_bet=None):
    """
    Détermine le résultat prédit à enregistrer dans l'historique.

    Priorité :
    1. Si un pari est sélectionné depuis l'interface, on l'utilise.
    2. Sinon, on prend le résultat avec la plus forte probabilité IA.
    """

    if selected_bet:
        return selected_bet

    probabilities = {
        home_team: prediction["home"],
        "Draw": prediction["draw"],
        away_team: prediction["away"],
    }

    return max(probabilities, key=probabilities.get)


def get_ai_probability_for_bet(prediction, selected_bet, home_team, away_team):
    if selected_bet is None:
        predicted_result = get_predicted_result(
            prediction,
            home_team,
            away_team,
            selected_bet,
        )

        if predicted_result == home_team:
            return prediction["home"]

        if predicted_result == away_team:
            return prediction["away"]

        return prediction["draw"]

    bet = str(selected_bet).lower()

    if str(home_team).lower() in bet:
        return prediction["home"]

    if str(away_team).lower() in bet:
        return prediction["away"]

    if "draw" in bet or "nul" in bet:
        return prediction["draw"]

    return prediction["home"]


def enrich_with_value_bet(
    prediction,
    home_team,
    away_team,
    selected_bet=None,
    selected_odd=None
):
    odd = selected_odd if selected_odd else DEFAULT_ODD

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

    prediction["selected_bet"] = get_predicted_result(
        prediction,
        home_team,
        away_team,
        selected_bet,
    )

    prediction["selected_odd"] = odd

    return prediction


def prepare_prediction_for_history(
    prediction,
    home_team,
    away_team,
    selected_bet=None,
):
    prediction["match"] = f"{home_team} - {away_team}"
    prediction["home_team"] = home_team
    prediction["away_team"] = away_team

    prediction["predicted_result"] = get_predicted_result(
        prediction,
        home_team,
        away_team,
        selected_bet,
    )

    return prediction


def add_prediction_metadata(
    prediction,
    league=None,
    season=None,
    match_date=None,
    bookmaker=None,
    bet_type=None,
):
    prediction["league"] = league
    prediction["season"] = season
    prediction["match_date"] = match_date
    prediction["bookmaker"] = bookmaker
    prediction["bet_type"] = bet_type

    return prediction


def save_prediction_safely(prediction):
    try:
        save_prediction(prediction)
    except Exception as error:
        print(f"Erreur sauvegarde historique : {error}")


def get_cached_or_compute_team_form(team_id, league_id, season):
    cached_form = load_team_form(team_id, league_id, season)

    if cached_form is not None:
        return cached_form

    last_matches = get_last_matches(team_id, league_id, season)
    form = compute_team_form(last_matches, team_id)
    save_team_form(team_id, league_id, season, form)

    return form


def get_fallback_prediction(
    home_team,
    away_team,
    selected_bet=None,
    selected_odd=None,
    league=None,
    season=None,
    match_date=None,
    bookmaker=None,
    bet_type=None,
):
    prediction = predict_match_v2(
        get_fake_stats("strong"),
        get_fake_stats("medium"),
        get_fake_form("strong"),
        get_fake_form("medium"),
    )

    prediction["fallback"] = True
    prediction["message"] = (
        "Données de démonstration utilisées car "
        "API-Football est indisponible."
    )

    prediction = enrich_with_value_bet(
        prediction,
        home_team,
        away_team,
        selected_bet,
        selected_odd
    )

    prediction = prepare_prediction_for_history(
        prediction,
        home_team,
        away_team,
        selected_bet
    )

    prediction = add_prediction_metadata(
        prediction,
        league,
        season,
        match_date,
        bookmaker,
        bet_type,
    )

    if SAVE_FALLBACK_PREDICTIONS:
        save_prediction_safely(prediction)

    return prediction


def get_prediction_for_match(
    home_team,
    away_team,
    league_id=DEFAULT_LEAGUE,
    season=DEFAULT_SEASON,
    selected_bet=None,
    selected_odd=None,
    league=None,
    match_date=None,
    bookmaker=None,
    bet_type=None,
):
    home_id = get_team_id(home_team)
    away_id = get_team_id(away_team)

    if home_id is None or away_id is None:
        if DEV_FALLBACK_ENABLED:
            return get_fallback_prediction(
                home_team,
                away_team,
                selected_bet,
                selected_odd,
                league,
                season,
                match_date,
                bookmaker,
                bet_type,
            )
        return None

    home_stats = get_team_statistics(home_id, league_id, season)
    away_stats = get_team_statistics(away_id, league_id, season)

    if home_stats is None or away_stats is None:
        if DEV_FALLBACK_ENABLED:
            return get_fallback_prediction(
                home_team,
                away_team,
                selected_bet,
                selected_odd,
                league,
                season,
                match_date,
                bookmaker,
                bet_type,
            )
        return None

    home_form = get_cached_or_compute_team_form(home_id, league_id, season)
    away_form = get_cached_or_compute_team_form(away_id, league_id, season)

    prediction = predict_match_v2(
        home_stats,
        away_stats,
        home_form,
        away_form,
    )

    prediction["fallback"] = False
    prediction["message"] = "Données réelles API-Football utilisées."

    prediction = enrich_with_value_bet(
        prediction,
        home_team,
        away_team,
        selected_bet,
        selected_odd
    )

    prediction = prepare_prediction_for_history(
        prediction,
        home_team,
        away_team,
        selected_bet
    )

    prediction = add_prediction_metadata(
        prediction,
        league,
        season,
        match_date,
        bookmaker,
        bet_type,
    )

    save_prediction_safely(prediction)

    return prediction
