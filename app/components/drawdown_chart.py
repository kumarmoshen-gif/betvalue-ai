import pandas as pd
import streamlit as st


def show_drawdown_chart(drawdown_history):
    """
    Affiche l'évolution du drawdown.
    """

    st.subheader("📉 Drawdown")

    if not drawdown_history:
        st.info("Aucune donnée disponible.")
        return

    df = pd.DataFrame(drawdown_history)

    df["created_at"] = pd.to_datetime(df["created_at"])

    df = df.set_index("created_at")

    st.area_chart(df["drawdown"])

    max_drawdown = df["drawdown"].min()

    st.metric(
        "📉 Maximum Drawdown",
        f"{max_drawdown:.2f} u".replace(".", ","),
    )