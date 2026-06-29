def result_from_score(home_team, away_team, home_score, away_score):
    if home_score > away_score:
        return home_team

    if away_score > home_score:
        return away_team

    return "Draw"


def is_bet_won(predicted_result, actual_result):
    return str(predicted_result).strip().lower() == str(actual_result).strip().lower()


def compute_profit(bet_won, odd, stake):
    if bet_won:
        return round(stake * (odd - 1), 2)

    return round(-stake, 2)
