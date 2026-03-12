import streamlit as st
from data.loader import DataLoadError, load_sales_data
from data.transforms import get_kpi_metrics
from components.kpi_cards import render_kpi_cards

DATA_PATH = "data/sales-data.csv"

try:
    df = load_sales_data(DATA_PATH)
    metrics = get_kpi_metrics(df)
    render_kpi_cards(
        total_sales=metrics["total_sales"],
        total_orders=metrics["total_orders"],
    )
except DataLoadError as e:
    st.error(str(e))
