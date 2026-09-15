"""
Điểm nối DUY NHẤT giữa Dashboard và dữ liệu đã làm sạch.

Dashboard luôn đọc data/cleaned_data.csv. Muốn cập nhật dữ liệu, hãy
đưa CSV nguồn vào data/raw/ rồi chạy scripts/clean_data.py. Các trang
trong src/pages/ không được đọc trực tiếp dữ liệu raw.
"""

from pathlib import Path
import pandas as pd
import streamlit as st

from src.shared.rfm_utils import build_rfm_table

ROOT_DIR = Path(__file__).resolve().parents[2]

CLEAN_DATA_PATH = ROOT_DIR / "data" / "cleaned_data.csv"


@st.cache_data
def load_orders() -> pd.DataFrame:
    if not CLEAN_DATA_PATH.exists() or CLEAN_DATA_PATH.stat().st_size == 0:
        raise FileNotFoundError(
            "Chưa có dữ liệu đã làm sạch. Hãy chạy: "
            "python scripts/clean_data.py"
        )

    df = pd.read_csv(CLEAN_DATA_PATH, parse_dates=["Order Date"])
    return df


@st.cache_data
def load_rfm() -> pd.DataFrame:
    orders = load_orders()
    return build_rfm_table(orders)
