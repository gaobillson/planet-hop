"""
SPDX-FileCopyrightText: 2024, Jason Treakle, thetreakle@gmail.com
SPDX-License-Identifier: GPL-3.0-or-later

See main.py for the full GPL-3.0 license header.
See LICENSE.txt for full GPL-3.0 license information.
See LICENSES directory for licensing of other works included in this project.
"""

import pygame


class Sun:
    def __init__(self, image, mass, game):
        self.name = 'sun'
        self.image = image
        self.radius = (image['img'].get_width() - 6) / 2  # Subtracting because 3 pixel empty space on all object images
        self.mass = mass
        self.game = game
        self.x = game.screen.get_width() / 2 - image['img'].get_width() / 2
        self.y = game.screen.get_height() / 2 - image['img'].get_height() / 2
        self.rect = pygame.Rect(self.x, self.y, self.image['img'].get_width(), self.image['img'].get_height())

    def render(self):
        self.game.screen.blit(source=self.image['img'], dest=(self.x, self.y))
