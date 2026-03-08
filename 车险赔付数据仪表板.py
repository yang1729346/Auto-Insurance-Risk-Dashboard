import streamlit as st
import pandas as pd
import plotly.express as px

# ==========================================
# 1. 页面整体设置与 CSS 样式
# ==========================================
st.set_page_config(
    page_title="车险赔付数据分析仪表板",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义 CSS 提升视觉效果
st.markdown("""
<style>
    .big-font { font-size: 26px !important; font-weight: bold; padding-bottom: 10px; }
    .insight-box {
        background-color: #1E1E2E; 
        padding: 20px; 
        border-radius: 10px; 
        border-left: 5px solid #FF3366;
        margin-top: 10px;
    }
    .insight-title { color: #00CFFF; margin-top: 0; font-size: 20px; font-weight: bold;}
    .insight-text { color: #E0E0E0; line-height: 1.8; font-size: 15px;}
</style>
""", unsafe_allow_html=True)

# Plotly 全局汉化与隐藏官方 Logo 配置
zh_config = {'locale': 'zh-CN', 'displaylogo': False}


# ==========================================
# 2. 核心数据加载与深度清洗 (完全汉化)
# ==========================================
@st.cache_data
def load_and_clean_data():
    df = pd.read_csv("car_insurance_claims.csv")

    claim_col = 'total_claim_amount'
    sex_col = 'insured_sex'
    age_col = 'age'
    make_col = 'auto_make'

    df = df.dropna(subset=[claim_col, sex_col, age_col, make_col])

    # 性别汉化
    gender_map = {'MALE': '男性', 'FEMALE': '女性', 'M': '男性', 'F': '女性'}
    df[sex_col] = df[sex_col].str.upper().map(gender_map).fillna(df[sex_col])

    # 汽车品牌汉化字典
    make_map = {
        'Accura': '讴歌', 'Audi': '奥迪', 'BMW': '宝马', 'Chevrolet': '雪佛兰',
        'Dodge': '道奇', 'Ford': '福特', 'Honda': '本田', 'Jeep': '吉普',
        'Mercedes': '奔驰', 'Nissan': '日产', 'Subaru': '斯巴鲁', 'Toyota': '丰田',
        'Volkswagen': '大众', 'Saab': '萨博', 'Porsche': '保时捷'
    }
    df[make_col] = df[make_col].replace(make_map)

    # 创建年龄分段
    bins = [18, 25, 35, 45, 55, 100]
    labels = ['18-25岁', '26-35岁', '36-45岁', '46-55岁', '56岁以上']
    df['年龄段'] = pd.cut(df[age_col], bins=bins, labels=labels, right=False)

    # 直接修改列名，完美适配悬停提示
    df = df.rename(columns={
        claim_col: '赔付金额',
        sex_col: '性别',
        make_col: '汽车品牌',
        age_col: '年龄'
    })

    return df


df = load_and_clean_data()

# ==========================================
# 3. 侧边栏：精准筛选 (全中文)
# ==========================================
with st.sidebar:
    st.markdown("<div class='big-font'>🚗 数据筛选</div>", unsafe_allow_html=True)

    gender_options = sorted(df['性别'].dropna().astype(str).unique())
    selected_gender = st.multiselect("选择受保人性别", options=gender_options, default=gender_options)

    make_options = sorted(df['汽车品牌'].dropna().astype(str).unique())
    selected_makes = st.multiselect("选择汽车品牌", options=make_options, default=make_options[:10])

    age_seg_options = sorted(df['年龄段'].dropna().astype(str).unique())
    selected_age_segs = st.multiselect("选择年龄段", options=age_seg_options, default=age_seg_options)

    st.divider()
    st.info("数据来源：天池车险索赔数据集")

filtered_df = df[
    (df['性别'].isin(selected_gender)) &
    (df['汽车品牌'].isin(selected_makes)) &
    (df['年龄段'].isin(selected_age_segs))
    ]

# ==========================================
# 4. 主界面：大标题与核心 KPI
# ==========================================
st.title("国内车险赔付数据可视化仪表板")
st.markdown(
    f"**杨磊磊作品** | 保险学专业学生 | 帮助风控部门快速发现高风险群体 | 当前分析数据量：**{filtered_df.shape[0]}** 条")
st.divider()

kpi1, kpi2, kpi3 = st.columns(3)
with kpi1:
    st.metric(label="总赔付金额 (元)", value=f"{filtered_df['赔付金额'].sum():,.0f}")
with kpi2:
    st.metric(label="案均赔款 (元/件)", value=f"{filtered_df['赔付金额'].mean():,.0f}")
with kpi3:
    st.metric(label="出险案件总数", value=f"{filtered_df.shape[0]:,}")
st.divider()

# ==========================================
# 5. 图表区
# ==========================================
col1, col2 = st.columns(2)

with col1:
    st.subheader("1. 赔付金额分布趋势")
    fig1 = px.histogram(
        filtered_df, x='赔付金额', color='性别', nbins=40,
        title="不同性别赔付区间分布"
    )
    fig1.update_layout(hovermode="x unified")
    st.plotly_chart(fig1, width="stretch", config=zh_config)

with col2:
    st.subheader("2. 各品牌汽车案均赔款对比")
    make_avg_df = filtered_df.groupby('汽车品牌')['赔付金额'].mean().reset_index().sort_values(by='赔付金额',
                                                                                               ascending=False).head(10)
    fig2 = px.bar(
        make_avg_df, x='汽车品牌', y='赔付金额', color='赔付金额', color_continuous_scale="Reds",
        title="识别高损车型"
    )
    st.plotly_chart(fig2, width="stretch", config=zh_config)

st.divider()

st.subheader("3. 行业标准：不同年龄段赔付金额分布与异常值")
st.markdown("""
<div style='background-color: #262730; padding: 12px; border-radius: 8px; margin-bottom: 20px; border-left: 4px solid #00CFFF;'>
    <span style='color: #A3A8B4; font-size: 14px;'>
    💡 <b>箱线图统计标识说明</b>：悬停显示的英文为国际通用统计标识。<br>
    <b>max / min</b>：正常范围内的最大/最小值 | <b>upper / lower fence</b>：上下边缘（超出此范围即为异常高额理赔）<br>
    <b>q3 / q1</b>：上/下四分位数 (75% / 25%位置) | <b>median</b>：中位数（代表该群体的一般赔付水平）
    </span>
</div>
""", unsafe_allow_html=True)

custom_colors = {'男性': '#00CFFF', '女性': '#FF3366'}

fig3 = px.box(
    filtered_df,
    x='年龄段',
    y='赔付金额',
    color='性别',
    color_discrete_map=custom_colors,
    category_orders={"年龄段": ['18-25岁', '26-35岁', '36-45岁', '46-55岁', '56岁以上']},
    points="outliers",
    title="评估各群体理赔波动率（点为极端高额理赔案件）"
)

fig3.update_layout(
    boxmode='group',
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    yaxis=dict(showgrid=True, gridcolor='#333333', zeroline=False),
    xaxis=dict(showgrid=False),
    margin=dict(l=10, r=10, t=40, b=10),
    legend=dict(title=None, orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)
fig3.update_traces(marker=dict(size=5, opacity=0.7, line=dict(width=1, color='white')), line=dict(width=2))
st.plotly_chart(fig3, width="stretch", config=zh_config)

# ==========================================
# 6. 业务洞察与个人分析 (全新添加部分)
# ==========================================
st.divider()
st.subheader("💡 业务洞察与未来展望")

st.markdown("""
<div class='insight-box'>
    <div class='insight-title'>📝 基于当前数据的核心发现 (分析人：杨磊磊)</div>
    <div class='insight-text'>
    <br>
    <b>1. 赔付金额的“长尾效应”与极值风险：</b><br>
    通过赔付金额直方图和下方的箱线图可以明显观察到，虽然大部分案件集中在常规金额区间，但存在较多极高额的理赔案件（异常点）。特别是在 <b>18-25岁</b> 和 <b>26-35岁</b> 的年轻群体中，理赔金额的波动率极大，上限极高。这提示风控部门需要针对年轻群体制定更精细化的核保规则（如引入免赔额条款或针对性提价）。<br><br>
    <b>2. 品牌溢价与案均赔款的强相关性：</b><br>
    高价值或特定品牌（如奥迪、奔驰、宝马等豪华车）的案均赔款显著高于普通品牌。这不仅是因为其零整比高（维修成本昂贵），也可能伴随着更高的道德风险（如零配件欺诈、扩损）。建议在传统的基于车价的定价模型中，赋予“车型品牌”更大的保费系数权重。<br><br>
    <b>3. 下一步规划：“保险 + AI”的反欺诈演进：</b><br>
    目前的探索性数据分析（EDA）已经能帮我们发现群体的宏观风险。作为“保险+AI”探索的核心，我的下一步计划是：打破传统精算的二维交叉分析局限，引入 <b>机器学习算法（如 XGBoost 或 随机森林）</b>。我将结合数据集中可能存在的 <code>fraud_reported</code>（欺诈标签），输入年龄、性别、品牌、出险地点等多维特征，训练一个<b>反欺诈智能评分模型</b>。未来的系统将实现从“事后宏观总结”向“事前微观预警”的跨越，为每一笔新报案打出“欺诈概率分”！
    </div>
</div>
""", unsafe_allow_html=True)
