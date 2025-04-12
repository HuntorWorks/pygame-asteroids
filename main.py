import pygame
import os
from random import randint, uniform

class Star(pygame.sprite.Sprite):
    def __init__(self, groups, surface):
        super().__init__(groups)
        self.image = surface
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
        self.SHIP_LASER_FIRE_COOLDOWN = 400
        self.SHIP_LASER_SPEED = 1000
        self.SHIP_LASER_DAMAGE = 1
        
        self.last_shot_time = 0
        self.shot_available = True

    def move(self, delta_time):
        keys = pygame.key.get_pressed()
        self.input_vector.x = int(keys[pygame.K_RIGHT] or keys[pygame.K_d]) - int(keys[pygame.K_LEFT] or keys[pygame.K_a])
        self.input_vector.y = int(keys[pygame.K_DOWN] or keys[pygame.K_s]) - int(keys[pygame.K_UP] or keys[pygame.K_w ])

        if self.input_vector.magnitude() != 0:
            self.input_vector = self.input_vector.normalize()
        self.rect.center += self.input_vector * self.SHIP_SPEED * delta_time 

    def can_shoot(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time > self.SHIP_LASER_FIRE_COOLDOWN:
            self.shot_available = True
        return self.shot_available
    
    def shoot(self):
        if self.can_shoot():
            keys = pygame.key.get_just_pressed()
            if keys[pygame.K_SPACE]:
                self.last_shot_time = pygame.time.get_ticks()
                self.shot_available = False
                Laser(laser_surface, self.rect.midtop, all_sprites_group, self.SHIP_LASER_SPEED)

    def destroy(self):
        self.kill()

    def update(self, delta_time):
        self.move(delta_time)
        self.shoot()

class Asteroid(pygame.sprite.Sprite):
    def __init__(self, groups, surface):
        super().__init__(groups)
        self.image = surface
        spawn_position = self.get_random_spawn_position()
        self.rect = self.image.get_frect(midbottom=spawn_position)
        self.move_direction = pygame.Vector2(uniform(-0.5, 0.5), 1)
        self.spawn_time = pygame.time.get_ticks()

        self.ASTEROID_SPEED = 250
        self.ASTEROID_DAMAGE = 10
        self.ASTEROID_SCORE_ON_DESTROY = 10

    def get_random_spawn_position(self):
        rect_width = self.image.get_width()
        return (randint(rect_width, WINDOW_WIDTH - rect_width), -10)

    def destroy_timer(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.spawn_time > 2000:
            self.destroy()

    def move(self, delta_time):
        self.rect.center += self.move_direction * self.ASTEROID_SPEED * delta_time
        
    def destroy(self):
        self.kill()

    def update(self, delta_time):
        self.move(delta_time)
        self.destroy_timer()

class Laser(pygame.sprite.Sprite):
    def __init__(self, surface, position, groups, laser_speed): 
        super().__init__(groups)
        self.image = surface
        self.rect = self.image.get_frect(midbottom=position)

        self.BASE_SPEED = 1
        self.speed = self.BASE_SPEED * laser_speed

    def move(self, delta_time):
        self.rect.y -= self.speed * delta_time

    def check_off_screen(self):
        if self.rect.midbottom[1] < 0: 
            self.kill()

    def check_collision(self):
        asteroid_group_sprites = pygame.sprite.spritecollide(self, asteroid_group, False)
        collided_asteroid = asteroid_group_sprites[0] if asteroid_group_sprites else None
        if collided_asteroid:
            collided_asteroid.destroy()
            self.destroy()
            update_score(collided_asteroid.ASTEROID_SCORE_ON_DESTROY)

    def destroy(self):
        self.kill()
    
    def update(self, delta_time):
        self.move(delta_time)
        self.check_collision()
        self.check_off_screen()

# BASE SETUP
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
BASE_PATH = os.path.join(os.getcwd(), "pygame-asteroids")

# INIT SETUP
pygame.init()
clock = pygame.time.Clock()
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Asteroids")
running = True

# ASSETS
ASTEROID_SPRITE_PATH = os.path.join(BASE_PATH, "assets", "images", "meteor.png")
STAR_SPRITE_PATH = os.path.join(BASE_PATH, "assets", "images", "star.png")       
LASER_SPRITE_PATH = os.path.join(BASE_PATH, "assets", "images", "laser.png")
FONT_PATH = os.path.join(BASE_PATH, "assets", "fonts", "Oxanium-Bold.ttf")

# ASSET SURFACES
asteroid_surface = pygame.image.load(ASTEROID_SPRITE_PATH).convert_alpha()
star_surface = pygame.image.load(STAR_SPRITE_PATH).convert_alpha()
laser_surface = pygame.image.load(LASER_SPRITE_PATH).convert_alpha()
font = pygame.font.Font(FONT_PATH, 32)
font_surface = font.render("Asteroids", True, (240, 240, 240))


#Sprites
all_sprites_group = pygame.sprite.Group()
asteroid_group = pygame.sprite.Group()
for i in range(20):
    Star(all_sprites_group, star_surface)
player = PlayerShip(all_sprites_group)

#events 
ASTEROID_SPAWN_RATE = 1000 # 1 second in milliseconds
asteroid_spawn_event = pygame.event.custom_type()
pygame.time.set_timer(asteroid_spawn_event, ASTEROID_SPAWN_RATE)

# SCORE
score = 0
def update_score(score_amount): 
    global score
    score += score_amount

def display_score(): 
    score_text = f"Score: {str(score)}"
    score_surface = font.render(score_text, True, (240, 240, 240))
    score_rect = score_surface.get_rect(midbottom=(WINDOW_WIDTH / 2, WINDOW_HEIGHT - 10 ))

    display_surface.blit(score_surface, score_rect)

while running:
    delta_time = clock.tick() / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == asteroid_spawn_event:
            Asteroid((all_sprites_group, asteroid_group), asteroid_surface)
    all_sprites_group.update(delta_time)

    #DRAW
    display_surface.fill("#3a2e3f")
    all_sprites_group.draw(display_surface)
    display_score()
    pygame.display.update()    

pygame.quit()



