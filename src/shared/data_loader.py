"""
Điểm nối DUY NHẤT giữa Dashboard và nguồn dữ liệu.

Hiện tại đang trỏ vào data/raw/mock_orders.csv (dữ liệu giả lập).
Khi bạn làm xong bước làm sạch dữ liệu thật (Giai đoạn 1-2), chỉ cần
đổi ORDERS_PATH bên dưới sang data/processed/orders_clean.csv
-> KHÔNG cần sửa bất kỳ file nào khác trong src/pages/.
"""

from pathlib import Path
import pandas as pd
import streamlit as st

from src.shared.rfm_utils import build_rfm_table

ROOT_DIR = Path(__file__).resolve().parents[2]

# <<< DÒNG DUY NHẤT CẦN SỬA KHI CÓ DATA THẬT >>>
ORDERS_PATH = ROOT_DIR / "data" / "raw" / "mock_orders.csv"


@st.cache_data
def load_orders() -> pd.DataFrame:
    df = pd.read_csv(ORDERS_PATH, parse_dates=["Order Date"])
    return df


@st.cache_data
def load_rfm() -> pd.DataFrame:
    orders = load_orders()
    return build_rfm_table(orders)
