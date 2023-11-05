
import pygame
from config import config
from maze import maze

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
wall_img = pygame.image.load("assets/wall.png")

counter = 0
mouse = pygame.image.load(mouse_imgs[counter])

chest_img = pygame.transform.scale(chest_img, (config["SCALING_FACTOR"], config["SCALING_FACTOR"]))
way_img = pygame.transform.scale(way_img, (config["SCALING_FACTOR"], config["SCALING_FACTOR"]))
wall_img = pygame.transform.scale(wall_img, (config["SCALING_FACTOR"], config["SCALING_FACTOR"]))
mouse = pygame.transform.scale(mouse, (config["SCALING_FACTOR"], config["SCALING_FACTOR"]))


pygame.init()

# Cria a tela do jogo de acordo com o tamanho do labirinto e o fator de escala (64 pixels, exemplo: labirinto 8x8, tela: 512x512)
screen = pygame.display.set_mode((maze.rows * config["SCALING_FACTOR"], maze.cols * config["SCALING_FACTOR"]))
clock = pygame.time.Clock()
running = True

dt = 0

player_pos = pygame.Vector2(maze.mouse)
chest_pos = pygame.Vector2(maze.exit)

# Variable to track if a movement key is being pressed
is_moving = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    
    # For each row of the matrix
    for row_index, row in enumerate(maze.room):
        # For each column in the row, check if it's a wall (1) or a path (0)
        for col_index, col in enumerate(row):
            if col == config["WALL"]:
                screen.blit(wall_img, (col_index * config["SCALING_FACTOR"], row_index * config["SCALING_FACTOR"]))
            else:
                screen.blit(way_img, (col_index * config["SCALING_FACTOR"], row_index * config["SCALING_FACTOR"]))
                
    move_speed = round(50 * dt)

    screen.blit(chest_img, chest_pos)
        

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_pos.y -= move_speed
        is_moving = True
    elif keys[pygame.K_s]:
        player_pos.y += move_speed
        is_moving = True
    elif keys[pygame.K_a]:
        player_pos.x -= move_speed
        is_moving = True
    elif keys[pygame.K_d]:
        player_pos.x += move_speed
        is_moving = True
    else:
        is_moving = False

    if is_moving:
        counter = (counter + 1) % len(mouse_imgs)
        mouse = pygame.image.load(mouse_imgs[counter])
    else:
        mouse = pygame.image.load(mouse_imgs[0])

    mouse = pygame.transform.scale(mouse, (config["SCALING_FACTOR"], config["SCALING_FACTOR"]))
    screen.blit(mouse, player_pos)

    pygame.display.flip()

    dt = clock.tick(60) / 1000

pygame.quit()