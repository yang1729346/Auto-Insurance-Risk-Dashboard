# 🛡️ 汽车保险索赔智能仪表板

> **Car Insurance Claims Intelligence Dashboard**  
> Made by **杨磊磊** · Powered by Streamlit + Plotly + Scikit-Learn

---

## 📊 项目简介

基于科大讯飞汽车保险索赔数据集（43万+条记录）构建的专业级交互式数据可视化仪表板，集成机器学习模型与多维度数据分析能力，为保险精算师、数据科学家和业务决策者提供实时洞察。

### 核心功能模块

| 模块 | 描述 |
|------|------|
| 📊 全局概览 | KPI 仪表卡、目标分布、区域索赔率、年龄/投保时长趋势 |
| 🗺️ 风险分布 | 年龄×车龄热力矩阵、区域 Treemap、3D 索赔曲面图 |
| 🚗 车辆特征 | 安全配置雷达图、气囊分析、发动机参数相关性 |
| 🤖 模型洞察 | Gradient Boosting 特征重要性、ROC曲线、K-Means聚类 |
| 🔬 深度下钻 | 多维筛选、平行坐标图、异常保单识别器、Sunburst |

---

## 🚀 本地部署

### 1. 克隆仓库

```bash
git clone https://github.com/YOUR_USERNAME/insurance-dashboard.git
cd insurance-dashboard
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 启动应用

```bash
streamlit run app.py
```

浏览器自动打开 `http://localhost:8501`

### 4. 上传数据

启动后，在左侧边栏上传 `train.csv` 文件，或选择「使用示例数据」直接体验。

> **数据说明**：`train.csv` 来自科大讯飞挑战赛「汽车保险索赔数据集」，包含 200,000 条训练记录，44 个特征字段。

---

## ☁️ Streamlit Cloud 部署（免费）

### 步骤 1：推送到 GitHub

```bash
# 初始化 Git 仓库
git init
git add .
git commit -m "feat: 车险索赔智能仪表板 by 杨磊磊"
git branch -M main

# 创建 GitHub 仓库后推送
git remote add origin https://github.com/YOUR_USERNAME/insurance-dashboard.git
git push -u origin main
```

> ⚠️ **注意**：由于 `train.csv`（28MB）较大，建议将数据文件加入 `.gitignore`，通过应用内上传功能加载数据。

### 步骤 2：连接 Streamlit Cloud

1. 访问 [share.streamlit.io](https://share.streamlit.io)
2. 点击 **「New app」**
3. 选择你的 GitHub 仓库
4. 主文件路径填写：`app.py`
5. 点击 **「Deploy!」**

### 步骤 3：访问应用

部署完成后获得公开 URL，格式为：
```
https://YOUR_USERNAME-insurance-dashboard-app-xxxxxx.streamlit.app
```

---

## 📁 项目结构

```
insurance-dashboard/
├── app.py                    # 主应用程序
├── requirements.txt          # Python 依赖
├── .streamlit/
│   └── config.toml          # Streamlit 主题配置
├── .gitignore               # Git 忽略文件
└── README.md                # 项目说明文档
```

---

## 🎨 技术栈

- **前端框架**：Streamlit 1.32+
- **可视化**：Plotly 5.18+（交互式图表）
- **机器学习**：Scikit-Learn（Gradient Boosting、K-Means）
- **数据处理**：Pandas 2.0+ / NumPy
- **主题设计**：深蓝色 InsurTech 风格，红-黄-绿渐变警示色

---

## 📖 数据字段说明

| 字段 | 含义 |
|------|------|
| `policy_tenure` | 投保时间段（归一化） |
| `age_of_car` | 汽车年龄（归一化） |
| `age_of_policyholder` | 投保人年龄 |
| `area_cluster` | 投保人区域集群（0-21） |
| `population_density` | 城市人口密度 |
| `airbags` | 安全气囊数量 |
| `ncap_rating` | NCAP安全评级（0-5星） |
| `target` | 是否在未来6个月内提出索赔（目标变量） |

完整字段说明详见 `汽车保险索赔数据集_readme.md`

---

## ⚡ 性能优化

- `@st.cache_data(ttl=300)` 数据缓存，避免重复加载
- 可调节样本量滑块（1,000 - 100,000 条）
- 大数据集自动采样，确保交互延迟 < 500ms
- Session State 缓存模型训练结果

---

## 📮 联系方式

**作者：杨磊磊**  
InsurTech Intelligence Platform · v2.0 · 2024

---

*数据来源：科大讯飞挑战赛「汽车保险索赔数据集」*  
*Citation: 小虎鲸5ieu (2023). 汽车保险索赔数据集. HeyWhale.*
