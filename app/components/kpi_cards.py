import streamlit as st


def show_kpi_cards(performance):
    """
    Affiche les cartes de performance du Dashboard.
    """

    st.subheader("💼 Performance des paris")

    p1, p2, p3, p4 = st.columns(4)

    p1.metric(
        "💰 Profit total",
        f"{performance['total_profit']:.2f} u".replace(".", ","),
    )

    p2.metric(
        "📈 ROI",
        f"{performance['roi']:.2f} %".replace(".", ","),
    )

    p3.metric(
        "🎯 Taux de réussite",
        f"{performance['hit_rate']:.2f} %".replace(".", ","),
    )

    p4.metric(
        "📊 Paris terminés",
        performance["total_bets"],
    )

    p5, p6, p7 = st.columns(3)

    p5.metric(
        "✅ Paris gagnés",
        performance["won_bets"],
    )

    p6.metric(
        "❌ Paris perdus",
        performance["lost_bets"],
    )

    p7.metric(
        "💵 Mises totales",
        f"{performance['total_stake']:.2f} u".replace(".", ","),
    )

    st.divider()