import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def build_region_chart(df: pd.DataFrame) -> go.Figure:
    fig = px.bar(df, x="total_sales", y="region", orientation="h")
    fig.update_layout(
        xaxis_title="Total Sales ($)",
        yaxis_title="Region",
        yaxis={"categoryorder": "total ascending"},
    )
    fig.update_traces(
        hovertemplate="<b>%{y}</b><br>Sales: $%{x:,.0f}<extra></extra>"
    )
    return fig
