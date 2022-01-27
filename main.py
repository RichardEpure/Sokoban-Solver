import sys
import pygame
import pygame_gui
import config
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

    setup_main_menu()
    setup_level_select()

    config.current_scene = config.scene_list["Main Menu"]

    clock = pygame.time.Clock()
    while True:
        time_delta = clock.tick(60) / 1000.0
        config.current_scene.update(time_delta)


def setup_level_select():
    scn_level_select = config.scene_list["Level Select"]

    hello_button = GButton(relative_rect=pygame.Rect(30, 20, 200, 60),
                           text='Say Hello',
                           manager=scn_level_select.ui_manager)

    def on_btn_down():
        print("btn_down")
    hello_button.on_btn_down = on_btn_down

    def on_click():
        print("click")
    hello_button.on_click = on_click


def setup_main_menu():
    scn_main_menu = config.scene_list["Main Menu"]

    txt_title = Text("Sokoban")
    txt_title.set_centre_x(config.window.center_x())
    txt_title.set_origin_y(0)

    txt_test = Text("Test Text")
    txt_test.set_centre_x(config.window.center_x())
    txt_test.set_origin_y(100)

    btn_play_game = Button('button_green_1', Text("Play Game"))
    btn_play_game.set_centre(config.window.center_x(), config.window.height / 2)

    def btn_play_game_click_handler():
        config.current_scene = config.scene_list["Level Select"]

    btn_play_game.onclick_event_handler = btn_play_game_click_handler

    btn_exit = Button('button_green_1', Text("Exit"))
    btn_exit.set_centre(config.window.center_x(), config.window.height / 2 + btn_exit.rect.height + 30)

    def btn_exit_click_handler():
        pygame.quit()
        sys.exit()

    btn_exit.onclick_event_handler = btn_exit_click_handler

    scn_main_menu.add_components([btn_play_game, btn_exit, txt_title])


if __name__ == '__main__':
    main()
