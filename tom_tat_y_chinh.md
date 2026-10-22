# Tóm tắt kết quả phân tích giao hàng và trải nghiệm khách hàng (Olist)

1. **Đơn trễ hẹn hiếm nhưng rất "đắt":** chỉ 6.77% (6,534/96,470 đơn) về sau
   `order_estimated_delivery_date`, nhưng nhóm này bị chấm trung bình **2.27 sao** so với
   **4.29 sao** của nhóm đúng hạn — mất 2.02 sao,
   kiểm định Mann-Whitney U = 467,426,830, p-value xấp xỉ 0.
2. **Cột mốc "hẹn" của Olist rất rộng lượng:** trung vị `delay_days` =
   -12 ngày, nghĩa là đơn thường về **sớm hơn hẹn ~12 ngày**.
   Vì vậy 6.77% chỉ là phần đuôi; nếu siết lịch hẹn sát thực tế thì tỉ lệ trễ thực tăng lên,
   và `is_late` chỉ đáng tin khi đi kèm `delay_days`.
3. **Thời gian giao:** trung bình 12.6 ngày, trung vị
   10 ngày, P95 = 29 ngày,
   dài nhất 210 ngày => phân phối lệch phải mạnh,
   các đặc trưng `avg_delivery_days` nên được log/ Winsorize trước khi chuẩn hóa.
4. **Tác động của giao hàng là ngưỡng, không tuyến tính:** điểm review vẫn ~
   4.32 khi đơn về sớm hơn hẹn trên 8 ngày, nhưng rơi xuống
   3.29 (trễ 1-3 ngày), 2.11 (trễ 4-7 ngày) và
   1.70 (trễ trên 7 ngày). Tương quan hạng toàn cục vì thế nhỏ
   (rho delay = -0.176, rho thời gian giao = -0.235) —
   nên đưa vào mô hình **cờ trễ + khoảng trễ chia tổ** thay vì một biến liên tục.
5. **Review thiên lệch tích cực:** trung bình 4.16/5, 78.9% đơn đạt 4-5 sao,
   chỉ 12.77% đơn 1-2 sao (12,236 đơn) — đây chính là nhóm "khách hàng rủi ro"
   mà bài toán phân cụm cần tách ra.
6. **Phí ship khác nhau chủ yếu theo địa lý, ít liên hệ trực tiếp tới điểm đánh giá:**
   khu vực Norte chịu R$ 41.3/đơn so với R$
   19.8 ở Sudeste, nhưng Spearman(freight, review) chỉ -0.089;
   tổng phí ship bằng 16.6% tổng giá hàng, còn mức
   `freight_to_price_ratio` của một khách trung vị là 0.22.
   Bang BA có phí ship cao nhất trong 10 bang đông đơn nhất, còn
   SP chiếm 42.0% tổng đơn.
7. **Bảng đặc trưng đã sẵn sàng cho clustering:** 93,350 dòng tương ứng 93,350
   `customer_unique_id` (không trùng), 99.4% khách có ít nhất một review,
   603 khách không có review (để trống `NaN`, không điền 0).
8. **Cảnh giác với đặc trưng dư thừa:** 97.0% khách chỉ có 1 đơn nên
   `late_delivery_rate` và `avg_review_score` thực chất là biến nhị phân ở nhóm này
   (thị trường khách nhiều đơn chỉ 3.0%, n = 2,801);
   tương quan Spearman `late_delivery_rate`~`avg_review_score` = -0.301 và
   `low_review_count`~`avg_review_score` = -0.655. Trước khi chạy K-means/DBSCAN nên
   chuẩn hóa Z-score, loại bỏ `low_review_count` (hoặc `avg_review_score`) và cân nhắc PCA.

---

**Nguồn số liệu:** Olist Brazilian E-Commerce Public Dataset by Uol; nhóm phân tích 96,470 đơn `delivered` có đủ ngày giao, độ phủ 93,350 khách hàng duy nhất.

**Bộ đặc trưng cho bước phân cụm:** `experience_features.csv` (customer_unique_id, n_orders, n_reviews, avg_review_score, late_delivery_rate, avg_delivery_days, avg_freight_value, freight_to_price_ratio, low_review_count).

**Hình ảnh minh họa (PNG, dpi 200) trong `figures/`:** fig_01_ti_le_giao_tre, fig_02_phan_phoi_thoi_gian_giao, fig_03_phan_phoi_review_score, fig_04_review_dung_han_vs_giao_tre, fig_05_freight_theo_bang, fig_06_freight_vs_review, fig_07_review_theo_thoi_gian_va_tre, fig_08_phan_phoi_dac_trung.
