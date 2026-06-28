import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT_DIR))

import streamlit as st

from providers.football_api import get_team_id, get_last_matches
from core.team_form import compute_team_form
from services.prediction_service import get_prediction_for_match

st.set_page_config(
    page_title="Analyse du match",
    page_icon="⚽",
    layout="wide"
)

st.title("⚽ Analyse IA du match")

if "match" not in st.session_state:
    st.warning("Aucun match sélectionné.")
    st.stop()

match = st.session_state["match"]
st.header(match)

try:
    home_team, away_team = match.split(" - ")
    home_team = home_team.strip()
    away_team = away_team.strip()
except ValueError:
    st.error("Format du match invalide.")
    st.stop()

prediction = get_prediction_for_match(home_team, away_team)

home_id = get_team_id(home_team)
away_id = get_team_id(away_team)

home_matches = get_last_matches(home_id) if home_id else []
away_matches = get_last_matches(away_id) if away_id else []

home_form = compute_team_form(home_matches, home_id) if home_id else None
away_form = compute_team_form(away_matches, away_id) if away_id else None

st.divider()

if prediction:
    st.subheader("🤖 Prédiction IA")

    c1, c2, c3 = st.columns(3)
    c1.metric(f"🏠 {home_team}", f"{prediction['home']} %")
    c2.metric("🤝 Match nul", f"{prediction['draw']} %")
    c3.metric(f"🚩 {away_team}", f"{prediction['away']} %")

st.divider()

st.subheader("📈 Forme récente - 5 derniers matchs")

col1, col2 = st.columns(2)

with col1:
    st.markdown(f"### 🏠 {home_team}")
    if home_form:
        st.metric("Score de forme", f"{home_form['form_score']} / 100")
        st.write(f"Victoires : {home_form['wins']}")
        st.write(f"Nuls : {home_form['draws']}")
        st.write(f"Défaites : {home_form['losses']}")
        st.write(f"Buts marqués : {home_form['goals_for']}")
        st.write(f"Buts encaissés : {home_form['goals_against']}")
        st.write(f"Points : {home_form['points']} / 15")
    else:
        st.warning("Forme indisponible.")

with col2:
    st.markdown(f"### 🚩 {away_team}")
    if away_form:
        st.metric("Score de forme", f"{away_form['form_score']} / 100")
        st.write(f"Victoires : {away_form['wins']}")
        st.write(f"Nuls : {away_form['draws']}")
        st.write(f"Défaites : {away_form['losses']}")
        st.write(f"Buts marqués : {away_form['goals_for']}")
        st.write(f"Buts encaissés : {away_form['goals_against']}")
        st.write(f"Points : {away_form['points']} / 15")
    else:
        st.warning("Forme indisponible.")

st.divider()

st.subheader("📊 Lecture rapide")

if prediction:
    best_result = max(prediction, key=prediction.get)

    if best_result == "home":
        st.success(f"Favori IA : {home_team}")
    elif best_result == "away":
        st.success(f"Favori IA : {away_team}")
    else:
        st.info("L'IA estime que le match nul est une issue importante.")

if home_form and away_form:
    diff = home_form["form_score"] - away_form["form_score"]

    if diff > 10:
        st.write(f"✅ {home_team} est nettement en meilleure forme récente.")
    elif diff < -10:
        st.write(f"✅ {away_team} est nettement en meilleure forme récente.")
    else:
        st.write("⚖️ Les deux équipes ont une forme récente assez proche.")

st.caption("Cette analyse utilise les statistiques réelles des équipes via API-Football.")