from database.repository import (
    load_fixtures,
    save_fixtures,
)
from providers.football_api import get_fixtures


FINISHED_STATUSES = {"FT", "AET", "PEN"}


def sync_fixtures(
    league_id=None,
    season=None,
    date=None,
    status=None,
):
    fixtures = get_fixtures(
        league_id=league_id,
        season=season,
        date=date,
        status=status,
    )
    save_fixtures(fixtures)

    return fixtures


def sync_finished_fixtures(league_id=None, season=None, date=None):
    synced = []

    for status in FINISHED_STATUSES:
        synced.extend(sync_fixtures(
            league_id=league_id,
            season=season,
            date=date,
            status=status,
        ))

    return synced


def get_cached_finished_fixtures(league_id=None, season=None, limit=500):
    fixtures = []

    for status in FINISHED_STATUSES:
        fixtures.extend(load_fixtures(
            league_id=league_id,
            season=season,
            status=status,
            limit=limit,
        ))

    return sorted(
        fixtures,
        key=lambda fixture: fixture.get("match_date") or "",
        reverse=True,
    )[:limit]
