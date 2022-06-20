import pygame
import os

pygame.mixer.init()
pygame.font.init()


# ----- Screen Variables
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 1200
FPS = 60
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))



# ----- Physics Variables
GRAVITY = 0.5
ACCELERATION = 0.3
MAX_SPEED = 10
DECELERATION = ACCELERATION / 5



# ----- Player Variables
PLAYER_SIZE = 32
PLAYER_WALL_ANTICLIP_VELOCITY = 1


# ----- Entity Variables
COIN_WIDTH = 30
COIN_HEIGHT = 30
BOMB_DAMAGE = 30
BOMB_FOLLOW_DISTANCE = 200
BULLET_RADIUS = 3
BULLET_COOLDOWN = FPS / 6
BULLET_SPEED = 10
RAY_WIDTH = 4



# ----- HUD Variables
TEXT_SIZE = 30
HEALTH_BAR_WIDTH = 300
HEALTH_BAR_HEIGHT = 20
HEALTH_BAR_MARGIN = 30
TEXT_POS_MARGIN = 10
SYSTEM_FONT = "courierprime"


# ----- Color Variables
PLAYER_COLOR = (0, 100, 255)
BACKGROUND_COLOR = (30, 30, 30)
WALL_COLOR = (0, 0, 0)
RAY_COLOR = (0, 255, 0)

# ----- System Variables
IMAGES = {
    "BULLET_COUNT": pygame.image.load(os.path.join('Resources', 'images', 'bullet_indicator_icon.png')).convert_alpha(),
    "COIN_COUNT": pygame.image.load(os.path.join('Resources', 'images', 'coin_icon.png')).convert_alpha(),
}



# ----- Controls
CONTROLS = {
    "up": pygame.K_w,
    "down": pygame.K_s,
    "left": pygame.K_a,
    "right": pygame.K_d,
    "shoot": pygame.K_SPACE
}



# ----- Sounds
SOUND_VOLUME = 0.1
SOUNDS = {
    "coin_pickup": pygame.mixer.Sound(os.path.join('Resources', 'sounds', 'coin_pickup.wav')),
    "explosion": pygame.mixer.Sound(os.path.join('Resources', 'sounds', 'explosion.wav')),
    "gun_shoot": pygame.mixer.Sound(os.path.join('Resources', 'sounds', 'gun_shoot.wav')),
    "bomb_die": pygame.mixer.Sound(os.path.join('Resources', 'sounds', 'bomb_die.wav')),
}

for sound in SOUNDS:
    SOUNDS[sound].set_volume(SOUND_VOLUME)



# ----- Cheats
PLAYER_INVINCIBLE = True
INFINITE_BULLETS = True
ENABLE_BOMBS = False
PLAYER_DEBUG = False