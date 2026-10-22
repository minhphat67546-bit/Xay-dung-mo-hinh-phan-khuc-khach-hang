"""
Module: models.py
Dự án: Phân khúc khách hàng Olist E-Commerce
Nhiệm vụ: A07 (Chạy K-Means, GMM, DBSCAN), A08 (Chọn số cụm k: Elbow, Silhouette, Davies-Bouldin)
Tác giả: Thành viên A (Trưởng nhóm & Kỹ sư mô hình hóa)
"""

import sys
from typing import Dict, List, Tuple
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans, DBSCAN
from sklearn.mixture import GaussianMixture
from sklearn.metrics import silhouette_score, davies_bouldin_score

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


def evaluate_kmeans_clusters(
    X_scaled: np.ndarray,
    k_range: range = range(3, 9),
    sample_size: int = 15000,
    random_state: int = 42
) -> pd.DataFrame:
    """
    Đánh giá số lượng cụm k tối ưu qua 3 chỉ số khoa học:
    1. Inertia (Elbow Method / WCSS)
    2. Silhouette Score (Độ tách biệt cụm, càng gần 1 càng tốt)
    3. Davies-Bouldin Index (Độ tương tự cụm, càng thấp càng tốt)
    """
    print("⏳ Dang tinh toan cac chi so danh gia cum k = 3 den 8...")
    results = []

    # Lấy mẫu ngẫu nhiên có đại diện để tính Silhouette nhanh chóng trên tập 93k dòng
    np.random.seed(random_state)
    sample_indices = np.random.choice(len(X_scaled), size=min(sample_size, len(X_scaled)), replace=False)
    X_sample = X_scaled[sample_indices]

    for k in k_range:
        kmeans = KMeans(n_clusters=k, random_state=random_state, n_init=10)
        labels = kmeans.fit_predict(X_scaled)

        inertia = kmeans.inertia_
        sil = silhouette_score(X_sample, labels[sample_indices])
        db = davies_bouldin_score(X_sample, labels[sample_indices])

        results.append({
            "k": k,
            "Inertia (WCSS)": round(inertia, 2),
            "Silhouette Score": round(sil, 4),
            "Davies-Bouldin Index": round(db, 4)
        })
        print(f"   [+] k = {k}: Silhouette = {sil:.4f}, Davies-Bouldin = {db:.4f}, Inertia = {inertia:,.1f}")

    df_eval = pd.DataFrame(results)
    return df_eval


def train_kmeans(
    X_scaled: np.ndarray,
    n_clusters: int = 4,
    random_state: int = 42
) -> Tuple[KMeans, np.ndarray]:
    """
    Huấn luyện mô hình K-Means với k tối ưu và trả về mô hình cùng nhãn phân cụm.
    """
    kmeans = KMeans(n_clusters=n_clusters, random_state=random_state, n_init=15)
    labels = kmeans.fit_predict(X_scaled)
    print(f"[+] Da huan luyen K-Means voi {n_clusters} cum.")
    return kmeans, labels


def train_gmm(
    X_scaled: np.ndarray,
    n_components: int = 4,
    random_state: int = 42
) -> Tuple[GaussianMixture, np.ndarray]:
    """
    Huấn luyện mô hình phân cụm xác suất Gaussian Mixture Model (GMM).
    """
    gmm = GaussianMixture(n_components=n_components, covariance_type="full", random_state=random_state)
    labels = gmm.fit_predict(X_scaled)
    print(f"[+] Da huan luyen GMM voi {n_components} thanh phan. BIC = {gmm.bic(X_scaled):,.2f}")
    return gmm, labels


def train_dbscan(
    X_scaled: np.ndarray,
    eps: float = 1.8,
    min_samples: int = 15
) -> Tuple[DBSCAN, np.ndarray]:
    """
    Huấn luyện mô hình phân cụm dựa trên mật độ DBSCAN để phát hiện ngoại lai.
    """
    dbscan = DBSCAN(eps=eps, min_samples=min_samples, n_jobs=-1)
    labels = dbscan.fit_predict(X_scaled)
    n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
    n_noise = (labels == -1).sum()
    print(f"[+] DBSCAN: Phat hien {n_clusters} cum va {n_noise:,} diem ngoai lai ({n_noise/len(labels):.2%}).")
    return dbscan, labels


def build_cluster_profiles(
    df_customers: pd.DataFrame,
    cluster_labels: np.ndarray
) -> pd.DataFrame:
    """
    Tổng hợp hồ sơ đặc trưng trung bình theo từng cụm để diễn giải ý nghĩa kinh doanh.
    """
    df_res = df_customers.copy()
    df_res["cluster"] = cluster_labels

    key_profile_cols = [
        "recency", "frequency", "monetary", "avg_order_value",
        "avg_delivery_duration_days", "delayed_order_ratio",
        "avg_review_score", "freight_ratio", "max_payment_installments"
    ]

    profile_df = df_res.groupby("cluster")[key_profile_cols].agg("mean").round(2)
    profile_df["customer_count"] = df_res.groupby("cluster")["customer_unique_id"].count()
    profile_df["customer_pct"] = (profile_df["customer_count"] / len(df_res) * 100).round(2)

    return profile_df
