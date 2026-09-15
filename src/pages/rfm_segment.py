"""
Trang Phân khúc khách hàng theo RFM.
Loại biểu đồ minh hoạ ở đây: Pie chart, Scatter plot, Box plot.
"""

from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import plotly.express as px
import streamlit as st
from src.shared.dashboard_context import render_page


def render(rfm_filtered):
    if rfm_filtered.empty:
        st.warning("Không có khách hàng nào khớp với bộ lọc hiện tại.")
        return

    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("Tỷ trọng khách hàng theo phân khúc (Pie chart)")
        seg_count = rfm_filtered["Segment"].value_counts().reset_index()
        seg_count.columns = ["Segment", "Count"]
        fig = px.pie(seg_count, names="Segment", values="Count", hole=0.4)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Frequency vs Monetary theo phân khúc (Scatter plot)")
        fig = px.scatter(
            rfm_filtered, x="Frequency", y="Monetary", color="Segment",
            size="Monetary", hover_data=["Customer ID", "Recency"],
        )
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Phân phối giá trị khách hàng (Monetary) theo phân khúc (Box plot)")
    fig = px.box(rfm_filtered, x="Segment", y="Monetary", color="Segment")
    st.plotly_chart(fig, use_container_width=True)

    with st.expander("Xem bảng chi tiết RFM"):
        st.dataframe(
            rfm_filtered[["Customer ID", "Country", "Recency", "Frequency", "Monetary", "RFM_Score", "Segment"]],
            use_container_width=True,
        )


st.set_page_config(page_title="RFM | Retail RFM", layout="wide")
render_page("👥 Phân khúc khách hàng RFM", render, use_rfm_data=True)
