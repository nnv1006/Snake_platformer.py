import pygame
from pygame import *
import random
import time
from Playe import Player
from Bots import Bot
from Shots import Shot

class Platform(sprite.Sprite):
    def __init__(self, x, y, filename):
        sprite.Sprite.__init__(self)
        filename=pygame.transform.scale(filename, (PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image = filename
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)

class Heal(sprite.Sprite):
    def __init__(self, x, y, filename):
        sprite.Sprite.__init__(self)
        filename = pygame.transform.scale(filename, (PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image = filename
        self.rect = Rect(x, y+PLATFORM_HEIGHT, PLATFORM_WIDTH, PLATFORM_HEIGHT)
        self.add(entities)
        self.add(heals)


class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)
    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)

def camera_configure(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t = -l + WIN_WIDTH / 2, -t + WIN_HEIGHT / 2
    l = min(0, l)  # Не движемся дальше левой границы
    l = max(-(camera.width - WIN_WIDTH), l)  # Не движемся дальше правой границы
    t = max(-(camera.height - WIN_HEIGHT), t)  # Не движемся дальше нижней границы
    t = min(0, t)  # Не движемся дальше верхней границы

    return Rect(l, t, w, h)


def cBot(group,group1,x,y):
    b_surf = [pygame.image.load(data['path']).convert_alpha() for data in b_data]
    inx = random.randint(0, len(b_surf) - 1)
    return Bot(b_surf[inx],group1, group, x, y,gab,coorx,coory,bot_spd,bot_JUMP,gravity,hero,PLATFORM_HEIGHT,PLATFORM_WIDTH)





def cShot(x, y, spd_shot,x1,y1):
    im = pygame.image.load("shot.png").convert_alpha()
    return Shot(x, y, x1*-1+pygame.mouse.get_pos()[0],y1*-1+pygame.mouse.get_pos()[1], total_level_width, total_level_height, spd_shot, im, shots,entities,spd_shot,total_level_height,total_level_width)


def cHeal(x,y):
    ik = pygame.image.load("platformPack_tile036.png").convert_alpha()
    return Heal(x,y,ik)






# ресурсы
level = [
       "--------------------------------------------------------------------------------------------------------------",
       "-                                                                                                            -",
       "-                                                                                                            -",
       "-                                                                                                            -",
       "-                                                                                                            -",
       "-                                                                                                            -",
       "-                                                                                                            -",
       "-                                                                                                            -",
       "-                                                                                                            -",
       "-                                                                                                            -",
       "-                                                                                                            -",
       "-0000000                           ---                                                                       -",
       "--------              -------------------------------------            -------------------                   -",
       "-                                                                                              ---           -",
       "-                                                                                                       ------",
       "-                                                                                                   ------   -",
       "-                                                                                               -------      -",
       "-                                                                                           -------          -",
       "-                                                                                    -------                 -",
       "-                                                                                ----                        -",
       "-                                                                         ----                               -",
       "-                      -                                          -------------                              -",
       "-          --          ---                                ----------------------------                       -",
       "--------------------------------------------------------------------------------------------------------------"]







b_data = ({'path': 'bot1.png', 'score': 100},
          {'path': 'bot2.png', 'score': 150},
          {'path': 'bot3.png', 'score': 200})
right=left=up=fire=0

WIN_WIDTH, WIN_HEIGHT= 1920, 1020
Display=(WIN_WIDTH,WIN_HEIGHT)
Fps=70
v_bots=15
s_bots=0
sound=0.05
gravity=0.33
PLATFORM_WIDTH = 60
PLATFORM_HEIGHT = 60
PLATFORM_COLOR = "#FF6262"

gab=(120,120)
JUMP_POWER = 15
spd=7
bot_spd=2
spd_shot=spd+5
bot_JUMP=10
defx=WIN_WIDTH//2
defy=WIN_HEIGHT//2
defy1=0
defx1=0
coorx=[]
coory=[]
g_score=0




# инициализация
pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()

#

# музыка фоновая
pygame.mixer.music.load("1234.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(sound)

f=pygame.font.SysFont('arial',30)

pygame.time.set_timer(pygame.USEREVENT, 200)

sc = pygame.display.set_mode(Display, pygame.RESIZABLE)

pygame.display.set_caption("snake")
pygame.display.set_icon(pygame.image.load("icon.png"))
bg = pygame.image.load("back1.jpg")
plat=pygame.image.load("icon1 (2).png")
clock = pygame.time.Clock()
plt=pygame.image.load("snake.png").convert_alpha()
plt = pygame.transform.scale(plt, gab)

hero=Player(200,200,plt,gravity,spd,JUMP_POWER )


entities = pygame.sprite.Group() # Все объекты
bots = pygame.sprite.Group()
platforms = [] # то, во что мы будем врезаться или опираться
entities.add(hero)
x = y = 0  # координаты
#bot_wait=pygame.event.Event(1)
shots = pygame.sprite.Group()
row1=len(level)-1
col1=0
row2=row1+1
environ=pygame.sprite.Group()
for row in level:  # вся строка

    for col in row:  # каждый символ

        if col == "-":
            pf = Platform(x, y, plat)
            entities.add(pf)
            environ.add(pf)
            platforms.append(pf)

        if col == " ":
            if row1>0:
                if level[len(level)-row1][col1] == "-" and col1 < len(row)-2 and level[len(level)-row1-1][col1+1] == " " and level[len(level)-row1-2][col1] == " " and level[len(level)-row1-2][col1+1] == " ":

                    coorx.append(x-gab[0]+PLATFORM_WIDTH)
                    coory.append(y-gab[1]+PLATFORM_HEIGHT)
        col1 += 1






        x += PLATFORM_WIDTH  # блоки платформы ставятся на ширине блоков
    row1 -= 1
    col1=0




    y += PLATFORM_HEIGHT  # то же самое и с высотой
    ym=y
    xm=x
    x = 0  # на каждой новой строчке начинаем с нуля


total_level_width = len(level[0]) * PLATFORM_WIDTH  # Высчитываем фактическую ширину уровня
total_level_height = len(level) * PLATFORM_HEIGHT  # высоту
tx=coorx
ty=coory
camera = Camera(camera_configure, total_level_width, total_level_height)



score = pygame.image.load('panelInset_beige.png').convert_alpha()
score = pygame.transform.scale(score,(300,100))
curs=pygame.image.load('cursorGauntlet_blue.png').convert_alpha()
heals=pygame.sprite.Group()

pygame.mouse.set_visible(False)
while 1:
    start_time=time.time()


    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            exit()
        if e.type == KEYDOWN and e.key == K_LEFT:
            left = True
        if e.type == KEYDOWN and e.key == K_RIGHT:
            right = True
        if e.type == KEYDOWN and e.key == K_UP:
            up = True
        if e.type == pygame.USEREVENT:

            s_bots=len(bots)
            if s_bots<v_bots:
                i = random.randint(0, len(coorx) - 1)
                cBot(bots,entities,coorx[i],coory[i])
                s_bots+=1
            if hero.hp<70:
                il=random.randint(0,len(coorx))
                cHeal(coorx[i],coory[i])


        if e.type == pygame.MOUSEBUTTONDOWN and e.button==1:
            defx = camera.state.x
            defy = camera.state.y
            cShot(hero.rect.center[0], hero.rect.center[1], spd_shot,defx,defy)
            fire=True
        if e.type == KEYUP and e.key == K_RIGHT:
            right = False
        if e.type == KEYUP and e.key == K_LEFT:
            left = False
        if e.type == KEYUP and e.key == K_UP:
            up = False
    jk=pygame.sprite.groupcollide(shots,environ,True,False)
    x=pygame.sprite.groupcollide(bots,shots,True,True)
    if x!= {}:
        g_score+=50

    sc.blit(bg, (0, 0))
    hero.update(left, right, up, platforms,bots,fire)  # передвижение
    bots.update(platforms)

    shots.update()
    camera.update(hero)
    hp1=hero.hp

    for e in entities:
        sc.blit(e.image, camera.apply(e))


    #sc_text1 = f.render(str(hp1), True, (205, 0, 205))

    #for i in range(0,hp1,25):
    #    sc.blit(sc_text1, (40, 40))



    sc_text = f.render('Score:' + str(g_score), True, (105, 105, 105))
    sc.blit(score, (0, 0))
    sc.blit(sc_text, (20, 10))
    sc_text1 = pygame.image.load('barGreen_horizontalLeft.png').convert_alpha()


    sc.blit(sc_text1, (20, 60))
    sc_text1 = pygame.image.load('barGreen_horizontalMid.png').convert_alpha()
    sc_text2 = pygame.image.load('barRed_horizontalMid.png').convert_alpha()

    x_h=29
    step=10
    for i in range(10,100,step):
        if i / step == ((100 - step) // step):
            sc_text2 = pygame.image.load('barRed_horizontalRight.png').convert_alpha()
        sc.blit(sc_text2, (x_h, 60))
        x_h += 18
    x_h = 29
    for i in range(10,hp1,step):
        if i / step == ((hp1 - step) // step):
            sc_text1 = pygame.image.load('barGreen_horizontalRight.png').convert_alpha()
        sc.blit(sc_text1, (x_h, 60))
        x_h += 18





    sc.blit(curs,pygame.mouse.get_pos())
    pygame.display.update()
    fire=0
    clock.tick(Fps)
    #print("FPS: ", 1.0 / (time.time() - start_time))












