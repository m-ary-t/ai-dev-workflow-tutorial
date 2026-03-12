import pandas as pd
import streamlit as st

REQUIRED_COLUMNS = {
    "date", "order_id", "product", "category",
    "region", "quantity", "unit_price", "total_amount",
}


class DataLoadError(Exception):
    pass


@st.cache_data
def load_sales_data(path: str) -> pd.DataFrame:
    try:
        df = pd.read_csv(path)
    except FileNotFoundError:
        raise DataLoadError(f"Sales data file not found: {path}")
    except Exception as e:
        raise DataLoadError(f"Failed to load sales data: {e}")

    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise DataLoadError(
            f"Sales data is missing required columns: {', '.join(sorted(missing))}"
        )

    if df["total_amount"].isnull().all():
        raise DataLoadError(
            "Sales data has no valid values in 'total_amount' — the file may be corrupt."
        )

    return df
