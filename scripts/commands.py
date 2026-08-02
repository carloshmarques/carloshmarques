import os

def get_prompt():
    host = os.getenv("COMPUTERNAME", "host").lower()
    profile = os.getenv("USERNAME", "user").lower()
    return f"{host}@{profile}$ "


def show_menu():
    print("\n=== MENU PRINCIPAL ===")
    print("1. Atualizar .gitignore")
    print("2. Atualizar .gitattributes")
    print("3. Atualizar CHANGELOG")
    print("4. Gerar árvore (update_tree)")
    print("5. Fazer push")
    print("0. Sair")

def get_choice():
    prompt = get_prompt()
    return input(f"\n{prompt} ").strip()
