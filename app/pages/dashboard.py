import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT_DIR))

import streamlit as st
import pandas as pd

from database.repository import (
    load_prediction_history,
    load_performance_stats,
)

st.set_page_config(
    page_title="Dashboard",
    page_icon="📊",
    layout="wide",
)

st.title("📊 Tableau de bord BetValue AI")

history = load_prediction_history(1000)
performance = load_performance_stats()

if not history:
    st.info("Aucune donnée disponible.")
    st.stop()

df = pd.DataFrame(history)

st.subheader("💼 Performance des paris")

p1, p2, p3, p4 = st.columns(4)

p1.metric(
    "💰 Profit total",
    f"{performance['total_profit']:.2f} u".replace(".", ","),
)

p2.metric(
    "📈 ROI",
    f"{performance['roi']:.2f} %".replace(".", ","),
)

p3.metric(
    "🎯 Réussite",
    f"{performance['hit_rate']:.2f} %".replace(".", ","),
)

p4.metric(
    "📊 Paris terminés",
    performance["total_bets"],
)

p5, p6, p7 = st.columns(3)

p5.metric("✅ Gagnés", performance["won_bets"])
p6.metric("❌ Perdus", performance["lost_bets"])
p7.metric(
    "💵 Mises totales",
    f"{performance['total_stake']:.2f} u".replace(".", ","),
)

st.divider()

st.subheader("🤖 Analyse IA")

c1, c2, c3, c4 = st.columns(4)

c1.metric("🔥 Points positifs", len(df[df["value"] > 0]))
c2.metric("⭐ Confiance moyenne", f"{df['confidence'].mean():.1f} %".replace(".", ","))
c3.metric("💰 EV moyen", f"{df['value'].mean():.2f} %".replace(".", ","))
c4.metric("⚽ Analyses", len(df))

st.divider()

st.subheader("📈 Évolution des Value Bet")

chart = (
    df[["created_at", "value"]]
    .copy()
    .sort_values("created_at")
    .set_index("created_at")
)

st.line_chart(chart)

st.divider()

st.subheader("📊 Répartition des décisions IA")

decision_counts = df["decision"].value_counts()

col1, col2, col3 = st.columns(3)

value_forte = decision_counts.get("🟢 VALUE FORTE", 0)
value = decision_counts.get("🟡 VALUE", 0) + decision_counts.get("🟢 VALUE", 0)
pas_value = (
    decision_counts.get("🔴 PAS DE VALEUR", 0)
    + decision_counts.get("🔴 PAS DE VALUE", 0)
)

col1.metric("🟢 VALUE FORTE", value_forte)
col2.metric("🟡 VALUE", value)
col3.metric("🔴 PAS DE VALEUR", pas_value)

st.divider()

st.subheader("🏆 Top 10 des meilleurs Value Bet")

top10 = (
    df.sort_values("value", ascending=False)
      .head(10)
      .copy()
)

top10 = top10.rename(
    columns={
        "match": "⚽ Match",
        "odd": "💰 Cote",
        "confidence": "⭐ Confiance",
        "value": "📈 Value",
        "decision": "🏆 Décision",
    }
)

top10["⭐ Confiance"] = top10["⭐ Confiance"].map(lambda x: f"{x:.0f} %")
top10["📈 Value"] = top10["📈 Value"].map(lambda x: f"{x:.2f} %".replace(".", ","))
top10["💰 Cote"] = top10["💰 Cote"].map(lambda x: f"{x:.2f}".replace(".", ","))

columns_to_show = [
    "⚽ Match",
    "💰 Cote",
    "⭐ Confiance",
    "📈 Value",
    "🏆 Décision",
]

st.dataframe(
    top10[columns_to_show],
    width="stretch",
    hide_index=True,
)

st.divider()

st.caption(
    "BetValue AI V4 • Tableau de bord alimenté automatiquement par l'historique SQLite."
)