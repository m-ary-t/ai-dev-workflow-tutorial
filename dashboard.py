import streamlit as st

st.set_page_config(page_title="ShopSmart Sales Dashboard", layout="wide")
st.title("ShopSmart Sales Dashboard")
from data.loader import DataLoadError, load_sales_data
from data.transforms import get_kpi_metrics, get_monthly_sales, get_category_sales, get_region_sales
from components.kpi_cards import render_kpi_cards
from components.trend_chart import build_trend_chart
from components.category_chart import build_category_chart
from components.region_chart import build_region_chart

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

    col_left, col_right = st.columns(2)
    with col_left:
        st.subheader("Sales by Category")
        st.plotly_chart(build_category_chart(get_category_sales(df)), use_container_width=True)
    with col_right:
        st.subheader("Sales by Region")
        st.plotly_chart(build_region_chart(get_region_sales(df)), use_container_width=True)

except DataLoadError as e:
    st.error(str(e))
