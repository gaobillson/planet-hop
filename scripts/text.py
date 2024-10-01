"""
SPDX-FileCopyrightText: 2024, Jason Treakle, thetreakle@gmail.com
SPDX-License-Identifier: GPL-3.0-or-later

See main.py for the full GPL-3.0 license header.
See LICENSE.txt for full GPL-3.0 license information.
See LICENSES directory for licensing of other works included in this project.
"""

import pygame

pygame.font.init()

# htp = how_to_play. Renders the fonts used in the game.
start_text = pygame.font.Font('fonts/darkstar.ttf', 100)
htp_title_text = pygame.font.Font('fonts/darkstar.ttf', 50)
htp_text = pygame.font.Font('fonts/darkstar.ttf', 20)
velocity_diff_text = pygame.font.Font(None, 30)

# Colors used in the game
RED = (207, 35, 64)
BLUE = (0, 198, 247)
GREEN = (98, 235, 0)

start_title = {
    'surf': start_text.render('PLANET HOP', True, GREEN),
    'dest': (160, 270)}

htp_1_line_1 = {
    'surf': htp_title_text.render('CONTROLS',
                                  True, GREEN),
    'dest': (100, 380)}
htp_1_line_2 = {
    'surf': htp_text.render('USE  THE  ARROW  KEYS  TO  POSITION  THE  ROCKET  BEFORE  LAUNCH',
                            True, GREEN),
    'dest': (100, 450)}
htp_1_line_3 = {
    'surf': htp_text.render('POINT  AND  CLICK  TO  LAUNCH  IN  THE  DIRECTION  OF  YOUR  CURSOR',
                            True, GREEN),
    'dest': (100, 510)}
htp_1_line_4 = {
    'surf': htp_text.render('POINT  AND  CLICK  AT  ANY  TIME  TO  CHANGE  THE  TRAJECTORY',
                            True, GREEN),
    'dest': (100, 570)}

htp_2_line_1 = {
    'surf': htp_title_text.render('STRATEGIES',
                                  True, GREEN),
    'dest': (100, 400)}
htp_2_line_2 = {
    'surf': htp_text.render('LAUNCH  WHEN  EARTH  IS  NEAR  THE  TARGET',
                            True, GREEN),
    'dest': (100, 470)}
htp_2_line_3 = {
    'surf': htp_text.render('AIM  AHEAD  OF  THE  TARGET  AND  APPROACH  FROM  BEHIND',
                            True, GREEN),
    'dest': (100, 530)}
htp_2_line_4 = {
    'surf': htp_text.render("THE  VELOCITY  OF  THE  ROCKET  MUST  BE  SIMILAR  TO  THE  TARGET  TO  LAND",
                            True, GREEN),
    'dest': (100, 590)}

velocity_diff = {
    'surf': None,
    'dest': (10, 620)
}

# Imported in the game file
how_to_play_text_1 = [htp_1_line_1, htp_1_line_2, htp_1_line_3, htp_1_line_4]
how_to_play_text_2 = [htp_2_line_1, htp_2_line_2, htp_2_line_3, htp_2_line_4]
start_title = [start_title]
velocity_diff = [velocity_diff]
