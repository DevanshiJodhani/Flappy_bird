import pygame
from random import randint
class Pipe:
    def __init__(self, scale_factor, move_speed):
        self.image_up = pygame.transform.scale_by(pygame.image.load("./gallery/images/pipe_up.png").convert_alpha(), scale_factor)
        self.image_down = pygame.transform.scale_by(pygame.image.load("./gallery/images/pipe_down.png").convert_alpha(), scale_factor)
        self.rect_up = self.image_up.get_rect()
        self.rect_down = self.image_down.get_rect()
        self.pipe_distance = 225
        self.rect_up.y = randint(250,520)
        self.rect_up.x = 600
        self.rect_down.y = self.rect_up.y - self.pipe_distance - self.rect_up.height
        self.rect_down.x = 600
        self.move_speed = move_speed

    def drawPipe(self,window):
        window.blit(self.image_up,self.rect_up)
        window.blit(self.image_down,self.rect_down)

    def update(self, dt):
        self.rect_up.x -= int(self.move_speed * dt)
        self.rect_down.x -= int(self.move_speed * dt)
