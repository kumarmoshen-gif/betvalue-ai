from database.database import get_connection


EXPECTED_COLUMNS = {
    "id",
    "team_api_id",
    "league_id",
    "season",
    "data",
    "updated_at",
}


def get_columns(conn):
    columns = conn.execute("PRAGMA table_info(team_form)").fetchall()
    return {column["name"] for column in columns}


def migrate():
    conn = get_connection()

    columns = get_columns(conn)

    if columns == EXPECTED_COLUMNS:
        print("Table team_form deja conforme.")
        conn.close()
        return

    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS team_form_new (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            team_api_id INTEGER,
            league_id INTEGER,
            season INTEGER,
            data TEXT,
            updated_at TEXT,
            UNIQUE(team_api_id, league_id, season)
        )
        """
    )

    if "team_api_id" in columns and "data" in columns:
        conn.execute(
            """
            INSERT INTO team_form_new (
                team_api_id,
                league_id,
                season,
                data,
                updated_at
            )
            SELECT
                team_api_id,
                NULL,
                NULL,
                data,
                updated_at
            FROM team_form
            """
        )

    conn.execute("DROP TABLE IF EXISTS team_form")
    conn.execute("ALTER TABLE team_form_new RENAME TO team_form")

    conn.commit()
    conn.close()

    print("Migration team_form terminee avec succes.")


if __name__ == "__main__":
    migrate()
