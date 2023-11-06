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
    
player_imgs = {
    "up": [
        "assets/scizor_up.png", "assets/scizor_up.png", "assets/scizor_up1.png"
    ],
    "down": [
        "assets/scizor_down.png", "assets/scizor_down.png", "assets/scizor_down1.png"
    ],
    "left": [
        "assets/scizor_left.png", "assets/scizor_left.png", "assets/scizor_left1.png"
    ],
    "right": [
        "assets/scizor_right.png", "assets/scizor_right.png", "assets/scizor_right1.png"
    ]
}

pc_img = pygame.image.load("assets/pc.png")
way_img = pygame.image.load("assets/way.png")
way2_img = pygame.image.load("assets/way2.png")
wall_img = pygame.image.load("assets/wall.png")
wall_horizontal_img = pygame.image.load("assets/wall_horizontal.png")

spr_direction = "down"
counter = 0
player = pygame.image.load(player_imgs[spr_direction][counter])

pc_img = pygame.transform.scale(pc_img, (config["SCALING_FACTOR"], config["SCALING_FACTOR"]))
way_img = pygame.transform.scale(way_img, (config["SCALING_FACTOR"], config["SCALING_FACTOR"]))
way2_img = pygame.transform.scale(way2_img, (config["SCALING_FACTOR"], config["SCALING_FACTOR"]))
wall_img = pygame.transform.scale(wall_img, (config["SCALING_FACTOR"], config["SCALING_FACTOR"]))
wall_horizontal_img = pygame.transform.scale(wall_horizontal_img, (config["SCALING_FACTOR"], config["SCALING_FACTOR"]))
player = pygame.transform.scale(player, (config["SCALING_FACTOR"], config["SCALING_FACTOR"]))

pygame.init()

# Cria a tela do jogo de acordo com o tamanho do labirinto e o fator de escala (64 pixels, exemplo: labirinto 8x8, tela: 512x512)
screen = pygame.display.set_mode((maze.rows * config["SCALING_FACTOR"], maze.cols * config["SCALING_FACTOR"]))
clock = pygame.time.Clock()
running = True

# Define se o rato está se movendo ou não e se deve virar para a esquerda ou nao (apenas controles de sprite)
is_moving = False

dt = 0

player_pos = pygame.Vector2(maze.mouse[1], maze.mouse[0]) * config["SCALING_FACTOR"]
pc_pos = pygame.Vector2(maze.exit[1], maze.exit[0]) * config["SCALING_FACTOR"]

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
            # Define a posição do sprite de acordo com a linha e coluna atual vezes o fator de escala
            x = col_index * config["SCALING_FACTOR"]
            y = row_index * config["SCALING_FACTOR"]
             
            if col == config["WALL"]:
                # Renderiza um chão em baixo da parede (árvore) apenas por estética
                screen.blit(way2_img, (x, y))
                
                screen.blit(wall_img, (x, y))
                    
            else:
                screen.blit(way_img, (x, y))
            
    # Define a velocidade de movimento do rato
    # Nesse caso, o rato se move config["SPEED"] pixels por segundo vezes o tempo entre cada frame (dt = delta time) que resulta em 5 pixels por frame
    move_speed = config["SPEED"] * dt
    
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
        
        # Define a direção do rato de acordo com a direção arredondada, já que nem sempre é um valor inteiro e menor que 0.
        # Dessa forma, é possível controlar a direção do rato de acordo com a posição do player e a posição do próximo passo
        relative_x = round(next_pos.x - player_pos.x)
        relative_y = round(next_pos.y - player_pos.y)
        

        if relative_x > 0:
            spr_direction = "right"
        elif relative_x < 0:
            spr_direction = "left"
        elif relative_y > 0:
            spr_direction = "down"
        elif relative_y < 0:
            spr_direction = "up"
            
        if is_moving:
            counter = (counter + 1) % len(player_imgs[spr_direction])
            player = pygame.image.load(player_imgs[spr_direction][counter])
        
        # Enquanto o player não estiver 1 passo de distância do próximo passo, o player continua se movendo para o mesmo passo
        if player_pos.distance_to(next_pos) < move_speed:
            maze.moves.pop()
            is_moving = False
    

        
    player = pygame.transform.scale(player, (config["SCALING_FACTOR"], config["SCALING_FACTOR"]))
   
    screen.blit(player, player_pos)
    screen.blit(pc_img, pc_pos)

    pygame.display.flip()
    
    dt = clock.tick(config["FPS_LIMIT"]) / 1000

pygame.quit()