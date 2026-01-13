from github import Github, Auth
import os
print("GH_TOKEN =", os.environ.get("GH_TOKEN"))

import json

# ---------------------------------------------------------
# 1. Autenticação
# ---------------------------------------------------------

token = os.getenv("GH_TOKEN")
if not token:
    raise RuntimeError("GH_TOKEN não encontrado nas variáveis de ambiente.")

g = Github(auth=Auth.Token(token))
user = g.get_user("carloshmarques")

languages = {}

# ---------------------------------------------------------
# 2. Recolher linguagens de todos os repositórios
# ---------------------------------------------------------

for repo in user.get_repos():
    try:
        langs = repo.get_languages()
        for lang, count in langs.items():
            languages[lang] = languages.get(lang, 0) + count
    except Exception:
        pass

# Ordenar linguagens (maior → menor)
sorted_langs = sorted(languages.items(), key=lambda x: x[1], reverse=True)

# ---------------------------------------------------------
# 3. Guardar stats.json (fonte de verdade para o gerador de imagem)
# ---------------------------------------------------------

with open("stats.json", "w", encoding="utf-8") as f:
    json.dump(dict(sorted_langs), f, indent=4, ensure_ascii=False)

# ---------------------------------------------------------
# 4. Criar texto para o README
# ---------------------------------------------------------

output_lines = []
output_lines.append("### Linguagens mais usadas (atualizado automaticamente)\n")

for lang, count in sorted_langs[:5]:
    output_lines.append(f"- **{lang}** — {count} bytes de código")

output = "\n".join(output_lines) + "\n"

# ---------------------------------------------------------
# 5. Atualizar README entre os marcadores
# ---------------------------------------------------------

with open("README.md", "r", encoding="utf-8") as f:
    readme = f.read()

start = "<!--LANG-STATS-START-->"
end = "<!--LANG-STATS-END-->"

if start not in readme or end not in readme:
    raise Exception("Marcadores <!--LANG-STATS-START/END--> não encontrados no README.md")

before, _, rest = readme.partition(start)
_, _, after = rest.partition(end)

new_readme = before + start + "\n" + output + "\n" + end + after

with open("README.md", "w", encoding="utf-8") as f:
    f.write(new_readme)

