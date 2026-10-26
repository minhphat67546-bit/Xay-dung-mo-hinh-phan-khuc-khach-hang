# KỊCH BẢN THUYẾT TRÌNH BẢO VỆ ĐỒ ÁN VÀ DEMO WEB UI
**Đề tài:** Xây dựng mô hình phân khúc khách hàng E-Commerce Olist kết hợp RFM và Trải nghiệm dịch vụ  
**Đơn vị:** Khoa Công nghệ Thông tin – Trường Đại học Công Thương TP.HCM (HUIT)  
**Nhóm sinh viên thực hiện:**  
- **Trần Duy Minh Phát** (Trưởng nhóm - Thành viên A: Kỹ thuật Pipeline, Mô hình K-Means & Web Demo)  
- **Huỳnh Bổ Bửu Quang** (Thành viên B: Lý thuyết Dịch vụ, Phân tích Giao hàng trễ & SLA Vận hành)  
- **Phạm Quốc Ân** (Thành viên C: Dữ liệu Online Retail II, Mô hình RFM & Chiến lược Marketing)  
**Tổng thời lượng:** 12 – 15 phút (Slide: 8 – 9 phút | Live Demo Web: 4 – 5 phút | Q&A: 5 phút)

---

## PHẦN I: KỊCH BẢN THUYẾT TRÌNH SLIDE (11 SLIDES ~ 8 - 9 PHÚT)

---

### SLIDE 1: Trang tiêu đề & Giới thiệu
* **Thời lượng:** 45 giây  
* **Người trình bày:** Thành viên A (Trần Duy Minh Phát)  
* **Hành động:** Đứng tự tin, chào Hội đồng / Giảng viên, phong thái đĩnh đạc.

> **Lời thoại:**  
> *"Kính thưa quý Thầy/Cô trong Hội đồng và các bạn sinh viên!  
> Em tên là **Trần Duy Minh Phát**, đại diện cho nhóm nghiên cứu gồm em, bạn **Huỳnh Bổ Bửu Quang** và bạn **Phạm Quốc Ân**, sinh viên Khoa Công nghệ Thông tin – Trường Đại học Công Thương TP.HCM.  
> Hôm nay, nhóm chúng em xin phép được báo cáo kết quả thực hiện đề tài: **'Xây dựng mô hình phân khúc khách hàng E-Commerce Olist kết hợp RFM và Trải nghiệm dịch vụ'**.  
> Đây là một đề tài ứng dụng kỹ thuật khai phá dữ liệu giải quyết bài toán kinh doanh thực tiễn chặng cuối rất nhức nhối trên các sàn thương mại điện tử hiện nay. Sau đây, em xin phép bắt đầu phần trình bày."*

---

### SLIDE 2: Bối cảnh & Vì sao cần phân khúc khách hàng?
* **Thời lượng:** 45 giây  
* **Người trình bày:** Thành viên A (hoặc C - Phạm Quốc Ân)  
* **Hành động:** Chỉ vào con số chi phí "5 - 7 lần" trên màn hình.

> **Lời thoại:**  
> *"Thưa Thầy Cô, trong thị trường thương mại điện tử cạnh tranh khốc liệt ngày nay, các nghiên cứu kinh tế đã chỉ ra rằng: **Chi phí để tìm kiếm một khách hàng mới (CAC) thường đắt gấp 5 đến 7 lần chi phí để giữ chân một khách hàng hiện hữu**.  
> Tuy nhiên, hầu hết các nền tảng TMĐT thường mắc phải sai lầm là đối xử với mọi khách hàng như nhau – áp dụng chung một mức phí ship, chung một thông điệp quảng cáo.  
> Nếu không phân khúc khách hàng chính xác, doanh nghiệp sẽ lãng phí ngân sách tiếp thị vào những người không có nhu cầu, đồng thời bỏ lỡ cơ hội chăm sóc nhóm khách hàng trung thành mang lại nguồn thu cốt lõi."*

---

