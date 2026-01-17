import json
from PIL import Image, ImageDraw

# Caminhos
OUTPUT_PNG = "screenshots/evolucao_linguagens.png"
BACKGROUND_PATH = "screenshots/fundo_adn.png"

# Dimensões
WIDTH = 800
HEIGHT = 400
MAX_BARS = 5


# 1. Ler stats.json
def load_stats(path="stats.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# 2. Extrair top linguagens
def get_top_languages(stats, max_slices=MAX_BARS):
    filtered = {k: v for k, v in stats.items() if isinstance(v, int)}
    sorted_langs = sorted(filtered.items(), key=lambda x: x[1], reverse=True)
    return sorted_langs[:max_slices]


# 3. Gradiente vertical Hydra
def draw_gradient(draw, x, y, w, h):
    for i in range(h):
        t = i / h
        r = int(0 * (1 - t) + 0 * t)
        g = int(255 * (1 - t) + 102 * t)
        b = int(255 * (1 - t) + 0 * t)
        draw.line([(x, y + i), (x + w, y + i)], fill=(r, g, b))


# 4. Glow cerimonial
def draw_glow(draw, x, y, w, h):
    glow_color = (0, 255, 255, 80)
    for i in range(12):
        draw.rectangle(
            [x - i, y - i, x + w + i, y + h + i],
            outline=glow_color
        )


# 5. Gerar PNG com fundo ADN
def generate_png(stats, output_path=OUTPUT_PNG, background_path=BACKGROUND_PATH):
    bg = Image.open(background_path).resize((WIDTH, HEIGHT))
    img = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    values = [v for _, v in stats]
    max_value = max(values) if max(values) > 0 else 1

    bar_area_width = WIDTH * 0.8
    bar_area_height = HEIGHT * 0.7
    bar_width = bar_area_width / (MAX_BARS * 1.5)
    spacing = bar_width * 0.5
    x_start = (WIDTH - bar_area_width) / 2
    y_base = HEIGHT * 0.85

    for i, (lang, value) in enumerate(stats):
        h = (value / max_value) * bar_area_height
        x = x_start + i * (bar_width + spacing)
        y = y_base - h

        draw_glow(draw, x, y, bar_width, h)
        draw_gradient(draw, x, y, bar_width, int(h))

    final = Image.alpha_composite(bg.convert("RGBA"), img)
    final.save(output_path)
    print(f"[Hydra] PNG gerado com filamentos: {output_path}")


# 6. Executar
def main():
    stats = load_stats()
    top = get_top_languages(stats)
    generate_png(top)


if __name__ == "__main__":
    main()
