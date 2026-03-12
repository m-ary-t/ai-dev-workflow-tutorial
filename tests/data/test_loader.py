import pytest
import pandas as pd
from data.loader import DataLoadError, load_sales_data

EXPECTED_COLUMNS = {
    "date", "order_id", "product", "category",
    "region", "quantity", "unit_price", "total_amount",
}


# T004: valid CSV path returns a DataFrame with expected columns
def test_load_sales_data_returns_dataframe(tmp_path):
    csv = tmp_path / "sales.csv"
    csv.write_text(
        "date,order_id,product,category,region,quantity,unit_price,total_amount\n"
        "2024-01-03,ORD-001,Earbuds,Audio,North,2,79.99,159.98\n"
    )
    df = load_sales_data(str(csv))
    assert isinstance(df, pd.DataFrame)
    assert EXPECTED_COLUMNS.issubset(set(df.columns))


# T005: missing file raises DataLoadError
def test_load_sales_data_missing_file_raises():
    with pytest.raises(DataLoadError):
        load_sales_data("/nonexistent/path/sales.csv")


# T017 [US5]: CSV missing required columns raises DataLoadError with descriptive message
def test_load_sales_data_missing_columns_raises(tmp_path):
    csv = tmp_path / "bad.csv"
    csv.write_text("date,order_id\n2024-01-01,ORD-001\n")
    with pytest.raises(DataLoadError, match="missing required columns"):
        load_sales_data(str(csv))


# T018 [US5]: CSV with all-null total_amount raises DataLoadError
def test_load_sales_data_all_null_total_amount_raises(tmp_path):
    csv = tmp_path / "nulls.csv"
    csv.write_text(
        "date,order_id,product,category,region,quantity,unit_price,total_amount\n"
        "2024-01-03,ORD-001,Earbuds,Audio,North,2,79.99,\n"
    )
    with pytest.raises(DataLoadError):
        load_sales_data(str(csv))
