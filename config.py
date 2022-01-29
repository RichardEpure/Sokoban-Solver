import pygame
from gui import Window

pygame.init()

start_width = 3840
start_height = 2160
window = Window(start_width, start_height)

path_style = 'resources/style.json'

if True:  # noqa: E402
    from manager import Scene

current_scene = Scene()
scene_list = {
    "Main Menu": Scene(),
    "Level Select": Scene(),
    "Test Menu": Scene()
}