### SLIDE 3: Mục tiêu & Ba đóng góp cốt lõi của đề tài
* **Thời lượng:** 45 giây  
* **Người trình bày:** Thành viên A (hoặc C)  
* **Hành động:** Nhấn mạnh 3 mục tiêu bằng 3 ngón tay hoặc trỏ laser theo thứ tự 1-2-3.

> **Lời thoại:**  
> *"Xuất phát từ thực tế đó, đề tài của nhóm tập trung vào 3 đóng góp kỹ thuật cốt lõi:  
> **Thứ nhất:** Xây dựng một quy trình tiền xử lý và pipeline hợp nhất tự động từ 9 bảng dữ liệu quan hệ của sàn Olist Brazil với hơn 100,000 đơn hàng.  
> **Thứ hai:** Đột phá về mặt phương pháp luận – nhóm không chỉ dừng lại ở mô hình RFM truyền thống, mà tích hợp thêm chiều **Trải nghiệm dịch vụ Logistics** (đo lường độ trễ hẹn và tỷ lệ phí vận chuyển).  
> **Thứ ba:** Xây dựng một hệ thống Web Dashboard tương tác thời gian thực, cho phép mô phỏng chính sách kinh doanh và phân loại tự động khách hàng mới."*

---

### SLIDE 4: Quy trình Pipeline: Từ dữ liệu giao dịch đến hồ sơ khách hàng
* **Thời lượng:** 50 giây  
* **Người trình bày:** Thành viên A (Trần Duy Minh Phát)  
* **Hành động:** Trỏ vào sơ đồ pipeline ETL và con số 93,350 khách hàng.

> **Lời thoại:**  
> *"Về mặt kỹ thuật dữ liệu, sàn Olist cung cấp 9 bảng dữ liệu thô với nhiều thách thức: đơn hủy, trùng lặp và mối quan hệ 1-n giữa tài khoản mua hàng và khách hàng định danh.  
> Nhóm em đã thiết kế pipeline ETL tự động trong module `src/data_pipeline.py`:  
> - Lọc 96,470 đơn hàng có trạng thái giao thành công (`delivered`).  
> - Khử trùng lặp giữa `customer_id` theo đơn và định danh duy nhất bằng `customer_unique_id`.  
> - Kết quả thu được tệp dữ liệu sạch chuẩn mực gồm **93,350 khách hàng duy nhất** với 29 trường thông tin toàn diện về giao dịch, thanh toán, vận chuyển và đánh giá sao."*

---

### SLIDE 5: Cơ sở lý thuyết SERVQUAL & Hiện tượng Giao trễ
* **Thời lượng:** 1 phút  
* **Người trình bày:** Thành viên B (Huỳnh Bổ Bửu Quang)  
* **Hành động:** Chuyển lời cho bạn Quang. Quang chỉ vào biểu đồ phân phối điểm review tụt dốc.

> **Lời thoại (Quang):**  
> *"Tiếp theo, em là Huỳnh Bổ Bửu Quang xin phép trình bày về phát hiện quan trọng nhất trong khâu khám phá dữ liệu (EDA):  
> Vận dụng mô hình chất lượng dịch vụ **SERVQUAL** của Parasuraman, nhóm nhận thấy sự hài lòng của khách hàng phụ thuộc vào 'Khoảng cách kỳ vọng' giữa ngày cam kết và ngày giao thực tế.  
> Trên sàn Olist, tỷ lệ giao hàng trễ hẹn chỉ chiếm **6.77%** (6,534 đơn). Nhưng đây lại là 'tử huyệt' dịch vụ:  
> - Đơn giao đúng hạn đạt điểm review trung bình rất cao: **4.29 sao**.  
> - Nhưng ngay khi đơn hàng bị trễ hẹn, điểm số rơi tự do xuống **1.66 sao** – với hơn 68% khách hàng thẳng tay đánh giá 1 sao và để lại phản hồi gay gắt.  
> Điều này chứng minh: Nếu chỉ dùng RFM mà bỏ qua chỉ số giao trễ, doanh nghiệp sẽ hoàn toàn 'mù màu' trước những khách hàng đang trên bờ vực rời bỏ sàn!"*

