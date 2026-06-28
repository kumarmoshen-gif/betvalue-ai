import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT_DIR))

import streamlit as st

from database.repository import (
    load_pending_predictions,
    update_prediction_result,
)

st.set_page_config(
    page_title="Résultats",
    page_icon="✅",
    layout="wide",
)

st.title("✅ Validation des résultats")

pending = load_pending_predictions()

if not pending:
    st.success("🎉 Aucun pari en attente de résultat.")
    st.stop()

for prediction in pending:

    st.divider()

    st.subheader(prediction["match"])

    st.write(f"**Prédiction IA :** {prediction['predicted_result']}")
    st.write(f"**Cote :** {prediction['odd']}")
    st.write(f"**Value :** {prediction['value']:.2f} %")

    result = st.selectbox(
        "Résultat réel",
        [
            prediction["home_team"],
            "Draw",
            prediction["away_team"],
        ],
        key=f"result_{prediction['id']}",
    )

    stake = st.number_input(
        "Mise",
        min_value=0.10,
        value=float(prediction["stake"]),
        step=0.10,
        key=f"stake_{prediction['id']}",
    )

    if st.button(
        "💾 Enregistrer",
        key=f"save_{prediction['id']}",
    ):

        info = update_prediction_result(
            prediction["id"],
            result,
            stake,
        )

        if info["bet_won"]:
            st.success(
                f"✅ Pari gagnant (+{info['profit']:.2f} unités)"
            )
        else:
            st.error(
                f"❌ Pari perdant ({info['profit']:.2f} unité)"
            )

        st.rerun()