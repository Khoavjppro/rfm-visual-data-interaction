"""Tạo data/processed/cleaned_data.csv từ một file CSV trong data/raw/."""

import argparse
from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.shared.data_cleaning import clean_orders


CLEAN_DATA_PATH = ROOT_DIR / "data" / "processed" / "cleaned_data.csv"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Làm sạch dữ liệu đơn hàng cho dashboard.")
    parser.add_argument(
        "raw_file",
        nargs="?",
        default="data/raw/mock_orders.csv",
        help="Đường dẫn CSV raw, tính từ thư mục gốc dự án.",
    )
    args = parser.parse_args()

    raw_path = Path(args.raw_file)
    if not raw_path.is_absolute():
        raw_path = ROOT_DIR / raw_path

    cleaned = clean_orders(raw_path, CLEAN_DATA_PATH)
    print(f"Da lam sach {len(cleaned):,} dong -> {CLEAN_DATA_PATH}")
