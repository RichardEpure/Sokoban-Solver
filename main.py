import os
import pygame
from pygame.locals import *
from gui import *


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
    window = Window(1920, 1080)
    pygame.display.set_caption('Sokoban')

    # Display some text
    font = pygame.font.Font(None, 36)
    text = font.render("Sokoban", True, (255, 255, 255))
    textpos = text.get_rect()
    textpos.centerx = window.get_rect().centerx
    window.draw(text, textpos)

    buttons = []

    button = Button('button_green_1', 'Play Game')
    button.set_centre(window.center_x(), window.height/2)
    buttons.append(button)
    button.draw(window)

    button = Button('button_green_1', 'Exit')
    button.set_centre(window.center_x(), window.height/2 + button.rect.height + 30)
    buttons.append(button)
    button.draw(window)

    # Event loop
    # TODO: make rect for click and rect for size separate
    while True:
        window.background.fill((0,0,0))

        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()

        for event in pygame.event.get():
            if event.type == QUIT:
                return

            if event.type == pygame.MOUSEBUTTONUP:
                pass

            if event.type == pygame.MOUSEBUTTONDOWN:
                pass

        for button in buttons:
            button.handle_mouse_events(mouse_pos, mouse_pressed)
            button.draw(window)

        window.update()


if __name__ == '__main__':
    main()
