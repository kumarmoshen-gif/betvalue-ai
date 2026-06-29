import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT_DIR))

import streamlit as st
import pandas as pd

from database.repository import (
    load_prediction_history,
    load_performance_stats,
    load_bankroll_history,
)

from app.components.kpi_cards import show_kpi_cards
from app.components.bankroll_chart import show_bankroll_chart
from app.components.value_chart import show_value_chart
from app.components.decision_chart import show_decision_chart
from app.components.top_value_table import show_top_value_table

st.set_page_config(
    page_title="Dashboard",
    page_icon="📊",
    layout="wide",
)

st.title("📊 Tableau de bord BetValue AI V5")

history = load_prediction_history(1000)
performance = load_performance_stats()
bankroll_history = load_bankroll_history()

if not history:
    st.info("Aucune donnée disponible.")
    st.stop()

df = pd.DataFrame(history)

show_kpi_cards(performance)
show_bankroll_chart(bankroll_history)

st.subheader("🤖 Analyse IA")

c1, c2, c3, c4 = st.columns(4)

c1.metric("🔥 Points positifs", len(df[df["value"] > 0]))
c2.metric("⭐ Confiance moyenne", f"{df['confidence'].mean():.1f} %".replace(".", ","))
c3.metric("💰 EV moyen", f"{df['value'].mean():.2f} %".replace(".", ","))
c4.metric("⚽ Analyses", len(df))

st.divider()

show_value_chart(df)
show_decision_chart(df)
show_top_value_table(df)

st.caption(
    "BetValue AI V5 • Dashboard modulaire avec performance, ROI et bankroll."
)