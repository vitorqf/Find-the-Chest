from config import config
from stack import Stack

class Maze:
    def __init__(self, room, rows, cols, mouse, exit):
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
    

    def find_path_dfs(self, current_pos):
        # Check if the current position is the exit
        if current_pos == self.__exit:
            self.__found = True
            return

        # Get the row and column of the current position
        row, col = current_pos

        # Mark the current position as visited
        self.__visited.append((row, col))

        # Define possible moves: up, down, left, right
        moves = [(0, -1), (0, 1), (-1, 0), (1, 0)]

        # Try each possible move
        for move in moves:
            new_row, new_col = row + move[0], col + move[1]

            # Check if the new position is within bounds and not visited
            if (
                0 <= new_row < self.__rows
                # Checa se é maior ou igual a 0 e se é menor que o numero de linhas
                and 0 <= new_col < self.__cols
                # Checa se é maior ou igual a 0 e se é menor que o numero de colunas
                and self.__room[new_row][new_col] != config["WALL"]
                # Checa se a nova posição não é uma parede
                and (new_row, new_col) not in self.__visited
                # Checa se a nova posição não foi visitada
            ):
                self.__path.append((new_col, new_row))
                self.find_path_dfs((new_row, new_col))
                

                # If the exit is found, return
                if self.__found:
                    return

                # If not, backtrack
                self.__path.pop()

    def find_path(self):
        # Clear previous results
        self.__visited = []
        self.__path = []
        self.__found = False

        # Start the DFS search from the mouse's initial position
        self.find_path_dfs(self.__mouse)
        
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
with open("maze16x16.txt", "r") as file:
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

mouse = (mouse_row, mouse_col)

      
# Mesma coisa da anterior, mas buscando a saída
for index, row in enumerate(room):
    if config["EXIT"] in row:
        exit_row = index
        exit_col = row.index(config["EXIT"])
        break

exit = (exit_row, exit_col)

# Create the Maze object
maze = Maze(room, rows, cols, mouse, exit)