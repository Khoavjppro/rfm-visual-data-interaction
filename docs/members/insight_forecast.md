# Phân công Insight, RFM và Forecast

**Phụ trách:**   
**Mục tiêu:** biến dữ liệu sạch thành các phân khúc khách hàng, insight kinh doanh và dự báo doanh thu có đánh giá rõ ràng.

## Phạm vi sở hữu

```text
src/shared/rfm_utils.py            Công thức RFM, score và segment
src/shared/forecasting.py          Sẽ tạo mới: chuẩn bị chuỗi thời gian, train, evaluate, predict
src/pages/4_forecast.py            Tích hợp đầu ra mô hình với người phụ trách Dashboard
docs/members/insight_forecast.md   Theo dõi giả định, metric và insight
```

Không thay đổi cách làm sạch dữ liệu trong `data_cleaning.py`. Không chỉnh layout/filter chung trong `dashboard_context.py` nếu chưa trao đổi với người phụ trách Dashboard.

## Phần nền tảng đã có

- [x] `rfm_utils.py` tính Recency, Frequency, Monetary theo `Customer ID`.
- [x] Có R/F/M score 1–5 và các segment: Champions, Loyal Customers, New Customers, At Risk, Lost, Need Attention.
- [x] Trang RFM đã hiển thị tỷ trọng segment, scatter Frequency–Monetary, box plot và bảng chi tiết.
- [x] Trang dự báo có Linear Regression demo, dự báo doanh thu ba tháng tiếp theo.

## Việc cần hoàn thiện: RFM và insight

- [ ] Xác nhận định nghĩa nghiệp vụ của Recency, Frequency, Monetary và ngày snapshot với nhóm.
- [ ] Kiểm thử RFM trên dữ liệu thật; xử lý trường hợp nhiều giá trị Recency trùng khiến `qcut` không tạo đủ nhóm.
- [ ] Viết mô tả và hành động đề xuất cho từng segment.
- [ ] Tạo các insight có bằng chứng: xu hướng doanh thu, khu vực/danh mục nổi bật, nhóm khách hàng giá trị cao và nhóm rủi ro.
- [ ] Mỗi insight cần có: quan sát dữ liệu, diễn giải ngắn và khuyến nghị hành động.

## Việc cần hoàn thiện: Forecast

- [ ] Tách logic hiện có trong `src/pages/4_forecast.py` sang `src/shared/forecasting.py`; page chỉ hiển thị kết quả.
- [ ] Tổng hợp doanh thu theo tháng, xử lý tháng bị thiếu và xác định horizon dự báo.
- [ ] Chia train/test theo thời gian, không chia ngẫu nhiên.
- [ ] Đánh giá mô hình bằng ít nhất MAE và RMSE; MAPE nếu doanh thu không bằng 0.
- [ ] So sánh Linear Regression với baseline đơn giản, ví dụ doanh thu tháng gần nhất hoặc trung bình trượt.
- [ ] Hiển thị actual, prediction trên tập test, future forecast và metric trên dashboard.
- [ ] Sửa cảnh báo feature name bằng cách dự đoán với DataFrame có cột `t`.
- [ ] Ghi rõ giả định và giới hạn của mô hình; không diễn giải forecast demo như kết quả chính thức.

## Hợp đồng bàn giao cho Dashboard

- Hàm RFM trả về tối thiểu: `Customer ID`, `Recency`, `Frequency`, `Monetary`, `R_score`, `F_score`, `M_score`, `RFM_Score`, `Segment`.
- Hàm forecast cần trả về dữ liệu theo tháng cho actual/test prediction/future prediction và dictionary metric.
- Gửi nội dung insight ngắn, có thể hiển thị dưới biểu đồ: tiêu đề, phát hiện, khuyến nghị.

## Tiêu chí hoàn thành

- RFM ổn định khi chạy với dữ liệu thật và segment có mô tả nghiệp vụ.
- Forecast có time-based validation, metric và biểu đồ dễ đối chiếu.
- Có danh sách insight/kết luận đủ để sử dụng trong dashboard và phần trình bày đồ án.
