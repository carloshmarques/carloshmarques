import datetime
import os
import re

CHANGELOG_PATH = "CHANGELOG.md"


def has_structural_changes():
    """Verifica se houve mudanças estruturais reais."""
    changed_files = os.popen("git diff --name-only").read().splitlines()

    structural = [
        "scripts/update_stats.py",
        "scripts/generate_language_image.py",
        "scripts/generate_language_pie.py",
        "stats.json",
        "README.md",
    ]

    return any(f in changed_files for f in structural)


def get_next_version():
    """Lê o CHANGELOG e calcula a próxima versão (incrementando o patch)."""
    if not os.path.exists(CHANGELOG_PATH):
        return "0.1.0"

    with open(CHANGELOG_PATH, "r", encoding="utf-8") as f:
        content = f.read() 
        versions = re.findall(r"\[(\d+\.\d+\.\d+)\]", content)

    if not versions:
        return "0.1.0"

    last = versions[-1]
    major, minor, patch = map(int, last.split("."))
    return f"{major}.{minor}.{patch + 1}"


def append_changelog(version):
    timestamp = datetime.date.today().isoformat()

    entry = f"""
## [{version}] - {timestamp}

### Added
- stats.json regenerado automaticamente.
- language_stats.png atualizado com base nos dados reais.
- README sincronizado entre texto e imagem.

### Changed
- Ajustes estéticos no painel cerimonial.
- Altura uniforme dos gráficos para harmonia visual.

### Ritual
- Workflow executado com dignidade.
- Fluxo de bytes analisado e transformado.
"""

    with open(CHANGELOG_PATH, "a", encoding="utf-8") as f:
        f.write(entry)


if __name__ == "__main__":
    if has_structural_changes():
        version = get_next_version()
        append_changelog(version)
        print(f"[Hydra] CHANGELOG atualizado com versão {version}")
    else:
        print("[Hydra] Nenhuma mudança estrutural detectada. CHANGELOG não modificado.")
