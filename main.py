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

    select_rect = pygame.Rect((0, 0), (800, 800))
    select_rect.centerx = config.window.center_x()
    select_rect.centery = config.window.center_y()
    select = GFileDialog(rect=select_rect,
                         manager=scn_level_select.ui_manager,
                         window_title="Select a level",
                         initial_file_path=config.path_levels)

    def on_file_select(path):
        print(f"file selected: {path}")
    select.on_file_select = on_file_select

    def on_window_close():
        config.current_scene = config.scene_list["Main Menu"]
    select.on_window_close = on_window_close


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
