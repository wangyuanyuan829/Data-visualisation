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

# ========= 色彩心理学｜梦幻雨帘配色 =========
scene_list = []
for rain in rain_values:
    if rain <= 0:
        mood_text = "Bright, Calm (Sunny)"
        bg_color = "#1a0633"      # 深紫夜空
        line_color = "#cbb8ff"    # 淡紫雨线
        drop_color = "#ffe8ff"   # 浅粉水滴
        line_count = 8
        drop_speed = 0.15
    elif rain <=5:
        mood_text = "Soft, Quiet (Light Rain)"
        bg_color = "#201045"
        line_color = "#a890f0"
        drop_color = "#e6d0ff"
        line_count = 20
        drop_speed = 0.35
    elif rain <=15:
        mood_text = "Damp, Gentle (Moderate Rain)"
        bg_color = "#181b50"
        line_color = "#6096ff"
        drop_color = "#c6e2ff"
        line_count = 45
        drop_speed = 0.6
    else:
        mood_text = "Heavy, Somber (Heavy Rain)"
        bg_color = "#0b1030"
        line_color = "#246bff"
        drop_color = "#94c8ff"
        line_count = 80
        drop_speed = 1.0
    scene_list.append({
        "rain":rain, "mood":mood_text,
        "bg":bg_color, "line_c":line_color, "drop_c":drop_color,
        "lines":line_count, "spd":drop_speed
    })

# 画布设置
fig, ax = plt.subplots(figsize=(10,6), dpi=120)
ax.set_xlim(0,100)
ax.set_ylim(0,60)
ax.set_axis_off()

# 初始化
current_scene = scene_list[0]
fig.patch.set_facecolor(current_scene["bg"])
ax.set_facecolor(current_scene["bg"])

# 竖线雨帘：存储每条竖线x坐标，水滴y坐标
x_lines = np.linspace(5,95, current_scene["lines"])
# 每条线上面多个水滴
drops_per_line = 6
drop_x = []
drop_y = []
for xi in x_lines:
    for _ in range(drops_per_line):
        drop_x.append(xi)
        drop_y.append(np.random.uniform(0,60))
drop_x = np.array(drop_x)
drop_y = np.array(drop_y)

# 画雨帘竖线
line_objs = []
for xi in x_lines:
    l, = ax.plot([xi,xi], [0,60], color=current_scene["line_c"], alpha=0.3, lw=1)
    line_objs.append(l)
# 水滴标记，用marker="v" 水滴形状
drops, = ax.plot(drop_x, drop_y, marker="v", linestyle="", color=current_scene["drop_c"], markersize=4, alpha=0.9)
info_text = ax.text(5,55, f"Average Rain: {current_scene['rain']:.1f} mm\nMood: {current_scene['mood']}",
                    color="#ffffff", fontsize=11)


def update(frame):
    global drop_x, drop_y, x_lines, line_objs
    idx = frame % len(scene_list)
    s = scene_list[idx]

    # 更新背景
    fig.patch.set_facecolor(s["bg"])
    ax.set_facecolor(s["bg"])

    # 重新生成雨帘竖线
    new_x_lines = np.linspace(5,95, s["lines"])
    # 清除旧线条
    for l in line_objs:
        l.remove()
    line_objs = []
    for xi in new_x_lines:
        l, = ax.plot([xi,xi], [0,60], color=s["line_c"], alpha=0.3, lw=1)
        line_objs.append(l)

    # 更新水滴：持续下落
    drop_y = drop_y - s["spd"]
    # 落到底部，回到顶部
    drop_y[drop_y < 0] = 60
    # 绑定水滴到竖线
    new_drop_x = []
    new_drop_y = []
    for xi in new_x_lines:
        for _ in range(drops_per_line):
            new_drop_x.append(xi)
            new_drop_y.append(np.random.uniform(0,60))
    drop_x = np.array(new_drop_x)
    drop_y = np.array(new_drop_y)

    drops.set_data(drop_x, drop_y)
    drops.set_color(s["drop_c"])
    info_text.set_text(f"Average Rain: {s['rain']:.1f} mm\nMood: {s['mood']}")
    return drops, info_text

ani = FuncAnimation(fig, update, frames=len(scene_list), interval=800, blit=True)
ani.save("site/rain_atmosphere.gif", writer="pillow", fps=10)
plt.close()

# ========= 生成带【鼠标掀开雨帘】互动的 index.html（Canvas 网页）=========
html = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Rainfall Mood Curtain Visualisation</title>
    <style>
        *{margin:0;padding:0;box-sizing:border-box}
        body{background:#0b1030; font-family:sans-serif; color:#fff; text-align:center; padding:20px;}
        canvas{border-radius:10px; max-width:90vw;}
        .desc{margin-top:20px; font-size:17px;}
    </style>
</head>
<body>
    <h2>Rain Curtain · Weather Mood Visualisation</h2>
    <p style="opacity:0.7; margin:8px 0">Move your mouse over to pull open the rain curtain</p>
    <canvas id="rainCanvas" width="900" height="520"></canvas>
    <div class="desc">
        Visual mapping based on colour psychology.<br>
        Rainfall controls curtain density and atmosphere.
    </div>
    <script>
        const canvas = document.getElementById("rainCanvas");
        const ctx = canvas.getContext("2d");
        let mouseX = -100;
        let lines = [];
        const totalLines = 70;

        // 初始化雨帘竖线
        for(let i=0;i<totalLines;i++){
            lines.push({
                baseX: 10 + i*(canvas.width-20)/totalLines,
                offset:0,
                speed: 1.2 + Math.random()*0.8
            })
        }
        canvas.onmousemove = e=>{
            const rect = canvas.getBoundingClientRect();
            mouseX = e.clientX - rect.left;
        }
        canvas.onmouseleave = ()=> mouseX = -100;

        function draw(){
            ctx.fillStyle="#0b1030";
            ctx.fillRect(0,0,canvas.width,canvas.height);

            lines.forEach(line=>{
                // 鼠标附近，雨线向两边偏移，制造掀开效果
                const dist = Math.abs(line.baseX - mouseX);
                if(dist < 120){
                    line.offset = (mouseX - line.baseX) * 0.4;
                }else{
                    line.offset *=0.92;
                }
                const x = line.baseX + line.offset;
                // 画雨线
                ctx.beginPath();
                ctx.moveTo(x, 0);
                ctx.lineTo(x, canvas.height);
                ctx.strokeStyle="#6096ff44";
                ctx.lineWidth=1;
                ctx.stroke();
                // 循环下落水滴
                for(let y= (Date.now()*0.04 * line.speed) % canvas.height; y>0; y-=70){
                    ctx.beginPath();
                    ctx.moveTo(x, y);
                    ctx.lineTo(x-4, y+9);
                    ctx.lineTo(x+4, y+9);
                    ctx.closePath();
                    ctx.fillStyle="#c6e2ff";
                    ctx.fill();
                }
            })
            requestAnimationFrame(draw);
        }
        draw();
    </script>
</body>
</html>
'''
with open("site/index.html","w",encoding="utf-8") as f:
    f.write(html)

print("✅ Done! Rain Curtain GIF + Interactive HTML saved to site/")
