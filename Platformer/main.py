import pygame, random
from Sprites import *
from Settings import *
from os import path

class Game():
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.gameDisplay = pygame.display.set_mode((display_width, display_height))
        pygame.display.set_caption('Platformer')
        self.clock = pygame.time.Clock()
        self.plat_counter = 0
        self.running = True
        self.load_data()

    def load_data(self):
        with open('HighScore.txt', 'r') as f:
            try:
                self.highscore = int(f.read())
            except:
                self.highscore = 0
        self.ss = Spritesheet(SPRITESHEET)
        self.jump_sound = pygame.mixer.Sound('sound/Jump22.wav')

    def new(self):
        # start a new game
        pygame.mixer.music.load('sound/Happy Tune.ogg')
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.powerups = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.mobs = pygame.sprite.Group()
        self.list_platforms = []
        self.score = 0
        self.time = pygame.time.get_ticks()

        self.player = Player(self)
        for plat in PLATFORM_LIST:
            Platform(self, *plat)

        self.run()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.jump()

    def run(self):
        #Game loop
        pygame.mixer.music.play(loops = -1)
        self.playing = True
        while self.playing:
            self.clock.tick(60)
            self.events()
            self.draw()
            self.update()
        pygame.mixer.music.fadeout(500)

    def update(self):
        self.all_sprites.update()

        if self.player.vel.y > 0:
            hits = pygame.sprite.spritecollide(self.player, self.platforms, False)
            for i in hits:
                if self.player.pos.x > i.rect.left - 10 and self.player.pos.x < i.rect.right + 10:
                    if self.player.pos.y < i.rect.bottom:
                        self.now = pygame.time.get_ticks()
                        self.player.pos.y = i.rect.top + 1
                        self.player.vel.y = 0

        mob_hits = pygame.sprite.spritecollide(self.player, self.mobs, True, pygame.sprite.collide_mask)
        if mob_hits:
            self.playing = False

        if self.player.rect.top <= display_height / 4:
            self.player.pos.y += max(abs(self.player.vel.y),2)
            for mob in self.mobs:
                mob.rect.y += max(abs(self.player.vel.y),2)
            for plat in self.platforms:
                plat.rect.y += max(abs(self.player.vel.y),2)
                if plat.rect.top >= display_height:
                    plat.kill()
                    self.score += 1

                now = pygame.time.get_ticks()
                if now - self.time > 5000:
                    self.time = now
                    Mob(self)

        while len(self.platforms) < 6:
            width = random.randrange(50, 100)
            Platform(self, random.randrange(0, display_width - width),random.randrange(-75, -30))

        if self.player.rect.top > display_height:
            self.playing = False

        hit = pygame.sprite.spritecollide(self.player, self.powerups, True)
        if hit:
            self.player.vel.y = -70


    def draw(self):
        self.gameDisplay.blit(bg, bg_rect)
        self.all_sprites.draw(self.gameDisplay)
        self.draw_text(self.gameDisplay,"Score", 30, 50,10)
        self.draw_text(self.gameDisplay,str(self.score), 30, 130,10)
        pygame.display.update()

    def draw_text(self, surf, text, size, x, y):
        font = pygame.font.Font('freesansbold.ttf', size)
        text_surface = font.render(text, True, (0,0,0))
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        surf.blit(text_surface, text_rect)

    def Starting_screen(self):
        self.sound_ss = pygame.mixer.music.load('sound/Yippee.ogg')
        pygame.mixer.music.play(loops = -1)
        self.gameDisplay.blit(bg, bg_rect)
        self.draw_text(self.gameDisplay, "JUMPY", 64, display_width / 2, display_height / 4)
        self.draw_text(self.gameDisplay, "Press space to continue", 30,  display_width / 2, display_height / 2)
        self.draw_text(self.gameDisplay, "High Score: " + str(self.highscore), 30,  display_width / 2, display_height - 50)
        pygame.display.update()
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        run = False
        pygame.mixer.music.fadeout(500)

    def Game_over(self):
        self.sound_ss = pygame.mixer.music.load('sound/Happy Tune.ogg')
        pygame.mixer.music.play(loops = -1)
        self.gameDisplay.blit(bg, bg_rect)
        self.draw_text(self.gameDisplay, "GAME OVER", 64, display_width / 2, display_height / 4)
        self.draw_text(self.gameDisplay, "Your score: " + str(self.score), 30,  display_width / 2, display_height / 2)
        self.draw_text(self.gameDisplay, "Press space to continue", 30,  display_width / 2, display_height -200)
        if self.score > self.highscore:
            self.highscore = self.score
            with open('HighScore.txt', 'w') as f:
                f.write(str(self.score))


        pygame.display.update()
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        run = False
        pygame.mixer.music.fadeout(500)

g = Game()
while g.running:
    g.Starting_screen()
    g.new()
    g.Game_over()
pygame.quit()
quit()
