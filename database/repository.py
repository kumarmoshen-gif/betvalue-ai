import json
from datetime import datetime

from database.database import get_connection


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