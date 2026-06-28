from core.form_model import form_score


def team_strength(stats, recent_matches, team_id, home=True):
    """
    Calcule un indice de puissance d'une équipe.
    """

    played = max(stats["fixtures"]["played"]["total"], 1)

    goals_for = stats["goals"]["for"]["total"]["total"] / played
    goals_against = stats["goals"]["against"]["total"]["total"] / played

    wins = stats["fixtures"]["wins"]["total"] / played

    clean_sheets = stats["clean_sheet"]["total"] / played

    form = form_score(recent_matches, team_id) / 15

    strength = (
        goals_for * 30
        + (3 - goals_against) * 20
        + wins * 30
        + clean_sheets * 10
        + form * 10
    )

    if home:
        strength += 5

    return strength


def predict_match(home_stats,
                  away_stats,
                  home_recent,
                  away_recent,
                  home_id,
                  away_id):

    home_strength = team_strength(
        home_stats,
        home_recent,
        home_id,
        True
    )

    away_strength = team_strength(
        away_stats,
        away_recent,
        away_id,
        False
    )

    total = home_strength + away_strength

    home = home_strength / total

    away = away_strength / total

    draw = 0.24

    # On réserve 24 % au nul
    home *= 0.76
    away *= 0.76

    return {
        "home": round(home * 100, 2),
        "draw": round(draw * 100, 2),
        "away": round(away * 100, 2),
    }