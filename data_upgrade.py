import pandas as pd

print("⏳ 正在启动数据现代化翻新程序...")

# 1. 读取原始历史数据
original_file = "car_insurance_claims.csv"
df = pd.read_csv(original_file)

# 2. 财务数据通胀调整 (Trending)
# 结合 2015-2026 年的 CPI 变化及汽车维修零整比上升趋势，设定综合通胀系数为 1.35 (即上涨35%)
inflation_rate = 1.35
if 'total_claim_amount' in df.columns:
    df['total_claim_amount'] = df['total_claim_amount'] * inflation_rate
    print(f"✅ 已将 [total_claim_amount] 按 {inflation_rate} 倍通胀系数进行上调。")

# 3. 时间轴平移 (Time Shifting)
# 天池/Kaggle 数据集常见的日期列名。将时间整体向后推移 11 年，对齐到 2026 年。
date_columns = ['incident_date', 'policy_bind_date', 'auto_year']

for col in date_columns:
    if col in df.columns:
        if col == 'auto_year':
            # 如果是车辆年份，直接加 11 年
            df[col] = df[col] + 11
            print(f"✅ 已将 [{col}] 车辆年份平移至当前时代。")
        else:
            # 如果是具体日期，转换为时间格式后加上 11 年
            df[col] = pd.to_datetime(df[col], errors='coerce')
            df[col] = df[col] + pd.DateOffset(years=11)
            df[col] = df[col].dt.strftime('%Y-%m-%d') # 转回清晰的字符串格式
            print(f"✅ 已将 [{col}] 发生日期平移 11 年。")

# 4. 保存为全新的数据集
new_filename = "car_insurance_claims_2026.csv"
df.to_csv(new_filename, index=False)
print(f"🎉 数据翻新大功告成！全新数据集已保存为: {new_filename}")
