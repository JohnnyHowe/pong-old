import pygame 
from window import Window

class Player:
    def __init__(self, up_key, down_key, x_position):
        self.up_key = up_key
        self.down_key = down_key
        self.rect = [x_position, 0.5, 0.02, 0.25]
        self.speed = 0.005

    def update(self):
        self.move()
        self.limit_movement()

    def move(self):
        self.rect[1] += self.get_key_dir() * self.speed

    def get_key_dir(self):
        m = 0
        if pygame.key.get_pressed()[self.up_key]: m -= 1
        if pygame.key.get_pressed()[self.down_key]: m += 1
        return m

    def limit_movement(self):
        """ Keep player on window """
        self.rect[1] = min(max(self.rect[3] / 2, self.rect[1]), 1 - self.rect[3] / 2)

    def show(self):
        Window.draw_rect(self.rect, (255, 255, 255))
