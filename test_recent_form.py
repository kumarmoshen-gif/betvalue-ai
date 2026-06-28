from core.recent_form_score import compute_recent_form_score

fake_form = {
    "points": 12,
    "goals_for": 10,
    "goals_against": 4,
}

print(compute_recent_form_score(fake_form))