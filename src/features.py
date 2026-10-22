"""
Module: features.py
Dự án: Phân khúc khách hàng Olist E-Commerce
Nhiệm vụ: A06 (Tiền xử lý đặc trưng cho mô hình phân cụm: Log1p, Winsorize, StandardScaler, PCA)
Tuân thủ đầy đủ các khuyến nghị từ Thành viên B (Trải nghiệm) và Thành viên C (Loyalty).
"""

import sys
from typing import Dict, List, Tuple
import numpy as np
import pandas as pd
from scipy.stats import mstats
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


def winsorize_series(s: pd.Series, limits: Tuple[float, float] = (0.01, 0.01)) -> pd.Series:
    """
    Cắt tỉa ngoại lệ (Winsorization) ở phân vị 1% và 99% để loại bỏ ảnh hưởng cực đoan.
    """
    lower = s.quantile(limits[0])
    upper = s.quantile(1.0 - limits[1])
    return s.clip(lower=lower, upper=upper)


def engineer_clustering_features(
    df: pd.DataFrame
) -> Tuple[pd.DataFrame, List[str]]:
    """
    Trích xuất và biến đổi các đặc trưng phục vụ phân cụm khách hàng (A06):
    1. Lựa chọn các đặc trưng đại diện không dư thừa từ cả 3 nhóm (RFM, Vận chuyển, Trải nghiệm).
    2. Tạo đặc trưng ngưỡng phi tuyến cho giao trễ (theo phát hiện của Thành viên B).
    3. Cắt tỉa ngoại lệ (Winsorize 1% - 99%) cho các biến liên tục lệch phải.
    4. Áp dụng log1p (x -> ln(1+x)) để đưa phân phối về dạng gần chuẩn.
    """
    df_feat = df.copy()

    # 1. Tạo biến ngưỡng phi tuyến cho giao trễ (theo kết luận của B: trễ > 3 ngày điểm review rơi thẳng đứng)
    # Bỏ qua delay_days liên tục, sử dụng cờ giao trễ nghiêm trọng
    df_feat["is_severely_delayed"] = (df_feat["avg_delay_days"] > 3.0).astype(float)

    # 2. Xử lý các biến bị thiếu nếu có
    df_feat["avg_review_score"] = df_feat["avg_review_score"].fillna(df_feat["avg_review_score"].median())
    df_feat["freight_ratio"] = df_feat["freight_ratio"].fillna(df_feat["freight_ratio"].median())

    # 3. Lựa chọn danh sách đặc trưng cốt lõi (Loại bỏ các biến tương quan quá cao)
    # Loại low_review_ratio vì tương quan -0.655 với avg_review_score
    # Loại max_order_value vì tương quan > 0.9 với monetary
    selected_features = [
        # Nhóm Loyalty & RFM (C05)
        "recency",
        "frequency",
        "monetary",
        "avg_order_value",
        # Nhóm Vận chuyển & Giao hàng (B03, B05)
        "avg_delivery_duration_days",
        "delayed_order_ratio",
        "is_severely_delayed",
        "freight_ratio",
        # Nhóm Đánh giá & Hài lòng (B04)
        "avg_review_score",
        # Nhóm Thanh toán & Tín dụng (C05)
        "max_payment_installments"
    ]

    df_selected = df_feat[["customer_unique_id"] + selected_features].copy()

    # 4. Winsorization (1% - 99%) cho các biến lệch
    skewed_cols = [
        "frequency", "monetary", "avg_order_value",
        "avg_delivery_duration_days", "freight_ratio", "max_payment_installments"
    ]
    for col in skewed_cols:
        df_selected[col] = winsorize_series(df_selected[col], limits=(0.01, 0.01))

    # 5. Log1p Transformation (ln(1 + x))
    log_cols = ["frequency", "monetary", "avg_order_value", "avg_delivery_duration_days", "max_payment_installments"]
    for col in log_cols:
        df_selected[f"{col}_log"] = np.log1p(df_selected[col])

    # Danh sách các đặc trưng cuối cùng đưa vào thuật toán phân cụm
    final_feature_cols = [
        "recency",
        "frequency_log",
        "monetary_log",
        "avg_order_value_log",
        "avg_delivery_duration_days_log",
        "delayed_order_ratio",
        "is_severely_delayed",
        "freight_ratio",
        "avg_review_score",
        "max_payment_installments_log"
    ]

    return df_selected, final_feature_cols


def scale_and_pca(
    df_features: pd.DataFrame,
    feature_cols: List[str],
    n_components: int = 2
) -> Tuple[np.ndarray, np.ndarray, StandardScaler, PCA]:
    """
    Chuẩn hóa dữ liệu bằng StandardScaler và áp dụng PCA để giảm chiều dữ liệu.
    """
    X = df_features[feature_cols].values

    # Chuẩn hóa StandardScaler (mean = 0, std = 1)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # PCA giảm chiều
    pca = PCA(n_components=n_components, random_state=42)
    X_pca = pca.fit_transform(X_scaled)

    print(f"[+] Ty le phuong sai giai thich (Explained Variance Ratio): {pca.explained_variance_ratio_.round(4)}")
    print(f"[+] Tong phuong sai giu lai: {pca.explained_variance_ratio_.sum():.2%}")

    return X_scaled, X_pca, scaler, pca
