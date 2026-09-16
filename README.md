# Phân tích hiệu suất bán hàng và phân khúc khách hàng (RFM)

Đồ án **Tương tác dữ liệu trực quan** trong lĩnh vực bán lẻ. Dự án xây dựng dashboard tương tác để theo dõi hiệu suất bán hàng của hệ thống siêu thị đa quốc gia, phân tích hành vi khách hàng theo mô hình RFM và minh hoạ xu hướng doanh thu.

## Mục tiêu

- Theo dõi doanh thu, lợi nhuận và số đơn hàng theo thời gian, danh mục và khu vực.
- Phân tích phân bố doanh thu theo địa lý bằng bản đồ tương tác.
- Phân khúc khách hàng bằng **RFM**: Recency, Frequency và Monetary.
- Hỗ trợ nhận diện nhóm khách hàng giá trị cao, khách hàng mới và nhóm có nguy cơ rời bỏ.
- Dự báo doanh thu ngắn hạn bằng mô hình Linear Regression (phiên bản demo).

## Công nghệ sử dụng

- Python 3.12+ và Streamlit
- Pandas, NumPy: xử lý dữ liệu
- Plotly: biểu đồ và bản đồ tương tác
- Scikit-learn: mô hình dự báo

## Cấu trúc dự án

```text
rfm-visual-data-interaction/
├── data/
│   ├── raw/                 # Dữ liệu đầu vào (mock data hoặc dữ liệu thật)
│   └── processed/
│       └── cleaned_data.csv # Dữ liệu chuẩn hoá duy nhất dashboard sử dụng
├── docs/
│   └── members/             # Hướng dẫn/phân công theo thành viên
├── scripts/
│   ├── generate_mock_data.py
│   └── clean_data.py
├── src/
│   ├── app.py               # Trang chủ Streamlit
│   ├── pages/               # Các trang dashboard tự động xuất hiện ở sidebar
│   └── shared/              # Loader, làm sạch dữ liệu, RFM và filter dùng chung
├── requirements.txt
└── README.md
```

## Luồng dữ liệu

```text
data/raw/*.csv → scripts/clean_data.py → data/processed/cleaned_data.csv → Streamlit dashboard
```

Dashboard chỉ đọc `data/processed/cleaned_data.csv`, không đọc trực tiếp `data/raw/`. Khi thay dữ liệu thật và schema vẫn đúng hợp đồng dữ liệu, chỉ cần chạy lại pipeline. Nếu schema khác dữ liệu mẫu, cần cập nhật pipeline/các phần liên quan trước khi làm mới dashboard.

`data/processed/` là thư mục output trung gian và là nguồn dữ liệu duy nhất được bàn giao cho Dashboard, RFM và Forecast. Không sửa trực tiếp `cleaned_data.csv`; mọi thay đổi phải bắt đầu từ file trong `data/raw/` và được tạo lại bằng pipeline.

## Cài đặt và chạy dự án

Cài đặt môi trường ảo của Pyhton cho dự án:
Thực hiện tại thư mục gốc của dự án (chạy 1 lần).

```cmd 
py -3.12 -m venv .venv
.venv\Scripts\activate.bat
python -m pip install -r requirements.txt
```
(khi có dataset thật sẽ update sau)
Tạo dữ liệu giả lập gồm tối thiểu 5.000 đơn hàng, làm sạch dữ liệu và chạy dashboard:

```cmd
python scripts\generate_mock_data.py
python scripts\clean_data.py
python -m streamlit run src\app.py
```

Mở địa chỉ Local URL mà Streamlit hiển thị, thường là `http://localhost:8501`.

## Sử dụng dữ liệu

1. Đặt file CSV nguồn vào thư mục `data/raw/`.
2. Chạy lệnh để làm sạch dữ liệu, ví dụ:

```cmd
python scripts\clean_data.py data/raw/superstore_real.csv
```

3. Làm mới dashboard. File `data/processed/cleaned_data.csv` sẽ được cập nhật và là nguồn duy nhất dashboard sử dụng.

Dataset nguồn không bắt buộc phải có đúng tên hoặc đúng thứ tự các cột của dữ liệu mẫu. Pipeline cần ánh xạ được các trường tương đương về schema đầu ra: `Order ID`, `Order Date`, `Customer ID`, `Country`, `Region`, `Category`, `Sub-Category`, `Sales`, `Quantity`, `Profit`. Đây là schema mà các hàm làm sạch, RFM, bộ lọc và biểu đồ hiện đang sử dụng sau khi chuẩn hoá. Nếu dataset thật thiếu trường, khác kiểu dữ liệu hoặc thay đổi ý nghĩa, hãy cập nhật `COLUMN_ALIASES`/pipeline và kiểm tra các phần liên quan; không tự tạo giá trị giả để giữ dashboard chạy.

## Các trang dashboard

- **Tổng quan:** KPI doanh thu/lợi nhuận/đơn hàng, doanh thu theo danh mục và xu hướng theo tháng.
- **Phân khúc RFM:** tỷ trọng segment, Frequency–Monetary scatter plot, box plot và bảng chi tiết khách hàng.
- **Phân tích địa lý:** choropleth map, treemap và heatmap.
- **Dự báo:** doanh thu thực tế và dự báo ba tháng tiếp theo bằng Linear Regression.

Tất cả trang dùng chung bộ lọc khu vực, quốc gia, thời gian và phân khúc RFM.

## Quy ước làm việc nhóm

- Không commit thư mục `.venv/`, cache Python hoặc file dữ liệu nhạy cảm/lớn.
- Không tính lại RFM trong `src/pages/`; sử dụng hàm trong `src/shared/rfm_utils.py`.
- Mỗi thay đổi chức năng nên được thực hiện có commit riêng, có mô tả rõ ràng.
- Cập nhật tài liệu nhiệm vụ tương ứng trong `docs/members/` khi mở rộng dashboard.

## Thành viên

- Phạm Đức Khoa
- Phạm Quốc Duy
- Nguyễn Văn Xuân An

> Thông tin phân công chi tiết được cập nhật trong thư mục `docs/members/`.
