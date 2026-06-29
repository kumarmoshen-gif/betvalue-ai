import json
from datetime import datetime

from database.database import get_connection


def save_team(team_data):
    team = team_data["team"]

    conn = get_connection()

    conn.execute(
        """
        INSERT OR REPLACE INTO teams
        (api_id, name, country, logo, raw_data, updated_at)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            team["id"],
            team["name"],
            team.get("country"),
            team.get("logo"),
            json.dumps(team_data),
            datetime.utcnow().isoformat(),
        ),
    )

    conn.commit()
    conn.close()


def load_team_by_name(team_name):
    conn = get_connection()

    row = conn.execute(
        """
        SELECT raw_data
        FROM teams
        WHERE LOWER(name) = LOWER(?)
        """,
        (team_name,),
    ).fetchone()

    conn.close()

    if row is None:
        return None

    return json.loads(row["raw_data"])


def save_team_statistics(team_api_id, league_id, season, data):
    conn = get_connection()

    conn.execute(
        """
        INSERT OR REPLACE INTO team_statistics
        (team_api_id, league_id, season, data, updated_at)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            team_api_id,
            league_id,
            season,
            json.dumps(data),
            datetime.utcnow().isoformat(),
        ),
    )

    conn.commit()
    conn.close()


def load_team_statistics(team_api_id, league_id, season):
    conn = get_connection()

    row = conn.execute(
        """
        SELECT data
        FROM team_statistics
        WHERE team_api_id = ?
        AND league_id = ?
        AND season = ?
        """,
        (team_api_id, league_id, season),
    ).fetchone()

    conn.close()

    if row is None:
        return None

    return json.loads(row["data"])


