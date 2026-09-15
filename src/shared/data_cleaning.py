"""Chuẩn hoá dữ liệu đơn hàng trước khi dashboard sử dụng."""

from pathlib import Path

import pandas as pd


REQUIRED_COLUMNS = [
    "Order ID", "Order Date", "Customer ID", "Country", "Region",
    "Category", "Sub-Category", "Sales", "Quantity", "Profit",
]

# Các tên cột thường gặp trong CSV thật. Có thể bổ sung khi nhóm nhận dataset.
COLUMN_ALIASES = {
    "order id": "Order ID",
    "order_id": "Order ID",
    "order date": "Order Date",
    "order_date": "Order Date",
    "customer id": "Customer ID",
    "customer_id": "Customer ID",
    "country": "Country",
    "region": "Region",
    "market": "Region",
    "category": "Category",
    "sub-category": "Sub-Category",
    "sub category": "Sub-Category",
    "sub_category": "Sub-Category",
    "sales": "Sales",
    "revenue": "Sales",
    "quantity": "Quantity",
    "profit": "Profit",
}


def clean_orders(raw_path: Path, clean_path: Path) -> pd.DataFrame:
    """Đọc CSV raw, chuẩn hoá schema và ghi một CSV sạch cho dashboard."""
    df = pd.read_csv(raw_path)
    df.columns = [str(column).strip() for column in df.columns]

    rename_map = {
        column: COLUMN_ALIASES[column.strip().lower()]
        for column in df.columns
        if column.strip().lower() in COLUMN_ALIASES
    }
    df = df.rename(columns=rename_map)

    missing_columns = sorted(set(REQUIRED_COLUMNS) - set(df.columns))
    if missing_columns:
        raise ValueError(
            "Dữ liệu thiếu các cột bắt buộc: " + ", ".join(missing_columns)
        )

    df = df[REQUIRED_COLUMNS].copy()
    df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")

    for column in ["Sales", "Quantity", "Profit"]:
        # Hỗ trợ giá trị như "$1,200.50" hoặc "1,200.50".
        df[column] = pd.to_numeric(
            df[column].astype(str).str.replace(r"[^0-9.-]", "", regex=True),
            errors="coerce",
        )

    for column in ["Order ID", "Customer ID", "Country", "Region", "Category", "Sub-Category"]:
        df[column] = df[column].astype("string").str.strip()

    df = df.dropna(subset=REQUIRED_COLUMNS).drop_duplicates()
    df = df[(df["Sales"] >= 0) & (df["Quantity"] > 0)]
    df = df.sort_values("Order Date").reset_index(drop=True)

    clean_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(clean_path, index=False)
    return df
