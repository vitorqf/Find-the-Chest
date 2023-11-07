import argparse
from config import config
from maze import Maze

# Cria um parser de argumentos
parser = argparse.ArgumentParser(description='Solve a maze using the DFS algorithm')

# Adiciona um argumento obrigatório, o caminho para o arquivo do labirinto
parser.add_argument('-f', '--file', required=True, help='Path to the maze file')

# Faz o parse dos argumentos
args = parser.parse_args()

# Define o caminho para o arquivo do labirinto
maze_file = args.file

# Abre o arquivo do labirinto e o separa por linhas
with open(maze_file, 'r') as file:
    maze_content = file.read().splitlines()
    
# Aqui, para cada item na primeira linha do arquivo, os separa por espaço e converte em inteiro, definindo a largura e altura
rows, cols = map(int, maze_content[0].split())

# Remove a primeira linha, contendo as dimensoes do labirinto
maze_content = maze_content[1:]

# Para cada linha do labirinto, verifica se o rato "m" está presente na linha, se estiver, procura pela primeira ocorrência e define a posição do rato
# Mesma coisa da anterior, mas buscando a saída
for index, row in enumerate(maze_content):
    if config["MOUSE"] in row:
        mouse_row = index
        mouse_col = row.index(config["MOUSE"])
        break

# Se o rato não for encontrado, lança uma exceção
if not mouse_row or not mouse_col:
    raise Exception("Mouse not found in maze")

mouse = (mouse_row, mouse_col)

# Mesma coisa da anterior, mas buscando a saída
for index, row in enumerate(maze_content):
    if config["EXIT"] in row:
        exit_row = index
        exit_col = row.index(config["EXIT"])
        break

# Se a saída não for encontrada, lança uma exceção
if not exit_row or not exit_col:
    raise Exception("Exit not found in maze")

exit = (exit_row, exit_col)

maze = Maze(maze_content, rows, cols, mouse, exit)