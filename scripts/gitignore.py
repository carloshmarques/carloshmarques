import os
from datetime import datetime

GITIGNORE_FILE = ".gitignore"

START = "###> carloshmarques/gitignore ###"
END   = "###< carloshmarques/gitignore ###"

def prompt_gitignore_update():
    print("\n📝 Deseja adicionar algo ao .gitignore? (yes/no)")
    choice = input("> ").strip().lower()

    if choice not in ["yes", "y"]:
        print("⏭️  Pulando atualização do .gitignore.")
        return False

    comment = input("💬 comment? ").strip()
    entry   = input("📂 entrada? ").strip()

    if not entry:
        print("❌ Nenhuma entrada fornecida.")
        return False

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    new_line = f"# {timestamp} - {comment}\n{entry}\n"

    # Se o ficheiro não existir → criar com bloco
    if not os.path.exists(GITIGNORE_FILE):
        with open(GITIGNORE_FILE, "w", encoding="utf-8") as f:
            f.write(f"{START}\n{new_line}{END}\n")
        print(f"✅ .gitignore criado com '{entry}'.")
        return True

    # Ler conteúdo existente
    with open(GITIGNORE_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Se os marcadores existirem → append dentro do bloco
    if START in content and END in content:
        before = content.split(START)[0]
        middle = content.split(START)[1].split(END)[0]
        after  = content.split(END)[1]

        middle = middle + new_line

        new_content = before + START + "\n" + middle + END + after

        with open(GITIGNORE_FILE, "w", encoding="utf-8") as f:
            f.write(new_content)

        print(f"✅ Entrada '{entry}' adicionada ao .gitignore.")
        return True

    # Se não existirem → reconstruir ficheiro
    with open(GITIGNORE_FILE, "w", encoding="utf-8") as f:
        f.write(f"{START}\n{new_line}{END}\n")

    print("⚠️ Marcadores não existiam — ficheiro reconstruído.")
    return True
