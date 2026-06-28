def implied_probability(odd: float) -> float:
    return round((1 / odd) * 100, 2)


def expected_value(odd: float, model_probability: float) -> float:
    probability = model_probability / 100
    return round(((probability * odd) - 1) * 100, 2)


def estimate_light_probability(odd: float, selection: str) -> float:
    bookmaker_probability = implied_probability(odd)

    adjustment = 0

    if odd < 1.35:
        adjustment -= 4
    elif odd > 8:
        adjustment -= 3
    elif 1.80 <= odd <= 3.50:
        adjustment += 2

    if selection.lower() == "draw":
        adjustment -= 2

    return max(1, min(99, round(bookmaker_probability + adjustment, 2)))


def betvalue_score(ev: float, odd: float) -> int:
    score = 50

    if ev > 0:
        score += min(ev * 3, 35)
    else:
        score += max(ev * 2, -35)

    if 1.50 <= odd <= 4.00:
        score += 10
    elif odd > 8:
        score -= 10

    return int(max(0, min(100, round(score))))


def analyse_odds(rows):
    analysed = []

    for row in rows:
        odd = float(row["Cote"])
        selection = row["Pari"]

        bookmaker_probability = implied_probability(odd)
        model_probability = estimate_light_probability(odd, selection)

        ev = expected_value(odd, model_probability)
        score = betvalue_score(ev, odd)

        analysed.append({
            **row,
            "Proba bookmaker": f"{bookmaker_probability:.2f} %",
            "Proba modèle": f"{model_probability:.2f} %",
            "EV numérique": ev,
            "EV": f"{ev:.2f} %",
            "Score": score,
            "Décision": "🟢 VALUE" if ev > 5 else "🔴 PASS",
        })

    return sorted(analysed, key=lambda x: x["Score"], reverse=True)