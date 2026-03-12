import pandas as pd
import plotly.graph_objects as go
from components.region_chart import build_region_chart


# T028 [US4]: build_region_chart returns a Figure with one bar trace, sorted descending
def test_build_region_chart_returns_figure():
    df = pd.DataFrame({
        "region": ["North", "South", "East", "West"],
        "total_sales": [4000.0, 3000.0, 2000.0, 1000.0],
    })
    fig = build_region_chart(df)
    assert isinstance(fig, go.Figure)


def test_build_region_chart_has_one_bar_trace():
    df = pd.DataFrame({
        "region": ["North", "South"],
        "total_sales": [4000.0, 3000.0],
    })
    fig = build_region_chart(df)
    assert len(fig.data) == 1
    assert fig.data[0].type == "bar"


def test_build_region_chart_sorted_descending():
    df = pd.DataFrame({
        "region": ["North", "South", "East", "West"],
        "total_sales": [4000.0, 3000.0, 2000.0, 1000.0],
    })
    fig = build_region_chart(df)
    x_values = list(fig.data[0].x)
    assert x_values == sorted(x_values, reverse=True)
