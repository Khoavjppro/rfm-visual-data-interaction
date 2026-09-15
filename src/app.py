"""
Trang chủ Dashboard. Chạy bằng:
    streamlit run src/app.py

Các trang chính nằm trong src/pages/. Streamlit tự hiển thị chúng ở
sidebar khi chạy app.py.
"""
from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


import streamlit as st

st.set_page_config(page_title="Retail RFM Dashboard", layout="wide")

st.title("📊 Phân tích hiệu suất bán hàng & Phân khúc khách hàng (RFM)")
st.caption("Chọn một trang phân tích từ menu ở sidebar.")
st.info(
    "Các trang Tổng quan, Phân khúc RFM, Phân tích địa lý và Dự báo "
    "được quản lý độc lập trong thư mục src/pages/."
)
