def form_score(matches, team_id):

    score = 0

    for match in matches:

        home = match["teams"]["home"]["id"]
        away = match["teams"]["away"]["id"]

        goals_home = match["goals"]["home"]
        goals_away = match["goals"]["away"]

        if home == team_id:

            if goals_home > goals_away:
                score += 3

            elif goals_home == goals_away:
                score += 1

        else:

            if goals_away > goals_home:
                score += 3

            elif goals_home == goals_away:
                score += 1

    return score