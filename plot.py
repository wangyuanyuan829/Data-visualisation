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

# 读取fetch生成的雨量数据
with open("weather_data.json", "r", encoding="utf-8") as f:
    weather = json.load(f)

rain_values = [region["max"] for region in weather["rainfall_regions"]]
avg_rain = np.mean(rain_values)
humidity = weather["humidity"]

fig, ax = plt.subplots(figsize=(10, 6), dpi=120)
ax.set_xlim(0, 100)
ax.set_ylim(0, 60)
ax.axis("off")

# 根据平均雨量切换画面风格
if avg_rain <= 0:
    bg_colour = "#fff8e8"
    drop_colour = "#ffd782"
    drop_count = 30
    drop_speed = 0.25
elif avg_rain < 10:
    bg_colour = "#d7e4f0"
    drop_colour = "#82a8d0"
    drop_count = 100
    drop_speed = 0.4
elif avg_rain < 30:
    bg_colour = "#547899"
    drop_colour = "#2c4b70"
    drop_count = 280
    drop_speed = 0.7
else:
    bg_colour = "#141c29"
    drop_colour = "#b8cbe6"
    drop_count = 600
    drop_speed = 1.1

fig.patch.set_facecolor(bg_colour)
x = np.random.uniform(0, 100, drop_count)
y = np.random.uniform(0, 60, drop_count)
raindrops, = ax.plot(x, y, '.', color=drop_colour, markersize=1.8, alpha=0.72)

def animate(frame):
    global x, y
    y = y - drop_speed
    reset_mask = y < 0
    y[reset_mask] = 60
    x[reset_mask] = np.random.uniform(0, 100, np.sum(reset_mask))
    raindrops.set_data(x, y)
    return raindrops,

# 导出GIF动画
animation = FuncAnimation(fig, animate, frames=140, interval=42, blit=True)
animation.save("site/rain_atmosphere.gif", writer="pillow")

# 生成网页index.html
html_page = f"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Weather Atmosphere</title>
<style>
body {{margin:0;background:#0f0f14;color:#f2f2f2;font-family:system-ui,sans-serif;text-align:center;padding:4rem 2rem;}}
.wrapper{{max-width:920px;margin:0 auto;}}
img{{width:100%;border-radius:8px;}}
</style>
</head>
<body>
<div class="wrapper">
<h1>Weather Atmosphere</h1>
<p>Real-time Hong Kong rainfall mood visualisation</p>
<img src="rain_atmosphere.gif">
<p>Average rainfall: {avg_rain:.2f} mm | Humidity: {humidity}%</p>
<p>Data source: Hong Kong Observatory Open Data API</p>
</div>
</body>
</html>
"""
with open("site/index.html", "w", encoding="utf-8") as html_file:
    html_file.write(html_page)

print("✅ GIF已生成在 site/rain_atmosphere.gif")