---

### SLIDE 6: Kỹ thuật hóa 10 đặc trưng mô hình hóa
* **Thời lượng:** 50 giây  
* **Người trình bày:** Thành viên A (Trần Duy Minh Phát)  
* **Hành động:** Trỏ vào bảng danh sách 10 đặc trưng đã biến đổi.

> **Lời thoại (Phát):**  
> *"Để đưa dữ liệu vào thuật toán học máy mà không bị thiên lệch bởi ngoại lai, nhóm em đã thực hiện chuỗi kỹ thuật tiền xử lý chuyên sâu:  
> 1. **Winsorization (1% - 99%)**: Cắt tỉa các giá trị cực đoan đối với các biến liên tục lệch phải như giá trị đơn hàng hay số ngày giao.  
> 2. **Biến đổi Log1p**: Đưa các phân phối lũy thừa về dạng phân phối chuẩn Gaussian.  
> 3. **Đặc trưng phi tuyến**: Tạo cờ cảnh báo trễ nghiêm trọng khi số ngày trễ vượt quá 3 ngày.  
> Bộ đặc trưng cuối cùng gồm **10 biến chuẩn hóa đại diện**, bao quát trọn vẹn 3 trụ cột: Giá trị giao dịch (RFM), Trải nghiệm Logistics và Tín dụng thanh toán."*

---

### SLIDE 7: Thực nghiệm thuật toán & Đánh giá chọn k = 4 tối ưu
* **Thời lượng:** 50 giây  
* **Người trình bày:** Thành viên A (Trần Duy Minh Phát)  
* **Hành động:** Chỉ vào đồ thị Elbow và đỉnh cực đại của Silhouette Score.

> **Lời thoại (Phát):**  
> *"Tại bước mô hình hóa, nhóm em đã thử nghiệm so sánh 3 thuật toán: K-Means, GMM (mô hình xác suất) và DBSCAN (dựa trên mật độ).  
> Để tìm ra số cụm $k$ tối ưu một cách khách quan nhất, nhóm thực hiện đo lường đồng thời 3 chỉ số khoa học với $k$ chạy từ 3 đến 8:  
> - **Điểm uốn Elbow (WCSS)** xuất hiện rõ rệt tại $k = 4$.  
> - **Chỉ số Silhouette Score** đạt đỉnh cực đại tại $k = 4$ với giá trị **0.2413**.  
> - **Chỉ số Davies-Bouldin** đạt giá trị nhỏ nhất **1.1945** (càng nhỏ cấu trúc cụm càng cô đặc và tách bạch).  
> Cả 3 tiêu chuẩn toán học đều đồng thuận kết luận: **$k = 4$ là cấu trúc phân cụm tự nhiên và chuẩn xác nhất** cho bộ dữ liệu Olist."*

---

### SLIDE 8: Chân dung 4 Phân khúc khách hàng Olist chính thức
* **Thời lượng:** 1 phút 15 giây  
* **Người trình bày:** Thành viên A (hoặc cả 3 người phối hợp)  
* **Hành động:** Trỏ vào bảng so sánh 4 cụm trên slide.

> **Lời thoại:**  
> *"Từ mô hình $k=4$, bức tranh toàn cảnh về 4 nhóm khách hàng Olist hiện lên vô cùng sắc nét:  
> 1. **VIP Champions (~3.0% - Cụm 2)**: Nhóm khách hàng tinh hoa với chi tiêu cao nhất (**309 BRL**), tần suất mua lặp lại đạt **2.11 đơn/khách** (gấp đôi bình quân sàn), điểm review 4.24 sao.  
> 2. **Satisfied Mainstream (~46.7% - Cụm 1)**: Lực lượng nòng cốt chiếm gần một nửa sàn. Chi tiêu vừa phải (252 BRL), phí ship hợp lý (13.2%), trải nghiệm logistics xuất sắc (0% trễ hẹn), điểm hài lòng 4.24 sao và chuộng trả góp 4 kỳ.  
> 3. **Freight-Sensitive (~44.8% - Cụm 0)**: Nhóm khách hàng mua đơn nhỏ (63 BRL) nhưng phải chịu tỷ lệ phí ship chiếm tới **28.8%** giá trị đơn. Họ vẫn đánh giá 4.34 sao khi hàng tới nơi, nhưng gánh nặng phí ship khiến họ ngần ngại quay lại lần 2.  
> 4. **At-Risk Delivery (~5.5% - Cụm 3)**: Nhóm 'tổn thương dịch vụ' nặng nhất với **100% đơn hàng bị giao trễ**, thời gian chờ đợi lên tới **36.5 ngày**. Điểm review chạm đáy **1.96 sao** và đang trên bờ vực rời bỏ sàn vĩnh viễn!"*

