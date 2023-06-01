from typing import Any
import pygame

class Bird(pygame.sprite.Sprite):
    def __init__(self, scale_factor):
        super(Bird, self).__init__()
        self.image_list = [pygame.transform.scale_by(pygame.image.load("./gallery/images/bird_up.png").convert_alpha(),scale_factor),
                           pygame.transform.scale_by(pygame.image.load("./gallery/images/bird_down.png").convert_alpha(),scale_factor)]

        self.image_index = 0
        self.image = self.image_list[self.image_index]
        self.rect = self.image.get_rect(center = (100,100))
        self.y_velocity = 0
        self.gravity = 10
        self.flap_speed = 250
        self.anim_counter = 0
        self.update_on = False

    
    def update(self, dt):
        if self.update_on:
            self.playAnimation()
            self.applyGravity(dt)

            if self.rect.y <= 0:
                self.rect.y = 0
                self.flap_speed = 0
                # self.y_velocity = 0
            elif self.rect.y > 0 and self.flap_speed == 0:
                self.flap_speed = 250
    
    def applyGravity(self, dt):                
        self.y_velocity += self.gravity * dt
        self.rect.y += self.y_velocity
    
    def flap(self, dt):
        self.y_velocity = -self.flap_speed * dt

    def playAnimation(self):
        if self.anim_counter == 5:
            self.image = self.image_list[self.image_index]
            if self.image_index == 0:
                self.image_index = 1
            else:
                self.image_index = 0
            self.anim_counter = 0

        self.anim_counter += 1

    def resetPosition(self):
        self.rect.center = (100,100)
        self.y_velocity = 0
        self.anim_counter = 0