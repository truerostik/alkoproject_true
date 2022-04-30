#Создай собственный Шутер!

from pygame import *
from random import randint
from time import time as timer
lost = 0
life = 0
now_time= 0
rel_time = False
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_y, size_x, player_speed):
       super().__init__()
       self.image = transform.scale(image.load(player_image), (65, 65))
       self.speed = player_speed
       self.rect = self.image.get_rect()
       self.rect.x = player_x
       self.rect.y = player_y
    def reset(self):
       window.blit(self.image, (self.rect.x, self.rect.y))
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if (keys[K_LEFT] or keys[K_a]) and self.rect.x > 5:
            self.rect.x -= self.speed
        if (keys[K_RIGHT] or keys[K_d]) and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('samolet11.png', self.rect.centerx -50, self.rect.top, 75, 60, -10)
        bullets.add(bullet)
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 600:
            self.rect.y = 700
            self.rect.x = randint(100, 1080)
            self.rect.y = -80
            lost = lost + 1
class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
           self.kill()
win_width = 1280
win_height = 640
window = display.set_mode((win_width, win_height))
display.set_caption("11 of September 2001")
background = transform.scale(image.load("nebo_goluboy_belyy_oblaka_nezhnost_4937_1280x720.jpg"), (win_width, win_height))
ship = Player('arab_11.png', 5, win_height - 80, 120, 100, 15)
house11_img_enemy = ('house11.png')
#ammo = ('samolet11.png')

monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy(house11_img_enemy, randint(100, win_width - 80), -40, 80, 50, 1)
    monsters.add(monster)


asteroids = sprite.Group()
for i in range(1, 3):
    asteroid = Enemy('aster1.png', randint(100, win_width - 80), -40, 80, 50, 1)
    asteroids.add(asteroid)
bullets = sprite.Group()

run = True
finish = False
clock = time.Clock()
FPS = 60
score = 0
max_lost = 99  
goal = 10
#музыка 

last_time = timer()
life_color = (250, 250, 250)
num_fire = 0
mixer.init()
mixer.music.load('Arabskaya_rEp.mp3')
mixer.music.play()

font.init()
font1 = font.SysFont('Arial', 80)
font2 = font.SysFont('Arial', 36)
win = font1.render('YOU WIN !', True, (255, 255, 255))
lose = font1.render('YOU LOSE !', True, (180, 0, 0))
fire_sound = mixer.Sound('ochen-gromkiy-zvuk-vyistrela1.ogg')
while run:
    for e in event.get():
        if e.type == QUIT:
           run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    num_fire += 1
                    fire_sound.play()
                    ship.fire()
                if num_fire >= 5 and rel_time == False:
                    last_time = timer()
                    rel_time = True
                    

  
    if not finish :
        window.blit(background,(0, 0))

        
        ship.update()
        monsters.update()
        bullets.update()
        asteroids.update()
        ship.reset()
        monsters.draw(window)
        bullets.draw(window)
        asteroids.draw(window)

        if rel_time == True:
            now_time = timer()

            if now_time - last_time < 1:
                reload = font2.render('Перезарядка...', 1, (150, 0, 0))
                window.blit(reload, (260, 460))
            else:
                num_fire = 0
                rel_time = False

        collidaster = sprite.groupcollide(asteroids, bullets, True, True)
        for c in collidaster:
            score = score + 1
            asteroid = Enemy('aster1.png', randint(100, win_width - 80), -40, 80, 50, 1)
            asteroids.add(asteroid)
        

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score = score + 1
            monster = Enemy(house11_img_enemy, randint(100, win_width - 80), -40, 80, 50, 2)
            monsters.add(monster)
        if sprite.spritecollide(ship, monsters, False) or lost >= max_lost:
            finish = True
            window.blit(lose, (200, 200))
        if score >= goal:
            finish = True
            window.blit(win, (200, 200))

        if lost >= 7:
            finish = True
            
            
        text = font2.render('Счет: ' + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))
            
        text_lose = font2.render('Пропушено: ' + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))
            
        if life == 3:
            life_color = (0, 150, 0)
        if life == 2:
            life_color = (150, 150, 0)
        if life == 1:
            life_color = (150, 0, 0)

        text_life = font1.render(str(life), 1, life_color)
        window. blit(text_life, (650, 10))



        display.update()
# TODO ifefji
    else:
        finish = False
        score = 0
        lost = 0
        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()
        for a in asteroids:
            a.kill()
        
        time.delay(3000)
        for i in range(1, 6):
            monster = Enemy(house11_img_enemy, randint(100, win_width - 80), -40, 80, 50, 2)
            monsters.add(monster)
        for i in range(1, 3):
            asteroid = Enemy('aster1.png', randint(100, win_width - 80), -40, 80, 50, 1)
            asteroids.add(asteroid)


    time.delay(20)