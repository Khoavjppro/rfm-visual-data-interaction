# Phân công Data Pipeline

**Phụ trách:**   
**Mục tiêu:** thu thập, kiểm tra và làm sạch dữ liệu bán hàng để tạo một nguồn dữ liệu đáng tin cậy cho toàn bộ dashboard và phân tích RFM.

## Phạm vi sở hữu

```text
data/raw/                         Dữ liệu nguồn; không đưa dữ liệu thật nhạy cảm lên Git
data/cleaned_data.csv             Dữ liệu sạch bàn giao cho nhóm
scripts/generate_mock_data.py     Sinh dữ liệu giả phục vụ phát triển UI
scripts/clean_data.py             Điểm chạy pipeline raw → clean
src/shared/data_cleaning.py       Quy tắc làm sạch và chuẩn hoá schema
src/shared/data_loader.py         Hợp đồng đọc dữ liệu đã làm sạch
```

Không sửa trực tiếp các file trong `src/pages/`; phần đó do Dashboard phụ trách. Khi schema thay đổi, thông báo nhóm trước khi sửa `data_loader.py`.

## Phần nền tảng đã có

- [x] Mock data 5.000 đơn hàng, 400 khách hàng và nhiều quốc gia/khu vực.
- [x] Script `generate_mock_data.py` tạo file `data/raw/mock_orders.csv`.
- [x] Pipeline `clean_data.py` đọc file raw và tạo `data/cleaned_data.csv`.
- [x] Làm sạch cơ bản: chuẩn hoá tên cột, ép kiểu ngày/số, loại missing value, duplicate và Quantity không hợp lệ.
- [x] Hỗ trợ alias phổ biến, ví dụ `Market` → `Region`, `Revenue` → `Sales`.

## Việc cần hoàn thiện

- [ ] Thu thập/chọn dataset thật đáp ứng tối thiểu 5.000 dòng và có nguồn trích dẫn rõ ràng.
- [ ] Lập data dictionary: tên cột, ý nghĩa, kiểu dữ liệu, đơn vị và quy tắc tính.
- [ ] Kiểm tra chất lượng dữ liệu: missing values, duplicate, ngày bất thường, Sales/Quantity/Profit bất thường.
- [ ] Xác định và ghi lại quy tắc xử lý outlier; không tự ý xoá outlier nếu chưa có lý do nghiệp vụ.
- [ ] Thực hiện EDA bằng Matplotlib/Seaborn, lưu biểu đồ/kết luận để dùng trong báo cáo đồ án.
- [ ] Cập nhật `COLUMN_ALIASES` hoặc pipeline nếu schema dataset thật khác mock data.
- [ ] Chạy lại pipeline và xác nhận dashboard/RFM đọc được dữ liệu thật.

## Hợp đồng bàn giao

File `data/cleaned_data.csv` cần có các cột bắt buộc:

```text
Order ID, Order Date, Customer ID, Country, Region,
Category, Sub-Category, Sales, Quantity, Profit
```

Quy ước dữ liệu:

- `Order Date` phải parse được thành ngày.
- `Sales`, `Quantity`, `Profit` là số; Profit được phép âm.
- `Sales >= 0`, `Quantity > 0`.
- Một `Order ID` có thể có nhiều dòng sản phẩm, vì vậy không được xoá trùng chỉ dựa trên `Order ID`.

## Lệnh sử dụng

```cmd
python scripts\generate_mock_data.py
python scripts\clean_data.py
python scripts\clean_data.py data/raw/ten_file_that.csv
```

## Tiêu chí hoàn thành

- Có dữ liệu sạch, tái tạo được bằng script và đủ điều kiện đầu vào cho dashboard.
- Có data dictionary và báo cáo chất lượng/EDA.
- Bàn giao schema ổn định cho Dashboard và Insight & Forecast.
