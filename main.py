import pygame
from config import config
from builder import maze

def initialize_game():
    pygame.init()
    screen = pygame.display.set_mode((maze.cols * config["SCALING_FACTOR"], maze.rows * config["SCALING_FACTOR"]))
    clock = pygame.time.Clock()
    return screen, clock

def handle_input():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return False
    return True

def initialize_assets():
    player_imgs = {
        "up": [
            "assets/lucas_up.png", "assets/lucas_up2.png", "assets/lucas_up3.png", "assets/lucas_up4.png"
        ],
        "down": [
            "assets/lucas_down.png", "assets/lucas_down2.png", "assets/lucas_down3.png", "assets/lucas_down4.png"
        ],
        "left": [
            "assets/lucas_left.png", "assets/lucas_left2.png", "assets/lucas_left3.png", "assets/lucas_left4.png"
        ],
        "right": [
            "assets/lucas_right.png", "assets/lucas_right2.png", "assets/lucas_right3.png", "assets/lucas_right4.png"
        ]
    }
    
    lugia_imgs = ["assets/lugia.png", "assets/lugia1.png"]
    way_img = pygame.image.load("assets/way.png")
    way2_img = pygame.image.load("assets/way2.png")
    wall_img = pygame.image.load("assets/wall.png")

    return {
        "player_imgs": player_imgs,
        "pc_imgs": lugia_imgs,
        "way_img": pygame.transform.scale(way_img, (config["SCALING_FACTOR"], config["SCALING_FACTOR"])),
        "way2_img": pygame.transform.scale(way2_img, (config["SCALING_FACTOR"], config["SCALING_FACTOR"])),
        "wall_img": pygame.transform.scale(wall_img, (config["SCALING_FACTOR"], config["SCALING_FACTOR"])),
    }

def draw_paths(path, visited, font, screen):
    visited_rect = pygame.Surface((config["SCALING_FACTOR"], config["SCALING_FACTOR"]), pygame.SRCALPHA)
    visited_rect.fill((255, 150, 150, 184))

    path_rect = pygame.Surface((config["SCALING_FACTOR"], config["SCALING_FACTOR"]), pygame.SRCALPHA)
    path_rect.fill((150, 150, 255, 184))

    for pos in visited:
        if pos not in path:
            screen.blit(visited_rect, pygame.Vector2(pos[1], pos[0]) * config["SCALING_FACTOR"])
            text = font.render(f"{pos[1], pos[0]}", True, (64, 64, 64))
            textRect = text.get_rect()
            textRect.center = (pos[1] * config["SCALING_FACTOR"] + config["SCALING_FACTOR"] / 2, pos[0] * config["SCALING_FACTOR"] + config["SCALING_FACTOR"] / 2)
            screen.blit(text, textRect)

    for pos in path:
        screen.blit(path_rect, pygame.Vector2(pos[1], pos[0]) * config["SCALING_FACTOR"])
        text = font.render(f"{pos[1], pos[0]}", True, (64, 64, 64))
        textRect = text.get_rect()
        textRect.center = (pos[1] * config["SCALING_FACTOR"] + config["SCALING_FACTOR"] / 2, pos[0] * config["SCALING_FACTOR"] + config["SCALING_FACTOR"] / 2)
        screen.blit(text, textRect)

def render_game(screen, player_pos, pc_pos, path, font, assets, move_speed):
    # Interpreta as coordenadas do labirinto e renderiza as imagens com base nas coordenadas e fator de escala
    for row_index, row in enumerate(maze.room):
        for col_index, col in enumerate(row):
            x = col_index * config["SCALING_FACTOR"]
            y = row_index * config["SCALING_FACTOR"]

            if col == config["WALL"]:
                screen.blit(assets["way2_img"], (x, y))
                screen.blit(assets["wall_img"], (x, y))
            else:
                screen.blit(assets["way_img"], (x, y))

    # Renderiza o player na posição atual
    screen.blit(assets["player"], player_pos)

    # Renderiza o PC na posição atual
    screen.blit(assets["pc"], pc_pos)
    
    # Renderiza os caminhos quando o player chegar ao final
    if player_pos.distance_to(pc_pos) <= move_speed:
        draw_paths(path, maze.visited, font, screen)

    pygame.display.flip()

