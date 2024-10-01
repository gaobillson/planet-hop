"""
Copyright (C) 2024, Jason Treakle, thetreakle@gmail.com

This program is free software: you can redistribute it and/or modify it under the terms of the
GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License,
or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License along with this program.
If not, see https://www.gnu.org/licenses/.

See LICENSE.txt for the full GPL-3.0 license information.
See LICENSES directory for licensing of other works included in this project.
"""

import sys
import pygame
import math
import random
import asyncio
import time

from scripts.utils import load_image, load_images, make_states_false, meters_to_pixels as met_pix
from scripts.screen import Screen
from scripts.text import how_to_play_text_1, how_to_play_text_2, start_title
from scripts.rocket import Rocket, SCALE
from scripts.planet import Planet
from scripts.sun import Sun
from scripts.collision_evaluation import find_collision_object


class Game:
    def __init__(self):
        pygame.init()

        SCREEN_WIDTH = 1024
        SCREEN_HEIGHT = 720

        self.FPS = 120
        self.target_FPS = 120

        self.prev_time = time.time()
        self.now = 0
        self.dt = 0

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Planet Hop")

        self.clock = pygame.time.Clock()

        # Load background images
        self.backgrounds = {'stars_bg': load_image(path='background/stars_bg.png', convert='convert_alpha()'),

                            'dark_bg': load_image(path='background/dark_bg.png',
                                                  convert='convert_alpha()'),
                            }

        # Load images for screens and the rest of the game
        self.assets = {'logo': load_image(path='logo/logo.png', convert='convert_alpha()'),

                       'start_menu': [load_image(path='buttons/start_btn.png', convert='convert()'),
                                      load_image(path='buttons/how_to_play_btn.png', convert='convert()'),
                                      load_image(path='buttons/exit_btn.png', convert='convert()')],

                       'start_menu_hover': [load_image(path='buttons/start_btn_hover.png', convert='convert()'),
                                            load_image(path='buttons/how_to_play_btn_hover.png', convert='convert()'),
                                            load_image(path='buttons/exit_btn_hover.png', convert='convert()')],

                       'pause_menu': [load_image(path='buttons/continue_btn.png', convert='convert()'),
                                      load_image(path='buttons/main_menu_btn.png', convert='convert()'),
                                      load_image(path='buttons/exit_btn.png', convert='convert()')],

                       'pause_menu_hover': [load_image(path='buttons/continue_btn_hover.png', convert='convert()'),
                                            load_image(path='buttons/main_menu_btn_hover.png', convert='convert()'),
                                            load_image(path='buttons/exit_btn_hover.png', convert='convert()')],

                       'arrows': [load_image(path='buttons/arrow_right.png', convert='convert()'),
                                  load_image(path='buttons/arrow_left.png', convert='convert()'),
                                  load_image(path='buttons/arrow_right_hover.png', convert='convert()'),
                                  load_image(path='buttons/arrow_left_hover.png', convert='convert()'), ],

                       'main_menu_btn': load_image(path='buttons/main_menu_btn.png', convert='convert()'),

                       'main_menu_btn_hover': load_image(path='buttons/main_menu_btn_hover.png', convert='convert()'),

                       'optimal_launch': load_image(path='how_to_play_screen/2/optimal_launch.png',
                                                    convert='convert()'),

                       'how_to_move_rocket': load_image(path='how_to_play_screen/1/how_to_move_rocket.png',
                                                        convert='convert()'),

                       'restart_btn': load_image(path='buttons/restart_btn.png', convert='convert()'),

                       'restart_btn_hover': load_image(path='buttons/restart_btn_hover.png', convert='convert()'),

                       'pause_btn': load_image(path='buttons/pause_btn.png', convert='convert()'),

                       'pause_btn_hover': load_image(path='buttons/pause_btn_hover.png', convert='convert()'),

                       'sun': load_image(path='objects/sun.png', convert='convert()'),

                       'earth': load_image(path='objects/earth.png', convert='convert()'),

                       'mars': load_image(path='objects/mars.png', convert='convert()'),

                       'rocket_rest': load_images(path='rocket/rest', convert='convert()'),

                       'rocket_fly': load_images(path='rocket/fly', convert='convert()'),

                       'rocket_explode': load_image(path='rocket/explode/rocket_explode.png', convert='convert()'),

                       'win_banners': load_images(path='end_screen/win', convert='convert()')[0:3],

                       'lose_banners': load_images(path='end_screen/lose', convert='convert()')[0:3],

                       'crash_into_sun_banner': load_image(path='end_screen/crash_into_sun_banner.png',
                                                           convert='convert()'),

                       'end_banners': load_images(path='end_screen/lose', convert='convert()')[0:3],

                       }

        # Resize images, set alphas
        self.backgrounds['stars_bg']['img'] = pygame.transform.scale_by(surface=self.backgrounds['stars_bg']['img'],
                                                                        factor=0.75)
        self.backgrounds['stars_bg']['img'].set_alpha(200)
        self.backgrounds['dark_bg']['img'].set_alpha(150)
        self.backgrounds['dark_bg']['img'] = pygame.transform.scale(
            surface=self.backgrounds['dark_bg']['img'],
            size=(1100, 800))
        self.assets['win_banners'][0]['img'] = pygame.transform.scale(surface=self.assets['win_banners'][0]['img'],
                                                                      size=(500, 102))
        self.assets['lose_banners'][0]['img'] = pygame.transform.scale(surface=self.assets['lose_banners'][0]['img'],
                                                                       size=(500, 102))
        self.assets['crash_into_sun_banner']['img'] = (
            pygame.transform.scale(surface=self.assets['crash_into_sun_banner']['img'],
                                   size=(400, 50)))
        self.assets['optimal_launch']['img'] = pygame.transform.scale(surface=self.assets['optimal_launch']['img'],
                                                                      size=(639, 368))
        self.assets['how_to_move_rocket']['img'] = pygame.transform.scale(
            surface=self.assets['how_to_move_rocket']['img'],
            size=(500, 313))
        self.assets['arrows'] = \
            [{'path': x['path'], 'img': pygame.transform.scale(surface=x['img'], size=(143, 75))}
             for x in self.assets['arrows']]
        self.assets['logo']['img'] = pygame.transform.scale(surface=self.assets['logo']['img'], size=(248, 248))

        # Initialize Screens using self.assets
        self.screens = {'start_menu_screen': Screen(buttons=self.assets['start_menu'],
                                                    hover_buttons=self.assets['start_menu_hover'],
                                                    btn_positions=[(362, 390), (362, 500), (362, 610)],
                                                    images=[self.assets['logo']], img_positions=[(388, 10)],
                                                    text=start_title, game=self),

                        'how_to_play_screen_1': Screen(buttons=[self.assets['main_menu_btn'], self.assets['arrows'][0]],
                                                       hover_buttons=[self.assets['main_menu_btn_hover'],
                                                                      self.assets['arrows'][2]],
                                                       btn_positions=[(362, 623), (675, 630)],
                                                       images=[self.assets['how_to_move_rocket']],
                                                       img_positions=[(262, 30)], text=how_to_play_text_1,
                                                       background=self.backgrounds['dark_bg'], game=self),

                        'how_to_play_screen_2': Screen(
                            buttons=[self.assets['arrows'][1], self.assets['main_menu_btn']],
                            hover_buttons=[self.assets['arrows'][3], self.assets['main_menu_btn_hover']],
                            btn_positions=[(206, 630), (362, 623)], images=[self.assets['optimal_launch'], ],
                            img_positions=[(193, 10)], background=self.backgrounds['dark_bg'],
                            text=how_to_play_text_2, game=self),

                        'level_select_screen': None,  # Future feature

                        'end_screen': Screen(images=self.assets['end_banners'],
                                             img_positions=[(262, 80), (367, 192), (367, 238)], game=self),

                        'restart_and_pause_screen': Screen(buttons=[self.assets['restart_btn'],
                                                                    self.assets['pause_btn']],
                                                           hover_buttons=[self.assets['restart_btn_hover'],
                                                                          self.assets['pause_btn_hover']],
                                                           btn_positions=[(924, 600), (974, 0)], game=self),

                        'pause_screen': Screen(buttons=self.assets['pause_menu'],
                                               hover_buttons=self.assets['pause_menu_hover'],
                                               btn_positions=[(362, 190), (362, 319), (362, 448)],
                                               background=self.backgrounds['dark_bg'], game=self),
                        # ' ': None,

                        }

        # Initialize Planets
        self.planets = {'earth': Planet(name='earth', angle=None, mass=5.9722 * (10 ** 24),
                                        image=self.assets['earth'], orbit_radius=200, orbit_rate=-0.007, game=self),

                        'mars': Planet(name='mars', angle=None, mass=6.39 * (10 ** 23),
                                       image=self.assets['mars'], orbit_radius=met_pix(228000000000, SCALE),
                                       orbit_rate=-0.00371, game=self),
                        }

        # Initialize a Sun
        self.sun = Sun(image=self.assets['sun'], mass=1.9891 * (10 ** 30), game=self)

        # Initialize a Rocket
        self.rocket = Rocket(mass=2 * (10 ** 6), rest_images=self.assets['rocket_rest'],
                             fly_images=self.assets['rocket_fly'], explode_image=self.assets['rocket_explode'],
                             game=self, base_planet=self.planets['earth'], target_planet=self.planets['mars'])

        # Set the possible game states. More than one state can be true at the same time
        self.state = {'start_menu_screen': True, 'how_to_play_screen_1': False, 'how_to_play_screen_2': False,
                      'level_select_screen': False, 'end_screen': False, 'restart_and_pause_screen': False,
                      'gameplay': False, 'pause_screen': False}

        self.mouse_pos = None

        self.user_won = ['', 0]  # [Planet landed on, velocity difference]

        pygame.display.set_icon(self.assets['logo']['img'])

    def initialize_gameplay(self):
        """
        Initializes the gameplay. Randomizes planetary positions and
        sets rocket to its initial state, positioning. Sets end_screen state to false
        if applicable and resets it if applicable.
        """
        make_states_false(self)
        self.state['stars_screen'] = True
        self.state['gameplay'] = True
        self.state['restart_and_pause_screen'] = True
        for planet in self.planets:
            self.planets[planet].angle = random.random() * math.pi * 2
        self.assets['end_banners'] = self.assets['lose_banners'].copy()
        self.screens['end_screen'].images = self.assets['end_banners']
        self.screens['end_screen'].img_positions = [(262, 80), (367, 192), (367, 238)]
        self.state['end_screen'] = False
        make_states_false(self.rocket)
        self.rocket.state['positioning'] = True

    def render_gameplay(self):
        """
        Renders the gameplay screen.
        """
        self.planets['earth'].image['img'] = pygame.transform.scale(surface=self.planets['earth'].image['img'],
                                                                    size=(55, 55))
        self.sun.render()
        pygame.draw.circle(surface=self.screen, color=(72, 216, 232),
                           center=(self.sun.rect.centerx, self.sun.rect.centery),
                           radius=self.planets['earth'].orbit_radius, width=1)
        pygame.draw.circle(surface=self.screen, color=(240, 125, 24),
                           center=(self.sun.rect.centerx, self.sun.rect.centery),
                           radius=self.planets['mars'].orbit_radius, width=1)
        self.planets['earth'].render()
        self.planets['mars'].render()
        self.rocket.render()

        # Only updates game if game is not paused
        if not self.state['pause_screen']:
            self.planets['earth'].update()
            self.planets['mars'].update()
            self.rocket.update()

            # Only checks collision if rocket left base planet
            if self.rocket.state['left_base_planet']:
                find_collision_object(self)


