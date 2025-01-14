import pygame
from pygame import *
import time as tm

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y,filename,gravity,spd,JUMP_POWER,):
        pygame.sprite.Sprite.__init__(self)
        self.xvel = 0  # скорость перемещения. 0 - стоять на месте
        self.yvel = 0
        self.hp=60
        self.startX = x  # Начальная позиция Х, пригодится когда будем переигрывать уровень
        self.startY = y
        self.image = filename
        self.rect = self.image.get_rect(center=(x, y))  # прямоугольный объект
        self.onGround = False
        self.gravity=gravity
        self.spd=spd
        self.JUMP_POWER=JUMP_POWER
        self.s1=pygame.image.load("snake.png").convert_alpha()
        self.s1=pygame.transform.scale(self.s1, (120, 120))
        self.s2 = pygame.image.load("snake1.png").convert_alpha()
        self.s2 = pygame.transform.scale(self.s2, (120, 120))
        self.s3 = pygame.image.load("snake2.png").convert_alpha()
        self.s3 = pygame.transform.scale(self.s3, (120, 120))
        self.s4 = pygame.image.load("snake4.png").convert_alpha()
        self.s4 = pygame.transform.scale(self.s4, (120, 120))

    def update(self,left,right,up, platforms,bots,fire):



        if self.hp<=0:
            self.rect.x=self.startX
            self.rect.y=self.startY

            self.hp=100
        if left:
                self.xvel = -self.spd  # Лево = x- n
                self.image=self.s2



        if right:
                self.xvel = self.spd  # Право = x + n
                self.image=self.s4




        if not (left or right):  # стоим, когда нет указаний идти
                self.xvel = 0
                self.image=self.s2
        if up:
            self.image=self.s3
            if self.onGround:  # прыгаем, только когда можем оттолкнуться от земли
                    self.yvel = -self.JUMP_POWER


        if left and up:
            self.image=self.s3

        elif right and up:
            self.image=self.s1




        if not self.onGround:
            self.yvel += self.gravity

        self.onGround = False
        self.rect.y += self.yvel
        self.collide(0, self.yvel, platforms,bots)

        self.rect.x += self.xvel  # переносим свои положение на xvel
        self.collide(self.xvel, 0, platforms,bots)
        last=lest=0

    def collide(self, xvel, yvel, platforms,bots):
        for p in platforms:
            if sprite.collide_rect(self, p): # если есть пересечение платформы с игроком

                if xvel > 0:                      # если движется вправо
                    self.rect.right = p.rect.left # то не движется вправо

                if xvel < 0:                      # если движется влево
                    self.rect.left = p.rect.right # то не движется влево

                if yvel > 0:                      # если падает вниз
                    self.rect.bottom = p.rect.top # то не падает вниз
                    self.onGround = True          # и становится на что-то твердое
                    self.yvel = 0                 # и энергия падения пропадает

                if yvel < 0:                      # если движется вверх
                    self.rect.top = p.rect.bottom # то не движется вверх
                    self.yvel = 0
        x=pygame.sprite.spritecollideany(self,bots)
        if x!=None and x.mind==True:
            self.hp-=10

            if x.rect.x<=self.rect.x:
                self.xvel = self.spd*5
                if self.onGround:
                 self.yvel = -self.JUMP_POWER//3
                x.PlayCol=2
                x.time_mind= tm.time()
            else:
                self.xvel = -self.spd * 5
                if  self.onGround:
                 self.yvel = -self.JUMP_POWER // 3
                x.PlayCol=3
                x.time_mind = tm.time()





