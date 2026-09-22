# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib","numpy","pillow"]
# ///
import json
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import os
os.makedirs("site", exist_ok=True)

# 读取雨量数据
with open("weather_data.json", "r", encoding="utf-8") as f:
    weather = json.load(f)
rain_values = [region["max"] for region in weather["rainfall_regions"]]

# 存储所有日期对应的视觉参数列表
scene_list = []
for rain in rain_values:
    if rain <= 0:
        mood_text = "Bright, Calm (Sunny)"
        bg_color = "#fff7bc"
        rain_color = "#fd8d3c"
        drop_count = 20
        drop_speed = 0.2
    elif rain <=5:
        mood_text = "Soft, Quiet (Light Rain)"
        bg_color = "#bdd7e7"
        rain_color = "#3182bd"
        drop_count = 60
        drop_speed = 0.4
    elif rain <=15:
        mood_text = "Damp, Gentle (Moderate Rain)"
        bg_color = "#6baed6"
        rain_color = "#08519c"
        drop_count = 150
        drop_speed = 0.7
    else:
        mood_text = "Heavy, Somber (Heavy Rain)"
        bg_color = "#2171b5"
        rain_color = "#032b47"
        drop_count = 300
        drop_speed = 1.2
    scene_list.append({"rain":rain, "mood":mood_text, "bg":bg_color, "rc":rain_color, "cnt":drop_count, "spd":drop_speed})

# 画布设置
fig, ax = plt.subplots(figsize=(10,6), dpi=120)
ax.set_xlim(0,100)
ax.set_ylim(0,60)
ax.set_axis_off()

# 初始化雨滴
current_scene = scene_list[0]
fig.patch.set_facecolor(current_scene["bg"])
ax.set_facecolor(current_scene["bg"])
x = np.random.uniform(0,100, size=current_scene["cnt"])
y = np.random.uniform(0,60, size=current_scene["cnt"])
raindrops, = ax.plot(x, y, marker=".", linestyle="", color=current_scene["rc"], markersize=3)
info_text = ax.text(5,55, f"Average Rain: {current_scene['rain']:.1f} mm\nMood: {current_scene['mood']}",
                    color="white", fontsize=11)

def update(frame):
    global x,y,raindrops,info_text
    # 根据帧数切换不同天气场景
    idx = frame % len(scene_list)
    s = scene_list[idx]

    # 更新画布背景颜色
    fig.patch.set_facecolor(s["bg"])
    ax.set_facecolor(s["bg"])

    # 雨滴数量变化：重新生成对应数量雨滴
    x = np.random.uniform(0,100, size=s["cnt"])
    y = np.random.uniform(0,60, size=s["cnt"])
    raindrops.set_color(s["rc"])
    raindrops.set_data(x,y)
    info_text.set_text(f"Average Rain: {s['rain']:.1f} mm\nMood: {s['mood']}")
    return raindrops, info_text

ani = FuncAnimation(fig, update, frames=len(scene_list), interval=600, blit=True)
# 导出GIF
ani.save("site/rain_atmosphere.gif", writer="pillow", fps=10)
plt.close()

# 网页，使用最后一组场景颜色
last_scene = scene_list[-1]
html = f'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Weather Mood Visualisation</title>
    <style>
        body {{
            background: {last_scene["bg"]};
            font-family: sans-serif;
            text-align: center;
            padding:30px;
        }}
        .container{{
            max-width:800px;
            margin:0 auto;
        }}
        img{{
            width:100%;
            border-radius:8px;
        }}
        .desc{{
            color:white;
            font-size:18px;
            margin-top:20px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h2>Rainfall → Mood Visualisation</h2>
        <img src="rain_atmosphere.gif">
        <div class="desc">
            Visual design based on color psychology<br>
            The animation cycles through different rainfall levels and corresponding emotional atmospheres
        </div>
    </div>
</body>
</html>
'''
with open("site/index.html","w",encoding="utf-8") as f:
    f.write(html)
print(f"✅ Done! Animation cycles through all rainfall mood scenes, GIF & HTML saved to site/")
