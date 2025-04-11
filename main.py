import pygame

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
MAX_FPS = 60

pygame.init()
clock = pygame.time.Clock()

display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Asteroids")
running = True

# plain surface
rect_surface = pygame.Surface((100, 150))
rect_surface.fill("orange")
x = 100

#img surface
player_surface = pygame.image.load("assets/images/player.png").convert_alpha()
player_speed = 0.8
player_pos_x = 300
player_pos_y = 350
move_dir_x = 0
move_dir_y = 0

def get_player_movement_vector():
    global move_dir_x, move_dir_y
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        move_dir_x = 1
        return move_dir_x
    elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
        move_dir_x = -1
        return move_dir_x
    elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
        move_dir_y = 1
        return move_dir_y
    elif keys[pygame.K_UP] or keys[pygame.K_w]:
        move_dir_y = -1
        return move_dir_y
    else:
        move_dir_x = 0
        move_dir_y = 0
        return move_dir_x, move_dir_y   

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    display_surface.fill("grey")
    get_player_movement_vector()
    
    # Update player position
    player_pos_x += move_dir_x * player_speed
    player_pos_y += move_dir_y * player_speed
    
    display_surface.blit(player_surface, (player_pos_x, player_pos_y))
    pygame.display.update()
        
    clock.tick(MAX_FPS)

pygame.quit()

