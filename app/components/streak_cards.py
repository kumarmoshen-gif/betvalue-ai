import streamlit as st


def show_streak_cards(stats):
    """
    Affiche les séries de victoires / défaites.
    """

    st.subheader("🔥 Séries")

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "🔥 Série actuelle",
        f"{stats['current']} {stats['current_type']}",
    )

    c2.metric(
        "🏆 Meilleure série",
        f"{stats['best_win']} victoires",
    )

    c3.metric(
        "❌ Pire série",
        f"{stats['best_loss']} défaites",
    )