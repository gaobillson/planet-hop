"""
SPDX-FileCopyrightText: 2024, Jason Treakle, thetreakle@gmail.com
SPDX-License-Identifier: GPL-3.0-or-later

Calculating gravitational forces, under elif self.state['flying'], copyright (C) 2020 user 000Nobody on GitHub
https://github.com/000Nobody/Orbit-Simulator

See main.py for the full GPL-3.0 license header.
See LICENSE.txt for full GPL-3.0 license information.
See LICENSES directory for licensing of other works included in this project.
"""

import pygame

import math

from scripts.utils import meters_to_pixels as met_pix, pixels_to_meters as pix_met
from scripts.collision_evaluation import collision

# Universal gravitational constant
G = 6.67408 * 10 ** -11

SCALE = 750000000


class Rocket:
    def __init__(self, mass, rest_images, fly_images, explode_image, base_planet, target_planet, game):
        self.mass = mass
        self.rest_images = rest_images
        self.fly_images = fly_images
        self.explode_image = explode_image
        for rest_image, fly_image in zip(self.rest_images, self.fly_images):
            rest_image['img'].set_colorkey((255, 255, 255))
            fly_image['img'].set_colorkey((255, 255, 255))
        self.explode_image['img'].set_colorkey((255, 255, 255))
        self.image = rest_images[0]
        self.base_planet = base_planet
        self.target_planet = target_planet
        self.current_planet = self.base_planet
        self.angle = math.pi * 1.5
        self.x = 0
        self.y = 0
        self.velocity = [0, 0]
        self.initial_velocity = [0, 0]
        self.planet_velocity = [0, 0]
        self.raw_velocity = [0, 0]
        self.fuel = 0
        self.target_pos = (0, 0)
        self.target_angle = 0
        self.frame = 1
        self.times_run_velocity_func = 0
        self.pos1 = (0, 0)
        self.pos2 = (0, 0)
        self.rect = pygame.Rect(self.x, self.y, self.image['img'].get_width(), self.image['img'].get_height())
        self.movement = [False, False]
        self.state = {'left_base_planet': False, 'positioning': True, 'setting_trajectory': False, 'flying': False,
                      'landing': False, 'crashing': False}
        self.game = game

    def update(self):
        if self.state['setting_trajectory']:
            self.target_pos = self.game.mouse_pos[0], self.game.mouse_pos[1]
            dx = self.target_pos[0] - self.rect.centerx
            dy = self.target_pos[1] - self.rect.centery
            self.target_angle = math.atan2(dy, dx)
            self.initial_velocity = [met_pix(500000000, SCALE) * math.cos(self.target_angle),
                                     met_pix(500000000, SCALE) * math.sin(self.target_angle)]
            self.velocity = self.initial_velocity
            self.state['setting_trajectory'] = False
            self.state['flying'] = True

        if self.state['positioning']:
            if self.movement[0]:
                self.angle += 0.05 * self.game.dt * self.game.target_FPS
            elif self.movement[1]:
                self.angle -= 0.05 * self.game.dt * self.game.target_FPS

            if self.angle >= math.pi * 2:
                self.angle = 0
            elif self.angle <= 0:
                self.angle = math.pi * 2

            self.update_image()

        elif self.state['flying']:

            # Calculating gravitational force copyright (C) 2020 000Nobody on GitHub
            # Attributed portions marked with Start and End
            for planet in self.game.planets.values():
                # Start
                dx = pix_met(planet.rect.centerx - self.rect.centerx, SCALE)
                dy = pix_met(planet.rect.centery - self.rect.centery, SCALE)

                angle = math.atan2(dy, dx)  # Calculate angle between rocket and planet

                d = math.sqrt((dx ** 2) + (dy ** 2))  # Calculate distance
                if d == 0:
                    d = 0.000001  # Prevent division by zero error

                f = G * self.mass * planet.mass / (d ** 2)  # Calculate gravitational force

                self.velocity[0] += ((math.cos(angle) * f) / self.mass) * self.game.dt * self.game.target_FPS
                self.velocity[1] += ((math.sin(angle) * f) / self.mass) * self.game.dt * self.game.target_FPS
                # End

                # Print information relating to rocket and planet
                # print(f'Planet: {planet.name}')
                # print('--------------------------------------')
                # print(f'Distance: {pix_met(dy, SCALE), pix_met(dx, SCALE)}')
                # print(f'Angle: {round(math.degrees(angle), 2)}')
                # print(f'Velocity: {[pix_met(self.velocity[0], SCALE), pix_met(self.velocity[1], SCALE)]}')
                # print(f'Position: {self.x, self.y}')
                # print()

            # Calculate Sun force
            # Start
            dx = pix_met(self.game.sun.rect.centerx - self.rect.centerx, SCALE)
            dy = pix_met(self.game.sun.rect.centery - self.rect.centery, SCALE)

            angle = math.atan2(dy, dx)  # Calculate angle between rocket and sun

            d = math.sqrt((dx ** 2) + (dy ** 2))  # Calculate distance
            if d == 0:
                d = 0.000001  # Prevent division by zero error

            f = G * self.mass * self.game.sun.mass / (d ** 2)  # Calculate gravitational force

            self.velocity[0] += ((math.cos(angle) * f) / self.mass) * self.game.dt * self.game.target_FPS
            self.velocity[1] += ((math.sin(angle) * f) / self.mass) * self.game.dt * self.game.target_FPS
            # End

            self.x += (self.velocity[0] + self.initial_velocity[0]) * self.game.dt * self.game.target_FPS
            self.y += (self.velocity[1] + self.initial_velocity[1]) * self.game.dt * self.game.target_FPS

            if not self.state['left_base_planet']:
                self.left_base_planet()

            self.get_raw_velocity()
            self.update_image()

            # print(f'Frame time: {self.game.frame_time}')
            # print(round(self.raw_velocity[0], 2), round(self.raw_velocity[1], 2))
            # print(round(self.target_planet.velocity[0], 2), round(self.target_planet.velocity[1], 2))

        elif self.state['landing'] or self.state['crashing']:
            self.velocity = [0, 0]
            self.rect.center = (self.current_planet.rect.centerx, self.current_planet.rect.centery)
            self.x, self.y = self.rect.x, self.rect.y
            self.update_image()

        self.rect = pygame.Rect(self.x, self.y, self.image['img'].get_width(), self.image['img'].get_height())

    def get_raw_velocity(self):
        if self.frame == 1:
            self.pos1 = (self.x, self.y)
            if self.times_run_velocity_func >= 1:
                self.raw_velocity = ((self.pos1[0] - self.pos2[0]) / self.game.dt,
                                     (self.pos1[1] - self.pos2[1]) / self.game.dt)
            self.frame += 1
        elif self.frame == 2:
            self.pos2 = (self.x, self.y)
            if self.times_run_velocity_func >= 1:
                self.raw_velocity = ((self.pos2[0] - self.pos1[0]) / self.game.dt,
                                     (self.pos2[1] - self.pos1[1]) / self.game.dt)
            self.frame -= 1

        self.times_run_velocity_func += 1

    def update_image(self):
        if self.state['positioning']:
            rest_angles = (17, 19, 21, 23, 1, 3, 5, 7, 9, 11, 13, 15)
            for i, val in enumerate(rest_angles):
                if i != 4:
                    if (math.pi / 12) * rest_angles[i - 1] <= self.angle < (math.pi / 12) * val:
                        self.image = self.rest_images[i - 1]
                        self.x = ((math.cos((math.pi / 12) * (rest_angles[i] - 1)) *
                                   (self.base_planet.image['img'].get_width() / 2 + 3) +
                                   self.base_planet.image['img'].get_width() / 2 -
                                   self.image['img'].get_width() / 2) +
                                  self.base_planet.rect.x)
                        self.y = ((math.sin((math.pi / 12) * (rest_angles[i] - 1)) *
                                   (self.base_planet.image['img'].get_height() / 2 + 3) +
                                   self.base_planet.image['img'].get_height() / 2 -
                                   self.image['img'].get_height() / 2) +
                                  self.base_planet.rect.y)
                        break
                else:
                    if (math.pi / 12) * 23 <= self.angle < math.pi * 2 or 0 <= self.angle < math.pi / 12:
                        self.image = self.rest_images[3]
                        self.x = (math.cos(0) * (self.base_planet.image['img'].get_width() / 2 + 3) +
                                  self.base_planet.image['img'].get_width() / 2 - self.image['img'].get_width() / 2 +
                                  self.base_planet.rect.x)
                        self.y = (math.sin(0) * (self.base_planet.image['img'].get_height() / 2 + 3) +
                                  self.base_planet.image['img'].get_height() / 2 - self.image['img'].get_height() / 2 +
                                  self.base_planet.rect.y)
                        break

        elif self.state['flying']:
            fly_angles = (1, 3, 5, 7, 9, 11)
            if -1 * (math.pi / 12) < self.target_angle <= (math.pi / 12):
                self.image = self.fly_images[0]
            elif (math.pi / 12) < self.target_angle <= (math.pi / 12) * 11:
                for i, val in enumerate(fly_angles):
                    if (math.pi / 12) * (val - 2) < self.target_angle <= (math.pi / 12) * val:
                        self.image = self.fly_images[i]
                        break
            elif -1 * (math.pi / 12) * 11 < self.target_angle <= -1 * (math.pi / 12):
                for i, val in enumerate(fly_angles):
                    if -1 * (math.pi / 12) * val < self.target_angle <= -1 * (math.pi / 12) * (val - 2):
                        self.image = self.fly_images[12 - i]
                        break
            elif ((math.pi / 12) * 11 < self.target_angle <= math.pi or
                  -1 * math.pi <= self.target_angle <= -1 * (math.pi / 12) * 11):
                self.image = self.fly_images[6]

        elif self.state['landing']:
            for i, fly_image in enumerate(self.fly_images):
                if self.image == fly_image:
                    if i <= 8:
                        self.image = self.rest_images[i + 3]
                    else:
                        self.image = self.rest_images[i - 9]

        elif self.state['crashing']:
            self.image = self.explode_image

    def left_base_planet(self):  # Only runs when in 'flying' state
        if not collision(rleft=self.rect.x, rtop=self.rect.y,
                         width=self.rect.width, height=self.rect.height,
                         center_x=self.base_planet.rect.centerx, center_y=self.base_planet.rect.centery,
                         radius=self.base_planet.radius + 30):
            self.state['left_base_planet'] = True

    def render(self):
        self.game.screen.blit(source=self.image['img'], dest=(self.x, self.y))
