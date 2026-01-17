import json
import matplotlib.pyplot as plt
import numpy as np
import os


STATS_PATH = "stats.json"
OUTPUT_PATH = "screenshots/evolucao_linguagens.png"


# ---------------------------------------------------------
# 1. Ler stats.json
# ---------------------------------------------------------
def load_stats():
    with open(STATS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


# ---------------------------------------------------------
# 2. Obter top linguagens (ignorando "colors")
# ---------------------------------------------------------
def get_top_languages(stats, limit=5):
    # Filtrar apenas linguagens com valores numéricos
    filtered = {k: v for k, v in stats.items() if isinstance(v, int)}

    # Ordenar por número de bytes
    sorted_langs = sorted(filtered.items(), key=lambda x: x[1], reverse=True)

    return sorted_langs[:limit]


# ---------------------------------------------------------
# 3. Gerar gráfico de barras com cores estáveis
# ---------------------------------------------------------
def generate_bar_chart(top_langs, colors):
    labels = [lang for lang, _ in top_langs]
    values = [count for _, count in top_langs]

    # Obter cores estáveis
    bar_colors = [colors.get(lang, "#00ffff") for lang in labels]

    y_pos = np.arange(len(labels))

    plt.figure(figsize=(10, 5))
    plt.barh(y_pos, values, color=bar_colors)
    plt.yticks(y_pos, labels)
    plt.xlabel("Bytes de código")
    plt.title("Linguagens mais usadas — Evolução Cerimonial Hydra")

    plt.tight_layout()
    plt.savefig(OUTPUT_PATH)
    plt.close()


# ---------------------------------------------------------
# 4. Fluxo principal
# ---------------------------------------------------------
def main():
    stats = load_stats()

    # Obter top linguagens
    top = get_top_languages(stats)

    # Obter mapa de cores estável
    colors = stats.get("colors", {})

    # Gerar gráfico
    generate_bar_chart(top, colors)

    print("[Hydra] evolucao_linguagens.png regenerado com dignidade.")


if __name__ == "__main__":
    main()
