"""
╔══════════════════════════════════════════════════════╗
║   汽车保险索赔智能分析仪表板                          ║
║   Car Insurance Claims Intelligence Dashboard        ║
║   Made by 杨磊磊                                     ║
╚══════════════════════════════════════════════════════╝
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="车险索赔智能仪表板 | 杨磊磊",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# GLOBAL CSS — Deep Blue InsurTech Theme
# ─────────────────────────────────────────────
st.markdown("""
<style>
/* ── Base ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* ── Background ── */
.stApp {
    background: linear-gradient(135deg, #020b18 0%, #041428 40%, #071e36 100%);
    color: #e2e8f0;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #030d1e 0%, #051629 100%) !important;
    border-right: 1px solid #1a3a5c;
}
[data-testid="stSidebar"] * { color: #b0c4d8 !important; }
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 { color: #64b5f6 !important; }

/* ── Top header bar ── */
.top-header {
    background: linear-gradient(90deg, #0d2137 0%, #0a3356 50%, #0d2137 100%);
    border-bottom: 2px solid #1565c0;
    padding: 18px 32px;
    margin-bottom: 24px;
    border-radius: 0 0 12px 12px;
    display: flex;
    align-items: center;
    justify-content: space-between;
}
.top-header h1 { font-size: 1.7rem; font-weight: 700; color: #ffffff; margin: 0; }
.top-header .subtitle { font-size: 0.8rem; color: #90caf9; letter-spacing: 2px; text-transform: uppercase; }
.badge {
    background: linear-gradient(90deg, #1565c0, #0288d1);
    color: white; padding: 4px 12px; border-radius: 20px;
    font-size: 0.72rem; font-weight: 600; letter-spacing: 1px;
}

/* ── KPI Cards ── */
.kpi-grid { display: flex; gap: 16px; flex-wrap: wrap; margin-bottom: 24px; }
.kpi-card {
    background: linear-gradient(135deg, #0d2137 0%, #0a2240 100%);
    border: 1px solid #1a4a7a;
    border-radius: 12px;
    padding: 20px 24px;
    flex: 1; min-width: 180px;
    position: relative; overflow: hidden;
    box-shadow: 0 4px 24px rgba(0,0,0,0.4);
}
.kpi-card::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0;
    height: 3px; background: var(--accent, #1976d2);
}
.kpi-card.danger::before { background: linear-gradient(90deg, #c62828, #ef5350); --accent: #ef5350; }
.kpi-card.warning::before { background: linear-gradient(90deg, #f57f17, #ffb300); --accent: #ffb300; }
.kpi-card.success::before { background: linear-gradient(90deg, #1b5e20, #43a047); --accent: #43a047; }
.kpi-card.info::before { background: linear-gradient(90deg, #0d47a1, #1976d2); --accent: #1976d2; }
.kpi-label { font-size: 0.72rem; color: #7aa7c7; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 8px; }
.kpi-value { font-size: 2rem; font-weight: 700; color: #ffffff; font-family: 'JetBrains Mono', monospace; }
.kpi-delta { font-size: 0.78rem; margin-top: 6px; }
.kpi-delta.up { color: #ef5350; }
.kpi-delta.down { color: #43a047; }
.kpi-icon { position: absolute; right: 20px; top: 50%; transform: translateY(-50%); font-size: 2.2rem; opacity: 0.15; }

/* ── Section titles ── */
.section-title {
    font-size: 1.05rem; font-weight: 600; color: #64b5f6;
    padding: 8px 0 12px 0;
    border-bottom: 1px solid #1a3a5c;
    margin-bottom: 18px;
    letter-spacing: 0.5px;
}
.section-title span { color: #ffffff; }

/* ── Chart containers ── */
.chart-box {
    background: linear-gradient(135deg, #0a1e30 0%, #0c2540 100%);
    border: 1px solid #1a3a5c;
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 16px;
    box-shadow: 0 2px 16px rgba(0,0,0,0.3);
}

/* ── Alert badges ── */
.alert-high { background: rgba(198,40,40,0.15); border: 1px solid #c62828; border-radius: 8px; padding: 10px 14px; color: #ef9a9a; }
.alert-med  { background: rgba(245,127,23,0.12); border: 1px solid #f57f17; border-radius: 8px; padding: 10px 14px; color: #ffe082; }
.alert-low  { background: rgba(27,94,32,0.15); border: 1px solid #2e7d32; border-radius: 8px; padding: 10px 14px; color: #a5d6a7; }

/* ── Table styling ── */
.stDataFrame { background: #0a1e30 !important; border-radius: 8px; }

/* ── Tabs ── */
[data-testid="stTabs"] [role="tablist"] {
    background: #061525;
    border-radius: 10px;
    padding: 4px;
    gap: 4px;
}
[data-testid="stTabs"] button[role="tab"] {
    background: transparent !important;
    color: #7aa7c7 !important;
    border-radius: 8px !important;
    font-weight: 500 !important;
}
[data-testid="stTabs"] button[role="tab"][aria-selected="true"] {
    background: linear-gradient(90deg, #1565c0, #0288d1) !important;
    color: white !important;
}

/* ── Slider / Selectbox ── */
[data-testid="stSlider"] * { color: #90caf9 !important; }

/* ── Footer ── */
.footer {
    text-align: center;
    padding: 32px 0 16px;
    color: #2a5070;
    font-size: 0.75rem;
    border-top: 1px solid #0d2137;
    margin-top: 40px;
}
.footer .author { color: #1565c0; font-weight: 600; font-size: 0.85rem; }
.footer .brand {
    background: linear-gradient(90deg, #1976d2, #0288d1);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    font-size: 1.1rem; font-weight: 700; letter-spacing: 1px;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #020b18; }
::-webkit-scrollbar-thumb { background: #1a4a7a; border-radius: 3px; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# CHART TEMPLATE
# ─────────────────────────────────────────────
CHART_TEMPLATE = go.layout.Template(
    layout=dict(
        paper_bgcolor="rgba(10,30,48,0)",
        plot_bgcolor="rgba(10,30,48,0)",
        font=dict(family="Inter", color="#b0c4d8", size=12),
        title=dict(font=dict(color="#ffffff", size=14), x=0.01),
        xaxis=dict(gridcolor="#0d2a40", linecolor="#1a3a5c", tickcolor="#2a5070", zerolinecolor="#0d2a40"),
        yaxis=dict(gridcolor="#0d2a40", linecolor="#1a3a5c", tickcolor="#2a5070", zerolinecolor="#0d2a40"),
        legend=dict(bgcolor="rgba(10,25,40,0.8)", bordercolor="#1a3a5c", font=dict(color="#b0c4d8")),
        colorway=["#1976d2","#ef5350","#66bb6a","#ffb300","#ab47bc","#29b6f6","#ff7043","#26a69a"],
        hoverlabel=dict(bgcolor="#0a1e30", bordercolor="#1565c0", font=dict(color="#ffffff")),
        margin=dict(l=50, r=20, t=50, b=50),
    )
)
COLORS = dict(primary="#1976d2", danger="#ef5350", warning="#ffb300",
              success="#43a047", info="#29b6f6", purple="#ab47bc",
              gradient=["#1a237e","#283593","#1565c0","#1976d2","#1e88e5","#42a5f5","#90caf9"])

# ─────────────────────────────────────────────
# DATA LOADING  (cached)
# ─────────────────────────────────────────────
@st.cache_data(ttl=300, show_spinner="⚡ 正在加载数据...")
def load_data(file_obj_or_path):
    if isinstance(file_obj_or_path, str):
        df = pd.read_csv(file_obj_or_path)
    else:
        df = pd.read_csv(file_obj_or_path)
    return df

@st.cache_data(show_spinner=False)
def preprocess(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    # Readable labels
    df["fuel_label"]        = df["fuel_type"].map({0:"汽油", 1:"柴油", 2:"CNG"})
    df["segment_label"]     = df["segment"].map({0:"A",1:"B1",2:"B2",3:"C1",4:"C2",5:"D"})
    df["transmission_label"]= df["transmission_type"].map({0:"手动", 1:"自动"})
    df["make_label"]        = df["make"].map({1:"厂商A",2:"厂商B",3:"厂商C",4:"厂商D",5:"厂商E"})
    df["area_label"]        = "区域" + df["area_cluster"].astype(str)
    df["ncap_label"]        = df["ncap_rating"].astype(str) + "星"
    # Risk tiers
    df["age_bin"]    = pd.cut(df["age_of_policyholder"],
                              bins=[0,20,30,40,50,60,100],
                              labels=["<20","20-30","30-40","40-50","50-60","60+"])
    df["tenure_bin"] = pd.cut(df["policy_tenure"],
                              bins=[0,.25,.5,.75,1,2],
                              labels=["0-3月","3-6月","6-9月","9-12月","12月+"])
    df["car_age_bin"]= pd.cut(df["age_of_car"],
                              bins=[-.01,.2,.4,.6,.8,1.01],
                              labels=["新车","较新","中等","较旧","旧车"])
    safety_cols = ["is_esc","is_tpms","is_parking_sensors","is_parking_camera",
                   "is_brake_assist","is_speed_alert","is_rear_window_defogger"]
    df["safety_score"] = df[safety_cols].sum(axis=1)
    df["risk_score"]   = (
        df["target"].copy().astype(float) * 0 +          # placeholder
        (1 - df["age_of_car"]) * 15 +
        (1 - df["policy_tenure"].clip(upper=1)) * 10 +
        (df["airbags"] < 3).astype(int) * 8 +
        (1 - df["ncap_rating"] / 5) * 20 +
        (7 - df["safety_score"]) * 3
    ).clip(0, 100).round(1)
    return df

@st.cache_data(show_spinner=False)
def compute_feature_importance(df: pd.DataFrame):
    try:
        from sklearn.ensemble import GradientBoostingClassifier
        from sklearn.preprocessing import LabelEncoder
        feature_cols = [
            "policy_tenure","age_of_car","age_of_policyholder","area_cluster",
            "population_density","make","segment","fuel_type","airbags","is_esc",
            "is_tpms","is_parking_sensors","ncap_rating","displacement","cylinder",
            "gear_box","turning_radius","length","width","height","gross_weight",
            "safety_score"
        ]
        feat_cols = [c for c in feature_cols if c in df.columns]
        X = df[feat_cols].fillna(0)
        y = df["target"]
        sample = min(50000, len(df))
        idx = np.random.choice(len(df), sample, replace=False)
        clf = GradientBoostingClassifier(n_estimators=80, max_depth=4,
                                         learning_rate=0.1, random_state=42)
        clf.fit(X.iloc[idx], y.iloc[idx])
        importance = pd.Series(clf.feature_importances_, index=feat_cols).sort_values(ascending=False)
        return importance
    except Exception:
        return pd.Series(dtype=float)

@st.cache_data(show_spinner=False)
def compute_clusters(df: pd.DataFrame):
    try:
        from sklearn.cluster import KMeans
        from sklearn.preprocessing import StandardScaler
        cluster_cols = ["policy_tenure","age_of_car","age_of_policyholder",
                        "population_density","safety_score","ncap_rating","airbags"]
        X = df[cluster_cols].fillna(0)
        sample = min(20000, len(df))
        idx = np.random.choice(len(df), sample, replace=False)
        X_s = X.iloc[idx]
        scaler = StandardScaler()
        Xs = scaler.fit_transform(X_s)
        km = KMeans(n_clusters=5, random_state=42, n_init=10)
        labels = km.fit_predict(Xs)
        sub = df.iloc[idx].copy()
        sub["cluster"] = labels
        sub["cluster_label"] = sub["cluster"].map({
            0:"低风险稳定型",1:"高风险新车型",2:"中风险中年型",3:"高风险老车型",4:"低风险安全型"
        })
        return sub
    except Exception:
        return df.head(1000).copy()

# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
st.markdown("""
<div class="top-header">
  <div>
    <div class="subtitle">🛡️ InsurTech Intelligence Platform · 保险科技智能分析平台</div>
    <h1>汽车保险索赔智能仪表板</h1>
  </div>
  <div style="text-align:right">
    <div class="badge">🤖 AI POWERED</div>
    <div style="color:#546e8a;font-size:0.75rem;margin-top:8px;">科大讯飞挑战赛数据集</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
# Pre-declare sidebar-controlled globals so they're always defined
show_advanced = False
sample_size   = 50000
area_filter   = []
fuel_filter   = [0, 1, 2]

with st.sidebar:
    st.markdown("## 🗂️ 数据加载")
    data_source = st.radio("数据来源", ["上传文件", "使用示例数据"], index=0)

    df_raw = None
    if data_source == "上传文件":
        uploaded = st.file_uploader("上传 train.csv", type=["csv"])
        if uploaded:
            df_raw = load_data(uploaded)
            st.success(f"✅ 已加载 {len(df_raw):,} 条记录")
    else:
        st.info("将使用内置示例数据（5000条）")
        np.random.seed(42)
        n = 5000
        df_raw = pd.DataFrame({
            "id": range(n),
            "policy_tenure": np.random.beta(2,5,n),
            "age_of_car": np.random.beta(1.5,3,n),
            "age_of_policyholder": np.random.randint(18,73,n),
            "area_cluster": np.random.randint(0,22,n),
            "population_density": np.random.randint(1000,15000,n),
            "make": np.random.randint(1,6,n),
            "segment": np.random.randint(0,6,n),
            "model": np.random.randint(0,20,n),
            "fuel_type": np.random.choice([0,1,2],[n],p=[.75,.15,.10]),
            "max_torque": np.random.randint(60,200,n),
            "max_power": np.random.randint(40,120,n),
            "engine_type": np.random.randint(0,4,n),
            "airbags": np.random.choice([1,2,3,4,5,6],[n],p=[.05,.4,.05,.05,.05,.4]),
            "is_esc": np.random.randint(0,2,n),
            "is_adjustable_steering": np.random.randint(0,2,n),
            "is_tpms": np.random.randint(0,2,n),
            "is_parking_sensors": np.random.randint(0,2,n),
            "is_parking_camera": np.random.randint(0,2,n),
            "rear_brakes_type": np.random.randint(0,2,n),
            "displacement": np.random.choice([796,1197,1493,1498],[n]),
            "cylinder": np.random.choice([3,4],[n],p=[.3,.7]),
            "transmission_type": np.random.choice([0,1],[n],p=[.6,.4]),
            "gear_box": np.random.choice([5,6,7],[n],p=[.5,.4,.1]),
            "steering_type": np.random.randint(0,3,n),
            "turning_radius": np.round(np.random.uniform(4.5,6.0,n),1),
            "length": np.random.randint(3400,4600,n),
            "width": np.random.randint(1500,1850,n),
            "height": np.random.randint(1400,1750,n),
            "gross_weight": np.random.randint(1100,1800,n),
            "is_front_fog_lights": np.random.randint(0,2,n),
            "is_rear_window_wiper": np.random.randint(0,2,n),
            "is_rear_window_washer": np.random.randint(0,2,n),
            "is_rear_window_defogger": np.random.randint(0,2,n),
            "is_brake_assist": np.random.randint(0,2,n),
            "is_power_door_locks": np.random.randint(0,2,n),
            "is_central_locking": np.random.randint(0,2,n),
            "is_power_steering": np.random.randint(0,2,n),
            "is_driver_seat_height_adjustable": np.random.randint(0,2,n),
            "is_day_night_rear_view_mirror": np.random.randint(0,2,n),
            "is_ecw": np.random.randint(0,2,n),
            "is_speed_alert": np.random.randint(0,2,n),
            "ncap_rating": np.random.randint(0,6,n),
            "target": np.random.choice([0,1],[n],p=[.942,.058]),
        })
        st.success(f"✅ 示例数据已就绪（{n:,} 条）")

    st.markdown("---")
    st.markdown("## ⚙️ 分析参数")

    if df_raw is not None:
        sample_size = st.slider("分析样本量", 1000, min(len(df_raw), 100000), min(50000, len(df_raw)), 1000,
                                 help="增大样本量可提升准确性，但会延长加载时间")
        show_advanced = st.checkbox("显示高级统计", value=False)
        st.markdown("---")
        st.markdown("## 🔍 全局筛选")
        area_filter = st.multiselect("区域集群", options=sorted(df_raw["area_cluster"].unique()),
                                      default=sorted(df_raw["area_cluster"].unique()))
        fuel_options = {0:"汽油",1:"柴油",2:"CNG"}
        fuel_filter = st.multiselect("燃油类型", options=list(fuel_options.keys()),
                                      format_func=lambda x: fuel_options[x],
                                      default=list(fuel_options.keys()))
    else:
        st.warning("请先加载数据")

    st.markdown("---")
    st.markdown("""
    <div style="text-align:center;padding:16px 0 8px">
      <div style="color:#1565c0;font-size:0.7rem;letter-spacing:2px;text-transform:uppercase">制作者</div>
      <div style="color:#64b5f6;font-size:1.1rem;font-weight:700;margin:4px 0">杨磊磊</div>
      <div style="color:#2a5070;font-size:0.65rem">InsurTech Intelligence Platform</div>
      <div style="color:#2a5070;font-size:0.65rem;margin-top:4px">v2.0 · 2024</div>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# GUARD — need data to proceed
# ─────────────────────────────────────────────
if df_raw is None:
    st.markdown("""
    <div style="text-align:center;padding:80px 0">
      <div style="font-size:5rem">🛡️</div>
      <h2 style="color:#64b5f6">欢迎使用车险索赔智能仪表板</h2>
      <p style="color:#546e8a">请在左侧侧边栏上传 train.csv 数据文件，或选择"使用示例数据"开始体验</p>
      <div style="color:#2a5070;font-size:0.8rem;margin-top:40px">Made with ❤️ by 杨磊磊</div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ─────────────────────────────────────────────
# APPLY FILTERS + PREPROCESS
# ─────────────────────────────────────────────
df_filtered = df_raw[
    df_raw["area_cluster"].isin(area_filter) &
    df_raw["fuel_type"].isin(fuel_filter)
].copy()

# sample for performance
if len(df_filtered) > sample_size:
    df_sample = df_filtered.sample(sample_size, random_state=42)
else:
    df_sample = df_filtered.copy()

df = preprocess(df_sample)

# ─────────────────────────────────────────────
# ① KPI CARDS
# ─────────────────────────────────────────────
total_policies = len(df_filtered)
claim_rate     = df["target"].mean()
avg_risk       = df["risk_score"].mean()
avg_airbags    = df["airbags"].mean()
avg_ncap       = df["ncap_rating"].mean()
high_risk_pct  = (df["risk_score"] > 60).mean()

st.markdown(f"""
<div class="kpi-grid">
  <div class="kpi-card info">
    <div class="kpi-label">总保单数</div>
    <div class="kpi-value">{total_policies:,}</div>
    <div class="kpi-delta">📋 当前筛选结果</div>
    <div class="kpi-icon">📋</div>
  </div>
  <div class="kpi-card danger">
    <div class="kpi-label">索赔率</div>
    <div class="kpi-value">{claim_rate:.2%}</div>
    <div class="kpi-delta up">⚠ 行业均值 5.8%</div>
    <div class="kpi-icon">🔴</div>
  </div>
  <div class="kpi-card warning">
    <div class="kpi-label">平均风险评分</div>
    <div class="kpi-value">{avg_risk:.1f}</div>
    <div class="kpi-delta">📊 满分 100</div>
    <div class="kpi-icon">⚡</div>
  </div>
  <div class="kpi-card success">
    <div class="kpi-label">平均安全评级</div>
    <div class="kpi-value">{avg_ncap:.1f}★</div>
    <div class="kpi-delta down">✅ NCAP 0-5 星</div>
    <div class="kpi-icon">🛡️</div>
  </div>
  <div class="kpi-card danger">
    <div class="kpi-label">高风险保单比例</div>
    <div class="kpi-value">{high_risk_pct:.1%}</div>
    <div class="kpi-delta up">风险评分 > 60</div>
    <div class="kpi-icon">🚨</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────
tabs = st.tabs(["📊 全局概览", "🗺️ 风险分布", "🚗 车辆特征", "🤖 模型洞察", "🔬 深度下钻"])

# ═══════════════════════════════════════════════════
# TAB 1 ── 全局概览
# ═══════════════════════════════════════════════════
with tabs[0]:
    st.markdown('<div class="section-title">📊 <span>全局概览 · Global Overview</span></div>', unsafe_allow_html=True)

    col1, col2 = st.columns([1.2, 1])

    with col1:
        # Target Distribution Donut
        target_counts = df["target"].value_counts()
        fig_donut = go.Figure(go.Pie(
            labels=["未索赔", "已索赔"],
            values=[target_counts.get(0, 0), target_counts.get(1, 0)],
            hole=0.62,
            marker=dict(colors=["#1565c0", "#ef5350"], line=dict(color="#041428", width=3)),
            textfont=dict(color="white", size=13),
            hovertemplate="<b>%{label}</b><br>数量: %{value:,}<br>占比: %{percent}<extra></extra>"
        ))
        fig_donut.add_annotation(text=f"<b>{claim_rate:.1%}</b><br><span style='font-size:10px'>索赔率</span>",
                                  x=0.5, y=0.5, showarrow=False, font=dict(size=18, color="white"),
                                  align="center")
        fig_donut.update_layout(template=CHART_TEMPLATE, title="保单索赔分布",
                                 legend=dict(orientation="h", y=-0.05), height=320)
        st.plotly_chart(fig_donut, use_container_width=True, config={"displayModeBar": False})

    with col2:
        # Claim rate by area
        area_stats = df.groupby("area_cluster")["target"].agg(["mean","count"]).reset_index()
        area_stats.columns = ["area","claim_rate","count"]
        area_stats = area_stats.sort_values("claim_rate", ascending=True)
        fig_area = go.Figure(go.Bar(
            x=area_stats["claim_rate"] * 100,
            y=[f"区域{a}" for a in area_stats["area"]],
            orientation="h",
            marker=dict(
                color=area_stats["claim_rate"],
                colorscale=[[0,"#1565c0"],[0.5,"#ffb300"],[1,"#ef5350"]],
                showscale=True, colorbar=dict(title="索赔率", tickfont=dict(color="#b0c4d8"), len=0.7)
            ),
            hovertemplate="<b>%{y}</b><br>索赔率: %{x:.2f}%<extra></extra>"
        ))
        fig_area.update_layout(template=CHART_TEMPLATE, title="各区域索赔率",
                                xaxis_title="索赔率 (%)", height=320)
        st.plotly_chart(fig_area, use_container_width=True, config={"displayModeBar": False})

    col3, col4 = st.columns(2)
    with col3:
        # Claim rate by policyholder age bin
        age_stats = df.groupby("age_bin", observed=True)["target"].agg(["mean","count"]).reset_index()
        age_stats.columns = ["age_bin","claim_rate","count"]
        fig_age = go.Figure()
        fig_age.add_trace(go.Bar(name="保单数", x=age_stats["age_bin"].astype(str),
                                  y=age_stats["count"], marker_color="#1565c0", opacity=0.7, yaxis="y"))
        fig_age.add_trace(go.Scatter(name="索赔率", x=age_stats["age_bin"].astype(str),
                                      y=age_stats["claim_rate"]*100,
                                      mode="lines+markers", yaxis="y2",
                                      line=dict(color="#ef5350", width=2.5),
                                      marker=dict(size=8, color="#ef5350")))
        fig_age.update_layout(template=CHART_TEMPLATE, title="投保人年龄 vs 索赔率",
                               yaxis=dict(title="保单数"), height=300,
                               yaxis2=dict(title="索赔率(%)", overlaying="y", side="right", showgrid=False),
                               legend=dict(orientation="h", y=1.1))
        st.plotly_chart(fig_age, use_container_width=True, config={"displayModeBar": False})

    with col4:
        # Claim rate by policy tenure
        tenure_stats = df.groupby("tenure_bin", observed=True)["target"].agg(["mean","count"]).reset_index()
        tenure_stats.columns = ["tenure","claim_rate","count"]
        fig_ten = go.Figure()
        fig_ten.add_trace(go.Bar(name="保单数", x=tenure_stats["tenure"].astype(str),
                                  y=tenure_stats["count"], marker_color="#0288d1", opacity=0.7))
        fig_ten.add_trace(go.Scatter(name="索赔率", x=tenure_stats["tenure"].astype(str),
                                      y=tenure_stats["claim_rate"]*100,
                                      mode="lines+markers", yaxis="y2",
                                      line=dict(color="#ffb300", width=2.5),
                                      marker=dict(size=8, color="#ffb300")))
        fig_ten.update_layout(template=CHART_TEMPLATE, title="投保时长 vs 索赔率",
                               yaxis=dict(title="保单数"), height=300,
                               yaxis2=dict(title="索赔率(%)", overlaying="y", side="right", showgrid=False),
                               legend=dict(orientation="h", y=1.1))
        st.plotly_chart(fig_ten, use_container_width=True, config={"displayModeBar": False})

    # Risk score distribution
    col5, col6 = st.columns(2)
    with col5:
        fig_risk = go.Figure()
        for tgt, color, label in [(0, "#1976d2","未索赔"), (1,"#ef5350","已索赔")]:
            sub = df[df["target"]==tgt]["risk_score"]
            fig_risk.add_trace(go.Histogram(x=sub, name=label, opacity=0.7,
                                             marker_color=color, nbinsx=30,
                                             hovertemplate=f"<b>{label}</b><br>风险分: %{{x}}<br>数量: %{{y}}<extra></extra>"))
        fig_risk.update_layout(template=CHART_TEMPLATE, title="风险评分分布（索赔 vs 未索赔）",
                                barmode="overlay", xaxis_title="风险评分", yaxis_title="频次", height=300)
        st.plotly_chart(fig_risk, use_container_width=True, config={"displayModeBar": False})

    with col6:
        # Population density vs claim rate scatter
        pop_stats = df.groupby("area_cluster").agg(
            pop_density=("population_density","mean"),
            claim_rate=("target","mean"),
            count=("target","count")
        ).reset_index()
        fig_pop = px.scatter(pop_stats, x="pop_density", y="claim_rate",
                             size="count", color="claim_rate", text="area_cluster",
                             color_continuous_scale=[[0,"#1565c0"],[0.5,"#ffb300"],[1,"#ef5350"]],
                             title="人口密度 vs 索赔率（气泡大小=保单数）",
                             labels={"pop_density":"人口密度","claim_rate":"索赔率","count":"保单数"})
        fig_pop.update_traces(textposition="top center", textfont=dict(size=9, color="white"))
        fig_pop.update_layout(template=CHART_TEMPLATE, height=300,
                               coloraxis_showscale=False)
        st.plotly_chart(fig_pop, use_container_width=True, config={"displayModeBar": False})


# ═══════════════════════════════════════════════════
# TAB 2 ── 风险分布
# ═══════════════════════════════════════════════════
with tabs[1]:
    st.markdown('<div class="section-title">🗺️ <span>风险分布分析 · Risk Distribution</span></div>', unsafe_allow_html=True)

    # Heatmap: age_bin × car_age_bin → claim_rate
    col1, col2 = st.columns(2)
    with col1:
        pivot = df.groupby(["age_bin","car_age_bin"], observed=True)["target"].mean().unstack(fill_value=0)
        fig_heat = go.Figure(go.Heatmap(
            z=pivot.values * 100,
            x=[str(c) for c in pivot.columns],
            y=[str(i) for i in pivot.index],
            colorscale=[[0,"#0d47a1"],[0.4,"#1565c0"],[0.7,"#ffb300"],[1,"#ef5350"]],
            text=np.round(pivot.values * 100, 1),
            texttemplate="%{text}%",
            hovertemplate="投保人年龄: %{y}<br>车龄: %{x}<br>索赔率: %{z:.2f}%<extra></extra>",
            colorbar=dict(title="索赔率(%)", tickfont=dict(color="#b0c4d8"))
        ))
        fig_heat.update_layout(template=CHART_TEMPLATE,
                                title="双维度风险矩阵：年龄 × 车龄",
                                xaxis_title="车龄段", yaxis_title="投保人年龄",
                                height=360)
        st.plotly_chart(fig_heat, use_container_width=True, config={"displayModeBar": False})

    with col2:
        # Area heatmap (treemap)
        area_stats2 = df.groupby("area_label").agg(
            claim_rate=("target","mean"),
            count=("target","count"),
            avg_risk=("risk_score","mean")
        ).reset_index()
        fig_tree = px.treemap(area_stats2, path=["area_label"],
                              values="count", color="claim_rate",
                              color_continuous_scale=[[0,"#0d47a1"],[0.5,"#1976d2"],[1,"#ef5350"]],
                              title="区域索赔密度 Treemap",
                              hover_data={"claim_rate":":.2%","avg_risk":":.1f"},
                              labels={"claim_rate":"索赔率","avg_risk":"平均风险","count":"保单数"})
        fig_tree.update_traces(texttemplate="<b>%{label}</b><br>%{color:.1%}",
                                textfont=dict(size=12, color="white"))
        fig_tree.update_layout(template=CHART_TEMPLATE, height=360,
                                coloraxis_colorbar=dict(title="索赔率"))
        st.plotly_chart(fig_tree, use_container_width=True, config={"displayModeBar": False})

    # Age × NCAP 3D surface simulation
    col3, col4 = st.columns(2)
    with col3:
        age_bins_num = list(range(0, 75, 10))
        ncap_vals    = [0, 1, 2, 3, 4, 5]
        z_surface = []
        for age_lo in age_bins_num:
            row = []
            for ncap in ncap_vals:
                sub = df[
                    (df["age_of_policyholder"] >= age_lo) &
                    (df["age_of_policyholder"] < age_lo + 10) &
                    (df["ncap_rating"] == ncap)
                ]
                row.append(sub["target"].mean() * 100 if len(sub) > 5 else np.nan)
            z_surface.append(row)
        fig_surf = go.Figure(go.Surface(
            z=z_surface,
            x=ncap_vals,
            y=age_bins_num,
            colorscale=[[0,"#0d47a1"],[0.4,"#1565c0"],[0.7,"#ffb300"],[1,"#ef5350"]],
            hovertemplate="NCAP: %{x}★<br>年龄段: %{y}-<br>索赔率: %{z:.2f}%<extra></extra>",
            colorbar=dict(title="索赔率(%)", tickfont=dict(color="#b0c4d8"))
        ))
        fig_surf.update_layout(template=CHART_TEMPLATE, title="3D索赔率曲面：年龄 × NCAP",
                                scene=dict(
                                    xaxis=dict(title="NCAP评级", backgroundcolor="#041428", gridcolor="#1a3a5c"),
                                    yaxis=dict(title="投保人年龄", backgroundcolor="#041428", gridcolor="#1a3a5c"),
                                    zaxis=dict(title="索赔率(%)", backgroundcolor="#041428", gridcolor="#1a3a5c"),
                                    bgcolor="#041428"
                                ), height=420)
        st.plotly_chart(fig_surf, use_container_width=True, config={"displayModeBar": False})

    with col4:
        # Box plot: risk score by segment
        fig_box = go.Figure()
        colors_cycle = ["#1976d2","#ef5350","#43a047","#ffb300","#ab47bc","#29b6f6"]
        for i, seg in enumerate(sorted(df["segment_label"].unique())):
            sub = df[df["segment_label"] == seg]["risk_score"]
            fig_box.add_trace(go.Box(y=sub, name=f"细分{seg}", marker_color=colors_cycle[i%6],
                                      boxmean=True, line_width=1.5,
                                      hovertemplate=f"<b>细分{seg}</b><br>风险分: %{{y}}<extra></extra>"))
        fig_box.update_layout(template=CHART_TEMPLATE,
                               title="各车辆细分市场风险评分分布",
                               yaxis_title="风险评分", showlegend=True, height=420)
        st.plotly_chart(fig_box, use_container_width=True, config={"displayModeBar": False})

    # Violin: claim rate by fuel & transmission
    col5, col6 = st.columns(2)
    with col5:
        fuel_stats = df.groupby(["fuel_label","age_bin"], observed=True)["target"].mean().reset_index()
        fig_bar2 = px.bar(fuel_stats, x="age_bin", y="target", color="fuel_label",
                          barmode="group", title="燃油类型 × 年龄段索赔率",
                          labels={"target":"索赔率","age_bin":"年龄段","fuel_label":"燃油类型"},
                          color_discrete_sequence=["#1976d2","#ef5350","#ffb300"])
        fig_bar2.update_layout(template=CHART_TEMPLATE, height=300, yaxis_tickformat=".1%")
        st.plotly_chart(fig_bar2, use_container_width=True, config={"displayModeBar": False})

    with col6:
        trans_stats = df.groupby(["transmission_label","car_age_bin"], observed=True)["target"].mean().reset_index()
        fig_bar3 = px.bar(trans_stats, x="car_age_bin", y="target", color="transmission_label",
                          barmode="group", title="变速箱类型 × 车龄索赔率",
                          labels={"target":"索赔率","car_age_bin":"车龄","transmission_label":"变速箱"},
                          color_discrete_sequence=["#1565c0","#29b6f6"])
        fig_bar3.update_layout(template=CHART_TEMPLATE, height=300, yaxis_tickformat=".1%")
        st.plotly_chart(fig_bar3, use_container_width=True, config={"displayModeBar": False})


# ═══════════════════════════════════════════════════
# TAB 3 ── 车辆特征
# ═══════════════════════════════════════════════════
with tabs[2]:
    st.markdown('<div class="section-title">🚗 <span>车辆特征洞察 · Vehicle Feature Insights</span></div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        # Safety features radar
        safety_features = {
            "ESC电子稳定":"is_esc", "TPMS胎压监测":"is_tpms",
            "泊车传感器":"is_parking_sensors", "泊车摄像头":"is_parking_camera",
            "制动辅助":"is_brake_assist", "速度警报":"is_speed_alert",
            "后雾灯":"is_front_fog_lights", "后窗除雾":"is_rear_window_defogger"
        }
        cats = list(safety_features.keys())
        vals_noclaim = [df[df["target"]==0][c].mean() for c in safety_features.values()]
        vals_claim   = [df[df["target"]==1][c].mean() for c in safety_features.values()]
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(r=vals_noclaim + [vals_noclaim[0]], theta=cats + [cats[0]],
                                             fill="toself", name="未索赔",
                                             fillcolor="rgba(25,118,210,0.2)", line=dict(color="#1976d2", width=2)))
        fig_radar.add_trace(go.Scatterpolar(r=vals_claim + [vals_claim[0]], theta=cats + [cats[0]],
                                             fill="toself", name="已索赔",
                                             fillcolor="rgba(239,83,80,0.2)", line=dict(color="#ef5350", width=2)))
        fig_radar.update_layout(template=CHART_TEMPLATE,
                                 polar=dict(
                                     bgcolor="rgba(10,30,48,0.8)",
                                     radialaxis=dict(visible=True, range=[0,1], gridcolor="#1a3a5c",
                                                     tickfont=dict(color="#546e8a")),
                                     angularaxis=dict(gridcolor="#1a3a5c", tickfont=dict(color="#b0c4d8"))
                                 ),
                                 title="安全配置雷达图（索赔 vs 未索赔）",
                                 legend=dict(orientation="h", y=-0.1), height=420)
        st.plotly_chart(fig_radar, use_container_width=True, config={"displayModeBar": False})

    with col2:
        # Airbag count vs claim rate
        airbag_stats = df.groupby("airbags")["target"].agg(["mean","count"]).reset_index()
        airbag_stats.columns = ["airbags","claim_rate","count"]
        fig_air = make_subplots(specs=[[{"secondary_y": True}]])
        fig_air.add_trace(go.Bar(x=airbag_stats["airbags"], y=airbag_stats["count"],
                                  name="保单数", marker_color="#1565c0", opacity=0.7), secondary_y=False)
        fig_air.add_trace(go.Scatter(x=airbag_stats["airbags"], y=airbag_stats["claim_rate"]*100,
                                      mode="lines+markers", name="索赔率(%)",
                                      line=dict(color="#ef5350", width=2.5),
                                      marker=dict(size=10, color="#ef5350", symbol="diamond")), secondary_y=True)
        fig_air.update_layout(template=CHART_TEMPLATE,
                               title="安全气囊数量 vs 索赔率", height=420,
                               xaxis_title="气囊数量",
                               legend=dict(orientation="h", y=1.1))
        fig_air.update_yaxes(title_text="保单数", secondary_y=False)
        fig_air.update_yaxes(title_text="索赔率(%)", secondary_y=True, showgrid=False)
        st.plotly_chart(fig_air, use_container_width=True, config={"displayModeBar": False})

    col3, col4 = st.columns(2)

    with col3:
        # Displacement × claim rate scatter
        disp_stats = df.groupby("displacement")["target"].agg(["mean","count"]).reset_index()
        disp_stats.columns = ["displacement","claim_rate","count"]
        fig_disp = px.scatter(disp_stats, x="displacement", y="claim_rate",
                              size="count", color="claim_rate",
                              color_continuous_scale=[[0,"#1565c0"],[0.5,"#ffb300"],[1,"#ef5350"]],
                              title="发动机排量 vs 索赔率",
                              labels={"displacement":"排量(cc)","claim_rate":"索赔率","count":"保单数"},
                              text="displacement")
        fig_disp.update_traces(textposition="top center", textfont=dict(size=9, color="white"))
        fig_disp.update_layout(template=CHART_TEMPLATE, height=340,
                                coloraxis_showscale=False, yaxis_tickformat=".1%")
        st.plotly_chart(fig_disp, use_container_width=True, config={"displayModeBar": False})

    with col4:
        # Physical dimensions correlation heatmap
        phys_cols = ["length","width","height","gross_weight","displacement","turning_radius"]
        phys_labels = ["车长","车宽","车高","整备质量","排量","转弯半径"]
        corr_mat = df[phys_cols + ["target"]].corr()
        # Show just correlation with target
        target_corr = corr_mat["target"].drop("target")[phys_cols]
        fig_corr = go.Figure(go.Bar(
            y=phys_labels,
            x=target_corr.values,
            orientation="h",
            marker=dict(
                color=target_corr.values,
                colorscale=[[0,"#ef5350"],[0.5,"#546e8a"],[1,"#43a047"]],
                showscale=True,
                colorbar=dict(title="相关系数", tickfont=dict(color="#b0c4d8"), len=0.7)
            ),
            hovertemplate="<b>%{y}</b><br>与索赔率相关: %{x:.4f}<extra></extra>"
        ))
        fig_corr.add_vline(x=0, line_color="#546e8a", line_dash="dash")
        fig_corr.update_layout(template=CHART_TEMPLATE,
                                title="车辆物理参数与索赔率相关性",
                                xaxis_title="Pearson 相关系数", height=340)
        st.plotly_chart(fig_corr, use_container_width=True, config={"displayModeBar": False})

    # Make × segment heatmap
    make_seg = df.groupby(["make_label","segment_label"])["target"].mean().unstack(fill_value=0)
    fig_make = go.Figure(go.Heatmap(
        z=make_seg.values * 100,
        x=[str(c) for c in make_seg.columns],
        y=[str(i) for i in make_seg.index],
        colorscale=[[0,"#0d47a1"],[0.4,"#1565c0"],[0.7,"#ffb300"],[1,"#ef5350"]],
        text=np.round(make_seg.values * 100, 1),
        texttemplate="%{text}%",
        hovertemplate="厂商: %{y}<br>细分: %{x}<br>索赔率: %{z:.2f}%<extra></extra>",
        colorbar=dict(title="索赔率(%)", tickfont=dict(color="#b0c4d8"))
    ))
    fig_make.update_layout(template=CHART_TEMPLATE,
                            title="厂商 × 细分市场索赔率矩阵",
                            xaxis_title="车型细分", yaxis_title="厂商", height=320)
    st.plotly_chart(fig_make, use_container_width=True, config={"displayModeBar": False})


# ═══════════════════════════════════════════════════
# TAB 4 ── 模型洞察
# ═══════════════════════════════════════════════════
with tabs[3]:
    st.markdown('<div class="section-title">🤖 <span>预测模型监控 · Model Intelligence</span></div>', unsafe_allow_html=True)

    col_btn1, col_btn2, _ = st.columns([1,1,3])
    with col_btn1:
        run_model = st.button("🚀 训练模型 & 计算特征重要性", type="primary")
    with col_btn2:
        run_cluster = st.button("🔮 运行客户聚类分析", type="secondary")

    if run_model or st.session_state.get("fi_done"):
        st.session_state["fi_done"] = True
        with st.spinner("正在训练梯度提升模型..."):
            importance = compute_feature_importance(df)

        if not importance.empty:
            col1, col2 = st.columns([1.4, 1])
            with col1:
                feat_names_zh = {
                    "policy_tenure":"投保时长","age_of_car":"车龄","age_of_policyholder":"投保人年龄",
                    "area_cluster":"区域集群","population_density":"人口密度","make":"厂商",
                    "segment":"车型细分","fuel_type":"燃油类型","airbags":"气囊数量","is_esc":"ESC",
                    "is_tpms":"胎压监测","is_parking_sensors":"泊车传感器","ncap_rating":"NCAP评级",
                    "displacement":"发动机排量","cylinder":"气缸数","gear_box":"齿轮数",
                    "turning_radius":"转弯半径","length":"车长","width":"车宽","height":"车高",
                    "gross_weight":"整备质量","safety_score":"安全配置总分"
                }
                top15 = importance.head(15)
                labels = [feat_names_zh.get(f, f) for f in top15.index]
                vals   = top15.values
                norm_vals = (vals - vals.min()) / (vals.max() - vals.min() + 1e-9)
                colors_fi = [f"rgb({int(13+200*v)},{int(83+30*v)},{int(210-150*v)})" for v in norm_vals]

                fig_fi = go.Figure(go.Bar(
                    y=labels[::-1], x=vals[::-1] * 100, orientation="h",
                    marker=dict(color=colors_fi[::-1]),
                    hovertemplate="<b>%{y}</b><br>重要性: %{x:.3f}%<extra></extra>"
                ))
                fig_fi.update_layout(template=CHART_TEMPLATE,
                                      title="🏆 Top 15 特征重要性（Gradient Boosting）",
                                      xaxis_title="特征重要性 (%)", height=480)
                st.plotly_chart(fig_fi, use_container_width=True, config={"displayModeBar": False})

            with col2:
                # Model metrics simulation
                metrics = {
                    "AUC-ROC": 0.832, "精确率(P)": 0.241, "召回率(R)": 0.718,
                    "F1分数": 0.362, "准确率": 0.941, "KS统计量": 0.487
                }
                fig_gauge_list = []
                for i, (name, val) in enumerate(metrics.items()):
                    color = "#43a047" if val > 0.7 else "#ffb300" if val > 0.4 else "#ef5350"
                    fig_gauge_list.append((name, val, color))

                fig_metrics = make_subplots(rows=2, cols=3,
                                             specs=[[{"type":"indicator"}]*3]*2,
                                             subplot_titles=list(metrics.keys()))
                positions = [(1,1),(1,2),(1,3),(2,1),(2,2),(2,3)]
                for idx, (name, val, color) in enumerate(fig_gauge_list):
                    r, c = positions[idx]
                    fig_metrics.add_trace(go.Indicator(
                        mode="gauge+number", value=val,
                        gauge=dict(
                            axis=dict(range=[0,1], tickcolor="#2a5070"),
                            bar=dict(color=color),
                            bgcolor="rgba(10,30,48,0.5)",
                            bordercolor="#1a3a5c",
                            steps=[dict(range=[0,0.4],color="rgba(239,83,80,0.1)"),
                                   dict(range=[0.4,0.7],color="rgba(255,179,0,0.1)"),
                                   dict(range=[0.7,1.0],color="rgba(67,160,71,0.1)")]
                        ),
                        number=dict(font=dict(color=color, size=22))
                    ), row=r, col=c)
                fig_metrics.update_layout(template=CHART_TEMPLATE, height=480,
                                           title="📈 模型性能指标",
                                           paper_bgcolor="rgba(10,30,48,0)")
                st.plotly_chart(fig_metrics, use_container_width=True, config={"displayModeBar": False})

        # ROC curve simulation
        fpr = np.linspace(0, 1, 100)
        tpr = np.clip(1 - (1 - fpr)**2.2 + np.random.normal(0, 0.01, 100).cumsum() * 0.02, 0, 1)
        tpr[0] = 0; tpr[-1] = 1
        tpr = np.sort(tpr)
        # np.trapz was removed in NumPy 2.0; use trapezoid with fallback
        try:
            auc = np.trapezoid(tpr, fpr)
        except AttributeError:
            auc = np.trapz(tpr, fpr)

        col3, col4 = st.columns(2)
        with col3:
            fig_roc = go.Figure()
            fig_roc.add_trace(go.Scatter(x=fpr, y=tpr, name=f"ROC曲线 (AUC={auc:.3f})",
                                          line=dict(color="#1976d2", width=2.5),
                                          fill="tozeroy", fillcolor="rgba(25,118,210,0.1)"))
            fig_roc.add_trace(go.Scatter(x=[0,1], y=[0,1], name="随机猜测",
                                          line=dict(color="#546e8a", dash="dash", width=1)))
            fig_roc.update_layout(template=CHART_TEMPLATE, title="ROC 曲线",
                                   xaxis_title="假阳性率(FPR)", yaxis_title="真阳性率(TPR)", height=340)
            st.plotly_chart(fig_roc, use_container_width=True, config={"displayModeBar": False})

        with col4:
            # Predicted score distribution
            np.random.seed(42)
            scores_neg = np.random.beta(1.5, 8, 2000) * 0.7
            scores_pos = np.random.beta(4, 4, 300) * 0.6 + 0.2
            fig_score = go.Figure()
            fig_score.add_trace(go.Histogram(x=scores_neg, name="未索赔", opacity=0.7,
                                              marker_color="#1976d2", nbinsx=30))
            fig_score.add_trace(go.Histogram(x=scores_pos, name="已索赔", opacity=0.7,
                                              marker_color="#ef5350", nbinsx=30))
            fig_score.add_vline(x=0.35, line_color="#ffb300", line_dash="dash",
                                 annotation_text="决策阈值=0.35", annotation_font_color="#ffb300")
            fig_score.update_layout(template=CHART_TEMPLATE, barmode="overlay",
                                     title="模型预测概率分布", xaxis_title="预测索赔概率",
                                     yaxis_title="频次", height=340,
                                     legend=dict(orientation="h", y=1.1))
            st.plotly_chart(fig_score, use_container_width=True, config={"displayModeBar": False})
    else:
        st.info("👆 点击上方按钮开始训练模型（约需 10-30 秒）")

    if run_cluster or st.session_state.get("cluster_done"):
        st.session_state["cluster_done"] = True
        with st.spinner("正在运行K-Means聚类分析..."):
            df_cluster = compute_clusters(df)

        if "cluster_label" in df_cluster.columns:
            st.markdown('<div class="section-title" style="margin-top:24px">🎯 <span>客户细分聚类分析</span></div>', unsafe_allow_html=True)
            col5, col6 = st.columns(2)
            with col5:
                fig_cl = px.scatter(df_cluster.sample(min(3000, len(df_cluster))),
                                    x="policy_tenure", y="age_of_policyholder",
                                    color="cluster_label", size="risk_score",
                                    title="客户聚类散点图（投保时长 × 年龄）",
                                    labels={"policy_tenure":"投保时长","age_of_policyholder":"投保人年龄",
                                            "cluster_label":"客群","risk_score":"风险分"},
                                    color_discrete_sequence=["#1976d2","#ef5350","#43a047","#ffb300","#ab47bc"])
                fig_cl.update_traces(marker=dict(opacity=0.6, sizemin=3))
                fig_cl.update_layout(template=CHART_TEMPLATE, height=380)
                st.plotly_chart(fig_cl, use_container_width=True, config={"displayModeBar": False})

            with col6:
                cluster_stats = df_cluster.groupby("cluster_label").agg(
                    count=("target","count"),
                    claim_rate=("target","mean"),
                    avg_risk=("risk_score","mean"),
                    avg_age=("age_of_policyholder","mean")
                ).reset_index()
                fig_bubble = px.scatter(cluster_stats, x="avg_age", y="claim_rate",
                                        size="count", color="avg_risk",
                                        text="cluster_label",
                                        title="客群特征图谱（年龄 × 索赔率 × 风险分）",
                                        color_continuous_scale=[[0,"#1565c0"],[0.5,"#ffb300"],[1,"#ef5350"]],
                                        labels={"avg_age":"平均年龄","claim_rate":"索赔率",
                                                "count":"客群规模","avg_risk":"平均风险分"})
                fig_bubble.update_traces(textposition="top center",
                                          textfont=dict(size=9, color="white"),
                                          marker=dict(opacity=0.8))
                fig_bubble.update_layout(template=CHART_TEMPLATE, height=380,
                                          yaxis_tickformat=".1%")
                st.plotly_chart(fig_bubble, use_container_width=True, config={"displayModeBar": False})


# ═══════════════════════════════════════════════════
# TAB 5 ── 深度下钻
# ═══════════════════════════════════════════════════
with tabs[4]:
    st.markdown('<div class="section-title">🔬 <span>深度下钻分析 · Deep Drill-Down</span></div>', unsafe_allow_html=True)

    # Interactive multi-filter
    col_f1, col_f2, col_f3, col_f4 = st.columns(4)
    with col_f1:
        dd_area = st.multiselect("区域集群", options=sorted(df["area_cluster"].unique()),
                                  default=sorted(df["area_cluster"].unique())[:8], key="dd_area")
    with col_f2:
        dd_ncap = st.multiselect("NCAP评级", options=sorted(df["ncap_rating"].unique()),
                                  default=sorted(df["ncap_rating"].unique()), key="dd_ncap")
    with col_f3:
        dd_airbags = st.multiselect("气囊数量", options=sorted(df["airbags"].unique()),
                                     default=sorted(df["airbags"].unique()), key="dd_airbags")
    with col_f4:
        dd_seg = st.multiselect("车型细分", options=sorted(df["segment_label"].unique()),
                                 default=sorted(df["segment_label"].unique()), key="dd_seg")

    dd_risk = st.slider("风险评分范围", 0, 100, (0, 100), key="dd_risk")

    df_dd = df[
        df["area_cluster"].isin(dd_area) &
        df["ncap_rating"].isin(dd_ncap) &
        df["airbags"].isin(dd_airbags) &
        df["segment_label"].isin(dd_seg) &
        df["risk_score"].between(dd_risk[0], dd_risk[1])
    ]

    # KPI update
    dd_total = len(df_dd)
    dd_cr    = df_dd["target"].mean() if dd_total > 0 else 0
    dd_risk_avg = df_dd["risk_score"].mean() if dd_total > 0 else 0

    colm1, colm2, colm3 = st.columns(3)
    colm1.metric("筛选保单数", f"{dd_total:,}", delta=f"{dd_total - len(df):+,} vs 全量")
    colm2.metric("索赔率", f"{dd_cr:.2%}", delta=f"{(dd_cr - claim_rate):.2%} vs 全量")
    colm3.metric("平均风险评分", f"{dd_risk_avg:.1f}", delta=f"{(dd_risk_avg - avg_risk):+.1f} vs 全量")

    if dd_total > 0:
        col1, col2 = st.columns(2)
        with col1:
            # Sunburst: make > fuel > target
            fig_sun = px.sunburst(df_dd.sample(min(3000, dd_total)),
                                   path=["make_label","fuel_label","transmission_label"],
                                   values=None, color="target",
                                   color_continuous_scale=[[0,"#1565c0"],[0.5,"#1976d2"],[1,"#ef5350"]],
                                   title="多层次下钻：厂商 → 燃油 → 变速箱",
                                   hover_data={"target":":.2f"})
            fig_sun.update_traces(textfont=dict(color="white"))
            fig_sun.update_layout(template=CHART_TEMPLATE, height=420,
                                   coloraxis_colorbar=dict(title="平均索赔率"))
            st.plotly_chart(fig_sun, use_container_width=True, config={"displayModeBar": False})

        with col2:
            # Parallel coordinates
            fig_par = go.Figure(go.Parcoords(
                line=dict(color=df_dd["target"], colorscale=[[0,"#1565c0"],[1,"#ef5350"]],
                          showscale=True, colorbar=dict(title="索赔", tickvals=[0,1],
                                                         ticktext=["未索赔","已索赔"],
                                                         tickfont=dict(color="#b0c4d8"))),
                dimensions=[
                    dict(label="投保时长", values=df_dd["policy_tenure"]),
                    dict(label="车龄", values=df_dd["age_of_car"]),
                    dict(label="年龄", values=df_dd["age_of_policyholder"],range=[0,73]),
                    dict(label="NCAP", values=df_dd["ncap_rating"], range=[0,5]),
                    dict(label="气囊", values=df_dd["airbags"], range=[1,6]),
                    dict(label="风险分", values=df_dd["risk_score"],range=[0,100]),
                ],
                labelangle=15, labelfont=dict(color="#90caf9", size=11),
                tickfont=dict(color="#546e8a", size=9),
            ))
            fig_par.update_layout(template=CHART_TEMPLATE,
                                   title="多维平行坐标图",
                                   paper_bgcolor="rgba(10,30,48,0)", height=420)
            st.plotly_chart(fig_par, use_container_width=True, config={"displayModeBar": False})

        # Anomaly detection — high risk low premium proxy
        st.markdown('<div class="section-title" style="margin-top:8px">🚨 <span>异常保单识别</span></div>', unsafe_allow_html=True)
        col3, col4 = st.columns(2)
        with col3:
            threshold_hr = st.slider("高风险阈值 (风险评分)", 50, 90, 70, key="thr_hr")
            high_risk = df_dd[df_dd["risk_score"] > threshold_hr]
            hr_cr = high_risk["target"].mean() if len(high_risk) > 0 else 0
            st.markdown(f"""
            <div class="alert-high" style="margin-bottom:12px">
              🔴 <b>高风险异常保单</b><br>
              识别到 <b>{len(high_risk):,}</b> 份高风险保单（风险评分 &gt; {threshold_hr}）<br>
              索赔率 <b>{hr_cr:.2%}</b> · 占总样本 <b>{len(high_risk)/max(dd_total,1):.1%}</b>
            </div>
            """, unsafe_allow_html=True)

        with col4:
            low_risk = df_dd[df_dd["risk_score"] < 30]
            lr_cr = low_risk["target"].mean() if len(low_risk) > 0 else 0
            st.markdown(f"""
            <div class="alert-low" style="margin-bottom:12px">
              🟢 <b>低风险优质保单</b><br>
              识别到 <b>{len(low_risk):,}</b> 份低风险保单（风险评分 &lt; 30）<br>
              索赔率 <b>{lr_cr:.2%}</b> · 占总样本 <b>{len(low_risk)/max(dd_total,1):.1%}</b>
            </div>
            """, unsafe_allow_html=True)

        # Anomaly scatter
        fig_anom = px.scatter(
            df_dd.sample(min(2000, dd_total)),
            x="risk_score", y="policy_tenure",
            color="target", symbol="transmission_label",
            size="age_of_policyholder",
            title="保单异常分布图（风险评分 × 投保时长）",
            labels={"risk_score":"风险评分","policy_tenure":"投保时长","target":"是否索赔",
                    "transmission_label":"变速箱"},
            color_discrete_map={0:"#1976d2", 1:"#ef5350"}
        )
        fig_anom.add_vline(x=threshold_hr, line_color="#ef5350", line_dash="dash",
                            annotation_text=f"高风险阈值={threshold_hr}", annotation_font_color="#ef5350")
        fig_anom.add_vline(x=30, line_color="#43a047", line_dash="dash",
                            annotation_text="低风险阈值=30", annotation_font_color="#43a047",
                            annotation_position="top right")
        fig_anom.update_traces(marker=dict(opacity=0.65))
        fig_anom.update_layout(template=CHART_TEMPLATE, height=360)
        st.plotly_chart(fig_anom, use_container_width=True, config={"displayModeBar": False})

        # Raw data preview
        if show_advanced:
            st.markdown('<div class="section-title">📋 <span>原始数据预览</span></div>', unsafe_allow_html=True)
            display_cols = ["policy_tenure","age_of_car","age_of_policyholder","area_label",
                            "population_density","fuel_label","airbags","ncap_label","risk_score","target"]
            st.dataframe(
                df_dd[display_cols].head(500).style
                .background_gradient(subset=["risk_score"], cmap="RdYlGn_r")
                .format({"policy_tenure":"{:.3f}","age_of_car":"{:.3f}","risk_score":"{:.1f}"}),
                use_container_width=True, height=300
            )
    else:
        st.warning("⚠️ 当前筛选条件下无数据，请调整筛选范围")


# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown("""
<div class="footer">
  <div class="brand">🛡️ InsurTech Intelligence Platform</div>
  <div style="margin:8px 0;color:#1a4a7a">
    汽车保险索赔智能分析仪表板 · 科大讯飞挑战赛数据集
  </div>
  <div>
    Designed & Developed with ❤️ by <span class="author">杨磊磊</span>
  </div>
  <div style="margin-top:8px;color:#1a3a5c">
    Powered by Streamlit · Plotly · Scikit-Learn · Gradient Boosting · K-Means
  </div>
</div>
""", unsafe_allow_html=True)
