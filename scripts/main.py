from commands import show_menu, get_choice
from gitignore import prompt_gitignore_update
from gitattributes import prompt_gitattributes_update
from changelog import prompt_changelog_update


def main():
    while True:
        show_menu()
        choice = get_choice()

        if choice == "1":
            prompt_gitignore_update()
            continue
        
        if choice == "2":
            prompt_gitattributes_update()
            continue

        if choice == "3":
            prompt_changelog_update()
            continue



        if choice == "0":
            print("\n👋 A sair...")
            break

        print(f"\n⚙️ Escolheste a opção: {choice}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n⚠️  Interrompido pelo utilizador.")


