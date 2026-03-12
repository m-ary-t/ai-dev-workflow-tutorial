import streamlit as st


def render_kpi_cards(total_sales: float, total_orders: int) -> None:
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Total Sales", value=f"${total_sales:,.0f}")
    with col2:
        st.metric(label="Total Orders", value=total_orders)
