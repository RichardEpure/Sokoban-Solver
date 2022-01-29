import sys
import pygame
import pygame_gui
import config
from pygame.locals import *
from gui import *
from sokoban import *
from helper import parse_level


class Scene:
    window = config.window

    def __init__(self, components=None):
        self.components = components if components else []
        self.ui_manager = pygame_gui.UIManager((config.start_width, config.start_height), config.path_style)
        self.game_manager = None

    def update(self, time_delta):
        mouse_pos = pygame.mouse.get_pos()
        mouse_pos = (mouse_pos[0] / self.window.x_scaling, mouse_pos[1] / self.window.y_scaling)

        mouse_pressed = pygame.mouse.get_pressed()
        events = pygame.event.get()

        for event in events:
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.VIDEORESIZE:
                self.window.resize(event.w, event.h)

            if event.type == pygame.MOUSEBUTTONUP:
                for component in self.components:
                    if isinstance(component, Button) and component.is_mouse_over(mouse_pos):
                        component.handle_click_event()

            self.ui_manager.process_events(event)

        for component in self.components:
            if isinstance(component, Button):
                component.handle_mouse_events(mouse_pos, mouse_pressed)
            component.draw(self.window)

        self.ui_manager.update(time_delta)
        self.window.update(self.ui_manager)

    def initialise_game(self, path):
        self.game_manager = GameManager(parse_level(path))
        level = self.game_manager.level
        for i in range(len(level)):
            for j in range(len(level[i])):
                entities = level[i][j]
                entities_to_add = []

                if Entity.FLOOR in entities or not entities:
                    floor = Tile('floor')
                    entities_to_add.append(floor)

                if Entity.DOCK in entities:
                    dock = Tile('dock')
                    entities_to_add.append(dock)

                if Entity.BOX in entities:
                    box = Box('box', 'box--docked')
                    entities_to_add.append(box)

                if Entity.WALL in entities:
                    wall = Tile('wall')
                    entities_to_add.append(wall)

                if Entity.PLAYER in entities:
                    player = Tile('player')
                    entities_to_add.append(player)

                for entity in entities_to_add:
                    entity.set_origin(j * entity.rect.width, i * entity.rect.height)

                self.add_components(entities_to_add)

    def add_components(self, components):
        try:
            self.components.extend(components)
        except TypeError:
            self.components.append(components)

    def remove_component(self, component):
        self.components.remove(component)


__all__ = ["Scene"]
