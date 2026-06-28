from core.match_predictor_v2 import predict_match_v2

home_stats = {
    "fixtures": {"played": {"total": 10}},
    "goals": {
        "for": {"total": {"total": 20}},
        "against": {"total": {"total": 10}},
    },
}

away_stats = {
    "fixtures": {"played": {"total": 10}},
    "goals": {
        "for": {"total": {"total": 15}},
        "against": {"total": {"total": 14}},
    },
}

home_form = {
    "points": 12,
    "goals_for": 10,
    "goals_against": 4,
}

away_form = {
    "points": 7,
    "goals_for": 6,
    "goals_against": 7,
}

print(predict_match_v2(home_stats, away_stats, home_form, away_form))