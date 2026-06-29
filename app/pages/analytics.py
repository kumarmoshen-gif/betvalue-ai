import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT_DIR))

import streamlit as st

from database.repository import (
    load_monthly_profit,
    load_roi_by_confidence,
)

from app.components.monthly_profit_chart import show_monthly_profit_chart
from app.components.roi_confidence_chart import show_roi_confidence_chart

st.set_page_config(
    page_title="Analytics",
    page_icon="📊",
    layout="wide",
)

st.title("📊 Analytics BetValue AI")

monthly_profit = load_monthly_profit()
roi_confidence = load_roi_by_confidence()

show_monthly_profit_chart(monthly_profit)

st.divider()

show_roi_confidence_chart(roi_confidence)