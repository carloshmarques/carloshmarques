# scripts/update_tree.py

TREE_START = "<!--TREE-START-->"
TREE_END = "<!--TREE-END-->"

# Lê a árvore gerada pelo comando tree
with open("directory_tree.txt", "r", encoding="utf-8") as f:
    tree = f.read().rstrip()

# Lê o README atual
with open("README.md", "r", encoding="utf-8") as f:
    content = f.read()

# Garante que o bloco existe
if TREE_START not in content or TREE_END not in content:
    raise ValueError("Bloco TREE-START / TREE-END não encontrado no README.md")

# Divide o conteúdo
before = content.split(TREE_START)[0]
after = content.split(TREE_END)[1]

# Monta o novo conteúdo
new_block = f"{TREE_START}\n```\n{tree}\n```\n{TREE_END}"

new_content = before + new_block + after

# Escreve o README atualizado
with open("README.md", "w", encoding="utf-8") as f:
    f.write(new_content)

print("Árvore de diretórios atualizada no README.md")

