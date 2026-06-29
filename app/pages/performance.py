import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT_DIR))

import streamlit as st

from database.repository import (
    load_performance_stats,
    load_bankroll_history,
    load_profit_history,
    load_roi_history,
    load_streak_stats,
)

from app.components.kpi_cards import show_kpi_cards
from app.components.streak_cards import show_streak_cards
from app.components.bankroll_chart import show_bankroll_chart
from app.components.profit_chart import show_profit_chart
from app.components.roi_chart import show_roi_chart

st.set_page_config(
    page_title="Performance",
    page_icon="📈",
    layout="wide",
)

st.title("📈 Performance BetValue AI")

include_fallback = st.checkbox(
    "Inclure les prédictions fallback",
    value=False,
)

performance = load_performance_stats(include_fallback=include_fallback)
streak_stats = load_streak_stats(include_fallback=include_fallback)
bankroll_history = load_bankroll_history(include_fallback=include_fallback)
profit_history = load_profit_history(include_fallback=include_fallback)
roi_history = load_roi_history(include_fallback=include_fallback)

show_kpi_cards(performance)

show_streak_cards(streak_stats)

show_bankroll_chart(bankroll_history)

show_profit_chart(profit_history)

show_roi_chart(roi_history)
