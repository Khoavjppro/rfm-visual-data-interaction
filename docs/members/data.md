# Phân công Data Pipeline

**Phụ trách:**   
**Mục tiêu:** thu thập, kiểm tra và làm sạch dữ liệu bán hàng để tạo một nguồn dữ liệu đáng tin cậy cho toàn bộ dashboard và phân tích RFM.

## Phạm vi sở hữu

```text
data/raw/                         Dữ liệu nguồn; không đưa dữ liệu thật nhạy cảm lên Git
data/processed/                   Nơi lưu dữ liệu do pipeline sinh ra; dashboard chỉ đọc từ đây
data/processed/cleaned_data.csv   Dữ liệu sạch bàn giao cho Dashboard và Insight & Forecast
scripts/generate_mock_data.py     Sinh dữ liệu giả phục vụ phát triển UI
scripts/clean_data.py             Điểm chạy pipeline raw → clean
src/shared/data_cleaning.py       Quy tắc làm sạch và chuẩn hoá schema
src/shared/data_loader.py         Hợp đồng đọc dữ liệu đã làm sạch
```

Không sửa trực tiếp các file trong `src/pages/`; phần đó do Dashboard phụ trách. Khi schema thay đổi, thông báo nhóm trước khi sửa `data_loader.py`.

## Phạm vi làm việc và luồng bàn giao

Data phụ trách từ file CSV nguồn trong `data/raw/` đến file chuẩn hoá trong `data/processed/`. Dashboard, RFM và Forecast chỉ nhận dữ liệu qua `src/shared/data_loader.py`; không đọc raw và không tự làm sạch lại dữ liệu.

```text
data/raw/*.csv
	↓ scripts/clean_data.py
data/processed/cleaned_data.csv
	↓ src/shared/data_loader.py
Dashboard / RFM / Forecast
```

`data/processed/cleaned_data.csv` là output có thể tái tạo, không chỉnh tay. Sau khi đổi dataset, phải chạy lại pipeline và kiểm tra các phần sử dụng schema trước khi bàn giao.

## Phần nền tảng đã có

- [x] Mock data (mẫu để test) 5.000 đơn hàng, 400 khách hàng và nhiều quốc gia/khu vực.
- [x] Script `generate_mock_data.py` tạo file `data/raw/mock_orders.csv`.
- [x] Pipeline `clean_data.py` đọc file raw và tạo `data/processed/cleaned_data.csv`.
- [x] Làm sạch cơ bản: chuẩn hoá tên cột, ép kiểu ngày/số, loại missing value, duplicate và Quantity không hợp lệ.
- [x] Hỗ trợ alias phổ biến, ví dụ `Market` → `Region`, `Revenue` → `Sales`.

## Việc cần hoàn thiện

- [ ] Thu thập/chọn dataset (thật) đáp ứng tối thiểu 5.000 dòng và có nguồn trích dẫn rõ ràng.
- [ ] Lập data dictionary: tên cột, ý nghĩa, kiểu dữ liệu, đơn vị và quy tắc tính.
- [ ] Kiểm tra chất lượng dữ liệu: missing values, duplicate, ngày bất thường, Sales/Quantity/Profit bất thường.
- [ ] Xác định và ghi lại quy tắc xử lý outlier; không tự ý xoá outlier nếu chưa có lý do nghiệp vụ.
- [ ] Thực hiện EDA bằng Matplotlib/Seaborn, lưu biểu đồ/kết luận để dùng trong báo cáo đồ án.
- [ ] Cập nhật `COLUMN_ALIASES` hoặc pipeline nếu schema dataset thật khác mock data.
- [ ] Chạy lại pipeline và xác nhận dashboard/RFM đọc được dữ liệu thật.

## Hợp đồng bàn giao

Hợp đồng cần phân biệt dữ liệu nguồn và dữ liệu sau làm sạch. Người tìm dữ liệu không bắt buộc phải tìm dataset có đúng tên cột, thứ tự cột hoặc đúng định dạng như dữ liệu mẫu. Dataset nguồn chỉ cần có thông tin tương đương và có thể ánh xạ được về schema chuẩn.

### Schema đầu ra bắt buộc

File `data/processed/cleaned_data.csv` hiện cần có các cột:

```text
Order ID, Order Date, Customer ID, Country, Region,
Category, Sub-Category, Sales, Quantity, Profit
```

Quy ước dữ liệu:

- `Order Date` phải parse được thành ngày.
- `Sales`, `Quantity`, `Profit` là số; Profit được phép âm.
- `Sales >= 0`, `Quantity > 0`.
- Một `Order ID` có thể có nhiều dòng sản phẩm, vì vậy không được xoá trùng chỉ dựa trên `Order ID`.

Đây là schema đầu ra, không phải yêu cầu dataset nguồn phải giống hệt dữ liệu mẫu. Schema này là hợp đồng tích hợp vì `data_cleaning.py`, `data_loader.py`, RFM, filter chung và các biểu đồ hiện đang phụ thuộc vào nó.

### Cách xử lý dataset khác mẫu

- Khác tên cột nhưng cùng ý nghĩa: bổ sung ánh xạ trong `COLUMN_ALIASES` hoặc cấu hình tương đương.
- Khác kiểu dữ liệu hoặc đơn vị: cập nhật bước chuẩn hoá, ghi rõ quy tắc chuyển đổi và kiểm tra lại chất lượng dữ liệu.
- Thiếu trường có thể suy dẫn một cách đáng tin cậy: chỉ tạo trong pipeline khi có quy tắc nghiệp vụ rõ ràng; không tự điền giá trị giả.
- Thiếu trường không thể suy dẫn: phải thống nhất giảm hoặc thay đổi tính năng phụ thuộc vào trường đó, rồi cập nhật `REQUIRED_COLUMNS`, pipeline, loader, RFM/forecast và các page liên quan.

Sau mọi thay đổi schema, người phụ trách Data phải thông báo Dashboard và Insight & Forecast, chạy lại pipeline, kiểm tra các hàm/biểu đồ liên quan và cập nhật tài liệu trước khi bàn giao.

Không nên bỏ qua kiểm tra schema để "cho chạy được": thiếu hoặc đổi nghĩa một cột có thể làm sai RFM, bộ lọc, KPI, bản đồ và dự báo.

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
