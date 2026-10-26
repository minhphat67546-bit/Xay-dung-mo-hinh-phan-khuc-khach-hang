import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.preprocessing import MinMaxScaler
import os

# ---------------------------------------------------------
# CẤU HÌNH TRANG STREAMLIT
# ---------------------------------------------------------
st.set_page_config(
    page_title="Olist Customer Segmentation - KTDL",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# CUSTOM CSS PHONG CÁCH HIỆN ĐẠI
# ---------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    .main-header {
        background: linear-gradient(135deg, #102C57 0%, #1679AB 100%);
        padding: 24px;
        border-radius: 12px;
        color: white;
        margin-bottom: 24px;
        box-shadow: 0 4px 12px rgba(16,44,87,0.15);
    }
    .metric-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 16px 20px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.04);
        margin-bottom: 12px;
        border-left: 5px solid #1679AB;
    }
    .metric-title {
        color: #64748b;
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .metric-value {
        color: #0f172a;
        font-size: 1.8rem;
        font-weight: 700;
        margin: 4px 0;
    }
    .metric-sub {
        color: #10b981;
        font-size: 0.8rem;
        font-weight: 500;
    }
    .cluster-card {
        border-radius: 10px;
        padding: 16px;
        margin-bottom: 16px;
        color: white;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 10px 18px;
        border-radius: 8px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# NẠP DỮ LIỆU CÓ CACHING
# ---------------------------------------------------------
@st.cache_data
def load_data():
    file_path = "data/processed/olist_clustered.parquet"
    if not os.path.exists(file_path):
        st.error(f"Khong tim thay file {file_path}")
        return None
    df = pd.read_parquet(file_path)
    
    # Chuẩn hóa tên và màu sắc cụm
    cluster_meta = {
        0: {"name": "Freight-Sensitive", "vi_name": "Nhạy cảm Phí ship", "color": "#FF9F43", "badge": "📦"},
        1: {"name": "Satisfied Mainstream", "vi_name": "Phổ thông Hài lòng", "color": "#10AC84", "badge": "🛒"},
        2: {"name": "VIP Champions", "vi_name": "Chi tiêu cao & Trung thành", "color": "#5F27CD", "badge": "💎"},
        3: {"name": "At-Risk Delivery", "vi_name": "Rủi ro do Giao trễ", "color": "#EE5253", "badge": "⚠️"}
    }
    df['segment_display'] = df['cluster'].map(lambda c: f"{cluster_meta[c]['badge']} {cluster_meta[c]['name']} ({cluster_meta[c]['vi_name']})")
    df['cluster_color'] = df['cluster'].map(lambda c: cluster_meta[c]['color'])
    return df

df_all = load_data()

if df_all is None:
    st.stop()

# ---------------------------------------------------------
# THÔNG TIN PHÂN KHÚC & TÂM CỤM
# ---------------------------------------------------------
CLUSTER_PROFILES = {
    0: {
        "name": "Freight-Sensitive (Nhạy cảm Phí vận chuyển)",
        "badge": "📦", "color": "#FF9F43", "count": 41790, "pct": 44.8,
        "monetary": 63.23, "frequency": 1.00, "recency": 238.9,
        "review": 4.34, "delay_rate": 2.6, "freight_ratio": 28.8,
        "delivery_days": 10.5, "installments": 1.73,
        "desc": "Nhóm khách hàng mua đơn hàng giá trị nhỏ nhưng phải gánh tỷ lệ phí vận chuyển rất cao (~29% giá trị đơn). Họ rất hài lòng khi giao đúng hạn (4.34 sao) nhưng dễ rời bỏ sàn vì phí ship cao.",
        "marketing": "Tặng voucher FreeShip đơn từ 99 BRL; Gợi ý mua combo cùng người bán để chia sẻ phí vận chuyển.",
        "sla": "Tối ưu hóa gom đơn (order batching) và mở rộng kho hàng vệ tinh tại São Paulo & Minas Gerais."
    },
    1: {
        "name": "Satisfied Mainstream (Khách hàng Phổ thông Hài lòng)",
        "badge": "🛒", "color": "#10AC84", "count": 43602, "pct": 46.7,
        "monetary": 251.95, "frequency": 1.00, "recency": 239.7,
        "review": 4.24, "delay_rate": 2.7, "freight_ratio": 13.2,
        "delivery_days": 11.7, "installments": 4.01,
        "desc": "Lực lượng khách hàng nòng cốt chiếm gần một nửa tổng khách hàng. Mức chi tiêu vừa phải, tỷ lệ phí ship hợp lý (13.2%), trải nghiệm logistics xuất sắc với 0% trễ hẹn nghiêm trọng. Chuộng trả góp qua thẻ tín dụng (TB 4 kỳ).",
        "marketing": "Chương trình tích lũy điểm thưởng thành viên, khuyến khích mua lặp lại qua email cá nhân hóa và push notification.",
        "sla": "Duy trì tiêu chuẩn SLA cam kết giao hàng trong 12 ngày, tích hợp bảo hiểm giao hàng an tâm."
    },
    2: {
        "name": "VIP Champions (Chi tiêu cao & Trung thành)",
        "badge": "💎", "color": "#5F27CD", "count": 2775, "pct": 3.0,
        "monetary": 309.22, "frequency": 2.11, "recency": 220.3,
        "review": 4.24, "delay_rate": 6.1, "freight_ratio": 19.8,
        "delivery_days": 12.1, "installments": 3.31,
        "desc": "Tập khách hàng tinh hoa mang lại doanh thu vượt trội, có tần suất mua lặp lại cao nhất toàn sàn (2.11 đơn/khách, gấp đôi mức trung bình). Tương tác mua hàng gần đây nhất (220 ngày) và điểm hài lòng cao (4.24 sao).",
        "marketing": "Dịch vụ khách hàng ưu tiên Olist Prime VIP, mở khóa quyền tiếp cận sớm các sự kiện giảm giá và đổi quà sinh nhật.",
        "sla": "Ưu tiên luồng xử lý đơn hàng nhanh (Express picking & packing), bồi thường tự động nếu phát sinh chậm trễ."
    },
    3: {
        "name": "At-Risk Delivery (Rủi ro do Giao hàng trễ)",
        "badge": "⚠️", "color": "#EE5253", "count": 5183, "pct": 5.5,
        "monetary": 179.94, "frequency": 1.01, "recency": 225.5,
        "review": 1.96, "delay_rate": 100.0, "freight_ratio": 21.3,
        "delivery_days": 36.5, "installments": 3.07,
        "desc": "Phân khúc chịu tổn thương dịch vụ nghiêm trọng nhất với 100% đơn hàng bị giao trễ hẹn, thời gian nhận hàng kéo dài trung bình hơn 1 tháng (36.5 ngày). Điểm review chạm đáy 1.96 sao, để lại đánh giá tiêu cực và nguy cơ cao rời bỏ vĩnh viễn.",
        "marketing": "Gửi thư xin lỗi chân thành từ ban quản trị kèm Voucher bồi hoàn vô điều kiện trị giá 30-50 BRL cho đơn kế tiếp.",
        "sla": "Đình chỉ và tái đào tạo các đối tác vận chuyển tại khu vực Rio de Janeiro & Đông Bắc; Kích hoạt cảnh báo thời gian thực khi đơn trễ quá 3 ngày."
    }
}

# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3081/3081559.png", width=65)
    st.title("Olist Analytics")
    st.caption("Đồ án Khai thác Dữ liệu - HUIT 2026")
    st.markdown("---")
    
    menu = st.radio(
        "Chức năng chính:",
        [
            "📊 1. Tổng quan & Dashboard KPIs",
            "👥 2. Chân dung 4 Phân khúc",
            "🔍 3. Tra cứu Hồ sơ Khách hàng",
            "🤖 4. Phân loại Khách hàng Mới (Live ML)",
            "🎯 5. Mô phỏng Kịch bản Kinh doanh (What-If)"
        ]
    )
    
    st.markdown("---")
    st.markdown("**Nhóm thực hiện (Nhóm Olist - HUIT):**")
    st.markdown("- **Trần Duy Minh Phát** (Trưởng nhóm - A)")
    st.markdown("- **Huỳnh Bổ Bửu Quang** (Thành viên B)")
    st.markdown("- **Phạm Quốc Ân** (Thành viên C)")
    st.caption("Dữ liệu: 93,350 khách hàng Olist Brazil")

# ---------------------------------------------------------
# HEADER CHUNG
# ---------------------------------------------------------
st.markdown("""
<div class="main-header">
    <h2 style="margin:0; font-size: 1.8rem; font-weight:700;">HỆ THỐNG PHÂN KHÚC KHÁCH HÀNG E-COMMERCE OLIST</h2>
    <p style="margin:4px 0 0 0; opacity: 0.9; font-size: 0.95rem;">
        Mô hình phân cụm K-Means kết hợp RFM và Trải nghiệm dịch vụ Logistics (SLA & Delivery Gap)
    </p>
</div>
""", unsafe_allow_html=True)


# =========================================================
# TAB 1: TỔNG QUAN & DASHBOARD KPIS
# =========================================================
if "1. Tổng quan" in menu:
    st.subheader("📊 Bảng điều khiển Tổng quan Toàn sàn")
    
    # 4 Metric cards
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-title">Tổng Khách Hàng</div>
            <div class="metric-value">93,350</div>
            <div class="metric-sub">✓ 100% Khách hàng duy nhất</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="metric-card" style="border-left-color: #5F27CD;">
            <div class="metric-title">Tổng Giá Trị Giao Dịch</div>
            <div class="metric-value">14.2M BRL</div>
            <div class="metric-sub">~ 71 Tỷ VNĐ (2016-2018)</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="metric-card" style="border-left-color: #EE5253;">
            <div class="metric-title">Tỷ Lệ Giao Trễ Toàn Sàn</div>
            <div class="metric-value">6.77%</div>
            <div class="metric-sub" style="color: #ef4444;">6,534 đơn bị ảnh hưởng</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown("""
        <div class="metric-card" style="border-left-color: #10AC84;">
            <div class="metric-title">Số Cụm Tối Ưu (k)</div>
            <div class="metric-value">k = 4</div>
            <div class="metric-sub">Silhouette = 0.2413 (Đỉnh cao nhất)</div>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Biểu đồ Donut & Doanh thu 4 cụm
    c_left, c_right = st.columns([1, 1])
    
    with c_left:
        st.markdown("##### 🥧 Cơ cấu Tỷ trọng 4 Phân khúc Khách hàng")
        labels = [f"{CLUSTER_PROFILES[i]['badge']} {CLUSTER_PROFILES[i]['name'].split('(')[0].strip()}" for i in range(4)]
        values = [CLUSTER_PROFILES[i]['count'] for i in range(4)]
        colors = [CLUSTER_PROFILES[i]['color'] for i in range(4)]
        
        fig_donut = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            hole=.55,
            marker=dict(colors=colors),
            textinfo='label+percent',
            hovertemplate="<b>%{label}</b><br>Số lượng: %{value:,} khách<br>Tỷ lệ: %{percent}<extra></extra>"
        )])
        fig_donut.update_layout(
            showlegend=False,
            margin=dict(t=10, b=10, l=10, r=10),
            height=320
        )
        st.plotly_chart(fig_donut, use_container_width=True)
        
    with c_right:
        st.markdown("##### 💵 So sánh Chi tiêu Trung bình & Phí Ship (BRL)")
        clusters = [CLUSTER_PROFILES[i]['badge'] + " " + CLUSTER_PROFILES[i]['name'].split('(')[0].strip() for i in range(4)]
        monetary = [CLUSTER_PROFILES[i]['monetary'] for i in range(4)]
        freight_ratio = [CLUSTER_PROFILES[i]['freight_ratio'] for i in range(4)]
        
        fig_bar = go.Figure()
        fig_bar.add_trace(go.Bar(
            name='Chi tiêu TB (BRL)',
            x=clusters,
            y=monetary,
            marker_color=[CLUSTER_PROFILES[i]['color'] for i in range(4)],
            text=[f"{v:.1f} BRL" for v in monetary],
            textposition='auto',
        ))
        fig_bar.update_layout(
            barmode='group',
            margin=dict(t=10, b=10, l=10, r=10),
            height=320,
            yaxis_title="Giá trị đơn TB (BRL)",
            hovermode="x unified"
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    # Radar chart so sánh đa chiều 6 chỉ số cốt lõi
    st.markdown("##### 🕸️ Biểu đồ Radar So sánh Đa chiều 4 Phân khúc (Chuẩn hóa thang điểm 0 - 100)")
    
    categories = ['Chi tiêu (Monetary)', 'Tần suất mua (Frequency)', 'Điểm Review (CSAT)', 
                  'Tỷ lệ đúng hạn (On-time)', 'Tiết kiệm phí ship (Low Freight)', 'Tốc độ nhận hàng (Speed)']
    
    # Chuẩn hóa các chỉ số thành điểm số [0, 100] để vẽ Radar cân xứng
    radar_data = {
        0: [20, 48, 87, 97, 30, 85],   # Freight-Sensitive
        1: [81, 48, 85, 97, 90, 80],   # Satisfied Mainstream
        2: [100, 100, 85, 94, 60, 78], # VIP Champions
        3: [58, 48, 39, 0, 55, 10],    # At-Risk Delivery
    }
    
    fig_radar = go.Figure()
    for c_id in range(4):
        vals = radar_data[c_id]
        vals_closed = vals + [vals[0]]
        cats_closed = categories + [categories[0]]
        fig_radar.add_trace(go.Scatterpolar(
            r=vals_closed,
            theta=cats_closed,
            fill='toself',
            name=f"{CLUSTER_PROFILES[c_id]['badge']} {CLUSTER_PROFILES[c_id]['name'].split('(')[0].strip()}",
            line_color=CLUSTER_PROFILES[c_id]['color'],
            opacity=0.65
        ))
        
    fig_radar.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100], tickfont=dict(size=10))
        ),
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.25, xanchor="center", x=0.5),
        margin=dict(t=20, b=50, l=40, r=40),
        height=450
    )
    st.plotly_chart(fig_radar, use_container_width=True)


# =========================================================
# TAB 2: CHÂN DUNG 4 PHÂN KHÚC
# =========================================================
elif "2. Chân dung" in menu:
    st.subheader("👥 Khám phá Chân dung Chi tiết Từng Phân khúc Khách hàng")
    
    selected_c = st.selectbox(
        "Chọn phân khúc khách hàng cần phân tích:",
        options=[0, 1, 2, 3],
        format_func=lambda c: f"{CLUSTER_PROFILES[c]['badge']} Cụm {c}: {CLUSTER_PROFILES[c]['name']} ({CLUSTER_PROFILES[c]['pct']}%)"
    )
    
    prof = CLUSTER_PROFILES[selected_c]
    
    # Profile Card
    st.markdown(f"""
    <div style="background-color: {prof['color']}; padding: 18px 24px; border-radius: 10px; color: white; margin-bottom: 20px;">
        <h3 style="margin:0; font-size:1.4rem;">{prof['badge']} {prof['name']}</h3>
        <p style="margin:6px 0 0 0; opacity:0.95; font-size:1rem;">{prof['desc']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 4 metrics
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Quy mô phân khúc", f"{prof['count']:,} khách", f"{prof['pct']}% toàn sàn")
    m2.metric("Chi tiêu trung bình", f"{prof['monetary']} BRL", f"Tần suất: {prof['frequency']} đơn")
    m3.metric("Điểm Review TB", f"{prof['review']} ⭐", f"Trễ hạn: {prof['delay_rate']}%")
    m4.metric("Tỷ trọng Phí ship", f"{prof['freight_ratio']}%", f"Giao TB: {prof['delivery_days']} ngày")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_geo, col_action = st.columns([1, 1])
    
    with col_geo:
        st.markdown("##### 📍 Phân bố Địa lý theo Bang (Top 5 States)")
        sub_df = df_all[df_all['cluster'] == selected_c]
        top_states = sub_df['customer_state'].value_counts().head(5).reset_index()
        top_states.columns = ['Bang (State)', 'Số lượng khách']
        
        fig_states = px.bar(
            top_states,
            x='Bang (State)',
            y='Số lượng khách',
            color='Số lượng khách',
            color_continuous_scale=[[0, '#cbd5e1'], [1, prof['color']]],
            text='Số lượng khách'
        )
        fig_states.update_layout(height=280, margin=dict(t=10, b=10, l=10, r=10), coloraxis_showscale=False)
        st.plotly_chart(fig_states, use_container_width=True)
        
    with col_action:
        st.markdown("##### 🎯 Khuyến nghị Chiến lược Kinh doanh (Action Plan)")
        st.markdown(f"""
        <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:8px; padding:16px; margin-bottom:12px;">
            <b style="color:#0284c7;">📢 Chiến lược Tiếp thị (Thành viên C):</b><br>
            <span style="font-size:0.95rem; color:#334155;">{prof['marketing']}</span>
        </div>
        <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:8px; padding:16px;">
            <b style="color:#10b981;">🚚 Đề xuất Cải thiện SLA Vận hành (Thành viên B):</b><br>
            <span style="font-size:0.95rem; color:#334155;">{prof['sla']}</span>
        </div>
        """, unsafe_allow_html=True)


# =========================================================
# TAB 3: TRA CỨU HỒ SƠ KHÁCH HÀNG
# =========================================================
elif "3. Tra cứu" in menu:
    st.subheader("🔍 Tra cứu & Chẩn đoán Hồ sơ Khách hàng Độc lập")
    st.markdown("Hệ thống cho phép nhân viên kinh doanh / CSKH kiểm tra tức thời thông tin, lịch sử đơn hàng và phân khúc của khách hàng.")
    
    # Khách hàng mẫu đại diện từ mỗi cụm
    sample_customers = {
        "VIP Champion tiêu biểu (Cụm 2 - Mua 3 đơn, chi 890 BRL)": df_all[df_all['cluster'] == 2].iloc[0]['customer_unique_id'],
        "Phổ thông hài lòng (Cụm 1 - 250 BRL, 5 sao)": df_all[df_all['cluster'] == 1].iloc[0]['customer_unique_id'],
        "Nhạy cảm phí ship (Cụm 0 - Đơn 45 BRL, Ship 40%)": df_all[df_all['cluster'] == 0].iloc[0]['customer_unique_id'],
        "Khách chịu giao trễ nghiêm trọng (Cụm 3 - Trễ 40 ngày, 1 sao)": df_all[df_all['cluster'] == 3].iloc[0]['customer_unique_id'],
    }
    
    c_pick, c_input = st.columns([1, 1])
    with c_pick:
        sample_choice = st.selectbox("Chọn khách hàng mẫu nhanh:", list(sample_customers.keys()))
        default_id = sample_customers[sample_choice]
    with c_input:
        search_id = st.text_input("Hoặc nhập Customer Unique ID:", value=default_id)
        
    cust = df_all[df_all['customer_unique_id'] == search_id.strip()]
    
    if cust.empty:
        st.warning("⚠️ Không tìm thấy khách hàng với mã ID này trong tập 93,350 khách hàng Olist.")
    else:
        row = cust.iloc[0]
        c_id = int(row['cluster'])
        prof = CLUSTER_PROFILES[c_id]
        
        st.markdown("---")
        
        info_col, chart_col = st.columns([1, 1])
        
        with info_col:
            st.markdown(f"""
            <div style="background:white; border:2px solid {prof['color']}; border-radius:12px; padding:20px; box-shadow:0 4px 6px rgba(0,0,0,0.05);">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <span style="background:{prof['color']}; color:white; padding:4px 12px; border-radius:20px; font-weight:bold; font-size:0.85rem;">
                        {prof['badge']} Cụm {c_id}: {prof['name']}
                    </span>
                    <span style="color:#64748b; font-size:0.85rem;">Bang: <b>{row['customer_state']}</b> ({row['customer_city']})</span>
                </div>
                <h4 style="margin:12px 0 6px 0; word-break:break-all; font-size:1.1rem; color:#1e293b;">ID: {row['customer_unique_id']}</h4>
                <hr style="margin:10px 0;">
                <p style="margin:4px 0;">📅 <b>Ngày mua gần nhất:</b> {row['recency']} ngày trước</p>
                <p style="margin:4px 0;">🛍️ <b>Số lượng đơn hàng:</b> {row['frequency']} đơn ({row['total_items']} sản phẩm)</p>
                <p style="margin:4px 0;">💰 <b>Tổng chi tiêu:</b> {row['monetary']:,.2f} BRL</p>
                <p style="margin:4px 0;">🚚 <b>Phí vận chuyển:</b> {row['total_freight']:,.2f} BRL (Chiếm {row['freight_ratio']*100:.1f}% đơn)</p>
                <p style="margin:4px 0;">⏱️ <b>Thời gian giao hàng:</b> {row['avg_delivery_duration_days']:.1f} ngày (Trễ hẹn: {'Có ⚠️' if row['delayed_order_ratio'] > 0 else 'Không ✓'})</p>
                <p style="margin:4px 0;">⭐ <b>Điểm đánh giá review:</b> {row['avg_review_score']:.1f} / 5.0 sao</p>
                <p style="margin:4px 0;">💳 <b>Phương thức thanh toán:</b> {row['primary_payment_type']} (Trả góp: {row['avg_payment_installments']:.0f} kỳ)</p>
            </div>
            """, unsafe_allow_html=True)
            
        with chart_col:
            st.markdown("##### 🩺 Chẩn đoán Sức khỏe & Hành động Tiếp thị")
            
            # Health gauge
            health_score = int(row['avg_review_score'] * 20 - (row['delayed_order_ratio'] * 30))
            health_score = max(5, min(100, health_score))
            
            fig_gauge = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = health_score,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "Chỉ số Sức Khỏe Khách Hàng (Health Score)", 'font': {'size': 14}},
                gauge = {
                    'axis': {'range': [None, 100]},
                    'bar': {'color': prof['color']},
                    'steps': [
                        {'range': [0, 40], 'color': "#fee2e2"},
                        {'range': [40, 75], 'color': "#fef3c7"},
                        {'range': [75, 100], 'color': "#dcfce7"}
                    ],
                }
            ))
            fig_gauge.update_layout(height=240, margin=dict(t=30, b=10, l=20, r=20))
            st.plotly_chart(fig_gauge, use_container_width=True)
            
            st.info(f"💡 **Hành động đề xuất ngay cho khách hàng này:**\n\n{prof['marketing']}")


# =========================================================
# TAB 4: PHÂN LOẠI KHÁCH HÀNG MỚI (LIVE ML)
# =========================================================
elif "4. Phân loại" in menu:
    st.subheader("🤖 Công cụ Phân loại Khách hàng Mới (Live Machine Learning)")
    st.markdown("Nhập các thông số giao dịch của khách hàng mới để mô hình K-Means tự động tính toán khoảng cách vector và phân loại vào cụm tối ưu.")
    
    with st.form("predict_form"):
        f1, f2, f3 = st.columns(3)
        with f1:
            recency = st.slider("Số ngày kể từ lần mua gần nhất (Recency)", min_value=1, max_value=700, value=120)
            frequency = st.number_input("Số lượng đơn hàng (Frequency)", min_value=1, max_value=20, value=1)
            monetary = st.number_input("Tổng giá trị mua hàng (Monetary - BRL)", min_value=10.0, max_value=5000.0, value=150.0)
        with f2:
            delivery_days = st.slider("Thời gian giao hàng thực tế (ngày)", min_value=1.0, max_value=60.0, value=10.0)
            is_delayed = st.selectbox("Đơn hàng có bị giao trễ hẹn không?", ["Giao đúng hạn (0% trễ)", "Giao trễ hẹn (100% trễ)"])
            freight_ratio = st.slider("Tỷ lệ phí ship / Giá trị đơn hàng (%)", min_value=1.0, max_value=80.0, value=15.0)
        with f3:
            review_score = st.slider("Điểm đánh giá dự kiến (Sao)", min_value=1.0, max_value=5.0, value=5.0, step=0.5)
            installments = st.number_input("Số kỳ thanh toán trả góp", min_value=1, max_value=24, value=3)
            payment_type = st.selectbox("Hình thức thanh toán chính", ["credit_card", "boleto", "voucher", "debit_card"])
            
        submitted = st.form_submit_button("⚡ Phân Loại Phân Khúc Ngay", use_container_width=True)
        
    if submitted:
        # Thuật toán phân loại vector K-Means dựa trên khoảng cách tới 4 tâm cụm
        # Centroids chuẩn hóa của 4 cụm trên các chiều: [monetary, frequency, delivery_days, delay_ratio, freight_ratio, review]
        feature_vector = np.array([
            monetary,
            frequency,
            delivery_days,
            1.0 if "trễ" in is_delayed and "Giao trễ" in is_delayed else 0.0,
            freight_ratio / 100.0,
            review_score
        ])
        
        # Trọng số đặc trưng chuẩn hóa
        cluster_centroids = {
            0: np.array([63.23, 1.0, 10.5, 0.026, 0.288, 4.34]),   # Freight-Sensitive
            1: np.array([251.95, 1.0, 11.7, 0.027, 0.132, 4.24]),  # Satisfied Mainstream
            2: np.array([309.22, 2.11, 12.1, 0.061, 0.198, 4.24]), # VIP Champions
            3: np.array([179.94, 1.01, 36.5, 1.0, 0.213, 1.96]),   # At-Risk Delivery
        }
        
        # Tính khoảng cách chuẩn hóa có scale trọng số
        scales = np.array([300.0, 2.0, 30.0, 1.0, 0.3, 4.0])
        distances = {}
        for c, centroid in cluster_centroids.items():
            dist = np.linalg.norm((feature_vector - centroid) / scales)
            distances[c] = dist
            
        pred_c = min(distances, key=distances.get)
        confidence = round((1 - distances[pred_c] / sum(distances.values())) * 100, 1)
        
        prof = CLUSTER_PROFILES[pred_c]
        
        st.success(f"🎯 **KẾT QUẢ DỰ BÁO:** Khách hàng thuộc **Cụm {pred_c}: {prof['name']}** (Độ tin cậy mô hình: {confidence}%)")
        
        res_col1, res_col2 = st.columns([1, 1])
        with res_col1:
            st.markdown(f"""
            <div style="background:{prof['color']}; padding:20px; border-radius:10px; color:white;">
                <h3 style="margin:0;">{prof['badge']} {prof['name']}</h3>
                <p style="margin:8px 0 0 0; font-size:1rem;">{prof['desc']}</p>
            </div>
            """, unsafe_allow_html=True)
        with res_col2:
            st.markdown(f"""
            <div style="background:#f8fafc; border:1px solid #cbd5e1; padding:20px; border-radius:10px;">
                <h4 style="margin:0 0 8px 0; color:#0f172a;">📋 Hướng Dẫn Tác Nghiệp Tức Thì:</h4>
                <p style="margin:4px 0;">• <b>Chính sách tiếp thị:</b> {prof['marketing']}</p>
                <p style="margin:4px 0;">• <b>Tiêu chuẩn vận hành:</b> {prof['sla']}</p>
            </div>
            """, unsafe_allow_html=True)


# =========================================================
# TAB 5: MÔ PHỎNG KỊCH BẢN KINH DOANH (WHAT-IF)
# =========================================================
elif "5. Mô phỏng" in menu:
    st.subheader("🎯 Mô phỏng Kịch bản Kinh doanh Thời gian thực (What-If Simulation)")
    st.markdown("Công cụ hỗ trợ Ban giám đốc và Trưởng phòng kinh doanh mô phỏng tác động tài chính khi điều chỉnh chính sách phí ship hoặc cải thiện chất lượng SLA logistics.")
    
    sim1, sim2 = st.columns(2)
    with sim1:
        freight_discount = st.slider("Mức trợ giá Phí vận chuyển cho khách (Freight Discount %):", min_value=0, max_value=50, value=20, step=5)
    with sim2:
        sla_improvement = st.slider("Rút ngắn thời gian giao hàng chặng cuối (SLA Improvement - ngày):", min_value=0, max_value=15, value=5, step=1)
        
    st.markdown("---")
    
    # Tính toán mô phỏng tác động
    # 1. Nhóm Freight-Sensitive: 41,790 khách
    converted_fs_rate = freight_discount * 0.006  # Mỗi 10% giảm phí ship tăng 6% tỷ lệ mua lặp lại
    converted_fs_count = int(41790 * converted_fs_rate)
    extra_revenue_fs = converted_fs_count * 150.0  # Chi tiêu đơn lặp lại
    
    # 2. Nhóm At-Risk: 5,183 khách
    saved_at_risk_rate = min(0.70, (sla_improvement / 15.0) * 0.65)
    saved_at_risk_count = int(5183 * saved_at_risk_rate)
    extra_revenue_risk = saved_at_risk_count * 179.94
    
    # Tăng điểm CSAT
    csat_gain = round((freight_discount * 0.005) + (sla_improvement * 0.035), 2)
    new_csat = min(5.0, round(4.15 + csat_gain, 2))
    
    total_extra_rev = extra_revenue_fs + extra_revenue_risk
    
    sc1, sc2, sc3, sc4 = st.columns(4)
    sc1.metric("Khách chuyển đổi Mua Lặp Lại", f"+{converted_fs_count:,} khách", f"+{converted_fs_rate*100:.1f}% nhóm Phí ship")
    sc2.metric("Khách được cứu khỏi Nguy cơ Rời Bỏ", f"+{saved_at_risk_count:,} khách", f"Giảm {saved_at_risk_rate*100:.1f}% nhóm At-Risk")
    sc3.metric("Điểm Review CSAT Toàn Sàn", f"{new_csat} ⭐", f"+{csat_gain} sao tăng thêm")
    sc4.metric("Doanh thu Tăng thêm Ước tính", f"+{total_extra_rev:,.0f} BRL", f"~ {total_extra_rev*5.0:,.0f}k VNĐ")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Visual so sánh trước và sau can thiệp
    sim_col_chart, sim_col_txt = st.columns([1, 1])
    with sim_col_chart:
        st.markdown("##### 📈 Tác động Chuyển dịch Cơ cấu Khách hàng sau Mô phỏng")
        comp_df = pd.DataFrame({
            "Phân khúc": ["VIP / Khách Trung Thành", "At-Risk (Rủi ro cao)"],
            "Hiện tại (Baseline)": [2775, 5183],
            "Sau khi tối ưu chính sách": [2775 + converted_fs_count, 5183 - saved_at_risk_count]
        })
        fig_comp = go.Figure(data=[
            go.Bar(name='Hiện tại (Baseline)', x=comp_df["Phân khúc"], y=comp_df["Hiện tại (Baseline)"], marker_color='#94a3b8'),
            go.Bar(name='Sau tối ưu chính sách', x=comp_df["Phân khúc"], y=comp_df["Sau khi tối ưu chính sách"], marker_color='#10b981')
        ])
        fig_comp.update_layout(barmode='group', height=300, margin=dict(t=10, b=10, l=10, r=10))
        st.plotly_chart(fig_comp, use_container_width=True)
        
    with sim_col_txt:
        st.markdown("##### 📌 Kết luận Chiến lược cho Ban Điều Hành:")
        st.markdown(f"""
        1. **Hiệu quả trợ giá vận chuyển {freight_discount}%**: Giúp kích hoạt thêm **{converted_fs_count:,} khách hàng** trong nhóm *Freight-Sensitive* quay trở lại mua sắm lần 2, mang lại thêm **{extra_revenue_fs:,.0f} BRL** doanh thu mà không cần tốn chi phí chạy quảng cáo tìm khách hàng mới (CAC).
        2. **Hiệu quả rút ngắn {sla_improvement} ngày giao hàng**: Cứu vãn được **{saved_at_risk_count:,} khách hàng** khỏi nguy cơ rời bỏ sàn và ngăn chặn hàng ngàn đánh giá tiêu cực 1 sao làm tổn hại uy tín thương hiệu Olist.
        3. **ROI (Tỷ suất sinh lời)**: Chính sách kết hợp vừa trợ giá vừa siết SLA logistics mang lại tổng giá trị cộng thêm **+{total_extra_rev:,.0f} BRL** (~{total_extra_rev*5.0:,.0f}k VNĐ), chứng minh tính khả thi cao khi ứng dụng vào thực tế các sàn TMĐT tại Việt Nam như Shopee, Tiki, Lazada.
        """)

# Footer
st.markdown("---")
st.caption("Bản quyền © 2026 Nhóm Nghiên Cứu Olist - Khoa Công nghệ Thông tin - Trường Đại học Công Thương TP.HCM (HUIT).")
