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

    if st.button("🔍 Analyser le match"):
        st.session_state["match"] = selected_match
        st.switch_page("pages/match.py")

    st.dataframe(
        df,
        width="stretch"
    )

else:
    st.info("Aucune cote disponible pour ce championnat.")