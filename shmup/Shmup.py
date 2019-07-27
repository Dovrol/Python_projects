import pygame, random, glob

pygame.init()
pygame.mixer.init()

display_width = 800
display_height = 600

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Shmup')

black = (0,0,0)
white = (255,255,255)

meteors = []
images = glob.glob('Images/Meteors/*.png')
for item in images:
    meteors.append(pygame.image.load(item).convert())




clock = pygame.time.Clock()
spaceShip = pygame.image.load('Images/Ship.png').convert()
Meteor = pygame.image.load('Images/Meteor.png').convert()
Laser = pygame.image.load('Images/laser.png').convert()
BG = pygame.image.load('Images/background.png').convert()

shoot_sound = pygame.mixer.Sound("Music/Pew.wav")
explosion = pygame.mixer.Sound("Music/Explosion.wav")
Bolt_sound = pygame.mixer.Sound("Music/PowerUpSound.wav")
shield_sound = pygame.mixer.Sound("Music/ShieldSound.wav")
pygame.mixer.music.load("Music/Music.ogg")
BG_rect = BG.get_rect()

regularExplosion = []
for i in range(9):
    img = pygame.image.load('Images/regularExplosion0{}.png'.format(i)).convert()
    img.set_colorkey(black)
    regularExplosion.append(img)


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font('Images/Space1.otf', size)
    text_surface = font.render(text, True, (255,255,255))
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def newmob():
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

def shieldBar(bar_long):
    draw_text(gameDisplay, "HP", 50, 50, 10)
    bar = pygame.draw.rect(gameDisplay, (0,0,0), (90,10,150,50), 3)
    fill = pygame.draw.rect(gameDisplay, (0,255,0), (93,13,bar_long - 6,44))

def show_go_screen():
    gameDisplay.blit(BG, BG_rect)
    draw_text(gameDisplay, "SHMUP", 64, display_width / 2, display_height / 4)
    draw_text(gameDisplay, "Arrow keys to move, space to shoot", 28, display_width / 2, display_height / 2)
    draw_text(gameDisplay, "Press s key to start", 32, display_width / 2, display_height * (3 / 4))
    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    waiting = False

def pause_screen():
    gameDisplay.blit(BG, BG_rect)
    draw_text(gameDisplay, "PAUSE", 64, display_width / 2, display_height / 4)
    draw_text(gameDisplay, "Arrow keys to move, space to shoot", 28, display_width / 2, display_height / 2)
    draw_text(gameDisplay, "Press escape key to restart", 32, display_width / 2, display_height * (3 / 4))
    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    waiting = False

def stage(level):
    gameDisplay.blit(BG, BG_rect)
    draw_text(gameDisplay, "Level {}".format(level), 64, display_width / 2, display_height / 2)
    pygame.display.update()
    for i in mobs:
        i.kill()
    for i in range(level + 3):
        newmob()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    waiting = False

# def Boss_stage(level):
#     running = True
#     while running = True:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 quit()
#         gameDisplay.blit(BG, BG_rect)
#         if boss.hp <= 0:
#             running = False
#
#         boss = Boss()
#         all_sprites.add(boss)
#         bosses.add(boss)
#         pygame.display.update()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(spaceShip,(50,38))
        self.rect = self.image.get_rect()
        self.radius = 20
        self.image.set_colorkey(black)
        self.rect.centerx = display_width / 2
        self.rect.bottom = display_height - 10
        self.speed_x = 0
        self.shield = 150
        self.shoot_delay = 250
        self.last_shoot = pygame.time.get_ticks()

    def update(self):
        self.speed_x = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speed_x = -5
        elif keystate[pygame.K_RIGHT]:
            self.speed_x = 5
        self.rect.x += self.speed_x
        if keystate[pygame.K_SPACE]:
            self.shoot(power_up_on)
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > display_width:
            self.rect.right = display_width
        if player.shield >= 150:
            player.shield = 150


    def shoot(self, power_up_on):
        now = pygame.time.get_ticks()
        if now - self.last_shoot > self.shoot_delay:
            self.last_shoot = now
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)
            shoot_sound.play()
            if power_up_on == True:

                bullet1 = Bullet(self.rect.centerx, self.rect.top, 5)
                all_sprites.add(bullet1)
                bullets.add(bullet1)

                bullet2 = Bullet(self.rect.centerx, self.rect.top, -5)
                all_sprites.add(bullet2)
                bullets.add(bullet2)

                time_now = pygame.time.get_ticks()
                if gun_powerup_time - time_now < -5000:
                    power_up_on = False
                    bullet1.kill()
                    bullet2.kill()

