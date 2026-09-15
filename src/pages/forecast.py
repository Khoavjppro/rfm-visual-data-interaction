"""
Trang Dự báo doanh thu.
Demo NHANH bằng Linear Regression trên dữ liệu giả lập.
Thành viên phụ trách "Insight & Forecast" sẽ thay bằng mô hình thật
(train kỹ hơn, có thể thêm Logistic Regression dự báo churn ở đây).
"""

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from sklearn.linear_model import LinearRegression


def render(orders_filtered):
    if orders_filtered.empty:
        st.warning("Không có dữ liệu khớp với bộ lọc hiện tại.")
        return

    st.subheader("Dự báo doanh thu 3 tháng tới (Linear Regression -- demo)")

    monthly = (
        orders_filtered.set_index("Order Date")
        .resample("MS")["Sales"]
        .sum()
        .reset_index()
    )
    if len(monthly) < 3:
        st.info("Cần ít nhất 3 tháng dữ liệu để dự báo. Hãy mở rộng khoảng thời gian ở bộ lọc.")
        return

    monthly["t"] = np.arange(len(monthly))
    model = LinearRegression().fit(monthly[["t"]], monthly["Sales"])

    future_t = np.arange(len(monthly), len(monthly) + 3)
    future_dates = pd.date_range(
        monthly["Order Date"].max() + pd.DateOffset(months=1), periods=3, freq="MS"
    )
    future_sales = model.predict(future_t.reshape(-1, 1))

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=monthly["Order Date"], y=monthly["Sales"],
                              mode="lines+markers", name="Thực tế"))
    fig.add_trace(go.Scatter(x=future_dates, y=future_sales,
                              mode="lines+markers", name="Dự báo",
                              line=dict(dash="dash")))
    st.plotly_chart(fig, use_container_width=True)

    st.caption(
        f"Hệ số góc (xu hướng/tháng): {model.coef_[0]:,.1f} -- "
        "đây là mô hình DEMO trên dữ liệu giả lập, sẽ train lại trên dữ liệu thật ở Giai đoạn 4-5."
    )
