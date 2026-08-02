import os
import json
from datetime import datetime

CHANGELOG_MD = "CHANGELOG.md"
CHANGELOG_JSON = "data/changelog.json"

# NOVOS MARCADORES INVISÍVEIS
START = "<!-- carloshmarques/changelog:start -->"
END   = "<!-- carloshmarques/changelog:end -->"


# =========================================================
#  SEMVER INCREMENT
# =========================================================

def increment_version(version: str) -> str:
    major, minor, patch = map(int, version.split("."))

    if patch < 9:
        patch += 1
    else:
        patch = 0
        minor += 1
        if minor > 9:
            minor = 0
            major += 1

    return f"{major}.{minor}.{patch}"


# =========================================================
#  LOAD JSON
# =========================================================

def load_json():
    if not os.path.exists(CHANGELOG_JSON):
        return {"version": "0.0.1", "entries": []}

    with open(CHANGELOG_JSON, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(data):
    with open(CHANGELOG_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


# =========================================================
#  BUILD CHANGELOG BLOCK
# =========================================================

def build_block(entry):
    return (
        f"## [{entry['id']}] - {entry['date']}\n\n"
        f"### Summary\n{entry['summary']}\n\n"
        f"### Adicionado\n" + ("\n".join(f"- {x}" for x in entry["added"]) or "- nada") + "\n\n"
        f"### Modificado\n" + ("\n".join(f"- {x}" for x in entry["modified"]) or "- nada") + "\n\n"
        f"### Ritual\n" + ("\n".join(f"- {x}" for x in entry["ritual"]) or "- nada") + "\n\n"
        f"### Suplemento-[{entry['id']}]-{entry['date']}\n"
        + ("\n".join(f"- {x}" for x in entry["supplement"]) or "- nada") + "\n\n"
        f"### Adenda-[{entry['id']}]-{entry['date']}\n"
        + ("\n".join(f"- {x}" for x in entry["adenda"]) or "- nada") + "\n\n"
    )


# =========================================================
#  UPDATE CHANGELOG.MD
# =========================================================

def update_changelog_md(block):
    with open(CHANGELOG_MD, "r", encoding="utf-8") as f:
        content = f.read()

    if START in content and END in content:
        before = content.split(START)[0]
        middle = content.split(START)[1].split(END)[0]
        after  = content.split(END)[1]

        middle = middle + block

        new_content = before + START + "\n" + middle + END + after

        with open(CHANGELOG_MD, "w", encoding="utf-8") as f:
            f.write(new_content)

        print("✅ Entrada adicionada ao CHANGELOG.md.")
    else:
        # reconstruir bloco dinâmico invisível
        with open(CHANGELOG_MD, "w", encoding="utf-8") as f:
            f.write(
                content
                + f"\n\n{START}\n{block}{END}\n"
            )

        print("⚠️ Marcadores não existiam — bloco reconstruído.")


# =========================================================
#  PROMPT
# =========================================================

def prompt_changelog_update():
    print("\n📝 Criar nova entrada no CHANGELOG? (yes/no)")
    choice = input("> ").strip().lower()

    if choice not in ["yes", "y"]:
        print("⏭️  Pulando atualização do CHANGELOG.")
        return False

    summary = input("💬 Summary curto: ").strip()

    added = []
    modified = []
    ritual = []
    supplement = []
    adenda = []

    print("\n📂 Adicionado (enter vazio termina):")
    while True:
        x = input("- ").strip()
        if not x:
            break
        added.append(x)

    print("\n🛠️ Modificado (enter vazio termina):")
    while True:
        x = input("- ").strip()
        if not x:
            break
        modified.append(x)

    print("\n🔮 Ritual (enter vazio termina):")
    while True:
        x = input("- ").strip()
        if not x:
            break
        ritual.append(x)

    print("\n📎 Suplemento (enter vazio termina):")
    while True:
        x = input("- ").strip()
        if not x:
            break
        supplement.append(x)

    print("\n🗒️ Adenda (enter vazio termina):")
    while True:
        x = input("- ").strip()
        if not x:
            break
        adenda.append(x)

    # JSON
    data = load_json()
    new_version = increment_version(data["version"])

    entry = {
        "id": new_version,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "summary": summary,
        "added": added,
        "modified": modified,
        "ritual": ritual,
        "supplement": supplement,
        "adenda": adenda
    }

    data["version"] = new_version
    data["entries"].append(entry)
    save_json(data)

    # MD
    block = build_block(entry)
    update_changelog_md(block)

    print(f"🎉 Entrada {new_version} criada com sucesso!")
    return True
