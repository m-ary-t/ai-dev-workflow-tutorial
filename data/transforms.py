import pandas as pd


def get_kpi_metrics(df: pd.DataFrame) -> dict:
    return {
        "total_sales": float(round(df["total_amount"].sum(), 2)),
        "total_orders": int(len(df)),
    }
