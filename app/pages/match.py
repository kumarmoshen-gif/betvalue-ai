import streamlit as st

st.set_page_config(
    page_title="Analyse du match",
    page_icon="⚽",
    layout="wide"
)

st.title("⚽ Analyse IA")

if "match" not in st.session_state:
    st.warning("Aucun match sélectionné.")
    st.stop()

match = st.session_state["match"]

st.header(match)

st.write("---")

st.info("Les statistiques détaillées apparaîtront ici.")

col1, col2 = st.columns(2)

with col1:
    st.subheader("🏠 Équipe domicile")

with col2:
    st.subheader("✈️ Équipe extérieure")