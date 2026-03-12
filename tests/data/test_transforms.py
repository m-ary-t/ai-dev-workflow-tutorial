import pytest
import pandas as pd
from data.transforms import get_kpi_metrics


# T007 [US1]: get_kpi_metrics returns correct keys and types
def test_get_kpi_metrics_keys_and_types(sample_df):
    result = get_kpi_metrics(sample_df)
    assert "total_sales" in result
    assert "total_orders" in result
    assert isinstance(result["total_sales"], float)
    assert isinstance(result["total_orders"], int)


def test_get_kpi_metrics_values(sample_df):
    result = get_kpi_metrics(sample_df)
    expected_sales = round(sample_df["total_amount"].sum(), 2)
    expected_orders = len(sample_df)
    assert result["total_sales"] == pytest.approx(expected_sales)
    assert result["total_orders"] == expected_orders
