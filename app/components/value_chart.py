import streamlit as st


def show_value_chart(df):
    st.subheader("📈 Évolution des Value Bet")

    chart = (
        df[["created_at", "value"]]
        .copy()
        .sort_values("created_at")
        .set_index("created_at")
    )

    st.line_chart(chart)

    st.divider()