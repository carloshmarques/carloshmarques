from github import Github, Auth
import os

# Autenticação
token = os.getenv("GH_TOKEN")
g = Github(auth=Auth.Token(token))

user = g.get_user("carloshmarques")

languages = {}

# Recolher linguagens
for repo in user.get_repos():
    try:
        langs = repo.get_languages()
        for lang, count in langs.items():
            languages[lang] = languages.get(lang, 0) + count
    except:
        pass

# Ordenar linguagens
sorted_langs = sorted(languages.items(), key=lambda x: x[1], reverse=True)

# Criar texto
output = "### Linguagens mais usadas (atualizado automaticamente)\n\n"
for lang, count in sorted_langs[:5]:
    output += f"- **{lang}** — {count} bytes de código\n"

# Ler README
with open("README.md", "r", encoding="utf-8") as f:
    readme = f.read()

start = "<!--LANG-STATS-START-->"
end = "<!--LANG-STATS-END-->"

# Verificar marcadores
if start not in readme or end not in readme:
    raise Exception("Marcadores não encontrados no README.md")

# Dividir de forma segura
before, _, rest = readme.partition(start)
_, _, after = rest.partition(end)

# Construir novo README
new_readme = before + start + "\n" + output + "\n" + end + after

# Guardar
with open("README.md", "w", encoding="utf-8") as f:
    f.write(new_readme)
