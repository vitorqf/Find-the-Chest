from config import config
from stack import Stack

class Maze:
    def __init__(self, room, rows, cols, mouse, exit):
        self.__room = room
        self.__rows = rows
        self.__cols = cols
        self.__mouse = mouse
        self.__exit = exit
        self.__found = False

        self.__moves = Stack()
        self.__visited = []
        self.__path = []

    def find_path_dfs(self, current_pos):
        # Se a a coordenada atual for equivalente à saída, define que o caminho foi encontrado
        if current_pos == self.__exit:
            self.__found = True
            return

        # Separa a coordenada atual em linha e coluna
        row, col = current_pos

        # Marca a coordenada atual como visitada
        self.__visited.append((row, col))

        # Define movimentos possíveis: direita, esquerda, baixo, cima
        # x, y
        moves = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        # Para cada movimento no array de movimentos é tentado encontrar um caminho
        for move in moves:
            # Define a nova posição como a posição atual + o movimento, ex: (0, 0) + (-1, 0) = (-1, 0)
            new_col, new_row = col + move[0], row + move[1]

            # Checa se a nova posição é válida
            if (
                # Checa se é maior ou igual a 0 e se é menor que o numero de linhas
                0 <= new_row < self.__rows
                # Checa se é maior ou igual a 0 e se é menor que o numero de colunas
                and 0 <= new_col < self.__cols
                # Checa se a nova posição não é uma parede
                and self.__room[new_row][new_col] != config["WALL"]
                # Checa se a nova posição não foi visitada
                and (new_row, new_col) not in self.__visited
            ):
                # Se a nova posição for válida, adiciona a posição atual ao array de movimentos
                self.__moves.push((new_row, new_col))
                # Chama a função novamente, passando a nova posição como parâmetro
                self.find_path_dfs((new_row, new_col))
                
                # Se o caminho for encontrado, saia do loop
                if self.__found:
                    return

                # Se o caminho não for encontrado, remove o último movimento do array de movimentos
                self.__moves.pop()

    def find_path(self):
        # Começa o algoritmo de busca em profundidade recursivamente passando a posição inicial do rato como parâmetro
        self.find_path_dfs(self.__mouse)
        
        if self.__found:
            self.__moves = self.__moves.reverse()
            
        else:
            print("No path found")
            exit()
        
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
    
    @found.setter
    def found(self, new_found):
        self.__found = new_found
    
    @start.setter
    def start(self, new_start):
        self.__start = new_start
        
    @path.setter
    def path(self, new_path):
        self.__path = new_path
        
    def __str__(self) -> str:
        return "\n".join(self.__room)
    
    def __repr__(self) -> str:
        return "\n".join(self.__room)