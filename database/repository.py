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

# ==========================================================
# Prediction History
# ==========================================================

def save_prediction(prediction):
    """
    Sauvegarde une prédiction dans l'historique SQLite.
    """

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
            fallback
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
        ),
    )

    conn.commit()
    conn.close()


def load_prediction_history(limit=100):
    """
    Retourne les dernières prédictions enregistrées.
    """

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