---

### SLIDE 9: Đối chiếu thực nghiệm: Vì sao Olist cần thêm chiều Trải nghiệm?
* **Thời lượng:** 45 giây  
* **Người trình bày:** Thành viên C (Phạm Quốc Ân)  
* **Hành động:** Chuyển lời cho bạn Ân. Ân so sánh cấu trúc Olist với Online Retail II.

> **Lời thoại (Ân):**  
> *"Em là Phạm Quốc Ân, xin phép trình bày phần đối chiếu thực nghiệm:  
> Khi nhóm thực hiện phân tích đối sánh với bộ dữ liệu bán lẻ Online Retail II của Anh Quốc – nơi khách hàng mua sỉ lặp lại nhiều lần, mô hình RFM truyền thống hoạt động rất tốt.  
> Tuy nhiên, trên sàn TMĐT đại chúng như Olist, có tới hơn 97% khách hàng chỉ mới phát sinh 1 đơn hàng trong kỳ quan sát. Nếu chỉ dùng RFM, hầu hết khách hàng sẽ bị dồn chung vào một nhóm 'Khách mới / Mua 1 lần'.  
> Chỉ khi chúng em đưa thêm 2 biến số **Phí vận chuyển** và **Giao trễ**, thuật toán mới bóc tách được: Khách hàng chưa mua lại là vì **Phí ship quá đắt (Cụm 0)** hay vì **Bị giao trễ tới phát bực (Cụm 3)**. Đây chính là đóng góp mang tính thực tiễn cao nhất của đề tài!"*

---

### SLIDE 10: Biến phân khúc thành hành động (SLA & Marketing)
* **Thời lượng:** 50 giây  
* **Người trình bày:** Thành viên B & C  
* **Hành động:** Nêu giải pháp tương ứng từng cụm.

> **Lời thoại (Quang & Ân):**  
> *"Từ kết quả phân cụm, nhóm chúng em đề xuất các chiến lược hành động cụ thể:  
> - **Với nhóm VIP Champions**: Triển khai gói hội viên ưu tiên *Olist Prime VIP*, đường dây hỗ trợ riêng và mở bán trước các sản phẩm giới hạn.  
> - **Với nhóm Freight-Sensitive**: Tung chính sách trợ giá vận chuyển *FreeShip Extra* cho đơn từ 99 BRL và gợi ý mua combo cùng gian hàng để gộp ship.  
> - **Với nhóm At-Risk Delivery**: Kích hoạt quy trình CSKH khẩn cấp – tự động gửi thư xin lỗi kèm Voucher bồi hoàn vô điều kiện trị giá 30–50 BRL; đồng thời siết chặt kỷ luật SLA với các đơn vị 3PL tại các bang có tỷ lệ trễ cao như Rio de Janeiro."*

---

### SLIDE 11: Kết luận & Chuyển sang phần Live Demo
* **Thời lượng:** 30 giây  
* **Người trình bày:** Thành viên A (Trần Duy Minh Phát)  
* **Hành động:** Kết luận ngắn gọn và chuyển màn hình sang trình duyệt Web.

