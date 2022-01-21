import pygame
from pygame.locals import *


def main():
    level = []
    with open('resources/levels/xsokoban/xsokoban_1.txt', 'r') as f:
        lines = f.readlines()

        for i in range(0, len(lines)):
            line = str.rstrip(lines[i])
            level.append([])
            for j in range(0, len(line)):
                level[i].append(line[j])

            print(level[i])

    # Initialise screen
    pygame.init()
    screen = pygame.display.set_mode((1920, 1080))
    pygame.display.set_caption('Pygame Program')

    # Fill background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 0, 0))

    # Display some text
    font = pygame.font.Font(None, 36)
    text = font.render("Hello There", 1, (180, 180, 180))
    textpos = text.get_rect()
    textpos.centerx = background.get_rect().centerx
    background.blit(text, textpos)

    # Blit everything to the screen
    screen.blit(background, (0, 0))
    pygame.display.flip()

    # Event loop
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                return

        screen.blit(background, (0, 0))
        pygame.display.flip()


if __name__ == '__main__':
    main()
