# Dự án Khai thác Dữ liệu & Phân cụm Khách hàng Olist (E-Commerce)

Dự án phân tích hành vi khách hàng, xây dựng đặc trưng RFM & trải nghiệm (phí vận chuyển, giao hàng, đánh giá), và phân cụm khách hàng thương mại điện tử Olist Brazil.

---

## 1. Cấu trúc thư mục dự án

```text
ktdl/
├── .gitignore                     # Cấu hình bỏ qua file lớn, cache, venv
├── README.md                      # Tài liệu hướng dẫn dự án & quy ước chung
├── requirements.txt               # Danh sách thư viện Python cần thiết
├── Phan_cong_nhiem_vu_Olist.xlsx  # Kế hoạch & phân công nhiệm vụ nhóm
│
├── data/                          # Dữ liệu (KHÔNG commit lên Git)
│   ├── raw/                       # File CSV gốc (Olist dataset)
│   └── processed/                 # Dữ liệu đã làm sạch, feature store (file .parquet)
│
├── notebooks/                     # Jupyter Notebooks phân tích, EDA, thử nghiệm
│   ├── 01_eda_olist_overview.ipynb
│   ├── 02_eda_reviews_delivery.ipynb
│   ├── 03_feature_engineering_rfm.ipynb
│   └── 04_customer_clustering.ipynb
│
├── src/                           # Mã nguồn Python tái sử dụng (Modules)
│   ├── __init__.py
│   ├── data_loader.py             # Hàm nạp và kiểm tra dữ liệu
│   ├── preprocessing.py          # Tiền xử lý, xử lý thiếu & ngoại lệ
│   ├── features.py               # Tạo đặc trưng (RFM, freight_ratio, review NLP)
│   ├── models.py                 # Thuật toán phân cụm (K-Means, DBSCAN...)
│   └── utils.py                  # Hàm tiện ích trực quan hóa, vẽ đồ thị
│
└── reports/                       # Báo cáo, slide thuyết trình & biểu đồ xuất ra
    ├── figures/                   # Biểu đồ phân tích (PNG/PDF)
    └── final_report.pdf           # Báo cáo tổng kết
```

---

## 2. Hướng dẫn thiết lập môi trường ảo (Virtual Environment)

Mỗi thành viên khi tải code về máy cần tạo môi trường ảo riêng biệt để tránh xung đột thư viện:

### Bước 1: Mở terminal tại thư mục dự án và tạo môi trường ảo
```bash
# Windows (dùng Python Launcher hoặc python)
py -m venv .venv
# hoặc: python -m venv .venv
```

### Bước 2: Kích hoạt môi trường ảo
```powershell
# PowerShell trên Windows:
.venv\Scripts\Activate.ps1

# Nếu gặp lỗi Script Execution Policy, chạy lệnh sau rồi kích hoạt lại:
# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Git Bash trên Windows:
source .venv/Scripts/activate
```

### Bước 3: Cài đặt thư viện chung
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Bước 4: Đăng ký môi trường vào Jupyter Notebook (để chọn kernel)
```bash
python -m ipykernel install --user --name=ktdl-env --display-name="Python (KTDL Olist)"
```

---

## 3. Quy ước đặt tên biến (Python / PEP 8 & Data Science)

Áp dụng quy chuẩn **PEP 8** kết hợp quy ước chuyên ngành Data Science để code đồng nhất, dễ đọc giữa các thành viên:

| Đối tượng | Quy tắc | Ví dụ | Lưu ý |
| :--- | :--- | :--- | :--- |
| **Biến thường, hàm** | `snake_case` (chữ thường, gạch dưới) | `customer_id`, `freight_value`, `calculate_rfm()` | Tên hàm nên bắt đầu bằng động từ (`clean_`, `get_`, `plot_`) |
| **Bảng dữ liệu (DataFrame)** | Bắt đầu bằng tiền tố `df_` | `df_orders`, `df_customers`, `df_features` | Tránh đặt chung chung là `df`, `data`, `data1` |
| **Chuỗi dữ liệu (Series)** | Bắt đầu bằng tiền tố `s_` hoặc tên rõ ràng | `s_review_scores`, `customer_totals` | |
| **Đặc trưng mô hình (Features)** | `X`, `y`, `feature_cols` | `X_train`, `X_scaled`, `cluster_labels` | `X` viết hoa vì là ma trận 2D; `y` thường vì là vector 1D |
| **Hằng số cấu hình** | `UPPER_SNAKE_CASE` (chữ hoa toàn bộ) | `RANDOM_STATE = 42`, `SNAPSHOT_DATE = "2018-10-18"` | Đặt ở đầu file/cell |
| **Lớp (Class)** | `PascalCase` | `CustomerClusteringPipeline`, `DataCleaner` | |
| **Cột trong DataFrame** | `snake_case` không dấu, tiếng Anh | `order_id`, `order_purchase_timestamp`, `freight_ratio` | Giữ nguyên tên gốc của Olist để tránh nhầm |

---

## 4. Quy ước đặt tên nhánh & Quy trình Git (Git Workflow)

### 4.1. Cấu trúc nhánh chính
- `main`: Nhánh ổn định cao nhất, chứa sản phẩm cuối cùng nộp bài (Lead quản lý).
- `develop`: Nhánh tích hợp code hàng tuần. Mọi nhánh tính năng đều tách ra từ đây và merge về đây.

### 4.2. Quy ước đặt tên nhánh tính năng
Cú pháp: `feature/<mã_nhiệm_vụ>-<tên_ngắn_gọn>` hoặc `feature/<thành_viên>-<tên_task>`

- Theo mã trong bảng phân công (khuyến nghị cho nhóm):
  - `feature/A02-clean-data`
  - `feature/B03-shipping-features`
  - `feature/B07-nlp-reviews`
  - `feature/C04-rfm-online-retail`
  - `feature/C05-rfm-olist`
- Nhánh sửa lỗi: `fix/<tên-lỗi>` (ví dụ: `fix/missing-customer-unique-id`)
- Nhánh phân tích EDA: `eda/<chủ-đề>` (ví dụ: `eda/delivery-delay-analysis`)

### 4.3. Quy trình làm việc nhóm hàng ngày

1. **Trước khi bắt đầu làm:**
   ```bash
   git checkout develop
   git pull origin develop
   ```
2. **Tạo nhánh làm việc riêng:**
   ```bash
   git checkout -b feature/B03-shipping-features
   ```
3. **Thực hiện công việc, commit thường xuyên với commit message rõ ràng:**
   ```bash
   git add src/features.py notebooks/02_eda_shipping.ipynb
   git commit -m "feat(features): them dac trung freight_ratio va so ngay giao hang"
   ```
4. **Đẩy nhánh lên GitHub và tạo Pull Request (PR):**
   ```bash
   git push origin feature/B03-shipping-features
   ```
   - Tạo PR từ `feature/B03-shipping-features` vào `develop`.
   - Trưởng nhóm (A) review code, kiểm tra không xung đột và merge PR.
