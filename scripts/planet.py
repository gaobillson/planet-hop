import math

import pygame


class Planet:
    def __init__(self, name, angle, gravity, mass, image, orbit_radius, orbit_rate, game):
        self.radius = (image['img'].get_width() - 6) / 2  # Subtracting because 3 pixel empty space on all object images
        self.gravity = gravity
        self.mass = mass
        self.velocity = (0, 0)
        self.x = 0
        self.y = 0
        self.angle = angle  # radians
        self.orbit_radius = orbit_radius
        self.orbit_rate = orbit_rate
        self.name = name
        self.image = image
        self.image['img'].set_colorkey((255, 255, 255))
        self.rect = pygame.Rect(self.x, self.y, self.image['img'].get_width(), self.image['img'].get_height())
        self.game = game

    def update(self):
        self.angle += self.orbit_rate
        if self.angle >= math.pi * 2:
            self.angle = 0
        self.x = (math.cos(self.angle) * self.orbit_radius + self.game.screen.get_width() / 2 -
                  self.image['img'].get_width() / 2)
        self.y = (math.sin(self.angle) * self.orbit_radius + self.game.screen.get_height() / 2 -
                  self.image['img'].get_height() / 2)
        self.rect = pygame.Rect(self.x, self.y, self.image['img'].get_width(), self.image['img'].get_height())

    def render(self):
        self.game.screen.blit(source=self.image['img'], dest=(self.x, self.y))
