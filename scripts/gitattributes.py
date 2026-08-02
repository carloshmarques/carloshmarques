import os
from datetime import datetime

GITATTR_FILE = ".gitattributes"

START = "###> carloshmarques/gitattributes ###"
END   = "###< carloshmarques/gitattributes ###"

def prompt_gitattributes_update():
    print("\n📝 Deseja adicionar algo ao .gitattributes? (yes/no)")
    choice = input("> ").strip().lower()

    if choice not in ["yes", "y"]:
        print("⏭️  Pulando atualização do .gitattributes.")
        return False

    comment = input("💬 comment? ").strip()
    entry   = input("📂 entrada? ").strip()

    if not entry:
        print("❌ Nenhuma entrada fornecida.")
        return False

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    new_line = f"# {timestamp} - {comment}\n{entry}\n"

    # Se o ficheiro não existir → criar com bloco mínimo
    if not os.path.exists(GITATTR_FILE):
        with open(GITATTR_FILE, "w", encoding="utf-8") as f:
            f.write(f"{START}\n{new_line}{END}\n")
        print(f"✅ .gitattributes criado com '{entry}'.")
        return True

    # Ler conteúdo existente
    with open(GITATTR_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Se os marcadores existirem → append dentro do bloco
    if START in content and END in content:
        before = content.split(START)[0]
        middle = content.split(START)[1].split(END)[0]
        after  = content.split(END)[1]

        middle = middle + new_line

        new_content = before + START + "\n" + middle + END + after

        with open(GITATTR_FILE, "w", encoding="utf-8") as f:
            f.write(new_content)

        print(f"✅ Entrada '{entry}' adicionada ao .gitattributes.")
        return True

    # Se não existirem → reconstruir ficheiro
    with open(GITATTR_FILE, "w", encoding="utf-8") as f:
        f.write(f"{START}\n{new_line}{END}\n")

    print("⚠️ Marcadores não existiam — ficheiro reconstruído.")
    return True
