from github import Github
import json
import os

token = os.getenv("GH_TOKEN")
g = Github(token)

user = g.get_user("carloshmarques")

languages = {}

for repo in user.get_repos():
    try:
        langs = repo.get_languages()
        for lang, count in langs.items():
            languages[lang] = languages.get(lang, 0) + count
    except:
        pass

# Ordenar por uso
sorted_langs = sorted(languages.items(), key=lambda x: x[1], reverse=True)

# Criar texto para o README
output = "### Linguagens mais usadas (atualizado automaticamente)\n\n"
for lang, count in sorted_langs[:5]:
    output += f"- **{lang}** — {count} bytes de código\n"

# Atualizar README
with open("README.md", "r", encoding="utf-8") as f:
    readme = f.read()
    start = "<!--LANG-STATS-START-->"    
    end = "<!--LANG-STATS-END-->"
    if start not in readme or end not in readme:
        raise Exception("Marcadores não encontrados no README.md")
    before = readme.split(start)[0]
    after = readme.split(end)[-1]  # usa o último elemento, evita IndexError

with open("README.md", "w", encoding="utf-8") as f:
    f.write(new_readme)
