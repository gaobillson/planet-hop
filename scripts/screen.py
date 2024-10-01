"""
SPDX-FileCopyrightText: 2024, Jason Treakle, thetreakle@gmail.com
SPDX-License-Identifier: GPL-3.0-or-later

See main.py for the full GPL-3.0 license header.
See LICENSE.txt for full GPL-3.0 license information.
See LICENSES directory for licensing of other works included in this project.
"""

import pygame


class Screen:
    def __init__(self, game, buttons: list[dict] = None, hover_buttons: list[dict] = None, images: list = None,
                 btn_positions: list[tuple] = None, img_positions: list[tuple] = None,
                 background=None, text: list = None):
        self.buttons = buttons
        self.rects = {}
        if buttons is not None:
            for button in buttons:
                self.rects[button['path']] = button['img'].get_rect()
        self.hover_buttons = hover_buttons
        self.images = images
        self.btn_positions = btn_positions
        self.img_positions = img_positions
        self.background = background
        self.text = text
        self.game = game

    def render(self):
        if self.background is not None:
            self.game.screen.blit(source=self.background['img'], dest=(-1, -1))

        if self.hover_buttons is not None:
            for button, hover_button, position in zip(self.buttons, self.hover_buttons, self.btn_positions):
                self.rects[button['path']] = pygame.rect.Rect(position[0], position[1],
                                                              button['img'].get_width(), button['img'].get_height())
                if self.rects[button['path']].collidepoint(pygame.mouse.get_pos()):
                    self.game.screen.blit(source=hover_button['img'], dest=position)
                else:
                    self.game.screen.blit(source=button['img'], dest=position)
        elif self.buttons is not None:
            for button, position in zip(self.buttons, self.btn_positions):
                self.game.screen.blit(source=button['img'], dest=position)
        # Else, do nothing

        if None not in (self.images, self.img_positions):
            for image, position in zip(self.images, self.img_positions):
                self.game.screen.blit(source=image['img'], dest=position)

        if self.text is not None:
            for text in self.text:
                self.game.screen.blit(source=text['surf'], dest=text['dest'])

    def current_hover(self):
        for button in self.buttons:
            if self.rects[button['path']].collidepoint(pygame.mouse.get_pos()):
                return button
