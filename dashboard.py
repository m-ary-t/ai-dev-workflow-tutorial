import streamlit as st
from data.loader import DataLoadError, load_sales_data
from data.transforms import get_kpi_metrics, get_monthly_sales
from components.kpi_cards import render_kpi_cards
from components.trend_chart import build_trend_chart

DATA_PATH = "data/sales-data.csv"

try:
    df = load_sales_data(DATA_PATH)

    metrics = get_kpi_metrics(df)
    render_kpi_cards(
        total_sales=metrics["total_sales"],
        total_orders=metrics["total_orders"],
    )

    st.subheader("Sales Trend")
    monthly_df = get_monthly_sales(df)
    st.plotly_chart(build_trend_chart(monthly_df), use_container_width=True)

except DataLoadError as e:
    st.error(str(e))
