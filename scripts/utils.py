"""
SPDX-FileCopyrightText: 2024, Jason Treakle, thetreakle@gmail.com
SPDX-License-Identifier: GPL-3.0-or-later

See main.py for the full GPL-3.0 license header.
See LICENSE.txt for full GPL-3.0 license information.
See LICENSES directory for licensing of other works included in this project.
"""

import os

import pygame

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


def resize_image(image, size):
    return pygame.transform.scale(surface=image, size=size)


def make_states_false(an_object):
    for state in an_object.state:
        an_object.state[state] = False


def meters_to_pixels(meters, scale):
    return meters / scale


def pixels_to_meters(pixels, scale):
    return pixels * scale
