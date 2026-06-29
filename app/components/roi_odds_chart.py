import pandas as pd
import streamlit as st


def show_roi_odds_chart(data):
    """
    Affiche le ROI par tranche de cotes.
    """

    st.subheader("💰 ROI par tranche de cotes")

    if not data:
        st.info("Aucune donnée disponible.")
        return

    df = pd.DataFrame(data)

    df = df.set_index("odd_range")

    st.bar_chart(df["roi"])

    st.dataframe(
        df,
        width="stretch",
        hide_index=False,
    )