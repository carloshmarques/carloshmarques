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
        "stats.json",
        "language_stats.png",
        "README.md",
    ]

    return any(f in changed_files for f in structural)

def get_next_version():
    """Lê o CHANGELOG e calcula a próxima versão."""
    with open(CHANGELOG_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    versions = re.findall(r"\[(\d+\.\d+\.\d+)\]", content)

    if not versions:
        return "0.1.0"

    major, minor, patch = map(int, versions[0].split("."))

    return f"{major}.{minor + 1}.0"

def append_changelog(version):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d")

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
        print(f"CHANGELOG atualizado com versão {version}")
    else:
        print("Nenhuma mudança estrutural detectada. CHANGELOG não modificado.")
# scripts/update_changelog.py