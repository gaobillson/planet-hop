import os

import pygame

import math

BASE_IMG_PATH = 'data/images/'


def load_image(path, convert):
    if convert == 'convert()':
        img = pygame.image.load(BASE_IMG_PATH + path).convert()
    elif convert == 'convert_alpha()':
        img = pygame.image.load(BASE_IMG_PATH + path).convert_alpha()
    else:
        img = pygame.image.load(BASE_IMG_PATH + path).convert()
    return {'path': path, 'img': img}


def load_images(path, convert):
    images = []
    if convert == 'convert()':
        for img_name in sorted(os.listdir(BASE_IMG_PATH + path)):
            images.append(load_image(path + '/' + img_name, 'convert()'))
    if convert == 'convert_alpha()':
        for img_name in sorted(os.listdir(BASE_IMG_PATH + path)):
            images.append(load_image(path + '/' + img_name, 'convert_alpha()'))
    else:
        for img_name in sorted(os.listdir(BASE_IMG_PATH + path)):
            images.append(load_image(path + '/' + img_name, 'convert()'))
    return images


def radians_degrees(angle):
    return angle * (180 / math.pi)
