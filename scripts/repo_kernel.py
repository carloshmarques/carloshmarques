#!/usr/bin/env python
import os
import subprocess
import sys
from datetime import datetime

# --- Configurações ---
GITIGNORE_FILE = ".gitignore"
GITATTR_FILE = ".gitattributes"
README_FILE = "README.md"
CHANGELOG_FILE = "CHANGELOG.md"

# =========================================================
# HEADER
# =========================================================

def print_header():
    print("\n" + "="*50)
    print("🛡️  REPO KERNEL - Gestão de Repositório")
    print("🛡️  Sessão de manutenção antes de push")
    print("="*50 + "\n")

# =========================================================
# EXECUTAR COMANDOS
# =========================================================

def run_command(cmd, description=""):
    print(f"⚙️  {description}...")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=True)
        if result.stdout:
            print(result.stdout.strip())
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao executar: {cmd}")
        print(e.stderr if e.stderr else "Erro desconhecido.")
        return False

# =========================================================
# GIT STATUS
# =========================================================

def check_git_status():
    print("\n🔍 A verificar estado do Git...")
    if not run_command("git status --porcelain", "Verificando alterações"):
        return False
    
    status = subprocess.run("git status --porcelain", shell=True, capture_output=True, text=True)
    if status.stdout.strip():
        print("⚠️  Existem alterações não commitadas.")
        return True
    else:
        print("✅ Tudo limpo. Não há alterações pendentes.")
        return False

# =========================================================
# .GITIGNORE (npm init style)
# =========================================================

def prompt_gitignore_update():
    print("\n📝 Deseja adicionar algo ao .gitignore? (yes/no)")
    choice = input("> ").strip().lower()

    if choice not in ['yes', 'y']:
        print("⏭️  Pulando atualização do .gitignore.")
        return False

    comment = input("💬 comment? ").strip()
    entry = input("📂 entrada? ").strip()

    if not entry:
        print("❌ Nenhuma entrada fornecida.")
        return False

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    new_line = f"# {timestamp} - {comment}\n{entry}\n"

    start = "###> carloshmarques/carloshmarques ###"
    end = "###< carloshmarques/carloshmarques ###"

    # Criar ficheiro se não existir
    if not os.path.exists(GITIGNORE_FILE):
        with open(GITIGNORE_FILE, "w", encoding="utf-8") as f:
            f.write(f"{start}\n{new_line}{end}\n")
        print(f"✅ .gitignore criado com '{entry}'.")
        return True

    # Atualizar ficheiro existente
    with open(GITIGNORE_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    if start in content and end in content:
        before = content.split(start)[0]
        middle = content.split(start)[1].split(end)[0]
        after = content.split(end)[1]

        middle = middle + new_line

        new_content = before + start + "\n" + middle + end + after

        with open(GITIGNORE_FILE, "w", encoding="utf-8") as f:
            f.write(new_content)

        print(f"✅ Entrada '{entry}' adicionada ao .gitignore.")
        return True

    else:
        # reconstruir ficheiro
        with open(GITIGNORE_FILE, "w", encoding="utf-8") as f:
            f.write(f"{start}\n{new_line}{end}\n")
        print("⚠️ Marcadores não existiam — ficheiro reconstruído.")
        return True

# =========================================================
# .GITATTRIBUTES (npm init style)
# =========================================================

def prompt_gitattributes_update():
    print("\n📝 Deseja adicionar algo ao .gitattributes? (yes/no)")
    choice = input("> ").strip().lower()

    if choice not in ['yes', 'y']:
        print("⏭️  Pulando atualização do .gitattributes.")
        return False

    comment = input("💬 comment? ").strip()
    entry = input("📂 entrada? ").strip()

    if not entry:
        print("❌ Nenhuma entrada fornecida.")
        return False

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    new_line = f"# {timestamp} - {comment}\n{entry}\n"

    start = "###> carloshmarques/gitattributes ###"
    end = "###< carloshmarques/gitattributes ###"

    # Criar ficheiro se não existir
    if not os.path.exists(GITATTR_FILE):
        with open(GITATTR_FILE, "w", encoding="utf-8") as f:
            f.write(f"{start}\n{new_line}{end}\n")
        print(f"✅ .gitattributes criado com '{entry}'.")
        return True

    # Atualizar ficheiro existente
    with open(GITATTR_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    if start in content and end in content:
        before = content.split(start)[0]
        middle = content.split(start)[1].split(end)[0]
        after = content.split(end)[1]

        middle = middle + new_line

        new_content = before + start + "\n" + middle + end + after

        with open(GITATTR_FILE, "w", encoding="utf-8") as f:
            f.write(new_content)

        print(f"✅ Entrada '{entry}' adicionada ao .gitattributes.")
        return True

    else:
        # reconstruir ficheiro
        with open(GITATTR_FILE, "w", encoding="utf-8") as f:
            f.write(f"{start}\n{new_line}{end}\n")
        print("⚠️ Marcadores não existiam — ficheiro reconstruído.")
        return True

# =========================================================
# LIMPAR SESSÃO
# =========================================================

def clean_session():
    print("\n🧹 A limpar sessão (ficheiros temporários)...")
    print("✅ Sessão limpa (simulação).")
    return True

# =========================================================
# PUSH FINAL
# =========================================================

def final_push():
    print("\n🚀 Preparado para fazer push?")
    print("1. Sim, fazer push agora")
    print("2. Não, voltar ao menu")
    choice = input("> ").strip()
    
    if choice == "1":
        print("\n📤 A fazer commit e push...")
        run_command("git add .", "Adicionando ficheiros")
        run_command('git commit -m "Kernel: Push automático pós-revisão"', "Commitando")
        if run_command("git push", "Fazendo push"):
            print("\n🎉 Push realizado com sucesso! Sessão concluída.")
            return True
        else:
            print("❌ Push falhou.")
            return False
    else:
        print("⏭️  Push cancelado.")
        return False

# =========================================================
# MAIN
# =========================================================

def main():
    print_header()
    
    has_changes = check_git_status()
    
    # .gitignore
    if has_changes or input("\n🤔 Atualizar .gitignore? (yes/no): ").strip().lower() in ['yes', 'y']:
        prompt_gitignore_update()

    # .gitattributes
    if input("\n🤔 Atualizar .gitattributes? (yes/no): ").strip().lower() in ['yes', 'y']:
        prompt_gitattributes_update()
    
    clean_session()
    
    if has_changes or input("\n🤔 Fazer push agora? (yes/no): ").strip().lower() in ['yes', 'y']:
        final_push()
    else:
        print("\n👋 Sessão encerrada sem push.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n⚠️  Interrompido pelo utilizador.")
        sys.exit(1)
