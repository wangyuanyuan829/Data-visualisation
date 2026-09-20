# /// script
# requires-python = ">=3.10"
# dependencies = ["requests"]
# ///
import json

# 模拟香港各站点一小时累计降雨量数据
result = {
    "rainfall_regions": [
        {"place": "Quarry Bay", "max": 12},
        {"place": "Central", "max": 8},
        {"place": "Kowloon", "max": 15},
        {"place": "Shatin", "max": 6},
        {"place": "Tsuen Wan", "max": 9}
    ],
    "humidity": 78,
    "record_time": "2026-09-20T15:00:00"
}

# 输出weather_data.json
with open("weather_data.json", "w", encoding="utf-8") as f:
    json.dump(result, f, indent=2, ensure_ascii=False)

print("✅ 模拟雨量数据已生成 weather_data.json")