class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_org = random.choice(meteors)
        self.image_org.set_colorkey(black)
        self.image = self.image_org.copy()
        self.rect = self.image.get_rect()
        self.radius = 18
        self.rect.x = random.randint(0, display_width - self.rect.width)
        self.rect.y = - 50
        self.speed_y = random.randint(3,8)
        self.angle = 0
        self.rot_speed = random.randint(-10,10)
        self.last_update = pygame.time.get_ticks()

    def update(self):
        self.rotate()
        self.rect.y += self.speed_y
        if self.rect.top > display_height + 10:
            self.rect.x = random.randint(0, display_width - self.rect.width)
            self.rect.y = - 50
            self.speed_y = random.randint(5,10)

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.angle = (self.angle + self.rot_speed) % 360
            old_center = self.rect.center
            self.image = pygame.transform.rotate(self.image_org, self.angle)
            self.rect = self.image.get_rect()
            self.rect.center = old_center

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, speed_x = 0):
        pygame.sprite.Sprite.__init__(self)
        self.image = Laser
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10
        self.speed_x = speed_x

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speed_x
        if self.rect.bottom < 0 or self.rect.top > display_height:
            self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.image = regularExplosion[0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(regularExplosion):
                self.kill()
            else:
                # center = self.rect.center
                self.image = regularExplosion[self.frame]
                # self.rect = self.image.get_rect()
                # self.rect.center = center

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['Gun', 'Shield'])
        self.image = powerUpType[self.type]
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 3

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

# class Boss(pygame.sprite.Sprite):
#     def __init__(self):
#         pygame.sprite.Sprite.__init__(self)
#         self.image = boss_img
#         self.image.set_colorkey(black)
#         self.rect = self.image.get_rect()
#         self.rect.x = display_width / 2
#         self.rect.y = display_height / 2
#         self.hp = 500
#         self.dmg = 35
#         self.move_x = 5
#
#     def update(self):
#         self.rect.x += self.move_x
#         if self.rect.x > display_width - self.rect.x or self.rect.x < 0:
#             self.move_x *= -1

powerUpType = {}
powerUpType['Gun'] = pygame.image.load("Images/Bolt.png")
powerUpType["Shield"] = pygame.image.load("Images/Shield.png")

game_over = True
pause = False

while True:
    if game_over == True:
        show_go_screen()
        game_over = False
        level = 1
        player = Player()
        all_sprites = pygame.sprite.Group()
        mobs = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        powerups = pygame.sprite.Group()
        bosses = pygame.sprite.Group()
        all_sprites.add(player)
        power_up_on = False
        pygame.mixer.music.play(loops = -1)
        score = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pause_screen()


            #UPDATE


    all_sprites.update()

    #Check if bullet hit a mobs
    mob_hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in mob_hits:
        score += 1
        expl = Explosion(hit.rect.center)
        all_sprites.add(expl)
        newmob()
        if random.random() > 0.93:
            powup = PowerUp(hit.rect.center)
            all_sprites.add(powup)
            powerups.add(powup)
        explosion.play()


    #Check if mob hit player
    hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
    for hit in hits:
        player.shield -= 50
        expl = Explosion(hit.rect.center)
        all_sprites.add(expl)
        newmob()
        if player.shield <= 0:
            game_over = True


    #Check if powerup hit player
    powerUpHit = pygame.sprite.spritecollide(player, powerups, True)
    for hit in powerUpHit:
        if hit.type == 'Shield':
            player.shield += random.randrange(10, 30)
            shield_sound.play()
        elif hit.type == 'Gun':
            gun_powerup_time = pygame.time.get_ticks()
            power_up_on = True
            Bolt_sound.play()



            #DRAW


    if score % 50 == 0:
        stage(level)
        score += 1
        level += 1


    # if level == 1:
    #     boss = Boss()
    #     all_sprites.add(boss)
    #     bosses.add(boss)

    gameDisplay.blit(BG, BG_rect)
    draw_text(gameDisplay, "SCORE", 45, display_width - 220, 10)
    draw_text(gameDisplay, str(score), 45, display_width - 55, 10)
    shieldBar(player.shield)

    all_sprites.draw(gameDisplay)

    pygame.display.update()
    clock.tick(60)
pygame.quit()
quit()
