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
        self.level_gui = None

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

            if event.type == pygame.KEYDOWN and self.game_manager is not None:
                has_moved = False
                if event.key == pygame.K_UP:
                    has_moved = self.game_manager.move(Direction.NORTH)
                elif event.key == pygame.K_RIGHT:
                    has_moved = self.game_manager.move(Direction.EAST)
                elif event.key == pygame.K_DOWN:
                    has_moved = self.game_manager.move(Direction.SOUTH)
                elif event.key == pygame.K_LEFT:
                    has_moved = self.game_manager.move(Direction.WEST)

                if has_moved:
                    self.__update_level_gui()

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
        self.level_gui = GridContainer((len(level[0]) * config.tile_size[1], len(level) * config.tile_size[0]))
        self.level_gui.set_centre(config.window.center_x(), config.window.center_y())
        self.__update_level_gui()
        self.add_components(self.level_gui)

    def __update_level_gui(self):
        level = self.game_manager.level
        components = []
        for i in range(len(level)):
            components.append([])
            for j in range(len(level[i])):
                entities = level[i][j]
                entities_to_add = []

                if Entity.FLOOR in entities:
                    entity = Tile('floor')
                    entities_to_add.append(entity)

                if Entity.DOCK in entities:
                    entity = Tile('dock')
                    entities_to_add.append(entity)

                if Entity.BOX in entities:
                    entity = Box('box', 'box--docked')
                    if Entity.DOCK in entities:
                        entity.docked()
                    entities_to_add.append(entity)

                if Entity.WALL in entities:
                    entity = Tile('wall')
                    entities_to_add.append(entity)

                if Entity.PLAYER in entities:
                    entity = Tile('player')
                    entities_to_add.append(entity)

                for entity in entities_to_add:
                    entity.set_origin(j * entity.rect.width, i * entity.rect.height)

                components[i].append(entities_to_add)

        self.level_gui.set_components(components)
        self.level_gui.update()

    def add_components(self, components):
        try:
            self.components.extend(components)
        except TypeError:
            self.components.append(components)

    def remove_component(self, component):
        self.components.remove(component)


__all__ = ["Scene"]
