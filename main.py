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
        self.original_image = pygame.image.load(os.path.join(BASE_PATH, "assets/images/player.png")).convert_alpha()
        self.image = self.original_image
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

        #ROTATION
        self.cur_vector = pygame.Vector2()
        self.angle = 0 
        self.target_angle = 90
        self.SHIP_ROTATION_SPEED = 80

        self.DAMAGE_SOUND = pygame.mixer.Sound(os.path.join(BASE_PATH, "assets", "audio", "damage.ogg"))
        self.EXPLODE_SOUND = pygame.mixer.Sound(os.path.join(BASE_PATH, "assets", "audio", "explosion.wav"))


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
                laser = Laser(laser_surface, self.rect.midtop, all_sprites_group, self.SHIP_LASER_SPEED)
                laser.play_sound()

    def destroy(self):
        self.kill()

    def damage(self, damage_amount):
        self.SHIP_HEALTH -= damage_amount
        self.play_sound("damage")
        if self.SHIP_HEALTH <= 0:
            self.destroy()
            self.play_sound("explosion")

    def play_sound(self, type: str):
        if type == "damage":
            print("damage")
            pygame.mixer.Sound.play(self.DAMAGE_SOUND)
        if type == "explosion":
            print("explosion")
            pygame.mixer.Sound.play(self.EXPLODE_SOUND)
    
    def update_health_bar(self):
        health_icon_surface = pygame.image.load(HEALTH_ICON_PATH).convert_alpha()
        health_icon_surface = pygame.transform.scale(health_icon_surface, (50, 50))
        health_icon_rect = health_icon_surface.get_rect(topleft=(10, 10))

        health_bar_surface = pygame.surface.Surface((self.SHIP_HEALTH, 35))
        health_bar_surface.fill((255, 0, 0))
        health_bar_rect = health_bar_surface.get_rect(topleft=(65, 20))

        health_bar_text_surface = font.render(f"{self.SHIP_HEALTH}/100", True, (255, 255, 255))
        health_bar_text_surface = pygame.transform.scale(health_bar_text_surface, (100, 50))
        
        alignment_rect = health_bar_rect.copy()

        display_surface.blit(health_icon_surface, health_icon_rect)
        display_surface.blit(health_bar_surface, health_bar_rect)
        display_surface.blit(health_bar_text_surface, alignment_rect.move(0, -2))

    def update(self, delta_time):
        self.move(delta_time)
        self.shoot()

class Asteroid(pygame.sprite.Sprite):
    def __init__(self, groups, surface):
        super().__init__(groups)
        self.original_image = surface
        self.image = self.original_image
        spawn_position = self.get_random_spawn_position()
        self.rect = self.image.get_frect(midbottom=spawn_position)
        self.move_direction = pygame.Vector2(uniform(-0.5, 0.5), 1)
        self.spawn_time = pygame.time.get_ticks()

        self.ASTEROID_SPEED = 250
        self.ASTEROID_DAMAGE = 10
        self.ASTEROID_SCORE_ON_DESTROY = 10
        self.is_exploding = False
        
        self.rotation_speed = randint(10, 40)
        self.rotation_angle = 0

        self.TIME_BETWEEN_FRAMES = 10
        self.last_frame_change_time = 0
        self.explosion_frame_index = 0
        self.explosion_frames_surface = []
        for i in range(0, 21):
            image = os.path.join(BASE_PATH, "assets", "images", "explosion", f"{i}.png")
            image_surface = pygame.image.load(image).convert_alpha()
            self.explosion_frames_surface.append(image_surface)            

        self.EXPLODE_SOUND = pygame.mixer.Sound(os.path.join(BASE_PATH, "assets", "audio", "explosion.wav"))

    def get_random_spawn_position(self):
        rect_width = self.image.get_width()
        return (randint(rect_width, WINDOW_WIDTH - rect_width), -10)

    def destroy_timer(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.spawn_time > 3500:
            self.destroy()

    def move(self, delta_time):
        self.rect.center += self.move_direction * self.ASTEROID_SPEED * delta_time

    def rotate(self, delta_time):
        self.rotation_angle += self.rotation_speed * delta_time
        self.image = pygame.transform.rotozoom(self.original_image, self.rotation_angle, 1)
        self.rect = self.image.get_frect(center=self.rect.center)        

    def destroy(self): 
        self.kill()

    def can_change_frame(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_frame_change_time > self.TIME_BETWEEN_FRAMES: 
            self.last_frame_change_time = current_time
            self.explosion_frame_index += 1
            return True
        return False
        
    def play_sound(self):
        pygame.mixer.Sound.play(self.EXPLODE_SOUND)
    
    def explode_animate(self):
        if self.explosion_frame_index >= len(self.explosion_frames_surface) -1 : 
            self.is_exploding = False
            self.explosion_frame_index = 0 
            self.destroy()
            self.play_sound()
            return
        
        if self.can_change_frame():
            self.is_exploding = True
            self.image = self.explosion_frames_surface[self.explosion_frame_index]
            self.rect = self.image.get_frect(center=self.rect.center)


    def check_collisions(self):
        if pygame.sprite.collide_mask(self, player):
            player.damage(self.ASTEROID_DAMAGE)
            self.destroy()
                #player.SHIP_HEALTH -= self.ASTEROID_DAMAGE

    def update(self, delta_time):
        if not self.is_exploding:   
            self.move(delta_time)
            self.rotate(delta_time)
            self.check_collisions()
            self.destroy_timer()
        else: 
            self.explode_animate()

class Laser(pygame.sprite.Sprite):
    def __init__(self, surface, position, groups, laser_speed): 
        super().__init__(groups)
        self.image = surface
        self.rect = self.image.get_frect(midbottom=position)

        self.BASE_SPEED = 1
        self.speed = self.BASE_SPEED * laser_speed

        self.laser_sound = pygame.mixer.Sound(os.path.join(BASE_PATH, "assets", "audio", "laser.wav"))

    def move(self, delta_time):
        self.rect.y -= self.speed * delta_time

    def check_off_screen(self):
        if self.rect.midbottom[1] < 0: 
            self.kill()

    def check_collision(self):
        asteroid_group_sprites = pygame.sprite.spritecollide(self, asteroid_group, False, pygame.sprite.collide_mask)
        collided_asteroid = asteroid_group_sprites[0] if asteroid_group_sprites else None
        if collided_asteroid:
            collided_asteroid.explode_animate()
            self.destroy()
            update_score(collided_asteroid.ASTEROID_SCORE_ON_DESTROY)

    def destroy(self):
        self.kill()

    def play_sound(self):
        pygame.mixer.Sound.play(self.laser_sound)
    
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

HEALTH_ICON_PATH = os.path.join(BASE_PATH, "assets", "images", "icons", "health.png")

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
    score_text = f"{str(score)}"
    score_surface = font.render(score_text, True, (240, 240, 240))
    score_rect = score_surface.get_rect(midbottom=(WINDOW_WIDTH / 2, WINDOW_HEIGHT - 25 ))

    # border_rect = score_rect.inflate(20,20).move(0, -8) 
    # border_rect.midbottom = score_rect.midbottom

    display_surface.blit(score_surface, score_rect)
    pygame.draw.rect(display_surface, (240, 240, 240), score_rect.inflate(20,10).move(0, -5), 5, 3)

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
    player.update_health_bar()
    display_score()
    pygame.display.update()    

pygame.quit()




