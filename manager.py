import sys
import pygame
from pygame.locals import *
from gui import *


class Scene:
    event_data = {}

    def __init__(self, window, components=None):
        self.components = components if components else []
        self.window = window

    def update(self):
        for event in Scene.event_data['events']:
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONUP:
                for component in self.components:
                    if isinstance(component, Button) and component.is_mouse_over(Scene.event_data['mouse_pos']):
                        component.handle_click_event()

        for component in self.components:
            if isinstance(component, Button):
                component.handle_mouse_events(Scene.event_data['mouse_pos'], Scene.event_data['mouse_pressed'])
            component.draw(self.window)

    def add_components(self, components):
        try:
            self.components.extend(components)
        except TypeError:
            self.components.append(components)

    def remove_component(self, component):
        self.components.remove(component)


__all__ = ["Scene"]