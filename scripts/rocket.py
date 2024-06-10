import pygame

import math

from scripts.utils import radians_degrees as rad_deg


class Rocket:
    def __init__(self, mass, images, base_planet, game):
        self.mass = mass
        self.images = images
        self.image = images[0]
        for image in self.images:
            image['img'].set_colorkey((255, 255, 255))
        self.base_planet = base_planet
        self.angle = math.pi * 1.5
        self.x = 0
        self.y = 0
        self.velocity = [0, 0]
        self.rect = pygame.Rect(self.x, self.y, self.image['img'].get_width(), self.image['img'].get_height())
        self.movement = [False, False]
        self.state = {'positioning': True, 'flying': False}
        self.game = game

    def update(self):
        if self.state['positioning']:
            if self.movement[0]:
                self.angle += 0.05
            elif self.movement[1]:
                self.angle -= 0.05

            if self.angle >= math.pi * 2:
                self.angle = 0
            elif self.angle <= 0:
                self.angle = math.pi * 2

            self.update_image()

            self.rect = pygame.Rect(self.x, self.y, self.image['img'].get_width(), self.image['img'].get_height())

            # Uncomment if you want continuous movement
            # self.x = ((math.cos(self.angle) * (self.base_planet.image['img'].get_width() / 2 + 3) +
            #           self.base_planet.image['img'].get_width() / 2 - self.image['img'].get_width() / 2) +
            #           self.base_planet.rect.x)
            # self.y = ((math.sin(self.angle) * (self.base_planet.image['img'].get_height() / 2 + 3) +
            #           self.base_planet.image['img'].get_height() / 2 - self.image['img'].get_height() / 2) +
            #           self.base_planet.rect.y)

        elif self.state['flying']:
            for planet in self.game.planets:
                dx = planet.rect.centerx - self.rect.centerx
                dy = planet.rect.centery - self.rect.centery
                angle = math.atan2(dy, dx)  # Calculate angle between planets
                d = math.sqrt((dx ** 2) + (dy ** 2))  # Calculate distance
                if d == 0:
                    d = 0.000001  # Prevent division by zero error
                f = planet.gravity * self.mass * planet.mass / (d ** 2)  # Calculate gravitational force

                self.velocity[0] += (math.cos(angle) * f) / self.mass
                self.velocity[1] += (math.sin(angle) * f) / self.mass

    def update_image(self):
        angles = (17, 19, 21, 23, 1, 3, 5, 7, 9, 11, 13, 15)
        if self.state['positioning']:
            for i, val in enumerate(angles):
                if i != 4:
                    if (math.pi / 12) * angles[i - 1] <= self.angle < (math.pi / 12) * val:
                        self.image = self.images[i - 1]
                        # Remove the below if you want continuous movement
                        self.x = ((math.cos((math.pi / 12) * (angles[i] - 1)) * (self.base_planet.image['img'].get_width() / 2 + 3) +
                                   self.base_planet.image['img'].get_width() / 2 - self.image['img'].get_width() / 2) +
                                  self.base_planet.rect.x)
                        self.y = ((math.sin((math.pi / 12) * (angles[i] - 1)) * (self.base_planet.image['img'].get_height() / 2 + 3) +
                                   self.base_planet.image['img'].get_height() / 2 - self.image['img'].get_height() / 2) +
                                  self.base_planet.rect.y)
                        break
                else:
                    if (math.pi / 12) * 23 <= self.angle < math.pi * 2 or 0 <= self.angle < math.pi / 12:
                        self.image = self.images[3]
                        # Remove the below if you want continuous movement
                        self.x = ((math.cos(0) * (self.base_planet.image['img'].get_width() / 2 + 3) +
                                   self.base_planet.image['img'].get_width() / 2 - self.image['img'].get_width() / 2) +
                                  self.base_planet.rect.x)
                        self.y = ((math.sin(0) * (self.base_planet.image['img'].get_height() / 2 + 3) +
                                   self.base_planet.image['img'].get_height() / 2 - self.image['img'].get_height() / 2) +
                                  self.base_planet.rect.y)
                        break
        elif self.state['flying']:
            pass

    def launch(self):
        pass

    def render(self):
        self.game.screen.blit(source=self.image['img'], dest=(self.x, self.y))