def game_loop(player_pos, pc_pos):
    screen, clock = initialize_game()
    assets = initialize_assets()
    font = pygame.font.Font('freesansbold.ttf', 8)
    counter = 0
    
    
    while True:
        if not handle_input():
            break  # Caso o usuário feche a janela ou pressione ESC, o loop é quebrado e o jogo é fechado

        dt = clock.tick(config["FPS_LIMIT"]) / 1000  # Delta time, calcula o tempo entre cada frame
        move_speed = config["SPEED"] * dt # Define a velocidade do movimento do player baseado no delta time, não importando a velocidade do computador
        
        # Atualiza a posição do player
        if not maze.moves.is_empty():
            # Determina a próxima posição do player
            next_pos = pygame.Vector2(maze.moves.peek()[1], maze.moves.peek()[0]) * config["SCALING_FACTOR"]
            
            # Subtrai a posição atual do player pela próxima posição, para determinar a direção
            # Ex: (0, 0) - (0, 1) = (0, -1) -> player deve ir para cima
            direction = next_pos - player_pos
            player_pos += direction.normalize() * move_speed  # É propriamente dito o movimento do player
            
            # Como estou usando imagens diferentes para cada direção, é necessário determinar a direção do player
            # Para isso, é feito a diferença entre a posição atual e a próxima posição
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

            # A cada frame, o contador é incrementado em 0.2
            counter += pygame.time.Clock().tick(config["FPS_LIMIT"]) / 1000 * 5
            
            # Caso o contador seja maior ou igual ao tamanho do array de imagens, reseta o contador
            if counter >= len(assets["player_imgs"][spr_direction]):
                counter = 0 

            # Define a imagem do player como a imagem atual da animação (se o contador for 0.2, 0.4, 0.6... a imagem será a primeira, se for 1.2, 1.2, 1.4..., será a segunda, e assim por diante)
            assets["player"] = pygame.image.load(assets["player_imgs"][spr_direction][int(counter)])
            assets["player"] = pygame.transform.scale(assets["player"], (config["SCALING_FACTOR"], config["SCALING_FACTOR"]))
            
            # Define a imagem do PC como a imagem atual da animação (se o contador for 0.2, 0.4, 0.6... a imagem será a primeira, se for 1.2, 1.2, 1.4..., será a segunda, e assim por diante)
            assets["pc"] = pygame.image.load(assets["pc_imgs"][int(counter) % 2])
            assets["pc"] = pygame.transform.scale(assets["pc"], (config["SCALING_FACTOR"] * 1.05, config["SCALING_FACTOR"] * 1.05))

            # Se a distância entre a posição atual e a próxima posição for menor que a velocidade do movimento, adiciona a posição atual ao array de caminho
            # Isso é feito para que o player não pule posições e se mova de forma suave, de acordo com a velocidade do jogo
            if player_pos.distance_to(next_pos) < move_speed:
                maze.path.append(maze.moves.pop())

        # Renderiza o jogo
        render_game(screen, player_pos, pc_pos, maze.path, font, assets, move_speed)

    pygame.quit()  # Fecha a instancia do pygame quando sair do loop

if __name__ == "__main__":
    maze.find_path()
    
    # Responsividade
    if maze.rows > 60 or maze.cols > 60:
        config["SCALING_FACTOR"] = config["SCALING_FACTOR_SMALL"]
        
    if maze.rows > 30 or maze.cols > 30:
        config["SCALING_FACTOR"] = config["SCALING_FACTOR_NORMAL"]

    # Define a posição inicial do player e do PC (rato e queijo)
    player_pos = pygame.Vector2(maze.mouse[1], maze.mouse[0]) * config["SCALING_FACTOR"]
    pc_pos = pygame.Vector2(maze.exit[1], maze.exit[0]) * config["SCALING_FACTOR"]

    # Inicia o loop principal do jogo
    game_loop(player_pos, pc_pos)