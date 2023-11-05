from config import config
from stack import Stack

class Maze:
    def __init__(self, room, rows, cols, mouse, exit) -> None:
        self.__room = room
        self.__rows = rows
        self.__cols = cols
        self.__mouse = mouse
        self.__exit = exit
        self.__start = mouse
        
        # Pilha de movimentos durante a execução do programa, limitada ao tamanho do labirinto
        self.__moves = Stack(self.__rows * self.__cols)
        
        self.__visited = []
        self.__path = []
        self.__found = False
        
    @property   
    def mouse(self):
        return self.__mouse
        
    @property
    def exit(self):
        return self.__exit
        
    @property
    def room(self):
        return self.__room
    
    @property
    def rows(self):
        return self.__rows
    
    @property
    def cols(self):
        return self.__cols
    
    @property
    def moves(self):
        return self.__moves
    
    @property
    def visited(self):
        return self.__visited
    
    @property
    def path(self):
        return self.__path
    
    @property
    def found(self):
        return self.__found
    
    @property
    def start(self):
        return self.__start
    
    @mouse.setter
    def mouse(self, new_mouse):
        self.__mouse = new_mouse
        
    @exit.setter
    def exit(self, new_exit):
        self.__exit = new_exit
        
    @room.setter
    def room(self, new_room):
        self.__room = new_room
    
    @rows.setter
    def rows(self, new_rows):
        self.__rows = new_rows
    
    @cols.setter
    def cols(self, new_cols):
        self.__cols = new_cols
    
    @moves.setter
    def moves(self, new_moves):
        self.__moves = new_moves
    
    @visited.setter
    def visited(self, new_visited):
        self.__visited = new_visited
    
    @path.setter
    def path(self, new_path):
        self.__path = new_path
    
    @found.setter
    def found(self, new_found):
        self.__found = new_found
    
    @start.setter
    def start(self, new_start):
        self.__start = new_start
        
    def __str__(self) -> str:
        return "\n".join(self.__room)
    
    def __repr__(self) -> str:
        return "\n".join(self.__room)

# Abre o arquivo de labirinto e extrai cada linha para uma posicao de array
with open("maze.txt", "r") as file:
    room = file.read().splitlines()

# Aqui, para cada item na primeira linha do arquivo, os separa por espaço e converte em inteiro, definindo a largura e altura
cols, rows = map(int, room[0].split())

# Remove a primeira linha, contendo as dimensoes do labirinto
room = room[1:]

# Para cada linha do labirinto, verifica se o rato "m" está presente na linha, se estiver, procura pela primeira ocorrência e define a posição do rato
# Mesma coisa da anterior, mas buscando a saída
for index, row in enumerate(room):
    if config["MOUSE"] in row:
        mouse_row = index
        mouse_col = row.index(config["MOUSE"])
        break

mouse = [mouse_row * config["SCALING_FACTOR"], mouse_col * config["SCALING_FACTOR"]]

      
# Mesma coisa da anterior, mas buscando a saída
for index, row in enumerate(room):
    if config["EXIT"] in row:
        exit_row = index
        exit_col = row.index(config["EXIT"])
        break

exit = [exit_col * config["SCALING_FACTOR"], exit_row * config["SCALING_FACTOR"]]

maze = Maze(room, rows, cols, mouse, exit)