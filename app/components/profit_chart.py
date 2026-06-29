import pandas as pd
import streamlit as st


def show_profit_chart(profit_history):
    """
    Affiche la courbe du profit cumulé.
    """

    st.subheader("📈 Profit cumulé")

    if not profit_history:
        st.info("Aucun pari terminé.")
        st.divider()
        return

    df = pd.DataFrame(profit_history)

    df["created_at"] = pd.to_datetime(df["created_at"])

    df = df.set_index("created_at")

    st.line_chart(df["cumulative_profit"])

    st.divider()