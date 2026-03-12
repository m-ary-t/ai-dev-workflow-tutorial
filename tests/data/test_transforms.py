import pytest
import pandas as pd
from data.transforms import get_kpi_metrics, get_monthly_sales, get_category_sales, get_region_sales


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


# T012 [US2]: get_monthly_sales returns correct columns, sorted chronologically
def test_get_monthly_sales_columns(sample_df):
    result = get_monthly_sales(sample_df)
    assert "month" in result.columns
    assert "total_sales" in result.columns


def test_get_monthly_sales_sorted(sample_df):
    result = get_monthly_sales(sample_df)
    assert list(result["month"]) == sorted(result["month"].tolist())


def test_get_monthly_sales_aggregation(sample_df):
    result = get_monthly_sales(sample_df)
    # sample_df has rows in Jan, Feb, Mar, Apr, May 2024
    assert len(result) == 5
    total = result["total_sales"].sum()
    assert total == pytest.approx(sample_df["total_amount"].sum(), rel=1e-3)


# T022 [US3]: get_category_sales returns correct columns, sorted descending
def test_get_category_sales_columns(sample_df):
    result = get_category_sales(sample_df)
    assert "category" in result.columns
    assert "total_sales" in result.columns


def test_get_category_sales_sorted_descending(sample_df):
    result = get_category_sales(sample_df)
    sales = result["total_sales"].tolist()
    assert sales == sorted(sales, reverse=True)


def test_get_category_sales_aggregation(sample_df):
    result = get_category_sales(sample_df)
    # sample_df has 5 distinct categories
    assert len(result) == 5
    assert result["total_sales"].sum() == pytest.approx(sample_df["total_amount"].sum(), rel=1e-3)


# T027 [US4]: get_region_sales returns correct columns, sorted descending
def test_get_region_sales_columns(sample_df):
    result = get_region_sales(sample_df)
    assert "region" in result.columns
    assert "total_sales" in result.columns


def test_get_region_sales_sorted_descending(sample_df):
    result = get_region_sales(sample_df)
    sales = result["total_sales"].tolist()
    assert sales == sorted(sales, reverse=True)


def test_get_region_sales_aggregation(sample_df):
    result = get_region_sales(sample_df)
    # sample_df has 4 distinct regions
    assert len(result) == 4
    assert result["total_sales"].sum() == pytest.approx(sample_df["total_amount"].sum(), rel=1e-3)
