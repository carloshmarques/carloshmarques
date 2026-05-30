#!/usr/bin/env python
import os

TREE_START = "<!--TREE-START-->"
TREE_END = "<!--TREE-END-->"
FILE_TREE = "directory_tree.txt"
FILE_README = "README.md"

# 1. Lista apenas o nível atual
entries = os.listdir(".")
entries.sort()

lines = ["."]
for e in entries:
    # ignora o próprio script
    if e == FILE_TREE:
        continue
    lines.append(f"|-- {e}")

tree_output = "\n".join(lines)

# 2. Escreve no directory_tree.txt
with open(FILE_TREE, "w", encoding="utf-8") as f:
    f.write(tree_output)

print(f"✅ {FILE_TREE} atualizado com sucesso.")

# 3. Lê o README
with open(FILE_README, "r", encoding="utf-8") as f:
    content = f.read()

if TREE_START not in content or TREE_END not in content:
    raise ValueError("Bloco TREE não encontrado no README")

before = content.split(TREE_START)[0]
after = content.split(TREE_END)[1]

new_block = f"{TREE_START}\n```\n{tree_output}\n```\n{TREE_END}"
new_content = before + new_block + after

# 4. Atualiza README
with open(FILE_README, "w", encoding="utf-8") as f:
    f.write(new_content)

print("🚀 README.md atualizado com a nova estrutura de diretórios!")
