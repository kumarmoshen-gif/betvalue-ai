import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT_DIR))

import pandas as pd
import streamlit as st

from services.backtesting_service import (
    get_backtest_options,
    run_backtest,
)

st.set_page_config(
    page_title="Backtesting",
    page_icon="📊",
    layout="wide",
)

st.title("📊 Backtesting")

options = get_backtest_options()

f1, f2, f3, f4, f5 = st.columns(5)

with f1:
    selected_league = st.selectbox("Ligue", options["leagues"])

with f2:
    selected_bookmaker = st.selectbox("Bookmaker", options["bookmakers"])

with f3:
    min_confidence = st.slider("Confiance min", 0, 100, 0, 5)

with f4:
    min_value = st.slider("Value min", -50, 50, -50, 1)

with f5:
    include_fallback = st.checkbox("Inclure fallback", value=False)

backtest = run_backtest(
    league=selected_league,
    bookmaker=selected_bookmaker,
    min_confidence=min_confidence,
    min_value=min_value,
    include_fallback=include_fallback,
)

summary = backtest["summary"]

c1, c2, c3, c4 = st.columns(4)
c1.metric("Paris", summary["total_bets"])
c2.metric("Profit", f"{summary['total_profit']:.2f} u".replace(".", ","))
c3.metric("ROI", f"{summary['roi']:.2f} %".replace(".", ","))
c4.metric("Hit rate", f"{summary['hit_rate']:.2f} %".replace(".", ","))

c5, c6, c7, c8 = st.columns(4)
c5.metric("Gagnés", summary["won_bets"])
c6.metric("Perdus", summary["lost_bets"])
c7.metric("Mises", f"{summary['total_stake']:.2f} u".replace(".", ","))
c8.metric(
    "Max drawdown",
    f"{summary['max_drawdown']:.2f} u".replace(".", ","),
)

st.divider()

curve = backtest["curve"]

if curve:
    curve_df = pd.DataFrame(curve)
    curve_df["created_at"] = pd.to_datetime(curve_df["created_at"])
    curve_df = curve_df.set_index("created_at")

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.subheader("Profit cumulé")
        st.line_chart(curve_df["profit"])

    with chart_col2:
        st.subheader("ROI cumulé")
        st.line_chart(curve_df["roi"])
else:
    st.info("Aucun pari terminé ne correspond aux filtres.")

st.divider()

predictions = backtest["predictions"]

if predictions:
    df = pd.DataFrame(predictions)
    columns = [
        "created_at",
        "match",
        "league",
        "bookmaker",
        "bet_type",
        "predicted_result",
        "result",
        "odd",
        "confidence",
        "value",
        "stake",
        "profit",
        "fallback",
        "fixture_api_id",
        "settled_at",
    ]

    st.dataframe(
        df[[column for column in columns if column in df.columns]],
        width="stretch",
        hide_index=True,
    )
