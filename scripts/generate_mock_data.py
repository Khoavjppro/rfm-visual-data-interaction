"""
Sinh dữ liệu GIẢ LẬP mô phỏng cấu trúc dataset Global Superstore.
Mục đích: có data để dựng khung Dashboard ngay, KHÔNG cần đợi bước
làm sạch dữ liệu thật xong. Sau này chỉ cần thay file này bằng dữ
liệu thật đã làm sạch (xem src/shared/data_loader.py).

Chạy: python scripts/generate_mock_data.py
Output: data/raw/mock_orders.csv
"""

import numpy as np
import pandas as pd
from pathlib import Path

np.random.seed(42)

N_ORDERS = 3000
N_CUSTOMERS = 400

COUNTRIES = {
    "Vietnam": "APAC", "Singapore": "APAC", "Japan": "APAC", "India": "APAC",
    "United States": "North America", "Canada": "North America",
    "Germany": "Europe", "France": "Europe", "United Kingdom": "Europe",
    "Brazil": "LATAM", "Mexico": "LATAM",
    "South Africa": "Africa", "Nigeria": "Africa",
}
COUNTRY_LIST = list(COUNTRIES.keys())

CATEGORIES = {
    "Electronics": ["Phone", "Laptop", "Headphone", "Camera"],
    "Home & Furniture": ["Chair", "Table", "Lamp", "Storage"],
    "Groceries": ["Snacks", "Beverage", "Fresh Produce", "Dairy"],
    "Fashion": ["Shirt", "Shoes", "Bag", "Accessories"],
}

# Toạ độ trung tâm gần đúng của mỗi quốc gia (để vẽ bản đồ)
COUNTRY_COORDS = {
    "Vietnam": (14.06, 108.28), "Singapore": (1.35, 103.82),
    "Japan": (36.20, 138.25), "India": (20.59, 78.96),
    "United States": (37.09, -95.71), "Canada": (56.13, -106.35),
    "Germany": (51.17, 10.45), "France": (46.23, 2.21),
    "United Kingdom": (55.38, -3.44), "Brazil": (-14.24, -51.93),
    "Mexico": (23.63, -102.55), "South Africa": (-30.56, 22.94),
    "Nigeria": (9.08, 8.68),
}

def generate():
    customer_ids = [f"CUS-{i:04d}" for i in range(1, N_CUSTOMERS + 1)]
    customer_country = {cid: np.random.choice(COUNTRY_LIST) for cid in customer_ids}

    rows = []
    start_date = pd.Timestamp("2023-01-01")
    end_date = pd.Timestamp("2025-12-31")
    date_range_days = (end_date - start_date).days

    for i in range(1, N_ORDERS + 1):
        cust = np.random.choice(customer_ids)
        country = customer_country[cust]
        region = COUNTRIES[country]
        category = np.random.choice(list(CATEGORIES.keys()))
        sub_category = np.random.choice(CATEGORIES[category])

        # khách "trung thành" có xu hướng đơn gần đây + nhiều đơn hơn (patterns giả cho demo)
        loyalty_bias = np.random.beta(2, 5)
        days_offset = int(np.random.uniform(0, date_range_days) * (1 - loyalty_bias * 0.6))
        order_date = start_date + pd.Timedelta(days=days_offset)

        base_price = {"Electronics": 400, "Home & Furniture": 150,
                      "Groceries": 15, "Fashion": 60}[category]
        sales = round(max(5, np.random.normal(base_price, base_price * 0.4)), 2)
        quantity = np.random.randint(1, 6)
        profit_margin = np.random.uniform(-0.1, 0.35)
        profit = round(sales * quantity * profit_margin, 2)

        rows.append({
            "Order ID": f"ORD-{i:05d}",
            "Order Date": order_date,
            "Customer ID": cust,
            "Country": country,
            "Region": region,
            "Category": category,
            "Sub-Category": sub_category,
            "Sales": round(sales * quantity, 2),
            "Quantity": quantity,
            "Profit": profit,
        })

    df = pd.DataFrame(rows)

    # gắn toạ độ quốc gia (phục vụ vẽ map)
    df["lat"] = df["Country"].map(lambda c: COUNTRY_COORDS[c][0])
    df["lon"] = df["Country"].map(lambda c: COUNTRY_COORDS[c][1])

    return df


if __name__ == "__main__":
    df = generate()
    out_path = Path(__file__).resolve().parents[1] / "data" / "raw" / "mock_orders.csv"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_path, index=False)
    print(f"Đã sinh {len(df)} dòng dữ liệu giả lập -> {out_path}")
