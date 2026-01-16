import json
import cairosvg
from PIL import Image

SVG_WIDTH = 800
SVG_HEIGHT = 400
MAX_BARS = 5


# ---------------------------------------------------------
# 1. Ease-in-out para transição suave
# ---------------------------------------------------------
def ease_in_out(t):
    return 3 * t * t - 2 * t * t * t


# ---------------------------------------------------------
# 2. Alinhar estados (top 5, ordem fixa, zeros)
# ---------------------------------------------------------
def align_top5(previous_stats, new_stats):
    prev_sorted = sorted(previous_stats.items(), key=lambda x: x[1], reverse=True)
    new_sorted = sorted(new_stats.items(), key=lambda x: x[1], reverse=True)

    new_top = dict(new_sorted[:MAX_BARS])
    prev_top = dict(prev_sorted[:MAX_BARS])

    aligned_prev = {lang: prev_top.get(lang, 0) for lang in new_top.keys()}
    aligned_new = {lang: new_top.get(lang, 0) for lang in new_top.keys()}

    return aligned_prev, aligned_new


# ---------------------------------------------------------
# 3. Gerar SVG a partir de um dicionário de stats
# ---------------------------------------------------------
def generate_svg(stats, output_svg):
    values = list(stats.values())
    max_value = max(values) if max(values) > 0 else 1

    bar_area_width = SVG_WIDTH * 0.8
    bar_area_height = SVG_HEIGHT * 0.7
    bar_width = bar_area_width / (MAX_BARS * 1.5)
    spacing = bar_width * 0.5
    x_start = (SVG_WIDTH - bar_area_width) / 2
    y_base = SVG_HEIGHT * 0.85

    svg = []

    svg.append(
        f'<svg width="{SVG_WIDTH}" height="{SVG_HEIGHT}" '
        f'viewBox="0 0 {SVG_WIDTH} {SVG_HEIGHT}" '
        f'xmlns="http://www.w3.org/2000/svg">'
    )

    svg.append('<rect width="100%" height="100%" fill="#00000000"/>')

    svg.append("""
<defs>
  <linearGradient id="hydraGradient" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="#00ffff"/>
    <stop offset="50%" stop-color="#0066ff"/>
    <stop offset="100%" stop-color="#000000"/>
  </linearGradient>

  <filter id="hydraGlow">
    <feGaussianBlur in="SourceGraphic" stdDeviation="8">
      <animate attributeName="stdDeviation"
               values="8;18;8"
               dur="0.8s"
               repeatCount="indefinite"
               calcMode="spline"
               keySplines=".42 0 .58 1; .42 0 .58 1"/>
    </feGaussianBlur>

    <feColorMatrix type="matrix"
                   values="0 0 0 0 0
                           0 0 0 0 1
                           0 0 0 0 1
                           0 0 0 1 0"/>
  </filter>
</defs>
""")

    svg.append('<g id="bars" filter="url(#hydraGlow)">')

    for i, (lang, value) in enumerate(stats.items()):
        height = (value / max_value) * bar_area_height
        x = x_start + i * (bar_width + spacing)
        y = y_base - height

        svg.append(
            f'<rect x="{x}" y="{y}" width="{bar_width}" height="{height}" '
            f'fill="url(#hydraGradient)" stroke="#000" stroke-width="1"/>'
        )