> **Lời thoại (Phát):**  
> *"Kính thưa Thầy Cô, đề tài đã hoàn thành xuất sắc các mục tiêu nghiên cứu và quản lý mã nguồn chuẩn Git Flow.  
> Để chứng minh tính ứng dụng của mô hình vào thực tế vận hành doanh nghiệp, nhóm em đã xây dựng một **Hệ thống Dashboard tương tác trực tiếp trên nền tảng Web**.  
> Sau đây, em xin phép kính mời Thầy Cô cùng theo dõi phần **Live Demo trực tiếp trên Web UI**!"*

---

## PHẦN II: KỊCH BẢN LIVE DEMO WEB UI (4 – 5 PHÚT)

* **Chuẩn bị trước:** Mở sẵn trình duyệt tại địa chỉ `http://localhost:8501` (hoặc mở file `demo_dashboard.html`).  
* **Người thực hiện thao tác chuột & thuyết minh:** Trần Duy Minh Phát (A).

---

### BƯỚC 1: Demo Phân hệ 1 – Tổng quan & Biểu đồ Radar Đa chiều (1 phút)
* **Thao tác chuột:** Nhấp vào tab **1. Tổng quan & Dashboard KPIs**. Cuộn chuột lướt qua 4 thẻ KPI và dừng lại ở Biểu đồ Radar.
* **Lời thoại:**
  > *"Thưa Thầy Cô, đây là giao diện chính của hệ thống Dashboard Olist Analytics.  
  > Trên màn hình, 4 thẻ KPI phản ánh ngay lập tức bức tranh toàn sàn: **93,350 khách hàng duy nhất**, **14.2 triệu BRL doanh thu**, tỷ lệ giao trễ **6.77%** và thuật toán tối ưu tại **$k = 4$**.  
  > Điểm nhấn độc đáo nhất ở đây là **Biểu đồ Radar đa chiều** chuẩn hóa thang điểm 0–100:  
  > *(Rê chuột vào đường viền màu tím)*: Cụm VIP Champions phủ rộng ở góc Chi tiêu và Tần suất mua hàng.  
  > *(Rê chuột vào đường viền màu đỏ)*: Cụm At-Risk Delivery bị co rúm hoàn toàn ở góc 'Đúng hạn' (0 điểm) và 'Tốc độ nhận hàng' (chỉ 10 điểm) do thời gian giao trung bình lên tới 36.5 ngày!"*

---

### BƯỚC 2: Demo Phân hệ 2 – Chân dung 4 Phân khúc (45 giây)
* **Thao tác chuột:** Nhấp sang tab **2. Chân dung 4 Phân khúc**. Chọn lần lượt Cụm 0 (Freight-Sensitive) rồi Cụm 3 (At-Risk).
* **Lời thoại:**
  > *"Tại tab Chân dung phân khúc, nhà quản lý có thể đi sâu vào từng nhóm:  
  > Khi em chọn **Cụm 0 - Freight-Sensitive**, hệ thống hiển thị ngay tỷ lệ phí ship chiếm tới **28.8%** giá trị đơn và tập trung tới gần 20,000 khách tại bang São Paulo.  
  > Bên cạnh đó, hệ thống tích hợp sẵn **Action Plan** cụ thể: Bộ phận Marketing cần làm gì (tặng voucher FreeShip), và Bộ phận Vận hành cần làm gì (tối ưu quy trình gom đơn)."*

---

### BƯỚC 3: Demo Phân hệ 3 – Tra cứu Hồ sơ Khách hàng Tức thời (1 phút)
* **Thao tác chuột:** Nhấp sang tab **3. Tra cứu Hồ sơ Khách hàng**.
  - Đầu tiên, chọn mẫu: **💎 VIP Champion**.
  - Tiếp theo, chuyển sang mẫu: **⚠️ Khách hàng giao trễ**.
