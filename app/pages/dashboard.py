import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT_DIR))

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from database.repository import load_prediction_history

st.set_page_config(
    page_title="Dashboard",
    page_icon="📊",
    layout="wide",
)

st.title("📊 Tableau de bord BetValue AI")

history = load_prediction_history(1000)

if not history:
    st.info("Aucune donnée disponible.")
    st.stop()

df = pd.DataFrame(history)

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

fig, ax = plt.subplots(figsize=(8, 3))

ax.barh(
    decision_counts.index,
    decision_counts.values,
)

ax.set_xlabel("Nombre de paris")
ax.set_ylabel("Décision")

for i, value in enumerate(decision_counts.values):
    ax.text(value + 0.05, i, str(value), va="center")

st.pyplot(fig)

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