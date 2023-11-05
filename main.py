
import pygame
from config import config
from maze import maze

maze.find_path()

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

player_pos = pygame.Vector2(maze.mouse[1], maze.mouse[0]) * config["SCALING_FACTOR"]
chest_pos = pygame.Vector2(maze.exit[1], maze.exit[0]) * config["SCALING_FACTOR"]


# Variable to track if a movement key is being pressed
is_moving = False
should_turn = False

path_index = 0

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
                
    move_speed = 300 * dt
    

    screen.blit(chest_img, chest_pos)
        
    if path_index < len(maze.path):
        # Get the next position in the path
        next_position = pygame.Vector2(maze.path[path_index])

        # Calculate the direction to move
        direction = next_position * config["SCALING_FACTOR"] - player_pos
        direction_length = direction.length()
        
        should_turn = False
       
        if direction[0] < 0:
            should_turn = True
        
        if direction_length > 0:
            # Normalize the direction vector and move the player
            move_vector = direction.normalize() * move_speed
            player_pos += move_vector
            
            # If the player has reached the next position, increment the path_index
            if direction_length <= move_speed:
                path_index += 1
                is_moving = False
            else:
                is_moving = True
    else:
        is_moving = False

    if is_moving:
        counter = (counter + 1) % len(mouse_imgs)
        mouse = pygame.image.load(mouse_imgs[counter])
    else:
        mouse = pygame.image.load(mouse_imgs[0])
    
    if should_turn:
        mouse = pygame.transform.flip(mouse, True, False)
        
    mouse = pygame.transform.scale(mouse, (config["SCALING_FACTOR"], config["SCALING_FACTOR"]))
   
    screen.blit(mouse, player_pos)

    pygame.display.flip()

    dt = clock.tick(60) / 1000

pygame.quit()