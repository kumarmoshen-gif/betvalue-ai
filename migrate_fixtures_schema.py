from database.database import get_connection


def migrate():
    conn = get_connection()

    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS fixtures (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            api_id INTEGER UNIQUE,
            league_id INTEGER,
            season INTEGER,
            match_date TEXT,
            status TEXT,
            home_team TEXT,
            away_team TEXT,
            home_team_api_id INTEGER,
            away_team_api_id INTEGER,
            home_score INTEGER,
            away_score INTEGER,
            raw_data TEXT,
            updated_at TEXT
        )
        """
    )

    conn.commit()
    conn.close()

    print("Migration fixtures terminee avec succes.")


if __name__ == "__main__":
    migrate()
