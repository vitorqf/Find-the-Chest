import pygame
from config import config
from maze import maze

# Inicia o algoritmo de busca
maze.find_path()

# Caso seja encontrado uma saída, inverte a pilha de movimentos para que seja renderizada corretamente
if maze.found:
    maze.moves = maze.moves.reverse()
else:
    print("No path found")
    exit()
    

mouse_imgs = [
    "assets/mouse.png",
    "assets/mouse_run1.png",
    "assets/mouse_run2.png",
    "assets/mouse_run3.png",
    "assets/mouse_run4.png",
    "assets/mouse_run5.png",
    "assets/mouse_run6.png",
    "assets/mouse_run7.png",
    "assets/mouse_run8.png"
]

chest_img = pygame.image.load("assets/chest.png")
way_img = pygame.image.load("assets/way.png")
way2_img = pygame.image.load("assets/way2.png")
wall_img = pygame.image.load("assets/wall.png")

counter = 0
mouse = pygame.image.load(mouse_imgs[counter])

chest_img = pygame.transform.scale(chest_img, (config["SCALING_FACTOR"], config["SCALING_FACTOR"]))
way_img = pygame.transform.scale(way_img, (config["SCALING_FACTOR"], config["SCALING_FACTOR"]))
way2_img = pygame.transform.scale(way2_img, (config["SCALING_FACTOR"], config["SCALING_FACTOR"]))
wall_img = pygame.transform.scale(wall_img, (config["SCALING_FACTOR"], config["SCALING_FACTOR"]))
mouse = pygame.transform.scale(mouse, (config["SCALING_FACTOR"], config["SCALING_FACTOR"]))



pygame.init()

# Cria a tela do jogo de acordo com o tamanho do labirinto e o fator de escala (64 pixels, exemplo: labirinto 8x8, tela: 512x512)
screen = pygame.display.set_mode((maze.rows * config["SCALING_FACTOR"], maze.cols * config["SCALING_FACTOR"]))
clock = pygame.time.Clock()
running = True

dt = 0

player_pos = pygame.Vector2(maze.mouse[1], maze.mouse[0]) * config["SCALING_FACTOR"]
chest_pos = pygame.Vector2(maze.exit[1], maze.exit[0]) * config["SCALING_FACTOR"]


# Define se o rato está se movendo ou não e se deve virar para a esquerda ou nao (apenas controles de sprite)
is_moving = False
should_turn = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    
    # Para cada linha da matriz
    for row_index, row in enumerate(maze.room):
        # Para cada coluna da linha da matriz verifica se é uma parede(1) ou um caminho(0)
        for col_index, col in enumerate(row):
            if col == config["WALL"]:
                screen.blit(way2_img, (col_index * config["SCALING_FACTOR"], row_index * config["SCALING_FACTOR"]))
                screen.blit(wall_img, (col_index * config["SCALING_FACTOR"], row_index * config["SCALING_FACTOR"]))
            else:
                screen.blit(way_img, (col_index * config["SCALING_FACTOR"], row_index * config["SCALING_FACTOR"]))
            

    screen.blit(chest_img, chest_pos)
    
    # Define a velocidade de movimento do rato
    # Nesse caso, o rato se move 300 pixels por segundo vezes o tempo entre cada frame (dt = delta time) que resulta em 5 pixels por frame
    move_speed = 300 * dt
    
    # Enquanto a pilha não estiver vazia o rato se move
    if not maze.moves.is_empty():
        
        # Define a próxima posição do rato, que é a head da pilha vezes o fator de escala
        next_pos = pygame.Vector2(maze.moves.peek()) * config["SCALING_FACTOR"]
        
        # Define a direção do rato, que é a próxima posição menos a posição atual (ex: posicao do rato=[512, 704], proxima posicao=[512, 768], direcao=[0, 64])
        direction = next_pos - player_pos
        
        # Define a posição do rato como a posição atual mais a direção normalizada vezes a velocidade de movimento vezes o tempo
        # Por que usar uma direcao normalizada? Porque dessa maneira consigo controlar a velocidade do rato, se eu não normalizar a direção, o rato vai se mover mais rápido quando estiver mais longe do destino
        # Exemplo, se o player deve se mover para cima, o direction.normalize() será [0, -1], se o player deve se mover para baixo, o direction.normalize() será [0, 1], multiplicando pela velocidade de movimento, o rato se moverá 5 pixels por frame na direção estipulada
        player_pos += direction.normalize() * move_speed
        is_moving = True
        should_turn = direction.x < 0
    
        
        # Enquanto o player não estiver 1 passo de distância do próximo passo, o player continua se movendo para o mesmo passo
        if player_pos.distance_to(next_pos) < move_speed:
            maze.moves.pop()
            is_moving = False
    

    if is_moving:
        counter = (counter + 1) % len(mouse_imgs)
        mouse = pygame.image.load(mouse_imgs[counter])
    else:
        mouse = pygame.image.load(mouse_imgs[0])
    
    if should_turn:
        mouse = pygame.transform.flip(mouse, True, False)
        should_turn = False
        
    mouse = pygame.transform.scale(mouse, (config["SCALING_FACTOR"], config["SCALING_FACTOR"]))
   
    screen.blit(mouse, player_pos)

    pygame.display.flip()
    
    dt = clock.tick(60) / 1000


pygame.quit()