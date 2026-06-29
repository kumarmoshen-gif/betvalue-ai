import pandas as pd
import streamlit as st


def show_roi_confidence_chart(data):
    """
    Affiche le ROI par niveau de confiance.
    """

    st.subheader("🎯 ROI par niveau de confiance")

    if not data:
        st.info("Aucune donnée disponible.")
        return

    df = pd.DataFrame(data)

    df = df.set_index("confidence")

    st.bar_chart(df["roi"])

    st.dataframe(
        df,
        width="stretch",
    )