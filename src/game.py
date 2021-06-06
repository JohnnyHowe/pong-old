import pygame
from window import Window
from player import Player

def event_loop():
    events = pygame.event.get()
    for event in events:
        if (event.type == pygame.QUIT):
            quit()

def main():
    player1 = Player(pygame.K_w, pygame.K_s, 0.1)
    player2 = Player(pygame.K_o, pygame.K_l, 0.9)

    while True:
        Window.surface.fill((100, 100, 100))
        event_loop()
        player1.update()
        player2.update()
        Window.update_display()

if __name__ == "__main__":
    main()