def compute_recent_form_score(form):
    """
    Calcule un score de forme récente sur 100.
    """

    if form is None:
        return 50

    points = form.get("points", 0)
    goals_for = form.get("goals_for", 0)
    goals_against = form.get("goals_against", 0)

    score = (
        points * 5
        + goals_for * 2
        - goals_against
    )

    return max(0, min(100, round(score, 1)))