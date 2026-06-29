import sys
from datetime import date
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT_DIR))

import pandas as pd
import streamlit as st

from config import DEFAULT_SEASON
from services.fixture_service import (
    get_cached_finished_fixtures,
    sync_finished_fixtures,
)

LEAGUES = {
    "Premier League": 39,
    "Ligue 1": 61,
    "Liga": 140,
    "Serie A": 135,
    "Bundesliga": 78,
}

st.set_page_config(
    page_title="Fixtures",
    page_icon="📅",
    layout="wide",
)

st.title("📅 Matchs et résultats")

f1, f2, f3 = st.columns(3)

with f1:
    selected_league = st.selectbox("Ligue", list(LEAGUES.keys()))

with f2:
    selected_season = st.number_input(
        "Saison",
        min_value=2000,
        max_value=2100,
        value=DEFAULT_SEASON,
        step=1,
    )

with f3:
    selected_date = st.date_input("Date", value=date.today())

league_id = LEAGUES[selected_league]

if st.button("Synchroniser les résultats terminés"):
    fixtures = sync_finished_fixtures(
        league_id=league_id,
        season=selected_season,
        date=selected_date.isoformat(),
    )
    st.success(f"{len(fixtures)} match(s) synchronisé(s).")

fixtures = get_cached_finished_fixtures(
    league_id=league_id,
    season=selected_season,
)

if not fixtures:
    st.info("Aucun résultat terminé en cache pour ces filtres.")
    st.stop()

df = pd.DataFrame(fixtures)

columns = [
    "match_date",
    "status",
    "home_team",
    "away_team",
    "home_score",
    "away_score",
]

st.dataframe(
    df[[column for column in columns if column in df.columns]],
    width="stretch",
    hide_index=True,
)
