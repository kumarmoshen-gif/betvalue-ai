from database.database import initialize_database
from migrate_fixtures_schema import migrate as migrate_fixtures_schema
from migrate_prediction_history import migrate as migrate_prediction_history
from migrate_prediction_metadata import migrate as migrate_prediction_metadata
from migrate_prediction_settlement import migrate as migrate_prediction_settlement
from migrate_team_form_schema import migrate as migrate_team_form_schema


def migrate():
    initialize_database()
    migrate_prediction_history()
    migrate_prediction_metadata()
    migrate_prediction_settlement()
    migrate_team_form_schema()
    migrate_fixtures_schema()

    print("Base SQLite initialisee et migrations appliquees.")


if __name__ == "__main__":
    migrate()
