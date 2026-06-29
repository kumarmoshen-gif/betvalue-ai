import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT_DIR))

from logging_config import setup_logging

# Initialisation du système de logs
setup_logging()

import streamlit as st
import pandas as pd

from core.odds_engine import analyse_odds
from services.match_service import get_league_odds
from config import DEFAULT_SEASON

st.set_page_config(
    page_title="BetValue AI",
    page_icon="📈",
    layout="wide",
)

st.title("📈 BetValue AI")
st.write("Application connectée aux vraies cotes ✅")

sports = {
    "Premier League": "soccer_epl",
    "Ligue 1": "soccer_france_ligue_one",
    "Liga": "soccer_spain_la_liga",
    "Serie A": "soccer_italy_serie_a",
    "Bundesliga": "soccer_germany_bundesliga",
}

football_api_leagues = {
    "Premier League": 39,
    "Ligue 1": 61,
    "Liga": 140,
    "Serie A": 135,
    "Bundesliga": 78,
}

col_a, col_b = st.columns(2)

with col_a:
    selected_league = st.selectbox(
        "Championnat",
        list(sports.keys())
    )

with col_b:
    only_value = st.checkbox(
        "Afficher uniquement les VALUE",
        value=False
    )

st.subheader(f"⚽ Cotes réelles - {selected_league}")

data = get_league_odds(sports[selected_league])
data = analyse_odds(data)

if only_value:
    data = [
        row
        for row in data
        if row["Décision"] == "🟢 VALUE"
    ]

df = pd.DataFrame(data)

value_bets = [
    row
    for row in data
    if row["Décision"] == "🟢 VALUE"
]

nb_values = len(value_bets)

avg_ev = (
    round(
        sum(row["EV numérique"] for row in value_bets) / nb_values,
        2
    )
    if nb_values
    else 0
)

avg_score = (
    round(
        sum(row["Score"] for row in value_bets) / nb_values
    )
    if nb_values
    else 0
)

nb_matches = len(set(row["Match"] for row in data)) if data else 0

c1, c2, c3, c4 = st.columns(4)

c1.metric("🔥 VALUE", nb_values)
c2.metric("💰 EV moyen", f"{avg_ev}%")
c3.metric("⭐ Score moyen", avg_score)
c4.metric("⚽ Matchs", nb_matches)

st.divider()

if not df.empty:

    st.write("### Choisir un match")

    matches = sorted(df["Match"].unique())

    selected_match = st.selectbox(
        "Match",
        matches
    )

    match_rows = df[df["Match"] == selected_match]
    selected_bet_index = st.selectbox(
        "Pari",
        match_rows.index,
        format_func=lambda index: (
            f"{df.loc[index, 'Pari']} @ {df.loc[index, 'Cote']} "
            f"({df.loc[index, 'Bookmaker']})"
        ),
    )

    if st.button("🔍 Analyser le match"):
        selected_bet_row = df.loc[selected_bet_index]

        st.session_state["match"] = selected_match
        st.session_state["selected_bet"] = selected_bet_row["Pari"]
        st.session_state["selected_odd"] = float(selected_bet_row["Cote"])
        st.session_state["bookmaker"] = selected_bet_row["Bookmaker"]
        st.session_state["bet_type"] = "h2h"
        st.session_state["league"] = selected_league
        st.session_state["league_id"] = football_api_leagues[selected_league]
        st.session_state["season"] = DEFAULT_SEASON
        st.session_state["match_date"] = selected_bet_row.get("Match date")
        st.switch_page("pages/match.py")

    st.dataframe(
        df,
        width="stretch"
    )

else:
    st.info("Aucune cote disponible pour ce championnat.")
