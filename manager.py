import sys
import pygame
from pygame.locals import *
from gui import *


class Scene:
    def __init__(self, window, components=None):
        self.components = components if components else []
        self.window = window

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()
        events = pygame.event.get()

        for event in events:
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONUP:
                for component in self.components:
                    if isinstance(component, Button) and component.is_mouse_over(mouse_pos):
                        component.handle_click_event()

        for component in self.components:
            if isinstance(component, Button):
                component.handle_mouse_events(mouse_pos, mouse_pressed)
            component.draw(self.window)

    def add_components(self, components):
        try:
            self.components.extend(components)
        except TypeError:
            self.components.append(components)

    def remove_component(self, component):
        self.components.remove(component)


__all__ = ["Scene"]