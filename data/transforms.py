import pandas as pd


def get_kpi_metrics(df: pd.DataFrame) -> dict:
    return {
        "total_sales": float(round(df["total_amount"].sum(), 2)),
        "total_orders": int(len(df)),
    }


def get_monthly_sales(df: pd.DataFrame) -> pd.DataFrame:
    monthly = (
        df.assign(month=pd.to_datetime(df["date"]).dt.to_period("M").dt.to_timestamp())
        .groupby("month", as_index=False)["total_amount"]
        .sum()
        .rename(columns={"total_amount": "total_sales"})
        .sort_values("month")
        .reset_index(drop=True)
    )
    return monthly
