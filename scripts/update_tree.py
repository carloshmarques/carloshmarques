#!/usr/bin/env python
import subprocess
import os

# Configurações
TREE_START = "<!--TREE-START-->"
TREE_END = "<!--TREE-END-->"
FILE_TREE = "directory_tree.txt"
FILE_README = "README.md"

# 1. Gera a árvore e guarda no ficheiro (executa o comando 'tree')
# O argumento "." indica a pasta atual. 
# Podes adicionar -I para ignorar pastas como .git ou venv
try:
    # Executa o comando e captura a saída
    # Correção na linha 17 do script:
    tree_output = subprocess.check_output(["tree"], text=True, encoding="utf-8")

        
    # Guarda no directory_tree.txt
    with open(FILE_TREE, "w", encoding="utf-8") as f:
        f.write(tree_output)
    print(f"✅ {FILE_TREE} atualizado com sucesso.")
except Exception as e:
    print(f"❌ Erro ao gerar a árvore: {e}")
    exit(1)

# 2. Lê a árvore que acabou de ser gerada
with open(FILE_TREE, "r", encoding="utf-8") as f:
    tree_content = f.read().rstrip()

# 3. Lê o README atual
if not os.path.exists(FILE_README):
    print(f"❌ Erro: {FILE_README} não encontrado.")
    exit(1)

with open(FILE_README, "r", encoding="utf-8") as f:
    content = f.read()

# 4. Garante que o bloco existe
if TREE_START not in content or TREE_END not in content:
    raise ValueError(f"Bloco {TREE_START} / {TREE_END} não encontrado no {FILE_README}")

# 5. Monta o novo conteúdo
before = content.split(TREE_START)[0]
after = content.split(TREE_END)[1]
new_block = f"{TREE_START}\n```\n{tree_content}\n```\n{TREE_END}"
new_content = before + new_block + after

# 6. Escreve o README atualizado
with open(FILE_README, "w", encoding="utf-8") as f:
    f.write(new_content)

print(f"🚀 README.md atualizado com a nova estrutura de diretórios!")
