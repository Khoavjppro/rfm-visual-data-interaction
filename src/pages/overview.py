"""
Trang Tổng quan doanh thu.
Loại biểu đồ minh hoạ ở đây: Bar chart, Line chart.
"""

import plotly.express as px
import streamlit as st


def render(orders_filtered):
    if orders_filtered.empty:
        st.warning("Không có dữ liệu khớp với bộ lọc hiện tại.")
        return

    col1, col2, col3 = st.columns(3)
    col1.metric("Tổng doanh thu", f"${orders_filtered['Sales'].sum():,.0f}")
    col2.metric("Tổng lợi nhuận", f"${orders_filtered['Profit'].sum():,.0f}")
    col3.metric("Số đơn hàng", f"{orders_filtered['Order ID'].nunique():,}")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Doanh thu theo danh mục (Bar chart)")
        by_cat = orders_filtered.groupby("Category", as_index=False)["Sales"].sum()
        fig = px.bar(by_cat, x="Category", y="Sales", color="Category")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Xu hướng doanh thu theo tháng (Line chart)")
        monthly = (
            orders_filtered.set_index("Order Date")
            .resample("MS")["Sales"]
            .sum()
            .reset_index()
        )
        fig = px.line(monthly, x="Order Date", y="Sales", markers=True)
        st.plotly_chart(fig, use_container_width=True)