* **Lời thoại:**
  > *"Phân hệ thứ ba hỗ trợ trực tiếp cho nhân viên chăm sóc khách hàng (CSKH) và nhân viên kinh doanh:  
  > Khi khách hàng liên hệ, nhân viên chỉ cần nhập mã Customer ID hoặc tra cứu nhanh:  
  > *(Chọn khách VIP)*: Hệ thống chẩn đoán ngay đây là khách VIP, chi 890 BRL với 3 đơn hàng, **Health Score đạt 95/100 (Tuyệt vời)**, gợi ý tặng quà tri ân.  
  > *(Chọn khách giao trễ)*: Ngay lập tức, thanh cảnh báo chuyển sang màu đỏ, **Health Score tụt xuống 20/100 (Báo động đỏ)** do đơn hàng bị giao trễ 15 ngày và khách đánh giá 1 sao. Hệ thống hướng dẫn nhân viên CSKH chủ động gọi điện xin lỗi và bồi hoàn voucher trước khi khách rời bỏ sàn!"*

---

### BƯỚC 4: Demo Phân hệ 4 – Phân loại Khách hàng Mới (Live ML) (1 phút)
* **Thao tác chuột:** Nhấp sang tab **4. Phân loại Khách mới (Live ML)**.
  - Điền thử thông số: Chi tiêu `200 BRL`, Đơn hàng `1`, Giao hàng `35 ngày`, Chọn `Có trễ hẹn`, Review `1 sao`.
  - Nhấn nút: **⚡ Phân Loại Phân Khúc Ngay**.
* **Lời thoại:**
  > *"Đây là tính năng mang tính kỹ thuật máy học cao nhất của Dashboard:  
  > Giả sử có một khách hàng mới vừa phát sinh đơn hàng: chi 200 BRL, thời gian giao bị kéo dài 35 ngày, đơn bị trễ hẹn và khách đánh giá 1 sao.  
  > Em nhấn nút **'Phân loại ngay'**: Thuật toán K-Means trong backend sẽ tính toán vector khoảng cách Euclidean và trả về kết quả trong chưa đầy 0.1 giây:  
  > Khách hàng được tự động gán nhãn vào **Cụm 3: At-Risk Delivery với độ tin cậy 94.8%**, đồng thời đưa ra chỉ dẫn hành động ứng biến ngay lập tức!"*

---

### BƯỚC 5: Demo Phân hệ 5 – Mô phỏng Kịch bản Kinh doanh What-If (1 phút)
* **Thao tác chuột:** Nhấp sang tab **5. Mô phỏng Kịch bản (What-If)**.
  - Kéo thanh slider **Mức trợ giá phí ship** lên `20%`.
  - Kéo thanh slider **Rút ngắn thời gian giao** lên `5 ngày`.
  - Chỉ vào 4 thẻ kết quả động nhảy số.
* **Lời thoại:**
  > *"Phân hệ cuối cùng là công cụ chiến lược dành riêng cho Ban Giám đốc – **Mô phỏng kịch bản What-If thời gian thực**:  
  > Giả sử Ban điều hành cân nhắc phương án: **Trợ giá 20% phí vận chuyển** và đầu tư công nghệ rút ngắn **5 ngày giao hàng chặng cuối**.  
  > Ngay khi em kéo thanh trượt, hệ thống tự động mô phỏng và dự báo tác động tài chính:  
  > - Kích hoạt thêm **+5,014 khách hàng** trong nhóm nhạy cảm phí ship quay trở lại mua sắm lần 2.  
  > - Cứu vãn được **+1,123 khách hàng** khỏi nguy cơ rời bỏ sàn do giao trễ.  
  > - Điểm review toàn sàn tăng thêm **+0.28 sao** (đạt 4.43 sao).  
  > - Và quan trọng nhất: **Doanh thu dự kiến tăng thêm gần 1 triệu BRL (~ 4.8 Tỷ VNĐ)**!  
  > Điều này giúp Ban Giám đốc dễ dàng đo lường tỷ suất sinh lời ROI trước khi quyết định ngân sách thực tế."*

---

## PHẦN III: LỜI KẾT VÀ MỞ ĐẦU Q&A (30 GIÂY)

* **Hành động:** Đứng thẳng, quay lại nhìn Thầy Cô, mỉm cười lịch thiệp.

