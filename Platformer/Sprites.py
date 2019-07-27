#Sprite classes for Platformer
import pygame, random
from Settings import *
vec = pygame.math.Vector2

class Player(pygame.sprite.Sprite):
    def __init__(self, Game):
        self.groups = Game.all_sprites
        self.layer = PLAYER_LAYER
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.Game = Game
        self.loadImages()
        self.last_update = 0
        self.frame = 0
        self.jumping = False
        self.walking = False
        self.image = self.standing[self.frame]
        self.rect = self.image.get_rect()
        self.image.set_colorkey(black)
        self.pos = vec(display_width / 2, display_height /2)
        self.vel = vec(0,0)
        self.acc = vec(0,0)

    def loadImages(self):
        self.standing = [self.Game.ss.get_image(614, 1063, 120, 191), self.Game.ss.get_image(690, 406, 120, 201)]
        for i in self.standing:
            i.set_colorkey(black)

        self.list_walking_l = []
        self.list_walking = [self.Game.ss.get_image(678, 860, 120, 201), self.Game.ss.get_image(692, 1458, 120, 207)]
        for i in self.list_walking:
            i.set_colorkey(black)
            self.list_walking_l.append(pygame.transform.flip(i, True, False))

    def frame_count(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 200:
            self.last_update = now
            if self.frame == 1:
                self.frame = 0
            else:
                self.frame = 1
        return self.frame

    def update(self):
        self.acc = vec(0,0.5)
        self.walking = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.acc.x += -player_acc
            if self.jumping ==False:
                self.walking = True
                bottom = self.rect.bottom
                self.image = self.list_walking_l[self.frame_count()]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
        elif keys[pygame.K_RIGHT]:
            self.acc.x += player_acc
            if self.jumping == False:
                self.walking = True
                bottom = self.rect.bottom
                self.image = self.list_walking[self.frame_count()]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

                #standing animation
        if self.walking == False:
            bottom = self.rect.bottom
            self.image = self.standing[self.frame_count()]
            self.rect = self.image.get_rect()
            self.rect.bottom = bottom


        if self.pos.x > display_width:
            self.pos.x = 0
        elif self.pos.x <= 0:
            self.pos.x = display_width

        self.acc.x += self.vel.x * player_friction
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        self.rect.midbottom = self.pos

                #jumping anmation
        if self.vel.y < -0.5:
            self.image = self.Game.ss.get_image(382,763,150,181)
            self.image.set_colorkey(black)

        self.mask = pygame.mask.from_surface(self.image)
    def jump(self):
        self.pos.y += 1
        hits = pygame.sprite.spritecollide(self, self.Game.platforms, False)
        last = pygame.time.get_ticks()
        self.pos.y -= 1
        if hits:
            if self.Game.now - last > -15:
                last = self.Game.now
                self.vel.y += -20 * player_grav
                self.Game.jump_sound.play()


class Platform(pygame.sprite.Sprite):
    def __init__(self,Game,x,y):
        self.layer = PLAYER_LAYER
        self.groups = Game.all_sprites, Game.platforms
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.Game = Game
        self.plat_img = [self.Game.ss.get_image(0,288,380,94),self.Game.ss.get_image(0, 768, 380 ,94)]
        self.image = self.Game.ss.get_image(0,960,380,94)
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        if random.randrange(100) < 4:
            Power(self.Game, self)

    # def update(self):
    #     if self.Game.score > 10:
    #         self.image  = self.plat_img[self.Game.plat_counter]
    #         self.image.set_colorkey(black)
    #         if self.Game.plat_counter == 1:
    #             self.Game.plat_counter = 0
    #         else:
    #             self.Game.plat_counter = 1


class Spritesheet(object):
    def __init__(self, filename):
        self.Spritesheet = pygame.image.load(filename).convert()

    def get_image(self, x, y, w, h):
        image = pygame.Surface((w,h))
        image.blit(self.Spritesheet, (0,0), (x,y,w,h))
        image = pygame.transform.scale(image, (w // 2, h // 2))
        return image


class Power(pygame.sprite.Sprite):
    def __init__(self,Game,plat):
        self.layer = POW_LAYER
        self.groups = Game.all_sprites, Game.powerups
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.plat = plat
        self.Game = Game
        self.image = self.Game.ss.get_image(814,1661,78,70)
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.x = self.plat.rect.centerx
        self.rect.bottom = self.plat.rect.top - 10

    def update(self):
        self.rect.bottom = self.plat.rect.top - 10
        if not self.Game.platforms.has(self.plat):
            self.kill()


class Mob(pygame.sprite.Sprite):
    def __init__(self, Game):
        self.layer = MOB_LAYER
        self.groups = Game.all_sprites, Game.mobs
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.Game = Game
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.img = [self.Game.ss.get_image(568,1671,122,139),self.Game.ss.get_image(568,1534,122,135)]
        self.image = self.img[self.frame]
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.center = (random.randrange(62,display_width - 62),20)
        self.speed = vec(5,2)
        self.mob_acc = vec(0,0.5)

    def update(self):
        self.time = pygame.time.get_ticks()
        if self.rect.left < 0:
            self.speed.x *= -1
        elif self.rect.right > display_width:
            self.speed.x *= -1
        self.rect.center += self.speed
        # self.speed += self.mob_acc
        # if self.speed.y > 3 or self.speed.y < -3:
        #     self.speed.y *= -1

        self.image = self.img[self.frame_count()]
        self.image.set_colorkey(black)
        self.mask = pygame.mask.from_surface(self.image)

    def frame_count(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 200:
            self.last_update = now
            if self.frame == 1:
                self.frame = 0
            else:
                self.frame = 1
        return self.frame
