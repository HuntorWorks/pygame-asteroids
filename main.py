import pygame
import os
from random import randint

class Star(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load(os.path.join(BASE_PATH, "assets/images/star.png")).convert_alpha()
        self.rect = self.image.get_frect(center=(randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT)))
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)

class PlayerShip(pygame.sprite.Sprite):

    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load(os.path.join(BASE_PATH, "assets/images/player.png")).convert_alpha()
        self.rect = self.image.get_frect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2))
        self.input_vector = pygame.Vector2()

        #SHIP PROPERTIES    
        self.SHIP_SPEED = 300
        self.SHIP_HEALTH = 100
        self.SHIP_MAX_HEALTH = 100
        self.SHIP_LASER_COOLDOWN = 0.5
        self.SHIP_LASER_SPEED = 12
        self.SHIP_LASER_DAMAGE = 1

    def move(self, delta_time):
        keys = pygame.key.get_pressed()
        self.input_vector.x = int(keys[pygame.K_RIGHT] or keys[pygame.K_d]) - int(keys[pygame.K_LEFT] or keys[pygame.K_a])
        self.input_vector.y = int(keys[pygame.K_DOWN] or keys[pygame.K_s]) - int(keys[pygame.K_UP] or keys[pygame.K_w ])

        if self.input_vector.magnitude() != 0:
            self.input_vector = self.input_vector.normalize()
        self.rect.center += self.input_vector * self.SHIP_SPEED * delta_time

    def shoot(self):
        keys = pygame.key.get_just_pressed()
        if keys[pygame.K_SPACE]:
            print("fire laser")

    def update(self, delta_time):
        self.move(delta_time)
        self.shoot()



WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
MAX_FPS = 60
BASE_PATH = os.path.join(os.getcwd(), "pygame-asteroids")

# ASSETS
BACKGROUND_SPRITE = os.path.join(BASE_PATH, "assets", "images", "background.png")
ASTEROID_SPRITE = os.path.join(BASE_PATH, "assets", "images", "meteor.png")
STAR_SPRITE = os.path.join(BASE_PATH, "assets", "images", "star.png")
LASER_SPRITE = os.path.join(BASE_PATH, "assets", "images", "laser.png")


# INIT SETUP
pygame.init()
clock = pygame.time.Clock()
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Asteroids")
running = True

#player
all_sprites_group = pygame.sprite.Group()
player = PlayerShip(all_sprites_group)

#laser_surface
laser_surface = pygame.image.load(LASER_SPRITE).convert_alpha()
laser_rect = laser_surface.get_frect(bottomleft=(20, WINDOW_HEIGHT - 20))
laser_pos_x = 0
laser_pos_y = 0
has_shot = False
laser_active = False

#star_surface
stars_list = []
for i in range(20):
    stars_list.append(Star(all_sprites_group))

#Asteroid_surface
asteroid_surface = pygame.image.load(ASTEROID_SPRITE).convert_alpha()
asteroid_rect = asteroid_surface.get_frect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2))


while running:
    delta_time = clock.tick() / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # BACKGROUND
    display_surface.fill("black")

    all_sprites_group.update(delta_time)
    all_sprites_group.draw(display_surface)
    
    pygame.display.update()    

pygame.quit()


