"""
Module: data_pipeline.py
Dự án: Phân khúc khách hàng Olist E-Commerce
Nhiệm vụ: A03, A04, A05 (Hợp nhất dữ liệu, Tiền xử lý làm sạch, Gộp về cấp khách hàng customer_unique_id)
Tác giả: Thành viên A (Trưởng nhóm & Kỹ sư dữ liệu)
"""

import sys
from pathlib import Path
from typing import Dict, Optional
import numpy as np
import pandas as pd

# Đảm bảo in tiếng Việt mượt mà trên console Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


def load_raw_data(data_dir: str = "data/raw") -> Dict[str, pd.DataFrame]:
    """
    Nạp 7 bảng dữ liệu Olist cần thiết cho pipeline từ thư mục data_dir.
    """
    path = Path(data_dir)
    print("[1/6] Dang nap cac bang du lieu goc...")
    datasets = {
        "orders": pd.read_csv(path / "olist_orders_dataset.csv"),
        "customers": pd.read_csv(path / "olist_customers_dataset.csv"),
        "items": pd.read_csv(path / "olist_order_items_dataset.csv"),
        "payments": pd.read_csv(path / "olist_order_payments_dataset.csv"),
        "reviews": pd.read_csv(path / "olist_order_reviews_dataset.csv"),
        "products": pd.read_csv(path / "olist_products_dataset.csv"),
        "translation": pd.read_csv(path / "product_category_name_translation.csv"),
    }
    print(f"[+] Da nap thanh cong {len(datasets)} bang du lieu.")
    return datasets


def clean_orders_and_items(
    df_orders: pd.DataFrame,
    df_customers: pd.DataFrame,
    df_items: pd.DataFrame,
    df_products: pd.DataFrame,
    df_translation: pd.DataFrame,
    df_payments: pd.DataFrame,
    df_reviews: pd.DataFrame
) -> pd.DataFrame:
    """
    Hợp nhất và làm sạch ở cấp đơn hàng (A03, A04):
    1. Lọc đơn 'delivered' có ngày nhận hàng hợp lệ.
    2. Chuyển đổi datetime và tính toán thời gian giao hàng, độ trễ.
    3. Tổng hợp thông tin từ items, products, payments, reviews lên cấp order_id để tránh trùng lặp dòng.
    """
    print("[2/6] Loc don hang hop le & chuyen doi thoi gian...")
    # Lọc chỉ lấy đơn hàng giao thành công và có ngày giao thực tế
    mask_delivered = (df_orders["order_status"] == "delivered") & (df_orders["order_delivered_customer_date"].notnull())
    orders_clean = df_orders[mask_delivered].copy()

    # Chuyển đổi định dạng thời gian
    time_cols = [
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date"
    ]
    for col in time_cols:
        orders_clean[col] = pd.to_datetime(orders_clean[col], errors="coerce")

    # Loại bỏ các đơn bất thường: ngày giao hàng trước ngày mua hàng
    valid_time_mask = orders_clean["order_delivered_customer_date"] >= orders_clean["order_purchase_timestamp"]
    orders_clean = orders_clean[valid_time_mask]

    # Tính thời gian giao hàng thực tế (ngày) và số ngày chênh lệch so với ngày dự kiến
    orders_clean["delivery_duration_days"] = (
        orders_clean["order_delivered_customer_date"] - orders_clean["order_purchase_timestamp"]
    ).dt.total_seconds() / (24 * 3600)

    orders_clean["delay_days"] = (
        orders_clean["order_delivered_customer_date"] - orders_clean["order_estimated_delivery_date"]
    ).dt.total_seconds() / (24 * 3600)

    orders_clean["is_delayed"] = (orders_clean["delay_days"] > 0).astype(int)

    print("[3/6] Tong hop du lieu mat hang (order_items) & san pham...")
    products_trans = df_products.merge(df_translation, on="product_category_name", how="left")
    products_trans["category_clean"] = products_trans["product_category_name_english"].fillna(
        products_trans["product_category_name"]
    ).fillna("other")

    items_with_prod = df_items.merge(
        products_trans[["product_id", "category_clean"]],
        on="product_id",
        how="left"
    )

    # Gom nhóm theo order_id
    items_agg = items_with_prod.groupby("order_id").agg(
        order_item_count=("order_item_id", "count"),
        total_items_price=("price", "sum"),
        total_freight_value=("freight_value", "sum"),
        unique_categories_in_order=("category_clean", "nunique"),
        main_order_category=("category_clean", lambda x: x.mode()[0] if not x.empty else "other")
    ).reset_index()

    print("[4/6] Tong hop du lieu thanh toan & danh gia...")
    # Thanh toán
    payments_agg = df_payments.groupby("order_id").agg(
        total_payment_value=("payment_value", "sum"),
        max_installments=("payment_installments", "max"),
        primary_payment_type=("payment_type", lambda x: x.mode()[0] if not x.empty else "unknown"),
        voucher_used=("payment_type", lambda x: int((x == "voucher").any())),
        voucher_count=("payment_type", lambda x: int((x == "voucher").sum()))
    ).reset_index()

    # Đánh giá
    reviews_agg = df_reviews.groupby("order_id").agg(
        review_score=("review_score", "mean"),
        has_review_comment=("review_comment_message", lambda x: int(x.notnull().any()))
    ).reset_index()

    print("[5/6] Ghep noi (Join) tat ca ve cap don hang...")
    # Join orders với customers để lấy customer_unique_id
    df_merged = orders_clean.merge(
        df_customers[["customer_id", "customer_unique_id", "customer_city", "customer_state"]],
        on="customer_id",
        how="inner"
    )

    # Join với các bảng con đã tổng hợp
    df_merged = df_merged.merge(items_agg, on="order_id", how="inner")
    df_merged = df_merged.merge(payments_agg, on="order_id", how="left")
    df_merged = df_merged.merge(reviews_agg, on="order_id", how="left")

    # Điền giá trị mặc định cho review nếu thiếu (dùng 5.0)
    df_merged["review_score"] = df_merged["review_score"].fillna(5.0)
    df_merged["has_review_comment"] = df_merged["has_review_comment"].fillna(0)

    # Điền giá trị thanh toán nếu thiếu
    df_merged["total_payment_value"] = df_merged["total_payment_value"].fillna(
        df_merged["total_items_price"] + df_merged["total_freight_value"]
    )
    df_merged["max_installments"] = df_merged["max_installments"].fillna(1)
    df_merged["primary_payment_type"] = df_merged["primary_payment_type"].fillna("credit_card")
    df_merged["voucher_used"] = df_merged["voucher_used"].fillna(0)
    df_merged["voucher_count"] = df_merged["voucher_count"].fillna(0)

    print(f"[+] Hoan tat hop nhat cap don hang: {len(df_merged):,} don hop le.")
    return df_merged


