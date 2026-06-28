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