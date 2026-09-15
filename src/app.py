"""
Điểm vào Dashboard. Chạy bằng:
    streamlit run src/app.py

Cấu trúc: 1 bộ filter dùng chung ở sidebar (áp dụng cho mọi tab)
+ 4 tab tương ứng 4 mảng việc trong nhóm. Mỗi tab hiện đang có 2
biểu đồ mẫu -- sau này mỗi thành viên mở rộng thêm trong file
src/pages/<ten_trang>.py tương ứng, KHÔNG sửa trực tiếp app.py
để tránh commit dẫm chân nhau.
"""

import pandas as pd
import streamlit as st

from src.shared.data_loader import load_orders, load_rfm
from src.pages import overview, rfm_segment, geo_analysis, forecast

st.set_page_config(page_title="Retail RFM Dashboard", layout="wide")

st.title("📊 Phân tích hiệu suất bán hàng & Phân khúc khách hàng (RFM)")
st.caption("Dữ liệu hiện tại: MOCK DATA (giả lập) -- sẽ thay bằng dữ liệu thật ở Giai đoạn 2")

orders = load_orders()
rfm = load_rfm()

# ---------- Bộ lọc dùng chung (sidebar) ----------
st.sidebar.header("Bộ lọc")

regions = sorted(orders["Region"].unique())
selected_regions = st.sidebar.multiselect("Khu vực", regions, default=regions)

countries_in_region = sorted(orders[orders["Region"].isin(selected_regions)]["Country"].unique())
selected_countries = st.sidebar.multiselect("Quốc gia (drill-down)", countries_in_region, default=countries_in_region)

date_min, date_max = orders["Order Date"].min(), orders["Order Date"].max()
date_range = st.sidebar.date_input("Khoảng thời gian", value=(date_min, date_max), min_value=date_min, max_value=date_max)

segments = sorted(rfm["Segment"].unique())
selected_segments = st.sidebar.multiselect("Phân khúc khách hàng (RFM)", segments, default=segments)

# áp filter
start_date, end_date = pd.Timestamp(date_range[0]), pd.Timestamp(date_range[1])
orders_filtered = orders[
    orders["Region"].isin(selected_regions)
    & orders["Country"].isin(selected_countries)
    & orders["Order Date"].between(start_date, end_date)
]
customers_filtered = orders_filtered["Customer ID"].unique()
rfm_filtered = rfm[
    rfm["Customer ID"].isin(customers_filtered) & rfm["Segment"].isin(selected_segments)
]

st.sidebar.markdown("---")
st.sidebar.metric("Số đơn hàng (sau lọc)", f"{len(orders_filtered):,}")
st.sidebar.metric("Số khách hàng (sau lọc)", f"{rfm_filtered['Customer ID'].nunique():,}")

# ---------- 4 tab tương ứng 4 mảng việc ----------
tab1, tab2, tab3, tab4 = st.tabs(["Tổng quan", "Phân khúc RFM", "Phân tích địa lý", "Dự báo"])

with tab1:
    overview.render(orders_filtered)

with tab2:
    rfm_segment.render(rfm_filtered)

with tab3:
    geo_analysis.render(orders_filtered)

with tab4:
    forecast.render(orders_filtered)
