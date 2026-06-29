from database.database import get_connection


def add_column_if_missing(conn, table_name, column_name, column_definition):
    columns = conn.execute(f"PRAGMA table_info({table_name})").fetchall()
    existing_columns = [column["name"] for column in columns]

    if column_name not in existing_columns:
        conn.execute(
            f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_definition}"
        )
        print(f"Colonne ajoutée : {column_name}")
    else:
        print(f"Colonne déjà existante : {column_name}")


def migrate():
    conn = get_connection()

    add_column_if_missing(conn, "prediction_history", "league", "TEXT")
    add_column_if_missing(conn, "prediction_history", "season", "INTEGER")
    add_column_if_missing(conn, "prediction_history", "match_date", "TEXT")
    add_column_if_missing(conn, "prediction_history", "home_score", "INTEGER")
    add_column_if_missing(conn, "prediction_history", "away_score", "INTEGER")
    add_column_if_missing(conn, "prediction_history", "bookmaker", "TEXT")
    add_column_if_missing(conn, "prediction_history", "bet_type", "TEXT")

    conn.commit()
    conn.close()

    print("Migration metadata terminée avec succès.")


if __name__ == "__main__":
    migrate()