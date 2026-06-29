from database.repository import load_completed_predictions


def _matches_filter(value, selected_value):
    return selected_value == "Tous" or value == selected_value


def _filter_predictions(
    predictions,
    league="Tous",
    bookmaker="Tous",
    min_confidence=0,
    min_value=-100,
    include_fallback=False,
):
    filtered = []

    for prediction in predictions:
        if not include_fallback and prediction.get("fallback"):
            continue

        if not _matches_filter(prediction.get("league") or "Non renseignee", league):
            continue

        if not _matches_filter(
            prediction.get("bookmaker") or "Non renseigne",
            bookmaker,
        ):
            continue

        if (prediction.get("confidence") or 0) < min_confidence:
            continue

        if (prediction.get("value") or 0) < min_value:
            continue

        filtered.append(prediction)

    return filtered


def _build_curve(predictions):
    total_profit = 0
    total_stake = 0
    peak = 0
    curve = []

    for prediction in predictions:
        total_profit += prediction.get("profit") or 0
        total_stake += prediction.get("stake") or 0
        peak = max(peak, total_profit)
        roi = (total_profit / total_stake) * 100 if total_stake else 0

        curve.append({
            "created_at": prediction["created_at"],
            "profit": round(total_profit, 2),
            "roi": round(roi, 2),
            "drawdown": round(total_profit - peak, 2),
        })

    return curve


def _summarize(predictions):
    total_bets = len(predictions)
    total_stake = sum(prediction.get("stake") or 0 for prediction in predictions)
    total_profit = sum(prediction.get("profit") or 0 for prediction in predictions)
    won_bets = sum(1 for prediction in predictions if prediction.get("bet_won"))
    lost_bets = total_bets - won_bets
    roi = (total_profit / total_stake) * 100 if total_stake else 0
    hit_rate = (won_bets / total_bets) * 100 if total_bets else 0

    curve = _build_curve(predictions)
    max_drawdown = min(
        (point["drawdown"] for point in curve),
        default=0,
    )

    return {
        "total_bets": total_bets,
        "total_stake": round(total_stake, 2),
        "total_profit": round(total_profit, 2),
        "won_bets": won_bets,
        "lost_bets": lost_bets,
        "roi": round(roi, 2),
        "hit_rate": round(hit_rate, 2),
        "max_drawdown": round(max_drawdown, 2),
    }


def get_backtest_options():
    predictions = load_completed_predictions(include_fallback=True)

    leagues = sorted({
        prediction.get("league") or "Non renseignee"
        for prediction in predictions
    })
    bookmakers = sorted({
        prediction.get("bookmaker") or "Non renseigne"
        for prediction in predictions
    })

    return {
        "leagues": ["Tous", *leagues],
        "bookmakers": ["Tous", *bookmakers],
    }


def run_backtest(
    league="Tous",
    bookmaker="Tous",
    min_confidence=0,
    min_value=-100,
    include_fallback=False,
):
    predictions = load_completed_predictions(
        include_fallback=include_fallback,
    )
    filtered = _filter_predictions(
        predictions,
        league=league,
        bookmaker=bookmaker,
        min_confidence=min_confidence,
        min_value=min_value,
        include_fallback=include_fallback,
    )

    return {
        "summary": _summarize(filtered),
        "curve": _build_curve(filtered),
        "predictions": filtered,
    }