> **Lời thoại (Trần Duy Minh Phát):**  
> *"Kính thưa quý Thầy/Cô trong Hội đồng,  
> Phần trình bày slide và demo hệ thống Web Dashboard của nhóm Olist đến đây là kết thúc.  
> Qua đề tài này, nhóm chúng em đã chứng minh được sự kết hợp giữa **Khai phá dữ liệu học máy** và **Bài toán kinh doanh thực tế** có thể mang lại những giải pháp giá trị cho các sàn thương mại điện tử.  
> Nhóm em xin chân thành cảm ơn quý Thầy Cô đã chú ý lắng nghe và rất mong nhận được những nhận xét, góp ý quý báu từ Hội đồng để đề tài được hoàn thiện hơn nữa!  
> **Nhóm em xin trân trọng kính mời quý Thầy Cô bước vào phần đặt câu hỏi Q&A!**"*

---

## BỘ CÂU HỎI HỘI ĐỒNG THƯỜNG HỎI & CÁCH TRẢ LỜI GỢI Ý

### Câu 1: *"Tại sao nhóm lại chọn k = 4 mà không phải k = 3 hay k = 5?"*
* **Người trả lời gợi ý:** Thành viên A (Phát)
* **Ý trả lời:**  
  *"Thưa Thầy Cô, nhóm đã thực hiện đánh giá đa tiêu chí khách quan:  
  1. Đồ thị Elbow giảm độ dốc rõ rệt nhất tại $k=4$.  
  2. Chỉ số **Silhouette Score** tại $k=4$ đạt đỉnh cực đại là **0.2413** (cao hơn $k=3$ là 0.22 và $k=5$ là 0.20).  
  3. Chỉ số **Davies-Bouldin** đạt giá trị nhỏ nhất là **1.1945**.  
  4. Về mặt nghiệp vụ: $k=4$ bóc tách được 4 nhóm khách hàng có hành vi hoàn toàn độc lập và có giải pháp kinh doanh riêng biệt, trong khi $k=3$ sẽ gộp chung nhóm phí ship và nhóm phổ thông, làm mất đi đặc trưng nhạy cảm về logistics."*

### Câu 2: *"Tại sao điểm Silhouette 0.2413 có vẻ không quá cao (thường người ta thích > 0.5)?"*
* **Người trả lời gợi ý:** Thành viên A (Phát) hoặc B (Quang)
* **Ý trả lời:**  
  *"Thưa Thầy Cô, trong dữ liệu giao dịch thương mại điện tử thực tế (Real-world transaction data), hành vi tiêu dùng là liên tục chứ không tách biệt tuyệt đối như các bài toán phân loại ảnh hay dữ liệu nhân tạo.  
  Các nghiên cứu phân cụm hành vi khách hàng trên thế giới trên các tập dữ liệu lớn (>50k dòng) thường có Silhouette trong khoảng 0.20 – 0.35. Giá trị 0.2413 là mức tối ưu cao nhất trên bộ dữ liệu Olist và phản ánh chính xác sự chuyển tiếp tự nhiên giữa các phân khúc."*

### Câu 3: *"Mô hình này có thể triển khai thực tế trên các sàn TMĐT Việt Nam như Shopee hay Tiki không?"*
* **Người trả lời gợi ý:** Thành viên C (Ân) hoặc B (Quang)
* **Ý trả lời:**  
  *"Dạ thưa Thầy Cô, hoàn toàn có thể triển khai ngay được ạ!  
  Thị trường TMĐT Việt Nam có đặc thù địa lý kéo dài Bắc - Nam, các đơn hàng liên tỉnh (ví dụ từ Hà Nội vào TP.HCM) cũng thường xuyên gặp vấn đề về phí ship cao và thời gian giao kéo dài giống hệt như Brazil.  
  Các sàn tại Việt Nam có thể kế thừa đúng 10 đặc trưng này và thuật toán K-Means để gắn tag phân khúc tự động cho khách hàng, từ đó phân bổ mã Freeship Extra hoặc tối ưu vị trí kho hàng vệ tinh."*
