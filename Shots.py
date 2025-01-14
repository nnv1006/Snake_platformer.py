import pygame
from pygame import *
import math

class Shot(pygame.sprite.Sprite):
    def __init__(self, x, y, x1, y1, w, h, spd, filename, group,entities,spd_shot,total_level_height,total_level_width):
        pygame.sprite.Sprite.__init__(self)
        filename = pygame.transform.scale(filename, (64, 64))
        self.w = w
        self.h = h
        self.x = x
        self.y = y
        self.total_level_height=total_level_height
        self.total_level_width=total_level_width
        self.x1 = x1
        self.y1 = y1
        self.image = filename
        self.spd = spd
        self.rect = self.image.get_rect(center=(x, y))
        self.add(group)
        self.add(entities)
        if self.rect.y + self.spd < h and self.rect.x + self.spd < w and self.rect.y - self.spd + 20 > 0 and self.rect.x - self.spd + 20 > 0:

            if self.x1 >= self.x and self.y1 <= self.y:
                self.a = self.x1 - self.rect.x
                self.b = self.rect.y - self.y1
                self.c = math.hypot(self.a, self.b)
                self.t = self.c / spd_shot + 1
                self.spdx = self.a / self.t
                self.spdy = -self.b / self.t

            elif self.x1 >= self.x and self.y1 >= self.y:
                self.a = self.x1 - self.rect.x
                self.b = self.y1 - self.rect.y
                self.c = math.hypot(self.a, self.b)
                self.t = self.c / spd_shot + 1
                self.spdx = self.a / self.t
                self.spdy = self.b / self.t

            elif self.x1 <= self.x and self.y1 >= self.y:
                self.a = self.rect.x - self.x1
                self.b = self.y1 - self.rect.y
                self.c = math.hypot(self.a, self.b)
                self.t = self.c / spd_shot + 1
                self.spdx = -self.a / self.t
                self.spdy = self.b / self.t


            elif self.x1 <= self.x and self.y1 <= self.y:
                self.a = self.rect.x - self.x1
                self.b = self.rect.y - self.y1
                self.c = math.hypot(self.a, self.b)
                self.t = self.c / spd_shot + 1
                self.spdx = -self.a / self.t
                self.spdy = -self.b / self.t

    def update(self, *args):
        if self.rect.y < self.total_level_height + 20 and self.rect.x < self.total_level_width + 20 and self.rect.y > 0 and self.rect.x > 0:
            self.rect.x = self.rect.x + self.spdx
            self.rect.y = self.rect.y + self.spdy
            self.spdy+=0.04
        else:
            self.kill()