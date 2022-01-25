import os
import pygame
from pygame.locals import *


def load_png(name):
    """ Load image and return image object"""
    fullname = os.path.join('resources\images', name)
    try:
        image = pygame.image.load(fullname)
        if image.get_alpha() is None:
            image = image.convert()
        else:
            image = image.convert_alpha()
    except pygame.error as message:
        print('Cannot load image:', fullname)
        raise SystemExit(message)
    return image