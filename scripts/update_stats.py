import json
import os
from github import Github, Auth

LOCK_PATH = "stats-lock.json"
README_PATH = "README.md"


# ---------------------------------------------------------
# 1. Ler estado antigo do stats-lock.json
# ---------------------------------------------------------
def load_previous_stats():
    if not os.path.exists(LOCK_PATH):
        return {}, ""

    with open(LOCK_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    html = data.get("html_content", "")
    prev = data.get("previous_stats", {})

    return prev, html

def compute_pie_percentages(stats):
    total = sum(stats.values()) if sum(stats.values()) > 0 else 1
    return {lang: (value / total) * 100 for lang, value in stats.items()}
# ---------------------------------------------------------
# 2. Guardar novo estado no stats-lock.json
# ---------------------------------------------------------
def save_new_stats(html_content, new_stats):
    pie = compute_pie_percentages(new_stats)

    data = {
        "html_content": html_content,
        "previous_stats": new_stats,
        "previous_pie": pie
    }

    with open(LOCK_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    print("[Hydra] stats-lock.json atualizado com pie chart.")





# ---------------------------------------------------------
# 3. Atualizar bloco HTML no README
# ---------------------------------------------------------
def update_readme(html_content):
    with open(README_PATH, "r", encoding="utf-8") as f:
        readme = f.read()

    start = "<!--HYDRA-CHAMBER-OPEN-->"
    end = "<!--HYDRA-CHAMBER-CLOSE-->"

    if start not in readme or end not in readme:
        raise Exception("Marcadores HYDRA-CHAMBER-OPEN/CLOSE não encontrados no README.md")

    before, _, rest = readme.partition(start)
    _, _, after = rest.partition(end)

    new_readme = before + start + "\n" + html_content + "\n" + end + after

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(new_readme)

    print("[Hydra] README atualizado com o painel cerimonial.")


# ---------------------------------------------------------
# 4. Recolher linguagens de todos os repositórios
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

    with open("stats.json", "w", encoding="utf-8") as f:
        json.dump(dict(sorted_langs), f, indent=4, ensure_ascii=False)

    print("[Hydra] stats.json regenerado.")

    return dict(sorted_langs)


# ---------------------------------------------------------
# 5. Construir tabela HTML cerimonial
# ---------------------------------------------------------

def build_html_panel():
    return """
<table width="100%" style="border:2px solid #00ffff; border-radius:6px;">
<tr>
<td>
<img src="screenshots/painel_mutacao.png" width="320px" height="250px"
style="border:2px solid #00ffff; border-radius:6px;">
</td>

<td style="text-align:left; padding:0 20px;">
<em>“Tudo flui, nada permanece.” — Heraclito</em><br><br>
<em>“Nada se perde, tudo se transforma.” — Lavoisier</em><br><br>
<em><a href="https://github.com/carloshmarques/HydraLife" style="color:#00ffff;">
“O software é uma entidade viva.” — HydraLife</a></em>
</td>

<td>
<img src="screenshots/language_pie.png" width="320px" height="250px"
style="border:2px solid #00ffff; border-radius:6px;">
</td>
</tr>
</table>
""".strip()





# ---------------------------------------------------------
# 6. Fluxo principal
# ---------------------------------------------------------
def main():
    # 1. Ler estado antigo
    previous_stats, old_html = load_previous_stats()

    # 2. Recolher estado novo
    new_stats = collect_language_stats()

    # 3. Construir HTML cerimonial
    html_panel = build_html_panel()

    # 4. Atualizar README
    update_readme(html_panel)

    # 5. Guardar novo estado no stats-lock.json
    save_new_stats(html_panel, new_stats)

    print("[Hydra] update_stats.py concluído com dignidade.")


if __name__ == "__main__":
    main()
