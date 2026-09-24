# /// script
# requires-python = ">=3.10"
# dependencies = ["requests"]
# ///
import requests
import csv
import json
from pathlib import Path

# 香港天文台官方真实雨量CSV
url = "https://data.weather.gov.hk/weatherAPI/cis/csvfile/HKO/ALL/daily_HKO_RF_ALL.csv"

Path("data").mkdir(exist_ok=True)
Path("site").mkdir(exist_ok=True)

csv_path = Path("data/daily_HKO_RF_ALL.csv")
json_path = Path("site/rain_data.json")

resp = requests.get(url, timeout=15)
resp.raise_for_status()
csv_text = resp.text
csv_path.write_text(csv_text, encoding="utf-8-sig")

rows = []
reader = csv.reader(csv_text.splitlines())

for row in reader:
    # 过滤：行太短直接跳过；年份必须能转成数字，跳过所有说明/注释行
    if len(row) < 4:
        continue
    year_str = row[0].strip()
    # 只处理年份是纯数字的行，直接跳过文字注释行，解决报错！
    if not year_str.isdigit():
        continue

    month_str = row[1].strip()
    day_str = row[2].strip()
    rain_raw = row[3].strip()

    # 天文台特殊标记处理
    if rain_raw == "Trace":
        rain = 0.5
    elif rain_raw == "-" or rain_raw == "":
        rain = 0.0
    else:
        try:
            rain = float(rain_raw)
        except ValueError:
            rain = 0.0

    year = int(year_str)
    month = int(month_str)
    day = int(day_str)

    # 色彩心理学情绪映射（你的作业设计）
    if rain <= 0:
        mood_name = "Calm · 晴朗宁静"
        mood_key = "clear"
    elif 0 < rain <= 5:
        mood_name = "Soft · 细雨舒缓"
        mood_key = "lightrain"
    elif 5 < rain <= 20:
        mood_name = "Heavy · 大雨压抑"
        mood_key = "heavyrain"
    else:
        mood_name = "Storm · 暴雨躁动"
        mood_key = "storm"

    rows.append({
        "year": year,
        "month": month,
        "day": day,
        "rainfall_mm": rain,
        "mood": mood_name,
        "mood_key": mood_key
    })

# 筛选2026年
data_2026 = [item for item in rows if item["year"] == 2026]

json_path.write_text(json.dumps(data_2026, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"✅ 香港天文台真实雨量，一共 {len(data_2026)} 条2026记录，写入 site/rain_data.json")
