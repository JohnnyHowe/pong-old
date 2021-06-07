import pygame
from window import Window
from player import Player
from ball import Ball


def event_loop():
    events = pygame.event.get()
    for event in events:
        if (event.type == pygame.QUIT):
            quit()


class Game:
    def __init__(self):
        self.reset()
        self.clock = pygame.time.Clock()

    def reset(self):
        self.players = [
            Player(pygame.K_w, pygame.K_s, 0.05),
            Player(pygame.K_o, pygame.K_l, 0.95),
        ]
        self.ball = Ball([self.players[0].rect[0] + 0.05, self.players[0].rect[1]])

    def display(self):
        Window.surface.fill((100, 100, 100))
        for player in self.players:
            player.show()
        self.ball.show()
        Window.update_display()

    def physics_step(self):
        self.ball.update()
        for player in self.players:
            player.update()
            self.ball.bounce_off_player(player.rect)
        if not self.ball.is_in_bounds():
            self.reset()

    def run(self):
        while True:
            self.clock.tick(100)
            event_loop()
            self.physics_step()
            self.display()

if __name__ == "__main__":
    Game().run()
