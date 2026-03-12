import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def build_category_chart(df: pd.DataFrame) -> go.Figure:
    fig = px.bar(df, x="total_sales", y="category", orientation="h")
    fig.update_layout(
        xaxis_title="Total Sales ($)",
        yaxis_title="Category",
        yaxis={"categoryorder": "total ascending"},
    )
    fig.update_traces(
        hovertemplate="<b>%{y}</b><br>Sales: $%{x:,.0f}<extra></extra>"
    )
    return fig
