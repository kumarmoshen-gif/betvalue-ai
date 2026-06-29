import sqlite3

from database.database import DB_PATH
from database.repository import save_fixture, save_prediction
from services.settlement_service import settle_pending_predictions_from_fixtures


TEST_MATCH = "Auto Home Test - Auto Away Test"
TEST_FIXTURE_ID = 999999002


def cleanup():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("DELETE FROM prediction_history WHERE match = ?", (TEST_MATCH,))
    conn.execute("DELETE FROM fixtures WHERE api_id = ?", (TEST_FIXTURE_ID,))
    conn.commit()
    conn.close()


cleanup()

save_prediction({
    "created_at": "2026-06-29T12:00:00",
    "match": TEST_MATCH,
    "home_team": "Auto Home Test",
    "away_team": "Auto Away Test",
    "selected_bet": "Auto Home Test",
    "home": 55,
    "draw": 25,
    "away": 20,
    "confidence": 70,
    "selected_odd": 2.0,
    "value_bet": {
        "bookmaker_probability": 50,
        "value": 5,
        "decision": "VALUE",
    },
    "fallback": False,
    "stake": 1,
    "league": "Test League",
    "season": 2024,
})

save_fixture({
    "fixture": {
        "id": TEST_FIXTURE_ID,
        "date": "2026-06-30T20:00:00+00:00",
        "status": {"short": "FT"},
    },
    "league": {
        "id": 39,
        "season": 2024,
    },
    "teams": {
        "home": {"id": 1001, "name": "Auto Home Test"},
        "away": {"id": 1002, "name": "Auto Away Test"},
    },
    "goals": {
        "home": 2,
        "away": 1,
    },
})

settlement = settle_pending_predictions_from_fixtures()

assert len(settlement["settled"]) == 1
assert settlement["settled"][0]["result"]["bet_won"] is True
assert settlement["settled"][0]["result"]["profit"] == 1.0

cleanup()
