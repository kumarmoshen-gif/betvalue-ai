import streamlit as st


def show_decision_chart(df):
    st.subheader("📊 Répartition des décisions IA")

    decision_counts = df["decision"].value_counts()

    col1, col2, col3 = st.columns(3)

    value_forte = decision_counts.get("🟢 VALUE FORTE", 0)
    value = decision_counts.get("🟡 VALUE", 0) + decision_counts.get("🟢 VALUE", 0)
    pas_value = (
        decision_counts.get("🔴 PAS DE VALEUR", 0)
        + decision_counts.get("🔴 PAS DE VALUE", 0)
    )

    col1.metric("🟢 VALUE FORTE", value_forte)
    col2.metric("🟡 VALUE", value)
    col3.metric("🔴 PAS DE VALEUR", pas_value)

    st.divider()