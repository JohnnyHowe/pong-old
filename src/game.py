import pygame
from pygame.constants import K_SPACE, SRCALPHA
from window import Window
from player import Player
from ball import Ball

class GameState:
    pregame = 0
    in_play = 1


class Game:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.next_start_player = 1
        self.font = pygame.font.Font("src/Pixeled.ttf", 80)
        self.controls_font = pygame.font.Font("src/Pixeled.ttf", 20)
        self.text_margin = [40, 20]
        self.players = [
            Player(pygame.K_w, pygame.K_s, 0.05),
            Player(pygame.K_o, pygame.K_l, 0.95),
        ]
        self.reset()
        self.color = (130, 180, 255)
        self.controls_text_color = (210, 235, 255)
        self.text_color = (190, 220, 255)
        self.bar_color = (150, 190, 255)

    def reset(self):
        self.players[0].reset()
        self.players[1].reset()
        self.ball = Ball([self.players[0].rect[0] + 0.05, self.players[0].rect[1]])
        self.state = GameState.pregame
        self.next_start_player = abs(self.next_start_player - 1)

    def event_loop(self):
        events = pygame.event.get()
        for event in events:
            if (event.type == pygame.QUIT):
                quit()
        self.system_events = events

    def display_start_controls(self):
        t = self.controls_font.render("Press Space to Start", True, self.controls_text_color)
        rect = t.get_rect()
        self.display_player_controls()
        Window.surface.blit(t, ((Window.size[0] - rect.width) / 2, (Window.size[1] - rect.height) / 2))

    def display_player_controls(self):
        # Player1
        w = self.controls_font.render("s", True, self.controls_text_color)
        s = self.controls_font.render("w", True, self.controls_text_color)
        wtext_rect = w.get_rect()
        stext_rect = s.get_rect()
        player1_rect = Window.scaled_rect(self.players[0].rect)
        Window.surface.blit(w, (player1_rect[0] - wtext_rect.width / 2, player1_rect[1] + player1_rect[3] / 2))
        Window.surface.blit(s, (player1_rect[0] - stext_rect.width / 2, player1_rect[1] - player1_rect[3] / 2 - stext_rect.height))
        # Player1
        w = self.controls_font.render("l", True, self.controls_text_color)
        s = self.controls_font.render("o", True, self.controls_text_color)
        wtext_rect = w.get_rect()
        stext_rect = s.get_rect()
        player1_rect = Window.scaled_rect(self.players[1].rect)
        Window.surface.blit(w, (player1_rect[0] - wtext_rect.width / 2, player1_rect[1] + player1_rect[3] / 2))
        Window.surface.blit(s, (player1_rect[0] - stext_rect.width / 2, player1_rect[1] - player1_rect[3] / 2 - stext_rect.height))

    def display(self):
        Window.surface.fill(self.color)
        Window.draw_rect((0.5, 0.5, 0.02, 1), self.bar_color)
        if (self.state == GameState.pregame):
            self.display_start_controls()

        # player1 score
        player1_score_surf = self.font.render(str(self.players[0].score), True, self.text_color)
        Window.surface.blit(player1_score_surf, (self.text_margin[0], self.text_margin[1]))

        # player2 score
        player2_score_surf = self.font.render(str(self.players[1].score), True, self.text_color)
        player2_score_surf_rect = player2_score_surf.get_rect()
        Window.surface.blit(player2_score_surf, (Window.size[0] - player2_score_surf_rect.width - self.text_margin[0], self.text_margin[1]))

        # player and ball
        for player in self.players:
            player.show()
        self.ball.show()

        Window.update_display()

    def physics_step(self):
        if (self.state == GameState.in_play):
            self.ball.update()
        else:
            self.ball.attach_to_player(self.players[self.next_start_player].rect, -(self.next_start_player * 2 - 1))
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                self.state = GameState.in_play

        for player in self.players:
            player.update()
            self.ball.bounce_off_player(player.rect)

        if not self.ball.is_in_bounds():
            if self.ball.position[0] < 0.5:
                self.players[1].score += 1
            else:
                self.players[0].score += 1
            self.reset()

    def run(self):
        while True:
            self.clock.tick(100)
            self.event_loop()
            self.physics_step()
            self.display()


if __name__ == "__main__":
    Game().run()