def save_prediction(prediction):
    conn = get_connection()

    conn.execute(
        """
        INSERT INTO prediction_history (
            created_at,
            match,
            home_team,
            away_team,
            predicted_result,
            home_probability,
            draw_probability,
            away_probability,
            confidence,
            odd,
            bookmaker_probability,
            value,
            decision,
            fallback,
            stake,
            result,
            bet_won,
            profit
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            datetime.utcnow().isoformat(),
            prediction["match"],
            prediction["home_team"],
            prediction["away_team"],
            prediction["selected_bet"],
            prediction["home"],
            prediction["draw"],
            prediction["away"],
            prediction["confidence"],
            prediction["selected_odd"],
            prediction["value_bet"]["bookmaker_probability"]
            if prediction.get("value_bet")
            else None,
            prediction["value_bet"]["value"]
            if prediction.get("value_bet")
            else None,
            prediction["value_bet"]["decision"]
            if prediction.get("value_bet")
            else None,
            int(prediction.get("fallback", False)),
            prediction.get("stake", 1),
            prediction.get("result"),
            prediction.get("bet_won"),
            prediction.get("profit", 0),
        ),
    )

    conn.commit()
    conn.close()


def load_prediction_history(limit=100):
    conn = get_connection()

    rows = conn.execute(
        """
        SELECT *
        FROM prediction_history
        ORDER BY created_at DESC
        LIMIT ?
        """,
        (limit,),
    ).fetchall()

    conn.close()

    return [dict(row) for row in rows]


def load_pending_predictions(limit=100):
    conn = get_connection()

    rows = conn.execute(
        """
        SELECT *
        FROM prediction_history
        WHERE result IS NULL
        ORDER BY created_at DESC
        LIMIT ?
        """,
        (limit,),
    ).fetchall()

    conn.close()

    return [dict(row) for row in rows]


def update_prediction_result(prediction_id, result, stake=1):
    conn = get_connection()

    row = conn.execute(
        """
        SELECT predicted_result, odd
        FROM prediction_history
        WHERE id = ?
        """,
        (prediction_id,),
    ).fetchone()

    if row is None:
        conn.close()
        return None

    predicted_result = row["predicted_result"]
    odd = row["odd"]

    bet_won = int(str(predicted_result).lower() == str(result).lower())

    if bet_won:
        profit = round((odd - 1) * stake, 2)
    else:
        profit = -stake

    conn.execute(
        """
        UPDATE prediction_history
        SET result = ?,
            stake = ?,
            bet_won = ?,
            profit = ?
        WHERE id = ?
        """,
        (
            result,
            stake,
            bet_won,
            profit,
            prediction_id,
        ),
    )

    conn.commit()
    conn.close()

    return {
        "prediction_id": prediction_id,
        "result": result,
        "stake": stake,
        "bet_won": bet_won,
        "profit": profit,
    }


def load_performance_stats():
    conn = get_connection()

    rows = conn.execute(
        """
        SELECT stake, bet_won, profit
        FROM prediction_history
        WHERE result IS NOT NULL
        """
    ).fetchall()

    conn.close()

    bets = [dict(row) for row in rows]

    total_bets = len(bets)
    won_bets = sum(1 for bet in bets if bet["bet_won"] == 1)
    lost_bets = sum(1 for bet in bets if bet["bet_won"] == 0)

    total_stake = sum(float(bet["stake"] or 0) for bet in bets)
    total_profit = sum(float(bet["profit"] or 0) for bet in bets)

    roi = round((total_profit / total_stake) * 100, 2) if total_stake else 0
    hit_rate = round((won_bets / total_bets) * 100, 2) if total_bets else 0

    return {
        "total_bets": total_bets,
        "won_bets": won_bets,
        "lost_bets": lost_bets,
        "total_stake": round(total_stake, 2),
        "total_profit": round(total_profit, 2),
        "roi": roi,
        "hit_rate": hit_rate,
    }
def load_bankroll_history():
    conn = get_connection()

    rows = conn.execute(
        """
        SELECT created_at, match, profit
        FROM prediction_history
        WHERE result IS NOT NULL
        ORDER BY created_at ASC
        """
    ).fetchall()

    conn.close()

    history = []
    bankroll = 0

    for row in rows:
        profit = float(row["profit"] or 0)
        bankroll += profit

        history.append({
            "created_at": row["created_at"],
            "match": row["match"],
            "profit": profit,
            "bankroll": round(bankroll, 2),
        })

    return history
def load_bankroll_history():
    conn = get_connection()

    rows = conn.execute(
        """
        SELECT created_at, match, profit
        FROM prediction_history
        WHERE result IS NOT NULL
        ORDER BY created_at ASC
        """
    ).fetchall()

    conn.close()

    history = []
    bankroll = 0

    for row in rows:
        profit = float(row["profit"] or 0)
        bankroll += profit

        history.append(
            {
                "created_at": row["created_at"],
                "match": row["match"],
                "profit": profit,
                "bankroll": round(bankroll, 2),
            }
        )

    return history

def load_profit_history():
    """
    Retourne l'évolution du profit cumulé.
    """

    conn = get_connection()

    rows = conn.execute(
        """
        SELECT
            created_at,
            profit
        FROM prediction_history
        WHERE result IS NOT NULL
        ORDER BY created_at ASC
        """
    ).fetchall()

    conn.close()

    history = []
    cumulative_profit = 0

    for row in rows:
        profit = float(row["profit"] or 0)
        cumulative_profit += profit

        history.append(
            {
                "created_at": row["created_at"],
                "profit": profit,
                "cumulative_profit": round(cumulative_profit, 2),
            }
        )

    return history


def load_roi_history():
    """
    Retourne l'évolution du ROI après chaque pari.
    """

    conn = get_connection()

    rows = conn.execute(
        """
        SELECT
            created_at,
            stake,
            profit
        FROM prediction_history
        WHERE result IS NOT NULL
        ORDER BY created_at ASC
        """
    ).fetchall()

    conn.close()

    history = []

    total_profit = 0
    total_stake = 0

    for row in rows:
        stake = float(row["stake"] or 0)
        profit = float(row["profit"] or 0)

        total_profit += profit
        total_stake += stake

        roi = (
            round((total_profit / total_stake) * 100, 2)
            if total_stake > 0
            else 0
        )

        history.append(
            {
                "created_at": row["created_at"],
                "roi": roi,
            }
        )

    return history