def aggregate_to_customer_level(
    df_orders_merged: pd.DataFrame,
    snapshot_date: Optional[pd.Timestamp] = None
) -> pd.DataFrame:
    """
    Gộp về cấp khách hàng customer_unique_id (A05) sử dụng phương pháp tối ưu hóa hiệu năng cao.
    Trích xuất đầy đủ 26+ đặc trưng đa chiều (RFM, vận chuyển, trải nghiệm, thanh toán).
    """
    print("[6/6] Nhom theo customer_unique_id va trich xuat dac trung...")

    if snapshot_date is None:
        snapshot_date = df_orders_merged["order_purchase_timestamp"].max() + pd.Timedelta(days=1)
        print(f"    Ngay moc Recency: {snapshot_date.strftime('%Y-%m-%d')}")

    # Tạo các cột phụ ở cấp đơn trước khi gộp để tính toán cực nhanh
    df = df_orders_merged.copy()
    df["order_total_value"] = df["total_items_price"] + df["total_freight_value"]
    df["is_low_review"] = (df["review_score"] <= 2).astype(int)

    # Vectorized Aggregation
    agg_dict = {
        "customer_state": "first",
        "customer_city": "first",
        "order_purchase_timestamp": ["min", "max"],
        "order_id": "nunique",
        "order_total_value": ["sum", "max"],
        "order_item_count": ["sum", "mean"],
        "total_freight_value": ["sum", "mean"],
        "delivery_duration_days": "mean",
        "delay_days": "mean",
        "is_delayed": ["sum", "mean"],
        "review_score": "mean",
        "is_low_review": "mean",
        "has_review_comment": "mean",
        "primary_payment_type": lambda x: x.mode()[0] if not x.empty else "credit_card",
        "max_installments": ["max", "mean"],
        "voucher_used": "sum",
        "unique_categories_in_order": "sum",
        "main_order_category": lambda x: x.mode()[0] if not x.empty else "other"
    }

    grouped = df.groupby("customer_unique_id").agg(agg_dict)

    # Đặt lại tên cột phẳng, chuẩn mực
    grouped.columns = [
        "customer_state",
        "customer_city",
        "first_purchase_date",
        "last_purchase_date",
        "frequency",
        "monetary",
        "max_order_value",
        "total_items",
        "avg_items_per_order",
        "total_freight",
        "avg_freight_value",
        "avg_delivery_duration_days",
        "avg_delay_days",
        "delayed_order_count",
        "delayed_order_ratio",
        "avg_review_score",
        "low_review_ratio",
        "has_comment_ratio",
        "primary_payment_type",
        "max_payment_installments",
        "avg_payment_installments",
        "voucher_used_count",
        "unique_categories_count",
        "favorite_category"
    ]

    customer_df = grouped.reset_index()

    # Tính toán các cột dẫn xuất
    customer_df["recency"] = (snapshot_date - customer_df["last_purchase_date"]).dt.days
    customer_df["avg_order_value"] = customer_df["monetary"] / customer_df["frequency"]
    customer_df["freight_ratio"] = np.where(
        customer_df["monetary"] > 0,
        customer_df["total_freight"] / customer_df["monetary"],
        0.0
    )
    customer_df["voucher_payment_ratio"] = customer_df["voucher_used_count"] / customer_df["frequency"]

    # Sắp xếp thứ tự cột logic và trực quan
    cols_order = [
        "customer_unique_id",
        "customer_state",
        "customer_city",
        "first_purchase_date",
        "last_purchase_date",
        # RFM & Loyalty (C05)
        "recency",
        "frequency",
        "monetary",
        "avg_order_value",
        "max_order_value",
        "total_items",
        "avg_items_per_order",
        # Vận chuyển & Giao hàng (B03, B05)
        "total_freight",
        "avg_freight_value",
        "freight_ratio",
        "avg_delivery_duration_days",
        "avg_delay_days",
        "delayed_order_count",
        "delayed_order_ratio",
        # Đánh giá & Trải nghiệm (B04)
        "avg_review_score",
        "low_review_ratio",
        "has_comment_ratio",
        # Thanh toán & Danh mục (C05)
        "primary_payment_type",
        "max_payment_installments",
        "avg_payment_installments",
        "voucher_used_count",
        "voucher_payment_ratio",
        "unique_categories_count",
        "favorite_category"
    ]
    customer_df = customer_df[cols_order]

    # Làm tròn
    round_dict = {
        "monetary": 2,
        "avg_order_value": 2,
        "max_order_value": 2,
        "total_freight": 2,
        "avg_freight_value": 2,
        "freight_ratio": 4,
        "avg_delivery_duration_days": 2,
        "avg_delay_days": 2,
        "delayed_order_ratio": 4,
        "avg_review_score": 2,
        "low_review_ratio": 4,
        "has_comment_ratio": 4,
        "avg_items_per_order": 2,
        "avg_payment_installments": 2,
        "voucher_payment_ratio": 4
    }
    customer_df = customer_df.round(round_dict)

    print(f"[+] Hoan tat gop ve cap khach hang! Tong so khach duy nhat: {len(customer_df):,}")
    return customer_df


def run_pipeline(
    raw_dir: str = "data/raw",
    output_parquet: str = "data/processed/olist_clean.parquet"
) -> pd.DataFrame:
    """
    Hàm chạy trọn vẹn pipeline dữ liệu Olist.
    """
    datasets = load_raw_data(raw_dir)
    df_orders_merged = clean_orders_and_items(
        df_orders=datasets["orders"],
        df_customers=datasets["customers"],
        df_items=datasets["items"],
        df_products=datasets["products"],
        df_translation=datasets["translation"],
        df_payments=datasets["payments"],
        df_reviews=datasets["reviews"]
    )

    df_customers_clean = aggregate_to_customer_level(df_orders_merged)

    out_path = Path(output_parquet)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    df_customers_clean.to_parquet(out_path, index=False)
    print(f"[+] Da xuat file Parquet thanh cong tai: {out_path.resolve()}")
    return df_customers_clean


if __name__ == "__main__":
    run_pipeline()
