def ratings_to_probabilities(home_rating, away_rating):
    """
    Transforme deux ratings en probabilités 1/N/2.
    """

    diff = home_rating - away_rating

    draw = 24

    if abs(diff) < 5:
        home = 38
        away = 38

    elif diff >= 30:
        home = 67
        draw = 17
        away = 16

    elif diff >= 20:
        home = 58
        draw = 20
        away = 22

    elif diff >= 10:
        home = 47
        draw = 23
        away = 30

    elif diff >= 5:
        home = 42
        draw = 24
        away = 34

    elif diff <= -30:
        home = 16
        draw = 17
        away = 67

    elif diff <= -20:
        home = 22
        draw = 20
        away = 58

    elif diff <= -10:
        home = 30
        draw = 23
        away = 47

    else:
        home = 34
        draw = 24
        away = 42

    return {
        "home": home,
        "draw": draw,
        "away": away,
        "diff": round(diff, 1),
    }