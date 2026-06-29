import pandas as pd
import streamlit as st


def show_bankroll_chart(bankroll_history):
    st.subheader("💹 Évolution de la bankroll")

    if not bankroll_history:
        st.info("Aucun pari terminé.")
        st.divider()
        return

    bankroll_df = pd.DataFrame(bankroll_history)
    bankroll_df["created_at"] = pd.to_datetime(bankroll_df["created_at"])
    bankroll_df = bankroll_df.set_index("created_at")

    st.line_chart(bankroll_df["bankroll"])

    st.divider()