<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<title>Soft Rain Curtain · Weather Mood Visualisation</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    background: radial-gradient(ellipse at center, #281458 0%, #05030f 70%);
    font-family: 'Segoe UI', sans-serif;
    color: #fff;
    text-align: center;
    padding: 30px 20px;
    min-height: 100vh;
  }
  h2 {
    font-size: 24px;
    font-weight: 300;
    letter-spacing: 2px;
    margin-bottom: 8px;
  }
  .sub {
    opacity: 0.6;
    font-size: 14px;
    margin-bottom: 18px;
  }
  canvas {
    width: min(900px, 92vw);
    border-radius: 16px;
    box-shadow: 0 0 60px rgba(160, 120, 255, 0.25);
    background: linear-gradient(180deg, #1c1042 0%, #000 100%);
    cursor: pointer;
  }
  .desc {
    margin-top: 22px;
    font-size: 15px;
    opacity: 0.75;
    line-height: 1.6;
    max-width: 720px;
    margin-left: auto;
    margin-right: auto;
  }
</style>
</head>
<body>

<h2>RAIN CURTAIN</h2>
<p class="sub">Move your mouse to gently pull open the soft rain curtain</p>

<canvas id="rainCanvas" width="900" height="520"></canvas>

<div class="desc">
  This interactive webpage visualises rainfall as a soft light curtain.
  Denser rain creates a heavier, more opaque atmosphere; lighter rain becomes
  a brighter, more transparent veil. The curtain bends, stretches, and springs
  back like a flexible fabric.
</div>

<script>
const canvas = document.getElementById("rainCanvas");
const ctx = canvas.getContext("2d");

const W = canvas.width;
const H = canvas.height;

let mouseX = -9999;
let mouseY = H / 2;
let mouseActive = false;

// 雨帘线条数量，后续可以对接降雨数据修改
const LINE_COUNT = 70;
const lines = [];

for (let i = 0; i < LINE_COUNT; i++) {
  lines.push({
    baseX: 12 + (i * (W - 24) / (LINE_COUNT - 1)),
    x: 12 + (i * (W - 24) / (LINE_COUNT - 1)),
    offset: 0,
    bend: 0,
    speed: 0.0004 + Math.random() * 0.0008,
    phase: Math.random() * Math.PI * 2
  });
}

canvas.addEventListener("mousemove", e => {
  const rect = canvas.getBoundingClientRect();
  mouseX = (e.clientX - rect.left) * (W / rect.width);
  mouseY = (e.clientY - rect.top) * (H / rect.height);
  mouseActive = true;
});

canvas.addEventListener("mouseleave", () => {
  mouseActive = false;
});

canvas.addEventListener("touchmove", e => {
  if (e.touches[0]) {
    const rect = canvas.getBoundingClientRect();
    mouseX = (e.touches[0].clientX - rect.left) * (W / rect.width);
    mouseY = (e.touches[0].clientY - rect.top) * (H / rect.height);
    mouseActive = true;
  }
});

canvas.addEventListener("touchend", () => {
  mouseActive = false;
});

function drawRainCurtain(time) {
  // 紫梦幻背景
  const bg = ctx.createLinearGradient(0, 0, 0, H);
  bg.addColorStop(0, "#1c1042");
  bg.addColorStop(1, "#02030a");
  ctx.fillStyle = bg;
  ctx.fillRect(0, 0, W, H);

  // 绘制柔软弯曲雨帘
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];

    if (mouseActive) {
      const dx = mouseX - line.baseX;
      const dy = Math.abs(mouseY - H / 2);
      const influence = Math.max(0, 1 - Math.abs(dx) / 140) * Math.max(0, 1 - dy / 200);
      line.offset += (dx * 0.35 - line.offset) * 0.12;
      line.bend += (influence * 0.9 - line.bend) * 0.08;
    } else {
      // 松手缓慢回弹，模拟布料柔软感
      line.offset *= 0.86;
      line.bend *= 0.88;
    }

    // 细微波浪飘动
    const wave = Math.sin(time * line.speed + line.phase) * 1.2 * line.bend;
    const currentX = line.baseX + line.offset + wave;

    // 外层紫蓝光带
    ctx.beginPath();
    ctx.moveTo(line.baseX, 0);
    ctx.quadraticCurveTo(currentX, H / 2, currentX, H);
    ctx.strokeStyle = `rgba(160,120,255, ${0.18 + line.bend * 0.25})`;
    ctx.lineWidth = 1 + line.bend * 0.6;
    ctx.shadowColor = "rgba(170, 130, 255, 0.8)";
    ctx.shadowBlur = 6 + line.bend * 8;
    ctx.stroke();

    // 内层高亮线
    ctx.beginPath();
    ctx.moveTo(line.baseX, 0);
    ctx.quadraticCurveTo(currentX, H / 2, currentX, H);
    ctx.strokeStyle = `rgba(220, 200, 255, ${0.35 + line.bend * 0.3})`;
    ctx.lineWidth = 0.6;
    ctx.shadowBlur = 0;
    ctx.stroke();

    // 泪滴雨滴粒子，沿着曲线下落
    const dropSpacing = 40;
    for (let y = (time * 0.06 * (0.8 + (i % 5) * 0.1)) % dropSpacing; y < H; y += dropSpacing) {
      const t = y / H;
      const dropX = line.baseX + (currentX - line.baseX) * t + wave * t;
      drawDrop(dropX, y, 2.2 + line.bend * 0.6, `rgba(210,190,255, 0.85)`);
    }

    // 掀开区域 金色发光粒子（参考星星窗帘的高光效果）
    if (line.bend > 0.3) {
      for (let k = 0; k < 2; k++) {
        const py = (time * 0.09 + k * 200 + i * 13) % H;
        const px = currentX + (Math.random() - 0.5) * 10 * line.bend;
        ctx.beginPath();
        ctx.arc(px, py, 1.1 + Math.random() * 0.6, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(255, 220, 120, ${0.3 + Math.random() * 0.3})`;
        ctx.shadowColor = "rgba(255, 200, 80, 0.9)";
        ctx.shadowBlur = 8;
        ctx.fill();
      }
    }
  }

  ctx.shadowBlur = 0;
  requestAnimationFrame(drawRainCurtain);
}

// 绘制泪滴形状雨滴
function drawDrop(x, y, size, color) {
  ctx.beginPath();
  ctx.moveTo(x, y - size);
  ctx.lineTo(x - size * 0.65, y + size * 0.7);
  ctx.lineTo(x + size * 0.65, y + size * 0.7);
  ctx.closePath();
  ctx.fillStyle = color;
  ctx.shadowColor = "rgba(180,140,255, 0.6)";
  ctx.shadowBlur = 4;
  ctx.fill();
}

drawRainCurtain(performance.now());
</script>

</body>
</html>
