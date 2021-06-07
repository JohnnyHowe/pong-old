import pygame
from window import Window
from player import Player
from ball import Ball

def event_loop():
    events = pygame.event.get()
    for event in events:
        if (event.type == pygame.QUIT):
            quit()

def main():
    player1 = Player(pygame.K_w, pygame.K_s, 0.05)
    player2 = Player(pygame.K_o, pygame.K_l, 0.95)
    ball = Ball([player1.rect[0] + 0.05, player1.rect[1]])
    
    c = pygame.time.Clock()    

    while True:
        c.tick(100)
        event_loop()
        Window.surface.fill((100, 100, 100))
        player1.update()
        player2.update()
        ball.update()
        ball.bounce_off_player(player1.rect)
        ball.bounce_off_player(player2.rect)
        Window.update_display()

if __name__ == "__main__":
    main()