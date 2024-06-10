import sys

import pygame

from scripts.utils import load_image, load_images
from scripts.screen import Screen
from scripts.sun import Sun
from scripts.planet import Planet
from scripts.rocket import Rocket

import math


class Game:
    def __init__(self):
        pygame.init()

        SCREEN_WIDTH = 1024
        SCREEN_HEIGHT = 720

        FPS = 120

        self.fps = FPS

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Rocket Game")

        self.clock = pygame.time.Clock()

        self.assets = {'background': pygame.transform.scale_by(load_image(path='background/stars_bg.png',
                                                                          convert='convert()')['img'], factor=0.75),

                       'start_menu': [load_image(path='buttons/start_btn.png', convert='convert_alpha()'),
                                      load_image(path='buttons/exit_btn.png', convert='convert_alpha()')],

                       'start_menu_hover': [load_image(path='buttons/start_btn_hover.png', convert='convert_alpha()'),
                                            load_image(path='buttons/exit_btn_hover.png', convert='convert_alpha()')],

                       'pause': None,

                       'pause_hover': None,

                       'level_select': None,

                       'level_select_hover': None,

                       'sun': load_image(path='objects/sun.png', convert='convert_alpha()'),

                       'earth': load_image(path='objects/earth.png', convert='convert()'),

                       'mars': load_image(path='objects/mars.png', convert='convert()'),

                       'rocket': load_images(path='rocket', convert='convert()'),

                       }

        self.screens = {'start_menu_screen': Screen(images=self.assets['start_menu'],
                                                    hover_images=self.assets['start_menu_hover'],
                                                    buffer=50, first_img_pos_y=250, game=self),

                        'pause_screen': None,

                        'level_select_screen': None,

                        }

        self.planets = {'earth': Planet(name='earth', angle=math.pi, gravity=9.81, mass=900,
                                        image=self.assets['earth'], orbit_radius=200, orbit_rate=0.01, game=self),

                        'mars': Planet(name='mars', angle=math.pi * 0.5, gravity=3.71, mass=900,
                                       image=self.assets['mars'], orbit_radius=300, orbit_rate=0.005, game=self),

                        }

        self.sun = Sun(image=self.assets['sun'], gravity=274, game=self)

        self.rocket = Rocket(mass=1000, images=self.assets['rocket'], base_planet=None, game=self)

        self.mouse_pos = None

        self.assets['background'].set_alpha(200)

        self.state = {'start_menu_screen': True, 'level_select_screen': False, 'pause_screen': False}

    def run(self):
        run = True

        while run:
            self.screen.fill((0, 0, 0))
            self.screen.blit(source=self.assets['background'], dest=(-400, 0))

            self.mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONUP:
                    if self.state['start_menu_screen']:
                        current_btn = self.screens['start_menu_screen'].current_hover()
                        if current_btn is None:
                            break
                        if self.screens['start_menu_screen'].rects[current_btn['path']].collidepoint(self.mouse_pos):
                            if current_btn['path'] == 'buttons/start_btn.png':
                                self.make_states_false()
                                self.state['level_select_screen'] = True
                            elif current_btn['path'] == 'buttons/exit_btn.png':
                                pygame.quit()
                                sys.exit()
                    if self.state['level_select_screen']:
                        pass
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        if self.rocket.state['positioning']:
                            self.rocket.movement[0] = True
                    if event.key == pygame.K_LEFT:
                        if self.rocket.state['positioning']:
                            self.rocket.movement[1] = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_RIGHT:
                        if self.rocket.state['positioning']:
                            self.rocket.movement[0] = False
                    if event.key == pygame.K_LEFT:
                        if self.rocket.state['positioning']:
                            self.rocket.movement[1] = False
                    if event.key == pygame.K_ESCAPE:
                        if not self.state['start_menu_screen']:
                            self.state['pause'] = True

            if self.state['start_menu_screen']:
                self.screens['start_menu_screen'].render()
            elif self.state['pause_screen']:
                pass
            elif self.state['level_select_screen']:
                self.rocket.base_planet = self.planets['earth']
                self.planets['mars'].image['img'] = pygame.transform.scale(surface=self.planets['mars'].image['img'],
                                                                           size=(60, 60))
                self.sun.render()
                self.planets['earth'].render()
                self.planets['mars'].render()
                self.rocket.render()

                self.planets['earth'].update()
                self.planets['mars'].update()
                self.rocket.update()

            pygame.display.update()
            self.clock.tick(self.fps)

    def make_states_false(self):
        for state in self.state:
            self.state[state] = False


Game().run()
