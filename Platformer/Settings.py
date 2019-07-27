import random, pygame

display_width = 600
display_height = 650
SPRITESHEET = 'pngs/spritesheet_jumper.png'

bg = pygame.image.load("pngs/bg.png")
bg_rect = bg.get_rect()

PLAYER_LAYER = 2
PLATFORM_LAYER = 1
MOB_LAYER = 2
POW_LAYER = 1

player_acc = 0.7
player_friction = -0.12
player_grav = 0.9
random_pos_x = random.randrange(0,display_width)
random_pos_y = random.randrange(0, display_height)

black = (0,0,0)
white = (255,255,255)

PLATFORM_LIST = [(0, display_height - 60),
                 (display_width / 2 - 50, display_height * 3 / 4 - 50),
                 (125, display_height - 350),
                 (350, 200),
                 (175, 100)]
