import pandas as pd
import streamlit as st


def show_monthly_profit_chart(monthly_profit):
    """
    Affiche le profit par mois.
    """

    st.subheader("📅 Profit mensuel")

    if not monthly_profit:
        st.info("Aucun pari terminé.")
        return

    df = pd.DataFrame(monthly_profit)
    df = df.set_index("month")

    st.bar_chart(df["profit"])