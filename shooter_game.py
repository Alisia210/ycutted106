from pygame import *
from random import randint
win_width = 700
win_height = 500
window = display.set_mode(
    (win_width, win_height)
)
display.set_caption('Шутер')
background = transform.scale(image.load('galaxy.jpg'), (700, 500))

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_width, player_height, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (player_width, player_height))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys_pressed[K_d] and self.rect.x < 630:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, 15)
        bullets.add(bullet)

lost = 0
number = 0
score = 0

class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y >= 500:
            self.rect.y = 0
            self.rect.x = randint(5, 633)
            lost = lost + 1

class Asteroid(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y >= 500:
            self.rect.y = 0
            self.rect.x = randint(5, 633)
            lost = lost + 1

font.init()
font1 = font.Font(None, 36)
font2 = font.Font(None, 70)

win = text3_win = font2.render("YOU WIN!", 1, (84, 247, 90))
lose = text4_lose = font2.render("YOU LOSE! ", 1, (247, 84, 84))

class Bullet(GameSprite):
    def update(self):
        global lost
        self.rect.y -= self.speed
        if self.rect.y <= 0:
            self.kill()

sprite1 = Player('rocket.png', 315, 430, 65, 65, 10)
sprite2 = Enemy('ufo.png', 315, 0, 65, 65, 3)
sprite3 = Enemy('ufo.png', 355, 0, 65, 65, 3)
sprite4 = Enemy('ufo.png', 395, 0, 65, 65, 3)
sprite5 = Enemy('ufo.png', 435, 0, 65, 65, 3)
sprite6 = Enemy('ufo.png', 475, 0, 65, 65, 3)
sprite7 = Asteroid('asteroid.png', 515, 0, 65, 65, 3)

monsters = sprite.Group()
monsters.add(sprite2)
monsters.add(sprite3)
monsters.add(sprite4)
monsters.add(sprite5)
monsters.add(sprite6)

asteroidsss = sprite.Group()
asteroidsss.add(sprite7)

bullets = sprite.Group()

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()

qwe = mixer.Sound('fire.ogg')

clock = time.Clock()
FPS = 60

finish = False
run = True
while run:
    clock.tick(FPS)

    if finish != True:
        window.blit(background, (0, 0))
        text_lose = font1.render("Пропущено: " +str(lost), 1, (255, 255, 255))
        text2_lose = font1.render("Счет: " +str(score), 1, (255, 255, 255))
        window.blit(text_lose, (10, 10))
        window.blit(text2_lose, (10, 40))
        sprite1.update()
        sprite1.reset()
        monsters.update()
        monsters.draw(window)
        asteroidsss.update()
        asteroidsss.draw(window)
        bullets.draw(window)
        bullets.update()
        if lost > 5:
            window.blit(lose, (250, 250))
            finish = True
        if lost > 100:
            window.blit(lose, (250, 250))
            finish = True
        if score > 29:
            window.blit(win, (250, 250))
            finish = True

        collides = sprite.groupcollide(
            monsters, bullets, True, True
        )
        for c in collides:
            score = score + 1
            monster = Enemy('ufo.png', randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)

        if sprite.spritecollide(
            sprite1, asteroidsss, False
        ):
            lost = 100

    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                sprite1.fire()
                qwe.play()

    display.update()