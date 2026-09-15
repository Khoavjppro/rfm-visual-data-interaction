# Phân công Dashboard Streamlit

**Phụ trách:** Phạm Đức Khoa  
**Mục tiêu:** xây dựng dashboard tương tác cho đồ án phân tích hiệu suất bán hàng và phân khúc khách hàng RFM.

## Phạm vi phụ trách

- Xây dựng giao diện và trải nghiệm người dùng bằng Streamlit.
- Duy trì các trang dashboard trong `src/pages/`.
- Tạo biểu đồ Plotly, bản đồ tương tác và các bộ lọc dùng chung.
- Kết nối giao diện với dữ liệu đã làm sạch tại `data/cleaned_data.csv`.
- Phối hợp với thành viên xử lý dữ liệu/RFM và thành viên phụ trách dự báo để tích hợp đầu ra vào dashboard.

## Kiến trúc cần tuân thủ

```text
src/app.py                         Trang chủ; Streamlit tự nhận các page
src/pages/overview.py              Trang tổng quan bán hàng
src/pages/rfm_segment.py           Trang phân khúc khách hàng RFM
src/pages/geo_analysis.py          Trang phân tích địa lý
src/pages/forecast.py              Trang dự báo doanh thu
src/shared/dashboard_context.py    Header, filter và context dùng chung
src/shared/data_loader.py          Chỉ đọc dữ liệu đã làm sạch
src/shared/rfm_utils.py            Công thức RFM dùng chung
```

Khi chạy `streamlit run src/app.py`, các file trong `src/pages/` tự xuất hiện trong menu sidebar. Mỗi file page phải tự gọi `render_page(...)`; không chỉ khai báo hàm `render(...)`.

## Input và output

### Input

- `load_orders()`: đơn hàng đã làm sạch từ `data/cleaned_data.csv`.
- `load_rfm()`: bảng RFM gồm `Customer ID`, Recency, Frequency, Monetary, điểm RFM và Segment.
- `get_filtered_data()`: dữ liệu sau filter khu vực, quốc gia, thời gian và segment.

### Output hiện có

- [x] Filter nhiều cấp: khu vực → quốc gia, thời gian và RFM segment.
- [x] Tổng quan: KPI, bar chart, line chart.
- [x] RFM: donut chart, scatter plot, box plot và bảng chi tiết.
- [x] Địa lý: choropleth map, treemap, heatmap.
- [x] Dự báo: thực tế và dự báo ba tháng với Linear Regression demo.
- [x] Tối thiểu 8 biểu đồ: bar, line, donut/pie, scatter, box, choropleth, treemap và heatmap.

## Việc cần hoàn thiện

- [ ] Thêm biểu đồ loại thứ 9 để phần dự báo không lặp lại line chart (gợi ý: top 10 sản phẩm dạng horizontal bar hoặc histogram giá trị đơn hàng).
- [ ] Viết insight ngắn dưới từng trang: điều gì xảy ra, nguyên nhân khả dĩ và hành động đề xuất.
- [ ] Kiểm thử với dữ liệu thật sau khi nhóm xử lý dữ liệu bàn giao.
- [ ] Hoàn thiện mô hình dự báo và đánh giá chất lượng dự báo trên dữ liệu thật.
- [ ] Cân nhắc drill-down/cross-filtering nếu phù hợp tiến độ.

## Quy tắc tích hợp

- Không đọc trực tiếp file trong `data/raw/` từ bất kỳ page nào.
- Không viết lại công thức RFM trong page; luôn sử dụng `src/shared/rfm_utils.py`.
- Không sửa `data_loader.py` để phục vụ riêng một biểu đồ; đề xuất thay đổi schema chung với nhóm trước.
- Khi thêm biểu đồ, đảm bảo xử lý trường hợp DataFrame rỗng và dùng `use_container_width=True`.
- Mỗi thay đổi nên có commit riêng, ví dụ: `feat: add top products chart`.
