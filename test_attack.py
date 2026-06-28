from core.attack_score import compute_attack_score

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
        }
    }
}

print(compute_attack_score(fake_stats))