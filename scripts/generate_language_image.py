import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import numpy as np

# Dados de exemplo (depois podemos integrar com update_stats.py)
languages = {
    'C#': 1071147,
    'CSS': 813893,
    'Jupyter Notebook': 271015,
    'QML': 121088,
    'JavaScript': 74520,
}

# Paleta baseada em pares telefónicos (menos usado → mais usado)
telephone_pairs = [
    "#0057B7",  # Azul
    "#FFA500",  # Laranja
    "#008000",  # Verde
    "#8B4513",  # Castanho
    "#808080",  # Cinzento
]

# Ordenar linguagens da menos usada → mais usada
sorted_langs = sorted(languages.items(), key=lambda x: x[1])

# Atribuir cores às linguagens
color_map = {}
for i, (lang, _) in enumerate(sorted_langs):
    color_map[lang] = telephone_pairs[i]

# Função para fazer interpolação linear entre duas cores HEX
def lerp_color(c1: str, c2: str, t: float) -> str:
    c1_rgb = tuple(int(c1[i:i + 2], 16) for i in (1, 3, 5))
    c2_rgb = tuple(int(c2[i:i + 2], 16) for i in (1, 3, 5))
    r = int(c1_rgb[0] + (c2_rgb[0] - c1_rgb[0]) * t)
    g = int(c1_rgb[1] + (c2_rgb[1] - c1_rgb[1]) * t)
    b = int(c1_rgb[2] + (c2_rgb[2] - c1_rgb[2]) * t)
    return f"#{r:02X}{g:02X}{b:02X}"

# Criar figura com fundo transparente
fig, ax = plt.subplots(figsize=(12, 6))
fig.patch.set_alpha(0)

# Cor base: linguagem mais usada
base_color = telephone_pairs[-1]
grad_color = lerp_color(base_color, "#FFFFFF", 0.6)

# Retângulo semi-transparente à esquerda
rect = FancyBboxPatch(
    (0.05, 0.1), 0.45, 0.8,
    boxstyle="round,pad=0.3",
    linewidth=2,
    edgecolor=grad_color,
    facecolor=(0, 0, 0, 0.25),
)
ax.add_patch(rect)

# Título dentro do retângulo
ax.text(0.07, 0.85, "Linguagens mais usadas:", fontsize=16, color=grad_color)

# Listagem das linguagens (do mais usado → menos usado)
y = 0.75
for lang, count in sorted_langs[::-1]:
    ax.text(
        0.07,
        y,
        f"{lang}: {count} bytes",
        fontsize=14,
        color=color_map[lang],
    )
    y -= 0.12

# Gráfico circular à direita
ax_pie = fig.add_axes([0.55, 0.15, 0.4, 0.7])
ax_pie.pie(
    [v for _, v in sorted_langs],
    labels=[k for k, _ in sorted_langs],
    colors=[color_map[k] for k, _ in sorted_langs],
    autopct='%1.1f%%',
    textprops={'color': 'white'},
)

ax.axis('off')

# Guardar imagem com fundo transparente
plt.savefig("language_stats.png", transparent=True, dpi=200)
plt.close()

