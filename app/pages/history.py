import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT_DIR))

import streamlit as st
import pandas as pd

from database.repository import load_prediction_history

st.set_page_config(
    page_title="Historique",
    page_icon="📜",
    layout="wide",
)

st.title("📜 Historique des prédictions")

history = load_prediction_history(500)

if not history:
    st.info("Aucune prédiction enregistrée pour le moment.")
    st.stop()

df = pd.DataFrame(history)

c1, c2, c3, c4 = st.columns(4)

c1.metric("📊 Prédictions", len(df))
c2.metric("⭐ Confiance moyenne", f"{round(df['confidence'].mean(), 1)} %")
c3.metric("💰 Value moyenne", f"{round(df['value'].mean(), 2)} %")
c4.metric("🔥 Value positives", len(df[df["value"] > 0]))

st.divider()

only_value = st.checkbox("Afficher uniquement les Value Bet positives", value=False)

if only_value:
    df = df[df["value"] > 0]

search = st.text_input("Rechercher un match ou une équipe")

if search:
    search_lower = search.lower()
    df = df[
        df["match"].str.lower().str.contains(search_lower)
        | df["home_team"].str.lower().str.contains(search_lower)
        | df["away_team"].str.lower().str.contains(search_lower)
    ]

st.dataframe(
    df[
        [
            "created_at",
            "match",
            "predicted_result",
            "odd",
            "home_probability",
            "draw_probability",
            "away_probability",
            "confidence",
            "bookmaker_probability",
            "value",
            "decision",
            "fallback",
            "fixture_api_id",
            "settled_at",
        ]
    ],
    width="stretch",
)

st.download_button(
    label="📥 Exporter en CSV",
    data=df.to_csv(index=False).encode("utf-8"),
    file_name="prediction_history.csv",
    mime="text/csv",
)
