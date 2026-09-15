"""Thành phần dùng chung cho các trang Streamlit trong src/pages/."""

import pandas as pd
import streamlit as st

from src.shared.data_loader import load_orders, load_rfm


def get_filtered_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    """Hiển thị sidebar filter và trả về đơn hàng/RFM sau lọc."""
    orders = load_orders()
    rfm = load_rfm()

    st.sidebar.header("Bộ lọc")
    regions = sorted(orders["Region"].unique())
    selected_regions = st.sidebar.multiselect("Khu vực", regions, default=regions)

    countries = sorted(
        orders[orders["Region"].isin(selected_regions)]["Country"].unique()
    )
    selected_countries = st.sidebar.multiselect(
        "Quốc gia (drill-down)", countries, default=countries
    )

    date_min, date_max = orders["Order Date"].min(), orders["Order Date"].max()
    date_range = st.sidebar.date_input(
        "Khoảng thời gian",
        value=(date_min, date_max),
        min_value=date_min,
        max_value=date_max,
    )

    segments = sorted(rfm["Segment"].unique())
    selected_segments = st.sidebar.multiselect(
        "Phân khúc khách hàng (RFM)", segments, default=segments
    )

    start_date, end_date = pd.Timestamp(date_range[0]), pd.Timestamp(date_range[1])
    orders_filtered = orders[
        orders["Region"].isin(selected_regions)
        & orders["Country"].isin(selected_countries)
        & orders["Order Date"].between(start_date, end_date)
    ]
    customers_filtered = orders_filtered["Customer ID"].unique()
    rfm_filtered = rfm[
        rfm["Customer ID"].isin(customers_filtered)
        & rfm["Segment"].isin(selected_segments)
    ]

    st.sidebar.divider()
    st.sidebar.metric("Số đơn hàng (sau lọc)", f"{len(orders_filtered):,}")
    st.sidebar.metric("Số khách hàng (sau lọc)", f"{rfm_filtered['Customer ID'].nunique():,}")
    return orders_filtered, rfm_filtered


def render_page(title: str, render_function, use_rfm_data: bool = False) -> None:
    """Dựng tiêu đề, filter chung và nội dung của một trang dashboard."""
    st.title(title)
    st.caption("Dashboard đang dùng dữ liệu đã làm sạch từ data/cleaned_data.csv")
    orders_filtered, rfm_filtered = get_filtered_data()
    render_function(rfm_filtered if use_rfm_data else orders_filtered)
