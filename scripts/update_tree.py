#!/usr/bin/env python
import os

TREE_START = "<!--TREE-START-->"
TREE_END = "<!--TREE-END-->"
FILE_README = "README.md"

# Pastas a ignorar (são do sistema)
PASTAS_IGNORE = {'.git', '.github', '.vscode', '.idea', '__pycache__', 'node_modules'}

print("🌳 A gerar árvore COMPLETA (incluindo conteúdo de scripts/)...")

lines = ["."]
base_dir = "."
# Nome do próprio script para o ignorar se necessário
script_name = os.path.basename(__file__)

# 1. Gerar a árvore recursiva
for root, dirs, files in os.walk(base_dir):
    # Filtrar PASTAS: Remover as da lista de ignorar E as que começam com .
    dirs[:] = [d for d in dirs if d not in PASTAS_IGNORE and not d.startswith('.')]
    
    # Ordenar
    dirs.sort()
    files.sort()
    
    # Calcular profundidade
    rel_path = os.path.relpath(root, base_dir)
    depth = 0 if rel_path == "." else rel_path.count(os.sep) + 1
    
    # Adicionar nome da pasta (exceto a raiz)
    if depth > 0:
        indent = "|   " * (depth - 1)
        lines.append(f"{indent}|-- {os.path.basename(root)}/")
        
    # Adicionar ficheiros
    file_indent = "|   " * depth
    for f in files:
        # Ignorar O PRÓPRIO SCRIPT (para não se listar a si mesmo)
        # Se quiseres ver o update_tree.py, comenta a linha abaixo:
        #if f == script_name:
           # continue
        
        # Não ignoramos ficheiros ocultos (.gitignore), só pastas
        lines.append(f"{file_indent}|-- {f}")

tree_output = "\n".join(lines)
print(f"✅ Árvore gerada ({len(lines)} linhas).")

# Debug: Mostrar o que foi gerado para confirmação
print("\n👀 Preview da árvore:")
for line in lines:
    print(line)
print("-" * 40)

# 2. Atualizar o README.md
if not os.path.exists(FILE_README):
    print(f"❌ Erro: {FILE_README} não encontrado!")
    exit()

with open(FILE_README, "r", encoding="utf-8") as f:
    content = f.read()

if TREE_START not in content or TREE_END not in content:
    print(f"❌ Erro: Marcadores {TREE_START} e {TREE_END} não encontrados!")
    exit()

# Substituir
before = content.split(TREE_START, 1)[0]
after = content.split(TREE_END, 1)[1]

new_block = f"{TREE_START}\n```\n{tree_output}\n```\n{TREE_END}"
new_content = before + new_block + after

with open(FILE_README, "w", encoding="utf-8") as f:
    f.write(new_content)

print("🚀 README.md atualizado com sucesso!")
print("💡 Dica: No VS Code, faça 'Reload Window' para ver as mudanças.")