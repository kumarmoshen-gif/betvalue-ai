from providers.football_api import (
    get_team_id,
    get_team_statistics,
    get_last_matches,
)

from core.team_form import compute_team_form
from core.match_predictor_v2 import predict_match_v2


def get_prediction_for_match(home_team, away_team, league_id=39, season=2024):
    home_id = get_team_id(home_team)
    away_id = get_team_id(away_team)

    if home_id is None or away_id is None:
        return None

    home_stats = get_team_statistics(home_id, league_id, season)
    away_stats = get_team_statistics(away_id, league_id, season)

    if home_stats is None or away_stats is None:
        return None

    home_last_matches = get_last_matches(home_id, league_id, season)
    away_last_matches = get_last_matches(away_id, league_id, season)

    home_form = compute_team_form(home_last_matches, home_id)
    away_form = compute_team_form(away_last_matches, away_id)

    return predict_match_v2(
        home_stats,
        away_stats,
        home_form,
        away_form,
    )