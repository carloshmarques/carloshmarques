import json
import os
from github import Github, Auth

LOCK_PATH = "stats-lock.json"
README_PATH = "README.md"
STATS_PATH = "stats.json"


# ---------------------------------------------------------
# 1. Função para gerar cores estáveis e imutáveis
# ---------------------------------------------------------
def assign_stable_colors(language_names):
    palette = [
        "#00bfff", "#ff00ff", "#00ffcc", "#9933ff", "#00ffff",
        "#ff8800", "#ff4444", "#44ff44", "#ffcc00", "#cc00ff"
    ]
    sorted_langs = sorted(language_names)
    return {lang: palette[i % len(palette)] for i, lang in enumerate(sorted_langs)}


# ---------------------------------------------------------
# 2. Recolher linguagens de todos os repositórios
# ---------------------------------------------------------
def collect_language_stats():
    token = os.getenv("GH_TOKEN")
    if not token:
        raise RuntimeError("GH_TOKEN não encontrado nas variáveis de ambiente.")

    g = Github(auth=Auth.Token(token))
    user = g.get_user("carloshmarques")

    languages = {}

    for repo in user.get_repos():
        try:
            langs = repo.get_languages()
            for lang, count in langs.items():
                languages[lang] = languages.get(lang, 0) + count
        except Exception:
            pass

    sorted_langs = sorted(languages.items(), key=lambda x: x[1], reverse=True)
    color_map = assign_stable_colors(languages.keys())

    stats = {lang: count for lang, count in sorted_langs}
    stats["colors"] = color_map

    with open(STATS_PATH, "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=4, ensure_ascii=False)

    print("[Hydra] stats.json regenerado com cores estáveis.")
    return stats


# ---------------------------------------------------------
# 3. Calcular percentagens para pie chart
# ---------------------------------------------------------
def compute_pie_percentages(stats):
    total = sum(stats.values()) if sum(stats.values()) > 0 else 1
    return {lang: (value / total) * 100 for lang, value in stats.items()}


# ---------------------------------------------------------
# 4. Guardar estado no stats-lock.json
# ---------------------------------------------------------
def save_new_stats(html_content, stats):
    pie = compute_pie_percentages({k: v for k, v in stats.items() if k != "colors"})
    data = {
        "html_content": html_content,
        "previous_stats": stats,
        "previous_pie": pie
    }
    with open(LOCK_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print("[Hydra] stats-lock.json atualizado com pie chart.")


# ---------------------------------------------------------
# 5. Atualizar painel superior no README
# ---------------------------------------------------------
def update_readme_panel():
    html = """
<table width="100%" style="border:2px solid #00ffff; border-radius:6px;">
<tr>
<td>
<img src="screenshots/evolucao_linguagens.png" width="500px" height="250px"
style="border:2px solid #00ffff; border-radius:6px;">
</td>

<td style="text-align:left; padding:0 20px;">
<em>“Tudo flui, nada permanece.” — Heraclito</em><br><br>
<em>“Nada se perde, tudo se transforma.” — Lavoisier</em><br><br>
<em><a href="https://github.com/carloshmarques/HydraLife" style="color:#00ffff;">
“O software é uma entidade viva.” — HydraLife</a></em>
</td>
</tr>
</table>
""".strip()

    with open(README_PATH, "r", encoding="utf-8") as f:
        readme = f.read()

    start = "<!--HYDRA-CHAMBER-OPEN-->"
    end = "<!--HYDRA-CHAMBER-CLOSE-->"

    if start not in readme or end not in readme:
        raise Exception("Marcadores HYDRA-CHAMBER-OPEN/CLOSE não encontrados no README.md")

    before, _, rest = readme.partition(start)
    _, _, after = rest.partition(end)

    new_readme = before + start + "\n" + html + "\n" + end + after

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(new_readme)

    print("[Hydra] README atualizado com o painel cerimonial.")
    return html


# ---------------------------------------------------------
# 6. Atualizar bloco textual + pie chart
# ---------------------------------------------------------
def update_readme_stats(stats):
    top = [(k, v) for k, v in stats.items() if k != "colors"][:5]
    colors = stats.get("colors", {})

    html = """
<table width="100%" style="border:2px solid #00ffff; border-radius:6px;">
<tr>

<td width="50%" style="vertical-align:top; padding:10px;">
<h3>Linguagens mais usadas (atualizado automaticamente)</h3>
<ul>
"""
    for lang, count in top:
        color = colors.get(lang, "#00ffff")
        html += f'<li><strong style="color:{color}">{lang}</strong> — {count} bytes de código</li>\n'

    html += """
</ul>
</td>

<td width="50%" style="text-align:center; padding:10px;">
<img src="screenshots/language_pie.png"
     style="width:100%; height:auto; border:2px solid #00ffff; border-radius:6px;">
</td>

</tr>
</table>
"""

    with open(README_PATH, "r", encoding="utf-8") as f:
        readme = f.read()

    start = "<!--LANG-STATS-START-->"
    end = "<!--LANG-STATS-END-->"

    before, _, rest = readme.partition(start)
    _, _, after = rest.partition(end)

    new_readme = before + start + "\n" + html + "\n" + end + after

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(new_readme)

    print("[Hydra] README atualizado com lista + pie chart harmonizados.")



# ---------------------------------------------------------
# 7. Fluxo principal
# ---------------------------------------------------------
def main():
    stats = collect_language_stats()
    html_panel = update_readme_panel()
    update_readme_stats(stats)
    save_new_stats(html_panel, stats)
    print("[Hydra] update_stats.py concluído com dignidade.")


if __name__ == "__main__":
    main()
