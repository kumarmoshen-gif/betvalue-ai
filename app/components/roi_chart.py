import pandas as pd
import streamlit as st


def show_roi_chart(roi_history):
    """
    Affiche la courbe du ROI.
    """

    st.subheader("📈 ROI cumulé")

    if not roi_history:
        st.info("Aucun pari terminé.")
        st.divider()
        return

    df = pd.DataFrame(roi_history)

    df["created_at"] = pd.to_datetime(df["created_at"])

    df = df.set_index("created_at")

    st.line_chart(df["roi"])

    st.divider()