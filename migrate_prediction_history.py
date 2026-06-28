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

    add_column_if_missing(conn, "prediction_history", "stake", "REAL DEFAULT 1")
    add_column_if_missing(conn, "prediction_history", "result", "TEXT")
    add_column_if_missing(conn, "prediction_history", "bet_won", "INTEGER")
    add_column_if_missing(conn, "prediction_history", "profit", "REAL DEFAULT 0")

    conn.commit()
    conn.close()

    print("Migration terminée avec succès.")


if __name__ == "__main__":
    migrate()