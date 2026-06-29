import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT_DIR))

import streamlit as st

from providers.football_api import get_team_id
from services.prediction_service import (
    get_cached_or_compute_team_form,
    get_prediction_for_match,
)
from config import DEFAULT_LEAGUE, DEFAULT_SEASON

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

selected_bet = st.session_state.get("selected_bet")
selected_odd = st.session_state.get("selected_odd")
bookmaker = st.session_state.get("bookmaker")
bet_type = st.session_state.get("bet_type")
league = st.session_state.get("league")
league_id = st.session_state.get("league_id")
season = st.session_state.get("season", DEFAULT_SEASON)
match_date = st.session_state.get("match_date")
effective_league_id = league_id if league_id else DEFAULT_LEAGUE

prediction = get_prediction_for_match(
    home_team,
    away_team,
    league_id=effective_league_id,
    season=season,
    selected_bet=selected_bet,
    selected_odd=selected_odd,
    league=league,
    match_date=match_date,
    bookmaker=bookmaker,
    bet_type=bet_type,
)

if prediction is None:
    st.warning("Analyse IA indisponible pour ce match.")
    st.info("Cause probable : quota API-Football atteint ou équipe non trouvée.")
    st.stop()

if prediction.get("fallback"):
    st.warning(prediction.get("message"))

st.divider()

st.subheader("🤖 Prédiction IA V2.2")

c1, c2, c3 = st.columns(3)
c1.metric(f"🏠 {home_team}", f"{prediction['home']} %")
c2.metric("🤝 Match nul", f"{prediction['draw']} %")
c3.metric(f"🚩 {away_team}", f"{prediction['away']} %")

st.divider()

st.subheader("⭐ Niveau de confiance")

confidence = prediction["confidence"]

st.metric("Confiance du moteur IA", f"{confidence} / 100")
st.progress(confidence / 100)

if confidence >= 85:
    st.success("🟢 Très forte confiance")
elif confidence >= 70:
    st.info("🔵 Bonne confiance")
elif confidence >= 60:
    st.warning("🟡 Confiance moyenne")
else:
    st.error("🔴 Match très incertain")

st.divider()

st.subheader("💰 Value Bet")

value_bet = prediction.get("value_bet")

if value_bet:
    v1, v2, v3 = st.columns(3)

    v1.metric("Cote bookmaker", value_bet["odd"])
    v2.metric("Proba bookmaker", f"{value_bet['bookmaker_probability']} %")
    v3.metric("Value", f"{value_bet['value']} %")

    st.write(f"Probabilité IA : {value_bet['ai_probability']} %")

    if bookmaker:
        st.caption(f"Bookmaker : {bookmaker} | Pari : {selected_bet}")

    if value_bet["value"] >= 5:
        st.success(value_bet["decision"])
    else:
        st.error(value_bet["decision"])
else:
    st.info("Aucune information Value Bet disponible.")

st.divider()

home_rating = prediction["home_rating"]
away_rating = prediction["away_rating"]

st.subheader("📊 Scores IA détaillés")

col1, col2 = st.columns(2)

with col1:
    st.markdown(f"### 🏠 {home_team}")
    st.metric("Note globale", f"{home_rating['rating']} / 100")

    st.write(f"Attaque : {home_rating['attack']} / 100")
    st.progress(home_rating["attack"] / 100)

    st.write(f"Défense : {home_rating['defense']} / 100")
    st.progress(home_rating["defense"] / 100)

    st.write(f"Forme : {home_rating['form']} / 100")
    st.progress(home_rating["form"] / 100)

    st.write(f"🏟️ Domicile : {home_rating['home']} / 100")
    st.progress(home_rating["home"] / 100)

with col2:
    st.markdown(f"### 🚩 {away_team}")
    st.metric("Note globale", f"{away_rating['rating']} / 100")

    st.write(f"Attaque : {away_rating['attack']} / 100")
    st.progress(away_rating["attack"] / 100)

    st.write(f"Défense : {away_rating['defense']} / 100")
    st.progress(away_rating["defense"] / 100)

    st.write(f"Forme : {away_rating['form']} / 100")
    st.progress(away_rating["form"] / 100)

    st.write(f"✈️ Extérieur : {away_rating['home']} / 100")
    st.progress(away_rating["home"] / 100)

st.divider()

st.subheader("📈 Forme récente - 5 derniers matchs")

home_id = get_team_id(home_team)
away_id = get_team_id(away_team)

home_form = (
    get_cached_or_compute_team_form(home_id, effective_league_id, season)
    if home_id
    else None
)
away_form = (
    get_cached_or_compute_team_form(away_id, effective_league_id, season)
    if away_id
    else None
)

col3, col4 = st.columns(2)

with col3:
    st.markdown(f"### 🏠 {home_team}")
    if home_form:
        st.write(f"Victoires : {home_form['wins']}")
        st.write(f"Nuls : {home_form['draws']}")
        st.write(f"Défaites : {home_form['losses']}")
        st.write(f"Buts marqués : {home_form['goals_for']}")
        st.write(f"Buts encaissés : {home_form['goals_against']}")
        st.write(f"Points : {home_form['points']} / 15")
    else:
        st.warning("Forme indisponible.")

with col4:
    st.markdown(f"### 🚩 {away_team}")
    if away_form:
        st.write(f"Victoires : {away_form['wins']}")
        st.write(f"Nuls : {away_form['draws']}")
        st.write(f"Défaites : {away_form['losses']}")
        st.write(f"Buts marqués : {away_form['goals_for']}")
        st.write(f"Buts encaissés : {away_form['goals_against']}")
        st.write(f"Points : {away_form['points']} / 15")
    else:
        st.warning("Forme indisponible.")

st.divider()

st.subheader("📌 Lecture rapide")

st.metric("Écart de niveau", f"{prediction['diff']} points")

best_result = max(
    {
        "home": prediction["home"],
        "draw": prediction["draw"],
        "away": prediction["away"],
    },
    key={
        "home": prediction["home"],
        "draw": prediction["draw"],
        "away": prediction["away"],
    }.get
)

if best_result == "home":
    st.success(f"Favori IA : {home_team}")
elif best_result == "away":
    st.success(f"Favori IA : {away_team}")
else:
    st.info("L'IA estime que le match nul est une issue importante.")

rating_diff = home_rating["rating"] - away_rating["rating"]

if rating_diff > 10:
    st.write(f"✅ {home_team} possède un avantage global net.")
elif rating_diff < -10:
    st.write(f"✅ {away_team} possède un avantage global net.")
else:
    st.write("⚖️ Les deux équipes sont assez proches selon le modèle IA.")

st.caption("BetValue AI V2.2 • Analyse basée sur attaque, défense, forme récente, avantage domicile, confiance IA, probabilités et Value Bet.")
