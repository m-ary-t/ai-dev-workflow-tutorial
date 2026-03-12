import pandas as pd
import streamlit as st


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
    return df
