import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT_DIR))

import streamlit as st

from database.repository import (
    load_monthly_profit,
    load_roi_by_confidence,
    load_roi_by_odds,
    load_drawdown_history,
)

from app.components.monthly_profit_chart import show_monthly_profit_chart
from app.components.roi_confidence_chart import show_roi_confidence_chart
from app.components.roi_odds_chart import show_roi_odds_chart
from app.components.drawdown_chart import show_drawdown_chart

st.set_page_config(
    page_title="Analytics",
    page_icon="📊",
    layout="wide",
)

st.title("📊 Analytics BetValue AI")

include_fallback = st.checkbox(
    "Inclure les prédictions fallback",
    value=False,
)

monthly_profit = load_monthly_profit(include_fallback=include_fallback)
roi_confidence = load_roi_by_confidence(include_fallback=include_fallback)
roi_odds = load_roi_by_odds(include_fallback=include_fallback)
drawdown_history = load_drawdown_history(include_fallback=include_fallback)

show_monthly_profit_chart(monthly_profit)

st.divider()

show_roi_confidence_chart(roi_confidence)

st.divider()

show_roi_odds_chart(roi_odds)

st.divider()

show_drawdown_chart(drawdown_history)
