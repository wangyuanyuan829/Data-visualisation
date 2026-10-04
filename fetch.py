# /// script
# requires-python = ">=3.10"
# dependencies = ["pandas"]
# ///
import pandas as pd
import json
import os

os.makedirs("data", exist_ok=True)
os.makedirs("site", exist_ok=True)

csv_path = "data/daily_HKO_RF_ALL.csv"
# 跳过前两行说明文字
df = pd.read_csv(csv_path, skiprows=2)

rain_data = []
for _, row in df.iterrows():
    try:
        year = int(row.iloc[0])
        month = int(row.iloc[1])
        day = int(row.iloc[2])
        raw_val = str(row.iloc[3]).strip()

        # 天文台标记：Trace = 微量降雨，记为0
        if raw_val.upper() == "TRACE":
            rain = 0.0
        else:
            rain = float(raw_val)

        rain_data.append({
            "date": f"{year}-{month:02d}-{day:02d}",
            "rainfall": rain
        })
    except Exception:
        # 碰到脏数据自动跳过这一行，不中断程序
        continue

out_json_path = "site/rain_data.json"
with open(out_json_path, "w", encoding="utf-8") as f:
    json.dump(rain_data, f, ensure_ascii=False, indent=2)

print(f"✅ 成功！生成 {out_json_path}，一共 {len(rain_data)} 条降雨记录")