def compute_team_form(last_matches, team_id):
    if not last_matches:
        return {
            "wins": 0,
            "draws": 0,
            "losses": 0,
            "goals_for": 0,
            "goals_against": 0,
            "points": 0,
            "form_score": 50,
        }

    wins = draws = losses = 0
    goals_for = goals_against = 0

    for match in last_matches:
        home_id = match["teams"]["home"]["id"]
        away_id = match["teams"]["away"]["id"]

        home_goals = match["goals"]["home"]
        away_goals = match["goals"]["away"]

        if team_id == home_id:
            gf = home_goals
            ga = away_goals
        elif team_id == away_id:
            gf = away_goals
            ga = home_goals
        else:
            continue

        goals_for += gf
        goals_against += ga

        if gf > ga:
            wins += 1
        elif gf == ga:
            draws += 1
        else:
            losses += 1

    points = wins * 3 + draws

    form_score = (
        points * 5
        + goals_for * 2
        - goals_against
    )

    form_score = max(0, min(100, round(form_score, 1)))

    return {
        "wins": wins,
        "draws": draws,
        "losses": losses,
        "goals_for": goals_for,
        "goals_against": goals_against,
        "points": points,
        "form_score": form_score,
    }