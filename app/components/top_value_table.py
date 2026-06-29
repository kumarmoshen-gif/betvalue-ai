import streamlit as st


def show_top_value_table(df):
    st.subheader("🏆 Top 10 des meilleurs Value Bet")

    top10 = (
        df.sort_values("value", ascending=False)
        .head(10)
        .copy()
    )

    top10 = top10.rename(
        columns={
            "match": "⚽ Match",
            "odd": "💰 Cote",
            "confidence": "⭐ Confiance",
            "value": "📈 Value",
            "decision": "🏆 Décision",
        }
    )

    top10["⭐ Confiance"] = top10["⭐ Confiance"].map(lambda x: f"{x:.0f} %")
    top10["📈 Value"] = top10["📈 Value"].map(
        lambda x: f"{x:.2f} %".replace(".", ",")
    )
    top10["💰 Cote"] = top10["💰 Cote"].map(
        lambda x: f"{x:.2f}".replace(".", ",")
    )

    columns_to_show = [
        "⚽ Match",
        "💰 Cote",
        "⭐ Confiance",
        "📈 Value",
        "🏆 Décision",
    ]

    st.dataframe(
        top10[columns_to_show],
        width="stretch",
        hide_index=True,
    )

    st.divider()