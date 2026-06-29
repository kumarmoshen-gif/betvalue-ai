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
)

from app.components.kpi_cards import show_kpi_cards
from app.components.bankroll_chart import show_bankroll_chart
from app.components.profit_chart import show_profit_chart
from app.components.roi_chart import show_roi_chart

st.set_page_config(
    page_title="Performance",
    page_icon="📈",
    layout="wide",
)

st.title("📈 Performance BetValue AI")

performance = load_performance_stats()
bankroll_history = load_bankroll_history()
profit_history = load_profit_history()
roi_history = load_roi_history()

show_kpi_cards(performance)

show_bankroll_chart(bankroll_history)

show_profit_chart(profit_history)

show_roi_chart(roi_history)