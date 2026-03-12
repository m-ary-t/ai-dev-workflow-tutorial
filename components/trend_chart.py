import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def build_trend_chart(df: pd.DataFrame) -> go.Figure:
    fig = px.line(df, x="month", y="total_sales")
    fig.update_layout(
        xaxis_title="Month",
        yaxis_title="Total Sales ($)",
    )
    fig.update_traces(
        hovertemplate="<b>%{x|%b %Y}</b><br>Sales: $%{y:,.0f}<extra></extra>"
    )
    return fig
