import pandas as pd
import plotly.graph_objects as go
from components.trend_chart import build_trend_chart


# T013 [US2]: build_trend_chart returns a Figure with one scatter trace
def test_build_trend_chart_returns_figure():
    df = pd.DataFrame({
        "month": pd.to_datetime(["2024-01-01", "2024-02-01", "2024-03-01"]),
        "total_sales": [1000.0, 1500.0, 1200.0],
    })
    fig = build_trend_chart(df)
    assert isinstance(fig, go.Figure)


def test_build_trend_chart_has_one_scatter_trace():
    df = pd.DataFrame({
        "month": pd.to_datetime(["2024-01-01", "2024-02-01"]),
        "total_sales": [1000.0, 1500.0],
    })
    fig = build_trend_chart(df)
    assert len(fig.data) == 1
    assert fig.data[0].type == "scatter"
