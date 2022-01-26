import sys
import pygame
from gui import *
from manager import *


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

    main_menu = Scene(window)

    # Display some text
    txt_title = Text("Sokoban")
    txt_title.set_centre_x(window.center_x())
    txt_title.set_origin_y(0)

    btn_play_game = Button('button_green_1', 'Play Game')
    btn_play_game.set_centre(window.center_x(), window.height/2)

    btn_exit = Button('button_green_1', 'Exit')
    btn_exit.set_centre(window.center_x(), window.height/2 + btn_exit.rect.height + 30)

    def btn_exit_click_handler():
        pygame.quit()
        sys.exit()
    btn_exit.onclick_event_handler = btn_exit_click_handler

    main_menu.add_components([btn_play_game, btn_exit, txt_title])

    # Event loop
    while True:
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()
        events = pygame.event.get()
        Scene.event_data.update({
            'mouse_pos': mouse_pos,
            'mouse_pressed': mouse_pressed,
            'events': events
        })
        main_menu.update()
        window.update()


if __name__ == '__main__':
    main()
