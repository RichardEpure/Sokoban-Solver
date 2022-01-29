import os
import pygame

import config


def load_png(name):
    """ Load image and return image object"""
    fullname = os.path.join(f'{config.path_images}', name)
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


def parse_level(path):
    level = []
    with open(path, 'r') as f:
        lines = f.readlines()

        for i in range(len(lines)):
            line = str.rstrip(lines[i])
            level.append([])
            for j in range(len(line)):
                if line[j] != ' ':
                    level[i].append([' ', line[j]])
                else:
                    level[i].append([line[j]])

    return level
