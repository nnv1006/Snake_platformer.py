import time as tm

import pygame
from pygame import *
import random
import math


class Bot(pygame.sprite.Sprite):
    def __init__(self, filename,group1, group,x,y,gab, coorx, coory,bot_spd, bot_JUMP,gravity,hero,PLATFORM_HEIGHT,PLATFORM_WIDTH):
        pygame.sprite.Sprite.__init__(self)
        filename = pygame.transform.scale(filename, gab)
        self.bot_spd=bot_spd
        self.bot_JUMP=bot_JUMP
        self.x=x
        self.y=y
        self.time_mind= tm.time()
        self.hero=hero
        self.coorx=coorx
        self.coory=coory
        self.PLATFORM_HEIGHT=PLATFORM_HEIGHT
        self.PLATFORM_WIDTH=PLATFORM_WIDTH
        self.gravity=gravity
        self.onGround = False
        self.onTarget = False
        self.PlayCol=0
        self.mind=True
        self.image = filename
        self.rect = self.image.get_rect(topleft=(x,y))
        self.add(group)
        self.add(group1)
        self.xvel = 0  # скорость перемещения. 0 - стоять на месте
        self.yvel = 0
        i=random.randint(0,len(coorx)-1)
        self.targ=(coorx[i],coory[i])
        self.play_s=(0,0)
        #print(self.targ)





    def update(self, platforms):

        if self.mind:
            self.play_s=(self.hero.rect.x,self.hero.rect.y)
            diagx=abs(self.rect.x-self.play_s[0])
            diagy=abs(self.rect.y-self.play_s[1])
            diag=math.hypot(diagx,diagy)
            if diag <= self.PLATFORM_WIDTH*8:
                if self.onGround:
                    if self.rect.y-self.play_s[1] > self.PLATFORM_HEIGHT*2:

                        self.yvel = -self.bot_JUMP



                elif self.rect.x > self.play_s[0]:
                    self.xvel = -self.bot_spd

                elif self.rect.x < self.play_s[0]:
                    self.xvel = self.bot_spd



            elif self.rect.x<= self.targ[0]+self.PLATFORM_WIDTH and self.rect.x>=self.targ[0] :
                i = random.randint(0, len(self.coorx) - 1)
                self.targ = (self.coorx[i], self.coory[i])



            else:
                if self.onGround and random.randint(0,10)==10:
                    if self.rect.y > self.targ[1]:
                        self.yvel = -self.bot_JUMP



                if self.rect.x > self.targ[0]:
                    self.xvel = -self.bot_spd

                elif self.rect.x < self.targ[0]+self.PLATFORM_WIDTH:
                    self.xvel = self.bot_spd


                #elif self.rect.y > self.targ[1]:

            if not self.onGround:
                self.yvel += self.gravity

            self.onGround = False


            if self.PlayCol != 0:
                self.mind = False
                if self.PlayCol == 2:
                    self.xvel += -self.bot_spd*10
                    self.yvel = -self.bot_JUMP//3


                elif self.PlayCol == 3:
                    self.xvel += self.bot_spd*10
                    self.yvel = -self.bot_JUMP//3

            self.rect.y += self.yvel
            self.collide(0, self.yvel, platforms)

            self.rect.x += self.xvel  # переносим свои положение на xvel
            self.collide(self.xvel, 0, platforms)
            self.PlayCol=0
        else:
            if not self.onGround:
                self.yvel += self.gravity

            self.onGround = False
            if self.xvel>0:
                self.xvel-=1
            elif self.xvel <0:
                self.xvel+=1


            self.rect.y += self.yvel
            self.collide(0, self.yvel, platforms)
            self.rect.x += self.xvel  # переносим свои положение на xvel
            self.collide(self.xvel, 0, platforms)
            if tm.time()-self.time_mind>=4:
                self.mind=True

                print(1)


    def collide(self, xvel, yvel, platforms):
            #if sprite.collide_rect(self,self.hero):
                #self.kill()

            for p in platforms:
                if sprite.collide_rect(self, p):  # если есть пересечение платформы с игроком

                    if xvel > 0:  # если движется вправо
                        self.rect.right = p.rect.left  # то не движется вправо
                        if self.onGround :
                                self.yvel = -self.bot_JUMP


                    if xvel < 0:  # если движется влево
                        self.rect.left = p.rect.right  # то не движется влево
                        if self.onGround:
                            self.yvel = -self.bot_JUMP
                    if yvel > 0:  # если падает вниз
                        self.rect.bottom = p.rect.top  # то не падает вниз
                        self.onGround = True  # и становится на что-то твердое
                        self.yvel = 0  # и энергия падения пропадает

                    if yvel < 0:  # если движется вверх
                        self.rect.top = p.rect.bottom  # то не движется вверх
                        self.yvel = 0