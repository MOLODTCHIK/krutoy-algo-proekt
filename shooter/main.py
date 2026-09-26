from pygame import *
from random import randint
mixer.init()

mixer.music.load('space.ogg')

mixer.music.play()
firesound = mixer.Sound('fire.ogg')
font.init()
font1 = font.SysFont('Arial', 80)
win = font1.render('YOU WIN!', True, (255, 255, 255)) 
lose = font1.render('YOU LOSE!', True, (180, 0, 0))
font2 = font.SysFont('Arial', 36)
w = 0 #сбитые
l = 0 #пропущенные
goal = 25
max_lost = 1


class gamesprite(sprite.Sprite):
    def __init__(self,playerimage, playerx, playery,playerspeed, sizex , sizey):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(playerimage), (sizex, sizey))
        self.speed = playerspeed
        self.rect = self.image.get_rect()
        self.rect.x = playerx
        self.rect.y = playery
    def reset(self):
        window.blit(self.image, (self.rect.x,self.rect.y))

class player(gamesprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_RIGHT] and self.rect.x<620:
            self.rect.x += self.speed

        if keys[K_LEFT] and self.rect.x>6:
            self.rect.x -= self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, -15, 15, 20)
        bullets.add(bullet)

class enemy(gamesprite):
    def update(self):
        self.rect.y += self.speed
        global l
        if self.rect.y > 500:
            self.rect.x = randint(80, 620)
            self.rect.y = -randint(20, 100)
            self.speed = randint(1, 3)
            l = l+ 1    

class Bullet(gamesprite):
    def update(self):
        self.rect.y +=self.speed
        if self.rect.y < 0: self.kill()     

window = display.set_mode((700, 500))
display.set_caption("shooter")
background = transform.scale(image.load('galaxy.jpg'),(700, 500))
finish = False

win_width = 700
win_height = 500
ship_width = 80
ship_height = 85
center_x = (win_width - ship_width) // 2
center_y = win_height - ship_height - 10
pla = player('rocket.png', center_x, center_y, 8, ship_width, ship_height)
monsters = sprite.Group()
for i in range(1, 6):
    monster = enemy('ufo.png', randint(80, 620), randint(-200, -40), randint(1, 3), 50, 50)
    monsters.add(monster)
bullets = sprite.Group()
    
run = True
finish = False

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                firesound.play()
                pla.fire()
    if not finish:
        window.blit(background,(0, 0))
        txt = font2.render('счет: ' + str(w), 1, (255, 255, 255))
        window.blit(txt, (10, 20))
        txt_l = font2.render('пропущено: ' + str(l), 1, (255, 255, 255))
        window.blit(txt_l, (10, 50))
        if sprite.spritecollide(pla, monsters, False):
            finish = True
            print("потрачено")
        pla.update()
        monsters.update()
        pla.reset()
        monsters.draw(window)
        bullets.update()
        bullets.draw(window)
        display.update()
        collides  = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            w = w+1
            monster = enemy('ufo.png', randint(80, 620), -40, randint(1, 3), 50, 50)
            monsters.add(monster)
        if sprite.spritecollide(pla, monsters, False) or l >= max_lost:
            finish = True
            window.blit(lose, (200, 200))
        if w >= goal:
            finish  = True
            window.blit(win, (200, 200))
        display.update()
    else: 
        finish = False
        w = 0
        l = 0
        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()
        time.delay(3000)
        for i in range(1, 6):
            monster = enemy('ufo.png', randint(80, 620), randint(-200, -40), randint(1, 3), 50, 50)
            monsters.add(monster)
            
    time.delay(50)

'''if finish:
    window.blit(background, (0, 0))
    txt_goose = font2.render('потрачено', 1, (255, 0, 0))
    window.blit(txt_goose, (250, 200))
    display.update()

    time.delay(3000)'''