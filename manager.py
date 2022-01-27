import sys
import pygame
import pygame_gui
import config
from pygame.locals import *
from gui import *


class Scene:
    window = config.window

    def __init__(self, components=None):
        self.components = components if components else []
        self.ui_manager = pygame_gui.UIManager((config.start_width, config.start_height), config.path_style)

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

    def add_components(self, components):
        try:
            self.components.extend(components)
        except TypeError:
            self.components.append(components)

    def remove_component(self, component):
        self.components.remove(component)


__all__ = ["Scene"]
