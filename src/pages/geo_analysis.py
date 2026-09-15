"""
Trang Phân tích địa lý.
Loại biểu đồ minh hoạ ở đây: Choropleth Map (bắt buộc theo barem),
Treemap, Heatmap.
"""

from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import plotly.express as px
import streamlit as st
from src.shared.dashboard_context import render_page


def render(orders_filtered):
    if orders_filtered.empty:
        st.warning("Không có dữ liệu khớp với bộ lọc hiện tại.")
        return

    st.subheader("Doanh thu theo quốc gia (Choropleth Map -- bắt buộc)")
    by_country = orders_filtered.groupby("Country", as_index=False)["Sales"].sum()
    fig = px.choropleth(
        by_country, locations="Country", locationmode="country names",
        color="Sales", color_continuous_scale="Blues",
    )
    st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Doanh thu theo Quốc gia / Danh mục (Treemap)")
        fig = px.treemap(
            orders_filtered, path=["Region", "Country", "Category"], values="Sales",
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Doanh thu theo Khu vực x Danh mục (Heatmap)")
        pivot = orders_filtered.pivot_table(
            index="Region", columns="Category", values="Sales", aggfunc="sum", fill_value=0
        )
        fig = px.imshow(pivot, text_auto=".0f", color_continuous_scale="Oranges")
        st.plotly_chart(fig, use_container_width=True)


st.set_page_config(page_title="Địa lý | Retail RFM", layout="wide")
render_page("🌍 Phân tích địa lý", render)
