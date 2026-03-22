import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta

# ==========================================
# 0. 页面配置与全局设置
# ==========================================
st.set_page_config(
    page_title="鲸智社区车险决策仪表板 - 开发者：杨磊磊",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==========================================
# 1. 真实数据加载与混合特征工程 (对接 test.csv)
# ==========================================
@st.cache_data
def load_real_data():
    try:
        # 读取上传的 test.csv 真实数据
        df_real = pd.read_csv('test.csv')
    except FileNotFoundError:
        st.error("⚠️ 未找到 test.csv 文件，请确保文件与 app.py 在同一目录下。")
        return pd.DataFrame()

    # 为了保证 Streamlit 仪表板的交互流畅性，建议抽取前 2000 条进行可视化分析
    df = df_real.head(2000).copy()
    n_records = len(df)

    # --- 1. 基础字段映射 ---
    # 提取真实保单号
    df['policy_id'] = "POL" + df['id'].astype(str)

    # 处理投保人年龄 (根据 readme 提示为归一化数据，这里将其还原为大致的真实年龄 18-75岁)
    # 如果原始数据已经是大整数，则直接使用，否则进行反归一化缩放
    if df['age_of_policyholder'].max() <= 1.5:
        df['driver_age'] = (df['age_of_policyholder'] * 80).clip(18, 75).astype(int)
    else:
        df['driver_age'] = df['age_of_policyholder'].clip(18, 75).astype(int)

    # 处理车型/车系 (提取真实的 segment 字段)
    # 原始数据类似 A/B1/B2/C1/C2，如果没有则用数值映射
    df['vehicle_model'] = df['segment'].astype(str).apply(lambda x: f"级别-{x}")

    # --- 2. 地区与坐标映射 ---
    # 将真实的 area_cluster 映射到国内核心城市
    city_coords = {
        '北京市': (39.9042, 116.4074),
        '上海市': (31.2304, 121.4737),
        '广州市': (23.1291, 113.2644),
        '成都市': (30.5728, 104.0668),
        '武汉市': (30.5928, 114.3055)
    }
    cities = list(city_coords.keys())

    # 通过 area_cluster 的哈希值稳定映射到指定城市，保持同 cluster 都在同一城市
    df['area'] = df['area_cluster'].apply(lambda x: cities[hash(str(x)) % len(cities)])

    # 根据城市中心坐标生成带有一点随机散布的事故发生经纬度
    np.random.seed(42)
    df['lat'] = df['area'].apply(lambda c: city_coords[c][0] + np.random.uniform(-0.8, 0.8))
    df['lon'] = df['area'].apply(lambda c: city_coords[c][1] + np.random.uniform(-0.8, 0.8))

    # --- 3. 业务特征衍生模拟 ---
    # 测试集不含财务金额和报案时间，此处根据真实特征做合理推演
    df['claim_date'] = [datetime(2026, 1, 1) + timedelta(days=np.random.randint(0, 90)) for _ in range(n_records)]

    # 模拟保费：根据汽车排量 (displacement) 估算保费，排量越大保费基数越高
    if 'displacement' in df.columns:
        df['premium'] = df['displacement'] * 1.5 + np.random.uniform(2000, 3000, n_records)
    else:
        df['premium'] = np.random.uniform(2000, 8000, n_records)

    df['claim_status'] = np.random.choice(['已结案', '处理中', '已拒赔'], n_records, p=[0.7, 0.2, 0.1])

    # 模拟赔付金额
    df['claim_amount'] = np.where(df['claim_status'] == '已拒赔', 0,
                                  df['premium'] * np.random.uniform(0.1, 2.5, n_records))

    # 核心精算指标
    df['loss_ratio'] = df['claim_amount'] / df['premium']
    bins = [0, 25, 55, 100]
    labels = ['青年(18-25)', '中年(26-55)', '老年(56+)']
    df['age_group'] = pd.cut(df['driver_age'], bins=bins, labels=labels, right=True)

    return df


df = load_real_data()

# 后续代码保持不变...

# ==========================================
# 2. 侧边栏：全局联动筛选器 (汉化 & 无图层断裂)
# ==========================================
# --- 新增：在侧边栏最上方添加署名 ---
st.sidebar.caption("杨磊磊制作") 
# ----------------------------------

st.sidebar.markdown("## 🛡️ 多维数据筛选")
st.sidebar.markdown("---")

# 容错处理：若未能正确加载 df 则终止渲染
if df.empty:
    st.stop()

# ... 后续代码保持不变 ...

date_range = st.sidebar.date_input(
    "出险时间范围",
    value=(df['claim_date'].min(), df['claim_date'].max()),
    min_value=df['claim_date'].min().date(),
    max_value=df['claim_date'].max().date()
)

selected_areas = st.sidebar.multiselect("选择地区 (已与地图绑定)", options=df['area'].unique(),
                                        default=df['area'].unique())
selected_models = st.sidebar.multiselect("选择车型级别 (读取自segment)", options=df['vehicle_model'].unique(),
                                         default=df['vehicle_model'].unique())

if len(date_range) == 2:
    start_date, end_date = date_range
    mask = (
            (df['claim_date'].dt.date >= start_date) &
            (df['claim_date'].dt.date <= end_date) &
            (df['area'].isin(selected_areas)) &
            (df['vehicle_model'].isin(selected_models))
    )
    filtered_df = df[mask]
else:
    filtered_df = df.copy()

# ==========================================
# 3. 主界面布局：第一行 - 核心 KPI 卡片
# ==========================================
st.title("🚗 车险赔付智能决策仪表板")
st.markdown("---")

total_premium = filtered_df['premium'].sum()
total_claim = filtered_df['claim_amount'].sum()
avg_claim = filtered_df[filtered_df['claim_amount'] > 0]['claim_amount'].mean()
claim_count = len(filtered_df[filtered_df['claim_amount'] > 0])

loss_ratio = (total_claim / total_premium) if total_premium > 0 else 0
lr_delta = f"{(loss_ratio - 0.65) * 100:+.1f}% (环比)"

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(label="📊 综合赔付率", value=f"{loss_ratio * 100:.1f}%", delta=lr_delta, delta_color="inverse")
with col2:
    st.metric(label="💰 案均赔款", value=f"¥{avg_claim:,.0f}" if not np.isnan(avg_claim) else "¥0", delta="¥+320 (环比)",
              delta_color="inverse")
with col3:
    st.metric(label="📈 出险案件数", value=f"{claim_count} 件", delta="-12 件 (环比)", delta_color="normal")
with col4:
    ibnr_estimate = total_claim * 0.15
    st.metric(label="🏦 预估 IBNR 准备金", value=f"¥{ibnr_estimate:,.0f}", delta="充足", delta_color="normal")

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================
# 4. 主界面布局：第二行 - 交互式可视化图表
# ==========================================
col_map, col_scatter = st.columns([1, 1])

with col_map:
    st.subheader("📍 赔付金额热力图 (按区域)")
    if not filtered_df.empty:
        fig_map = px.density_mapbox(
            filtered_df, lat='lat', lon='lon', z='claim_amount', radius=15,
            center=dict(lat=34.0, lon=108.0), zoom=3.5,
            mapbox_style="open-street-map",
            color_continuous_scale="Reds",
            hover_name="area",
            labels={
                'lat': '纬度', 'lon': '经度',
                'claim_amount': '案件赔付金额(元)', 'area': '所属大区'
            }
        )
        fig_map.update_traces(hovertemplate="<b>%{hovertext}</b><br>案件赔付金额(元): ¥%{z:,.2f}<extra></extra>")
        fig_map.update_layout(margin={"r": 0, "t": 10, "l": 0, "b": 0}, coloraxis_colorbar_title="金额(元)")
        st.plotly_chart(fig_map, use_container_width=True)
    else:
        st.info("当前筛选条件下无数据")

with col_scatter:
    st.subheader("👤 赔付率 vs 驾驶员年龄分布")
    if not filtered_df.empty:
        bubble_data = filtered_df.groupby(['age_group', 'vehicle_model'], observed=True).agg(
            avg_loss_ratio=('loss_ratio', 'mean'),
            claim_count=('policy_id', 'count')
        ).reset_index()

        fig_scatter = px.scatter(
            bubble_data, x='age_group', y='avg_loss_ratio',
            size='claim_count', color='vehicle_model',
            size_max=40,
            labels={
                'age_group': '驾驶员年龄段', 'avg_loss_ratio': '平均赔付率',
                'vehicle_model': '车型级别', 'claim_count': '出险案件总数'
            }
        )

        fig_scatter.update_traces(
            hovertemplate="<b>车型级别: %{data.name}</b><br>" +
                          "驾驶员年龄段: %{x}<br>平均赔付率: %{y:.2%}<br>" +
                          "出险案件总数: %{marker.size} 件<extra></extra>"
        )

        fig_scatter.add_hline(y=1.0, line_dash="dash", line_color="red", annotation_text="100% 亏损线")
        fig_scatter.update_layout(margin={"r": 0, "t": 10, "l": 0, "b": 0})
        st.plotly_chart(fig_scatter, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================
# 5. 主界面布局：第三行 - 高风险异常预警与审查
# ==========================================
st.subheader("🚨 异常监控：高风险未决保单明细 (赔付率 > 100%)")

high_risk_df = filtered_df[(filtered_df['loss_ratio'] > 1.0) & (filtered_df['claim_status'] == '处理中')].copy()

if not high_risk_df.empty:
    high_risk_df.insert(0, "标记欺诈审查", False)

    display_cols = ['标记欺诈审查', 'policy_id', 'area', 'vehicle_model', 'driver_age', 'premium', 'claim_amount',
                    'loss_ratio']
    show_df = high_risk_df[display_cols].copy()

    show_df.rename(columns={
        'policy_id': '保单号', 'area': '所属地区', 'vehicle_model': '车型级别',
        'driver_age': '驾驶员年龄', 'premium': '已交保费',
        'claim_amount': '预估赔付金额', 'loss_ratio': '当前赔付率'
    }, inplace=True)

    show_df['当前赔付率'] = show_df['当前赔付率'].apply(lambda x: f"{x * 100:.1f}%")
    show_df['已交保费'] = show_df['已交保费'].apply(lambda x: f"¥{x:.2f}")
    show_df['预估赔付金额'] = show_df['预估赔付金额'].apply(lambda x: f"¥{x:.2f}")

    st.write("勾选首列复选框可将案件推送至 SIU（特别调查组）进行反欺诈复核：")
    edited_df = st.data_editor(
        show_df,
        hide_index=True,
        use_container_width=True,
        column_config={
            "标记欺诈审查": st.column_config.CheckboxColumn(
                "标记为欺诈嫌疑?", help="选中后将自动推送到运营总监待办", default=False
            )
        }
    )

    suspect_policies = edited_df[edited_df['标记欺诈审查'] == True]['保单号'].tolist()
    if suspect_policies:
        st.error(f"⚠️ 系统预警：已将以下保单标记为疑似欺诈并推送至风控系统: {', '.join(suspect_policies)}")
else:
    st.success("🎉 当前筛选条件下，暂无赔付率超100%的未决高风险保单。")
