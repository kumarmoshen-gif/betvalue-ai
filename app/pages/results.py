import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT_DIR))

import streamlit as st

from database.repository import (
    load_pending_predictions,
    update_prediction_score_result,
)
from core.result_settlement import result_from_score
from services.settlement_service import settle_pending_predictions_from_fixtures

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

include_fallback = st.checkbox(
    "Inclure les prédictions fallback dans le règlement automatique",
    value=False,
)

if st.button("Régler automatiquement depuis les fixtures"):
    settlement = settle_pending_predictions_from_fixtures(
        include_fallback=include_fallback,
    )
    st.success(
        f"{len(settlement['settled'])} prédiction(s) réglée(s)."
    )

    if settlement["unmatched"]:
        st.info(
            f"{len(settlement['unmatched'])} prédiction(s) sans fixture correspondante."
        )

    st.rerun()

for prediction in pending:

    st.divider()

    st.subheader(prediction["match"])

    st.write(f"**Prédiction IA :** {prediction['predicted_result']}")
    st.write(f"**Cote :** {prediction['odd']}")
    st.write(f"**Value :** {prediction['value']:.2f} %")

    score_col1, score_col2 = st.columns(2)

    with score_col1:
        home_score = st.number_input(
            f"Score {prediction['home_team']}",
            min_value=0,
            value=0,
            step=1,
            key=f"home_score_{prediction['id']}",
        )

    with score_col2:
        away_score = st.number_input(
            f"Score {prediction['away_team']}",
            min_value=0,
            value=0,
            step=1,
            key=f"away_score_{prediction['id']}",
        )

    result = result_from_score(
        prediction["home_team"],
        prediction["away_team"],
        home_score,
        away_score,
    )

    st.write(f"**Résultat déduit :** {result}")

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

        info = update_prediction_score_result(
            prediction["id"],
            home_score,
            away_score,
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
