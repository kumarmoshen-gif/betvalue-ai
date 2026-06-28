from core.defense_score import compute_defense_score

fake_stats = {
    "fixtures": {
        "played": {
            "total": 10
        }
    },
    "goals": {
        "against": {
            "total": {
                "total": 10
            }
        }
    }
}

print(compute_defense_score(fake_stats))