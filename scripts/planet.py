"""
SPDX-FileCopyrightText: 2024, Jason Treakle, thetreakle@gmail.com
SPDX-License-Identifier: GPL-3.0-or-later

See main.py for the full GPL-3.0 license header.
See LICENSE.txt for full GPL-3.0 license information.
See LICENSES directory for licensing of other works included in this project.
"""

import math

import pygame


class Planet:
    def __init__(self, name, angle, mass, image, orbit_radius, orbit_rate, game):
        self.radius = (image['img'].get_width() - 6) / 2  # Subtracting because 3 pixel empty space on all object images
        self.mass = mass
        self.x = 0
        self.y = 0
        self.velocity = [0, 0]
        self.angle = angle  # radians, relative to the Sun
        self.orbit_radius = orbit_radius
        self.orbit_rate = orbit_rate
        self.name = name
        self.image = image
        self.image['img'].set_colorkey((0, 0, 0))
        self.rect = pygame.Rect(self.x, self.y, self.image['img'].get_width(), self.image['img'].get_height())
        self.frame = 1
        self.pos1 = (0, 0)
        self.pos2 = (0, 0)
        self.times_run_velocity_func = 0
        self.game = game

    def update(self):
        self.angle += self.orbit_rate * self.game.dt * self.game.target_FPS
        self.get_velocity()
        if self.angle >= math.pi * 2:
            self.angle = 0
        self.x = (math.cos(self.angle) * self.orbit_radius + self.game.screen.get_width() / 2 -
                  self.image['img'].get_width() / 2)
        self.y = (math.sin(self.angle) * self.orbit_radius + self.game.screen.get_height() / 2 -
                  self.image['img'].get_height() / 2)
        self.rect = pygame.Rect(self.x, self.y, self.image['img'].get_width(), self.image['img'].get_height())

    def get_velocity(self):
        if self.frame == 1:
            self.pos1 = (self.x, self.y)
            if self.times_run_velocity_func >= 1:
                self.velocity = ((self.pos1[0] - self.pos2[0]) / self.game.dt,
                                 (self.pos1[1] - self.pos2[1]) / self.game.dt)
            self.frame += 1
        elif self.frame == 2:
            self.pos2 = (self.x, self.y)
            if self.times_run_velocity_func >= 1:
                self.velocity = ((self.pos2[0] - self.pos1[0]) / self.game.dt,
                                 (self.pos2[1] - self.pos1[1]) / self.game.dt)
            self.frame -= 1

        self.times_run_velocity_func += 1

    def render(self):
        self.game.screen.blit(source=self.image['img'], dest=(self.x, self.y))
