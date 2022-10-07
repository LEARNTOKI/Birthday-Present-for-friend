import pygame
import random
import os

FPS = 60
WIDTH = 500
HEIGHT = 600

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)

# game start
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Birthday Present")
clock = pygame.time.Clock()

# image
background_img = pygame.image.load(os.path.join("img", "background1.png")).convert()
player_img = pygame.image.load(os.path.join("img", "randomloti.png")).convert()
rock_img = pygame.image.load(os.path.join("img", "randombro.png")).convert()
bullet_img = pygame.image.load(os.path.join("img", "love2.png")).convert()
power_img = pygame.image.load(os.path.join("img", "randomspy.png")).convert()

# sound
shoot_sound = pygame.mixer.Sound(os.path.join("sound", "biu.mp3"))
collide_sound = pygame.mixer.Sound(os.path.join("sound", "mua.mp3"))
pygame.mixer.music.load(os.path.join("sound", "aiyaya.mp3"))
pygame.mixer.music.set_volume(10) 

font_name = pygame.font.match_font("楷体")
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface, text_rect)

def new_rock():
    r = Rock()
    all_sprites.add(r)
    rocks.add(r)

def draw_health(surf, hp, x, y):
    if hp < 0:
        hp = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (hp/100)*BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)

def draw_init():
    screen.fill(BLACK)
    draw_text(screen, "Happy Birthday!", 64, WIDTH/2, HEIGHT/4)
    draw_text(screen, "Move (<- ->)  Space  (shoot)", 22, WIDTH/2, HEIGHT/2)
    draw_text(screen, "Press any button to start the game", 18, WIDTH/2, HEIGHT/3)
    pygame.display.update()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return True
            elif event.type == pygame.KEYUP:
                waiting = False
                return False

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (80, 80))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.radius = 40
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = WIDTH/2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 11
        self.health = 100 

    def update(self):
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_RIGHT]:
            self.rect.x += self.speedx
        if self.rect.left > WIDTH:
            self.rect.right = 0
        if key_pressed[pygame.K_LEFT]:
            self.rect.x -= self.speedx
        if self.rect.right < 0:
            self.rect.left = WIDTH

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
        shoot_sound.play()

class Rock(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = rock_img
        self.image.set_colorkey(WHITE)
        self.image = pygame.transform.scale(rock_img, (70, 70))
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * 1 / 2)
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(2, 15)
        self.speedx = random.randrange(-3, 15)

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT or self.rect.left > WIDTH or self.rect.right < 0:
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(2, 10)
            self.speedx = random.randrange(-3, 3)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(bullet_img, (40, 40))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -20

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

class Power(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(power_img, (70, 70))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.kill()

pygame.mixer.music.play(-1)
 

# LOOP
show_init = True
running = True

while running:
    if show_init:
        close = draw_init()
        if close:
            break
        show_init = False
        all_sprites = pygame.sprite.Group()
        rocks = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        powers = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        for i in range(8):
            new_rock()
        score = 0

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    #game update
    all_sprites.update()
    hits = pygame.sprite.groupcollide(rocks, bullets, True, True)
    for hit in hits:
        score += hit.radius
        r = Rock()
        if random.random() > 0.8:
            pow = Power(hit.rect.center)
            all_sprites.add(pow)
            powers.add(pow)
        new_rock()


    #rock
    hits = pygame.sprite.spritecollide(player, rocks, True, pygame.sprite.collide_circle)
    for hit in hits:
        new_rock()
        player.health -= hit.radius
        collide_sound.play()
        if player.health <=0:
            show_init = True
 


    #collide
    hits = pygame.sprite.spritecollide(player, powers, True)
    for hit in hits:
        player.health += 20
        if player.health > 100:
            player.health = 100

    #screen
    screen.fill(BLACK)
    screen.blit(background_img, (0, 0))
    all_sprites.draw(screen)
    draw_text(screen, str(score), 18, WIDTH/2, 10)
    draw_health(screen, player.health, 5, 15)
    pygame.display.update()

pygame.quit()