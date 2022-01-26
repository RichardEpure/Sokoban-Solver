import pygame
from helper import load_png
from abc import ABC


class Window:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.window = pygame.display.set_mode((width, height))
        self.background = pygame.Surface(self.window.get_size())
        self.background = self.background.convert()
        self.background.fill((0, 0, 0))

    def update(self):
        self.window.blit(self.background, (0, 0))
        pygame.display.flip()
        self.background.fill((0, 0, 0))

    def draw(self, item, item_rect=None):
        if item_rect:
            self.background.blit(item, item_rect)
        else:
            self.background.blit(item, item.get_rect())

    def get_rect(self):
        return self.background.get_rect()

    def center_x(self):
        return self.background.get_rect().centerx

    def center_y(self):
        return self.background.get_rect().centery


class GuiComponent(ABC):
    def __init__(self):
        super().__init__()
        self.render = None
        self.rect = None
        self.center_x = self.center_y = self.x = self.y = 0

    def _update_rects_centre(self):
        self.rect.centerx = self.center_x
        self.rect.centery = self.center_y
        self.x = self.rect.x
        self.y = self.rect.y

    def _update_rects_origin(self):
        self.rect.x = self.x
        self.rect.y = self.y
        self.center_x = self.rect.centerx
        self.center_y = self.rect.centery

    def draw(self, context):
        if isinstance(context, Window):
            context.background.blit(self.render, self.rect)
        else:
            context.blit(self.render, self.rect)

    def set_centre(self, x, y):
        self.center_x = x
        self.center_y = y
        self._update_rects_centre()

    def set_centre_x(self, x):
        self.center_x = x
        self._update_rects_centre()

    def set_centre_y(self, y):
        self.center_y = y
        self._update_rects_centre()

    def set_origin(self, x, y):
        self.x = x
        self.y = y
        self._update_rects_origin()

    def set_origin_x(self, x):
        self.x = x
        self._update_rects_origin()

    def set_origin_y(self, y):
        self.y = y
        self._update_rects_origin()


class Clickable(ABC):
    def __init__(self):
        super().__init__()

        def onclick():
            pass
        self.onclick_event_handler = onclick

    def handle_click_event(self):
        self.onclick_event_handler()


class Button(GuiComponent, Clickable):
    def __init__(self, path, text_content="", size=(400, 100), font_size=36, font_colour=(255, 255, 255)):
        super().__init__()

        image = load_png(f'{path}.png')
        image_hover = load_png(f'{path}--hover.png')
        image_active = load_png(f'{path}--active.png')

        image = pygame.transform.scale(image, size)
        image_hover = pygame.transform.scale(image_hover, size)
        image_active = pygame.transform.scale(image_active, (size[0], (size[1]/8)*7))
        image_rect = image.get_rect()

        font = pygame.font.Font(None, font_size)
        text = font.render(text_content, True, font_colour)
        text_rect = text.get_rect()
        text_rect.centerx = image_rect.centerx
        text_rect.centery = image_rect.centery * 0.8

        image.blit(text, text_rect)
        image_hover.blit(text, text_rect)
        image_active.blit(text, text_rect)

        self.is_active = False
        self.is_hover = False

        self.image = image
        self.image_hover = image_hover
        self.image_active = image_active

        self.render = self.image
        self.rect = image_rect
        self.normal_rect = self.rect.copy()
        self.active_rect = image_active.get_rect()

        self.font = font
        self.text = text_content

    def _update_rects_centre(self):
        super()._update_rects_centre()
        self.normal_rect.centerx = self.center_x
        self.normal_rect.centery = self.center_y

        y_offset = (self.normal_rect.height - self.active_rect.height) / 2
        self.active_rect.centerx = self.center_x
        self.active_rect.centery = self.center_y + y_offset
        
    def _update_rects_origin(self):
        super()._update_rects_origin()
        self.normal_rect.x = self.x
        self.normal_rect.y = self.y

        y_offset = self.normal_rect.height - self.active_rect.height
        self.active_rect.x = self.x
        self.active_rect.y = self.y + y_offset

    def draw(self, context):
        self.rect = self.normal_rect

        if self.is_active:
            self.render = self.image_active
            self.rect = self.active_rect
        elif self.is_hover:
            self.render = self.image_hover
        else:
            self.render = self.image

        super().draw(context)

    def handle_mouse_events(self, mouse_pos, mouse_pressed):
        left, middle, right = mouse_pressed

        if self.is_mouse_over(mouse_pos):
            self.active() if left else self.hover()
        else:
            self.unfocused()

    def is_mouse_over(self, mouse_pos):
        return self.normal_rect.collidepoint(mouse_pos)

    def active(self):
        self.is_active = True
        self.is_hover = False

    def hover(self):
        self.is_hover = True
        self.is_active = False

    def unfocused(self):
        self.is_active = False
        self.is_hover = False


class Text(GuiComponent):
    def __init__(self, text_content="", font_size=36, font_colour=(255, 255, 255)):
        super().__init__()
        font = pygame.font.Font(None, font_size)
        text = font.render(text_content, True, font_colour)
        self.rect = text.get_rect()
        self.render = text


__all__ = ["Window", "GuiComponent", "Clickable", "Button", "Text"]