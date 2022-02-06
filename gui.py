import pygame
import pygame_gui
from pygame_gui.core import ObjectID, UIElement, IContainerLikeInterface
from pygame_gui.core.interfaces import IUIManagerInterface
from typing import Union, Dict, Iterable
from abc import ABC

import config
from helper import load_png


class Window:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.x_scaling = 1
        self.y_scaling = 1
        self.window = None
        self.background = None

    def init(self):
        self.window = pygame.display.set_mode((self.width, self.height))
        display_info = pygame.display.Info()
        self.window = pygame.display.set_mode((display_info.current_w, display_info.current_h))
        pygame.display.toggle_fullscreen()
        self.background = pygame.Surface(self.window.get_size())
        self.background = self.background.convert()
        self.background.fill((0, 0, 0))

    def update(self, ui_manager):
        self.window.blit(self.background, (0, 0))
        ui_manager.draw_ui(self.window)
        pygame.display.flip()
        self.background.fill((0, 0, 0))

    def draw(self, item, item_rect=None):
        if item_rect:
            self.background.blit(item, item_rect)
        else:
            self.background.blit(item, item.get_rect())

    def resize(self, width, height):
        self.width = width
        self.height = height
        self.x_scaling = self.width / config.start_width
        self.y_scaling = self.height / config.start_height
        self.background = pygame.transform.scale(self.background, (width, height))

    def get_rect(self):
        return self.background.get_rect()

    def center_x(self):
        return self.background.get_rect().centerx

    def center_y(self):
        return self.background.get_rect().centery


class GButton(pygame_gui.elements.UIButton):
    def __init__(self, relative_rect: pygame.Rect,
                 text: str,
                 manager: IUIManagerInterface,
                 container: Union[IContainerLikeInterface, None] = None,
                 tool_tip_text: Union[str, None] = None,
                 starting_height: int = 1,
                 parent_element: UIElement = None,
                 object_id: Union[ObjectID, str, None] = None,
                 anchors: Dict[str, str] = None,
                 allow_double_clicks: bool = False,
                 generate_click_events_from: Iterable[int] = frozenset([pygame.BUTTON_LEFT]),
                 visible: int = 1
                 ):
        super().__init__(relative_rect, text, manager, container, tool_tip_text, starting_height,
                         parent_element, object_id, anchors, allow_double_clicks, generate_click_events_from, visible)

        def on_btn_down():
            pass

        self.on_btn_down = on_btn_down

        def on_click():
            pass

        self.on_click = on_click

    def process_event(self, event: pygame.event.Event) -> bool:
        if event.type == pygame_gui.UI_BUTTON_START_PRESS and event.ui_element == self:
            self.on_btn_down()
        if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == self:
            self.on_click()

        return super().process_event(event)


class GFileDialog(pygame_gui.windows.UIFileDialog):
    def __init__(self,
                 rect: pygame.Rect,
                 manager: IUIManagerInterface,
                 window_title: str = 'pygame-gui.file_dialog_title_bar',
                 initial_file_path: Union[str, None] = None,
                 object_id: Union[ObjectID, str] = ObjectID('#file_dialog', None),
                 allow_existing_files_only: bool = False,
                 allow_picking_directories: bool = False,
                 visible: int = 1
                 ):
        super().__init__(rect, manager, window_title, initial_file_path, object_id, allow_existing_files_only,
                         allow_picking_directories, visible)

        def on_file_select(path):
            pass
        self.on_file_select = on_file_select

        def on_window_close():
            pass
        self.on_window_close = on_window_close

    def process_event(self, event: pygame.event.Event) -> bool:
        if event.type == pygame_gui.UI_FILE_DIALOG_PATH_PICKED and event.ui_element == self:
            self.on_file_select(event.text)

        return super().process_event(event)

    def on_close_window_button_pressed(self):
        self.on_window_close()

    def kill(self):
        pass


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
        rect = self.rect.copy()
        render = self.render.copy()
        rect.x *= config.window.x_scaling
        rect.y *= config.window.y_scaling
        width = rect.width * config.window.x_scaling
        height = rect.height * config.window.y_scaling
        render = pygame.transform.smoothscale(render, (width, height))
        if isinstance(context, Window):
            context.background.blit(render, rect)
        else:
            context.blit(render, rect)

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
    def __init__(self, path, txt_component, size=(400, 100)):
        super().__init__()

        image = load_png(f'{path}.png')
        image_hover = load_png(f'{path}--hover.png')
        image_active = load_png(f'{path}--active.png')

        image = pygame.transform.scale(image, size)
        image_hover = pygame.transform.scale(image_hover, size)
        image_active = pygame.transform.scale(image_active, (size[0], (size[1] / 8) * 7))
        image_rect = image.get_rect()

        txt_component.set_centre(image_rect.centerx, image_rect.centery * 0.8)
        txt_component.draw(image)
        txt_component.draw(image_hover)
        txt_component.draw(image_active)
        self.text = txt_component

        self.is_active = False
        self.is_hover = False

        self.image = image
        self.image_hover = image_hover
        self.image_active = image_active

        self.render = self.image
        self.rect = image_rect
        self.normal_rect = self.rect.copy()
        self.active_rect = image_active.get_rect()

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


class Tile(GuiComponent):
    def __init__(self, path, size=config.tile_size):
        super().__init__()

        image = load_png(f'{path}.png')
        image = pygame.transform.scale(image, size)
        image_rect = image.get_rect()

        self.image = image
        self.render = image
        self.rect = image_rect


class Box(Tile):
    def __init__(self, box_texture, docked_texture, size=config.tile_size):
        super().__init__(box_texture, size)

        image_docked = load_png(f'{docked_texture}.png')
        image_docked = pygame.transform.scale(image_docked, size)

        self.image_docked = image_docked
        self.is_docked = False

    def draw(self, context):
        if self.is_docked:
            self.render = self.image_docked
        else:
            self.render = self.image

        super().draw(context)

    def docked(self):
        self.is_docked = True

    def undocked(self):
        self.is_docked = False


class GridContainer(GuiComponent):
    def __init__(self, size, components=None):
        super().__init__()
        self.components = components if components is not None else [[]]
        self.background = pygame.Surface(size)
        self.background.convert()
        self.background.fill((100, 100, 100))
        self.rect = self.background.get_rect()
        self.render = self.background

    def update(self):
        self.background.fill((100, 100, 100))
        for i in range(len(self.components)):
            for j in range(len(self.components[i])):
                for component in self.components[i][j]:
                    component.draw(self.background)

    def set_components(self, components):
        self.components = components

    def update_component(self, i, j, component):
        self.components[i][j] = component


__all__ = ["Window", "GuiComponent", "Clickable", "Button", "Text", "GButton", "GFileDialog", "Tile", "Box", "GridContainer"]
