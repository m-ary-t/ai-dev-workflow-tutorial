import pandas as pd
import plotly.graph_objects as go
from components.category_chart import build_category_chart


# T023 [US3]: build_category_chart returns a Figure with one bar trace, sorted descending
def test_build_category_chart_returns_figure():
    df = pd.DataFrame({
        "category": ["Electronics", "Audio", "Wearables"],
        "total_sales": [5000.0, 3000.0, 1000.0],
    })
    fig = build_category_chart(df)
    assert isinstance(fig, go.Figure)


def test_build_category_chart_has_one_bar_trace():
    df = pd.DataFrame({
        "category": ["Electronics", "Audio"],
        "total_sales": [5000.0, 3000.0],
    })
    fig = build_category_chart(df)
    assert len(fig.data) == 1
    assert fig.data[0].type == "bar"


def test_build_category_chart_sorted_descending():
    df = pd.DataFrame({
        "category": ["Electronics", "Audio", "Wearables"],
        "total_sales": [5000.0, 3000.0, 1000.0],
    })
    fig = build_category_chart(df)
    x_values = list(fig.data[0].x)
    assert x_values == sorted(x_values, reverse=True)