game = Game()


async def main():

    while True:
        # Compute delta time
        game.now = time.time()
        game.dt = game.now - game.prev_time
        game.prev_time = game.now

        game.screen.fill((0, 0, 0))
        game.screen.blit(source=game.backgrounds['stars_bg']['img'], dest=(-400, 0))

        game.mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONUP:
                if game.state['start_menu_screen']:
                    current_btn = game.screens['start_menu_screen'].current_hover()
                    if current_btn is None:
                        break
                    if game.screens['start_menu_screen'].rects[current_btn['path']].collidepoint(game.mouse_pos):
                        if current_btn['path'] == 'buttons/start_btn.png':
                            game.initialize_gameplay()
                        elif current_btn['path'] == 'buttons/how_to_play_btn.png':
                            game.state['start_menu_screen'] = False
                            game.state['how_to_play_screen_1'] = True
                        elif current_btn['path'] == 'buttons/exit_btn.png':
                            pygame.quit()
                            sys.exit()

                elif game.state['how_to_play_screen_1']:
                    current_btn = game.screens['how_to_play_screen_1'].current_hover()
                    if current_btn is None:
                        break
                    if game.screens['how_to_play_screen_1'].rects[current_btn['path']].collidepoint(game.mouse_pos):
                        if current_btn['path'] == 'buttons/main_menu_btn.png':
                            game.state['how_to_play_screen_1'] = False
                            game.state['start_menu_screen'] = True
                        elif current_btn['path'] == 'buttons/arrow_right.png':
                            game.state['how_to_play_screen_1'] = False
                            game.state['how_to_play_screen_2'] = True

                elif game.state['how_to_play_screen_2']:
                    current_btn = game.screens['how_to_play_screen_2'].current_hover()
                    if current_btn is None:
                        break
                    if game.screens['how_to_play_screen_2'].rects[current_btn['path']].collidepoint(game.mouse_pos):
                        if current_btn['path'] == 'buttons/main_menu_btn.png':
                            game.state['how_to_play_screen_2'] = False
                            game.state['start_menu_screen'] = True
                        elif current_btn['path'] == 'buttons/arrow_left.png':
                            game.state['how_to_play_screen_2'] = False
                            game.state['how_to_play_screen_1'] = True

                elif game.state['pause_screen']:
                    current_btn = game.screens['pause_screen'].current_hover()
                    if current_btn is None:
                        break
                    if game.screens['pause_screen'].rects[current_btn['path']].collidepoint(game.mouse_pos):
                        if current_btn['path'] == 'buttons/continue_btn.png':
                            game.state['pause_screen'] = False
                            game.state['restart_and_pause_screen'] = True
                        elif current_btn['path'] == 'buttons/main_menu_btn.png':
                            make_states_false(game)
                            game.state['stars_screen'] = True
                            game.state['start_menu_screen'] = True
                        elif current_btn['path'] == 'buttons/exit_btn.png':
                            pygame.quit()
                            sys.exit()

                elif game.state['gameplay']:
                    current_btn = game.screens['restart_and_pause_screen'].current_hover()
                    if current_btn is not None:
                        if game.screens['restart_and_pause_screen'].rects[current_btn['path']].collidepoint(
                                game.mouse_pos):
                            if current_btn['path'] == 'buttons/pause_btn.png':
                                game.state['restart_and_pause_screen'] = False
                                game.state['pause_screen'] = True
                            elif current_btn['path'] == 'buttons/restart_btn.png':
                                game.initialize_gameplay()
                            break
                    else:
                        if True in (game.rocket.state['positioning'], game.rocket.state['flying']):
                            if game.rocket.state['positioning']:
                                game.rocket.state['positioning'] = False
                            game.rocket.state['setting_trajectory'] = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    if game.rocket.state['positioning']:
                        game.rocket.movement[0] = True
                if event.key == pygame.K_LEFT:
                    if game.rocket.state['positioning']:
                        game.rocket.movement[1] = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    if game.rocket.state['positioning']:
                        game.rocket.movement[0] = False
                if event.key == pygame.K_LEFT:
                    if game.rocket.state['positioning']:
                        game.rocket.movement[1] = False
                if event.key == pygame.K_ESCAPE:
                    if (game.state['start_menu_screen'], game.state['how_to_play_screen_1']) == (False, False):
                        game.state['pause_screen'] = not game.state['pause_screen']
                        game.state['restart_and_pause_screen'] = not game.state['restart_and_pause_screen']

        if game.state['gameplay']:
            game.render_gameplay()

        for screen in game.screens:
            if game.state[screen]:
                game.screens[screen].render()

        pygame.display.update()
        game.clock.tick(game.FPS)

        await asyncio.sleep(0)

asyncio.run(main())
