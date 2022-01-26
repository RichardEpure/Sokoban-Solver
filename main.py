import sys
import pygame
import config
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

    pygame.init()
    pygame.display.set_caption('Sokoban')

    scn_main_menu = config.scene_list["Main Menu"]

    txt_title = Text("Sokoban")
    txt_title.set_centre_x(config.window.center_x())
    txt_title.set_origin_y(0)

    txt_test = Text("Test Text")
    txt_test.set_centre_x(config.window.center_x())
    txt_test.set_origin_y(100)

    btn_play_game = Button('button_green_1', Text("Play Game"))
    btn_play_game.set_centre(config.window.center_x(), config.window.height/2)

    btn_exit = Button('button_green_1', Text("Exit"))
    btn_exit.set_centre(config.window.center_x(), config.window.height/2 + btn_exit.rect.height + 30)

    def btn_exit_click_handler():
        pygame.quit()
        sys.exit()
    btn_exit.onclick_event_handler = btn_exit_click_handler

    scn_main_menu.add_components([btn_play_game, btn_exit, txt_title])

    config.current_scene = scn_main_menu

    # Event loop
    while True:
        config.current_scene.update()
        config.window.update()


if __name__ == '__main__':
    main()
