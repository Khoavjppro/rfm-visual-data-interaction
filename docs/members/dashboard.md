# Phân công Dashboard Streamlit

**Phụ trách:** Phạm Đức Khoa  
**Mục tiêu:** xây dựng giao diện Streamlit trực quan, nhất quán và tích hợp các đầu ra do phần Data và Insight & Forecast bàn giao.

## Phạm vi phụ trách

- Xây dựng giao diện và trải nghiệm người dùng bằng Streamlit.
- Duy trì các trang dashboard trong `src/pages/`.
- Tạo biểu đồ Plotly, bản đồ tương tác và các bộ lọc dùng chung.
- Tích hợp dữ liệu đã làm sạch, bảng RFM và kết quả dự báo vào giao diện.
- Không sở hữu logic làm sạch dữ liệu, công thức RFM hay thuật toán dự báo.

## Kiến trúc cần tuân thủ

```text
src/app.py                         Trang chủ; Streamlit tự nhận các page
src/pages/1_overview.py            Trang tổng quan bán hàng
src/pages/2_rfm_segment.py         Trang phân khúc khách hàng RFM
src/pages/3_geo_analysis.py        Trang phân tích địa lý
src/pages/4_forecast.py            Giao diện hiển thị kết quả dự báo
src/shared/dashboard_context.py    Header, filter và context dùng chung
```

Khi chạy `streamlit run src/app.py`, các file trong `src/pages/` tự xuất hiện trong menu sidebar. Mỗi file page phải tự gọi `render_page(...)`; không chỉ khai báo hàm `render(...)`.

## Input và output

### Input

- Dữ liệu đơn hàng sạch từ `data/processed/cleaned_data.csv`, bảng RFM và kết quả dự báo theo schema đầu ra đã chuẩn hoá; dataset nguồn không nhất thiết phải giống tên cột của mock data.
- `get_filtered_data()`: dữ liệu sau filter khu vực, quốc gia, thời gian và segment.

### Output hiện có

- [x] Filter nhiều cấp: khu vực → quốc gia, thời gian và RFM segment.
- [x] Tổng quan: KPI, bar chart, line chart.
- [x] RFM: donut chart, scatter plot, box plot và bảng chi tiết.
- [x] Địa lý: choropleth map, treemap, heatmap.
- [x] Trang dự báo: biểu đồ thực tế và dự báo ba tháng; mô hình là đầu ra do phần Insight & Forecast chịu trách nhiệm.
- [x] Tối thiểu 8 biểu đồ: bar, line, donut/pie, scatter, box, choropleth, treemap và heatmap.

## Việc cần hoàn thiện

- [ ] Thêm biểu đồ loại thứ 9 để phần dự báo không lặp lại line chart (gợi ý: top 10 sản phẩm dạng horizontal bar hoặc histogram giá trị đơn hàng).
- [ ] Cân nhắc drill-down/cross-filtering nếu phù hợp tiến độ.
- [ ] Hoàn thiện UI: theme, màu sắc nhất quán, logo/tên nhóm, tooltip và trạng thái không có dữ liệu.
- [ ] Tích hợp và kiểm tra hiển thị khi nhận schema/kết quả chính thức từ hai phần còn lại.

## Quy tắc tích hợp

- Không đọc trực tiếp file trong `data/raw/` từ bất kỳ page nào.
- Chỉ đọc dữ liệu đã làm sạch qua `data_loader.py` từ `data/processed/cleaned_data.csv`; không tự quy ước schema khác trong page.
- Không viết lại công thức RFM hoặc thuật toán dự báo trong page.
- Thống nhất schema với người phụ trách Data/Insight trước khi thay đổi cách hiển thị. Khi dataset thật khác dữ liệu mẫu hoặc thiếu trường, kiểm tra/cập nhật các filter, KPI và biểu đồ bị ảnh hưởng sau khi Data cập nhật pipeline; không giả định mọi tính năng vẫn áp dụng được.
- Khi thêm biểu đồ, đảm bảo xử lý trường hợp DataFrame rỗng và dùng `use_container_width=True`.
- Mỗi thay đổi nên có commit riêng, ví dụ: `feat: add top products chart`.
