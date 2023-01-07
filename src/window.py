import pygame

class _Window:
    def __init__(self):
        self.size = (500, 500)
        self.surface = pygame.display.set_mode(self.size, pygame.SCALED, vsync=1)
        pygame.init()

    def update_display(self):
        pygame.display.update()

    def draw_rect(self, rect, color):
        pygame.draw.rect(self.surface, color, self.converted_rect(self.scaled_rect(rect)))

    def draw_circle(self, position, radius, color):
        pygame.draw.circle(self.surface, color, self.scaled_position(position), radius * min(self.size))

    def converted_rect(self, rect):
        """ Given a rect where the position is the center, return a copy such that the position
        components are the top left """
        return (rect[0] - rect[2] / 2, rect[1] - rect[3] / 2, rect[2], rect[3])

    def scaled_rect(self, rect):
        sp = self.scaled_position((rect[0], rect[1]))
        ss = self.scaled_size((rect[2], rect[3]))
        return sp + ss

    def scaled_size(self,size):
        return self.scaled_position(size)

    def scaled_position(self,position):
        return (position[0] * self.size[0], position[1] * self.size[1])


# Give a refernce to a already instantiated object
# Now acts like a singleton
Window = _Window()