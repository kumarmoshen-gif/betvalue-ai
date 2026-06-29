from database.database import get_connection


def add_column_if_missing(conn, table_name, column_name, column_definition):
    columns = conn.execute(f"PRAGMA table_info({table_name})").fetchall()
    existing_columns = [column["name"] for column in columns]

    if column_name not in existing_columns:
        conn.execute(
            f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_definition}"
        )
        print(f"Colonne ajoutee : {column_name}")
    else:
        print(f"Colonne deja existante : {column_name}")


def migrate():
    conn = get_connection()

    add_column_if_missing(
        conn,
        "prediction_history",
        "fixture_api_id",
        "INTEGER",
    )
    add_column_if_missing(
        conn,
        "prediction_history",
        "settled_at",
        "TEXT",
    )

    conn.commit()
    conn.close()

    print("Migration settlement terminee avec succes.")


if __name__ == "__main__":
    migrate()
