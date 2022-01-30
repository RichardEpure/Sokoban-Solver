import pygame

pygame.init()

tile_size = (64, 64)

path_style = 'resources/style.json'
path_levels = 'resources/levels'
path_images = 'resources/images'

if True:  # noqa: E402
    from gui import Window

start_width = 3840
start_height = 2160
window = Window(start_width, start_height)

if True:  # noqa: E402
    from manager import Scene

current_scene = Scene()
scene_list = {
    "Main Menu": Scene(),
    "Level Select": Scene(),
    "Game": Scene(),
    "Test Menu": Scene()
}
