from core.team_rating import compute_team_rating

fake_stats = {
    "fixtures": {
        "played": {
            "total": 10
        }
    },
    "goals": {
        "for": {
            "total": {
                "total": 20
            }
        },
        "against": {
            "total": {
                "total": 10
            }
        }
    }
}

fake_form = {
    "points": 12,
    "goals_for": 10,
    "goals_against": 4,
}

print(compute_team_rating(fake_stats, fake_form))