from database.repository import (
    find_finished_fixture_for_prediction,
    load_pending_predictions,
    update_prediction_from_fixture,
)


def settle_pending_predictions_from_fixtures(include_fallback=False):
    pending = load_pending_predictions()
    settled = []
    unmatched = []

    for prediction in pending:
        if prediction.get("fallback") and not include_fallback:
            unmatched.append({
                "prediction": prediction,
                "reason": "fallback",
            })
            continue

        fixture = find_finished_fixture_for_prediction(prediction)

        if fixture is None:
            unmatched.append({
                "prediction": prediction,
                "reason": "no_fixture",
            })
            continue

        result = update_prediction_from_fixture(
            prediction["id"],
            fixture,
        )
        settled.append({
            "prediction": prediction,
            "fixture": fixture,
            "result": result,
        })

    return {
        "settled": settled,
        "unmatched": unmatched,
    }
