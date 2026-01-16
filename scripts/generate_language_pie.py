import json
import matplotlib.pyplot as plt

# Caminho de saída
OUTPUT_PNG = "screenshots/language_pie.png"
MAX_SLICES = 5


# 1. Ler stats.json
def load_stats(path="stats.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# 2. Extrair top linguagens
def get_top_languages(stats, max_slices=MAX_SLICES):
    sorted_langs = sorted(stats.items(), key=lambda x: x[1], reverse=True)
    return sorted_langs[:max_slices]


# 3. Gerar gráfico circular
def generate_pie_chart(stats_path="stats.json", output_path=OUTPUT_PNG):
    stats = load_stats(stats_path)
    top = get_top_languages(stats)

    labels = [lang for lang, _ in top]
    values = [v for _, v in top]
    total = sum(values) if sum(values) > 0 else 1
    percentages = [v / total * 100 for v in values]

    fig, ax = plt.subplots(figsize=(6, 6), dpi=150)
    fig.patch.set_facecolor("black")
    ax.set_facecolor("black")

    colors = ["#00ffff", "#0066ff", "#7f00ff", "#00ff99", "#ff00aa"]

    wedges, _, autotexts = ax.pie(
        values,
        colors=colors[:len(values)],
        startangle=90,
        counterclock=False,
        autopct=lambda pct: f"{pct:.1f}%",
        pctdistance=0.8,
        textprops={"color": "#00ffff", "fontsize": 10},
    )

    legend_labels = [
        f"{lang}: {val} bytes ({pct:.1f}%)"
        for (lang, val), pct in zip(top, percentages)
    ]

    ax.legend(
        wedges,
        legend_labels,
        title="Linguagens mais usadas",
        loc="center left",
        bbox_to_anchor=(1, 0, 0.5, 1),
        facecolor="black",
        edgecolor="#00ffff",
        labelcolor="#00ffff",
    )

    ax.set_title("Linguagens mais usadas", color="#00ffff", fontsize=14, pad=20)

    plt.tight_layout()
    plt.savefig(output_path, transparent=True, facecolor=fig.get_facecolor())
    plt.close(fig)

    print(f"[Hydra] Pie chart gerado em: {output_path}")


# 4. Executar
if __name__ == "__main__":
    generate_pie_chart()
