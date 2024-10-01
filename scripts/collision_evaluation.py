"""
SPDX-FileCopyrightText: 2024, Jason Treakle, thetreakle@gmail.com
SPDX-License-Identifier: GPL-3.0-or-later

The collision function copyright (C) 2014 user Martineau on Stack Overflow
https://stackoverflow.com/questions/24727773/detecting-rectangle-collision-with-a-circle

See main.py for the full GPL-3.0 license header.
See LICENSE.txt for full GPL-3.0 license information.
See LICENSES directory for licensing of other works included in this project.
"""

import math

from scripts.planet import Planet
from scripts.utils import make_states_false


# Copyright (C) 2014 Martineau
def collision(rleft, rtop, width, height,  # rectangle definition
              center_x, center_y, radius, ):  # circle definition
    """ Detect collision between a rectangle and circle. """

    # complete boundbox of the rectangle
    rright, rbottom = rleft + width, rtop + height

    # bounding box of the circle
    cleft, ctop = center_x - radius, center_y - radius
    cright, cbottom = center_x + radius, center_y + radius

    # trivial reject if bounding boxes do not intersect
    if rright < cleft or rleft > cright or rbottom < ctop or rtop > cbottom:
        return False  # no collision possible

    # check whether any point of rectangle is inside circle's radius
    for x in (rleft, rleft + width):
        for y in (rtop, rtop + height):
            # compare distance between circle's center point and each point of
            # the rectangle with the circle's radius
            if math.hypot(x - center_x, y - center_y) <= radius:
                return True  # collision detected

    # check if center of circle is inside rectangle
    if rleft <= center_x <= rright and rtop <= center_y <= rbottom:
        return True  # overlaid

    return False  # no collision detected


def find_collision_object(game):
    """
    Determines if the rocket has collided with a planet or the Sun.
    Updates game.user_won.
    """
    # Check collision with planets
    for planet in game.planets.values():
        if collision(rleft=game.rocket.rect.x, rtop=game.rocket.rect.y,
                     width=game.rocket.rect.width, height=game.rocket.rect.height,
                     center_x=planet.rect.centerx, center_y=planet.rect.centery,
                     radius=planet.radius):
            game.rocket.current_planet = planet
            update_user_won(game)

    # Check collision with Sun
    if collision(rleft=game.rocket.rect.x, rtop=game.rocket.rect.y,
                 width=game.rocket.rect.width, height=game.rocket.rect.height,
                 center_x=game.sun.rect.centerx, center_y=game.sun.rect.centery,
                 radius=game.sun.radius):
        game.rocket.current_planet = game.sun
        update_user_won(game)


def update_user_won(game):  # Runs upon a collision
    # Add name of collided planet to user win variable
    game.user_won[0] = game.rocket.current_planet.name

    # If rocket did not crash into the sun
    if game.rocket.current_planet.name != 'sun':
        # Decide if rocket landed on correct planet
        if game.user_won[0] == game.rocket.target_planet.name:
            # Correct planet
            game.assets['end_banners'][1] = game.assets['win_banners'][1]
        else:
            # Incorrect planet
            game.assets['end_banners'][1] = game.assets['lose_banners'][1]

        # Decide if rocket came in at proper velocity
        if (math.fabs(game.rocket.raw_velocity[0] - game.rocket.current_planet.velocity[0]) <= 51 and
                math.fabs(game.rocket.raw_velocity[1] - game.rocket.current_planet.velocity[1]) <= 51):
            # If rocket did not crash
            game.user_won[1] = True
            game.assets['end_banners'][2] = game.assets['win_banners'][2]
        else:
            # If rocket crashed (difference between velocities too great)
            game.user_won[1] = False
            game.assets['end_banners'][2] = game.assets['lose_banners'][2]

        # Evaluate main win/lose banner
        if game.user_won[0] == game.rocket.target_planet.name and game.user_won[1]:
            # Win
            game.assets['end_banners'][0] = game.assets['win_banners'][0]
        else:
            # Lose
            game.assets['end_banners'][0] = game.assets['lose_banners'][0]
    else:
        game.user_won[1] = False
        game.assets['end_banners'][0] = game.assets['lose_banners'][0]
        game.assets['end_banners'][1] = game.assets['crash_into_sun_banner']
        game.assets['end_banners'].pop(2)
        game.screens['end_screen'].img_positions[1] = (312, 192)

    # Update rocket state
    make_states_false(game.rocket)
    if game.user_won[1]:
        game.rocket.state['landing'] = True
    else:
        game.rocket.state['crashing'] = True

    game.screens['end_screen'].images = game.assets['end_banners']
    game.state['end_screen'] = True
    # show_end_screen(game)


# Displays the end message to the console. Not used.
def show_end_screen(game):
    if game.user_won[0] == 'sun':
        # Lose
        print('You obliterated your rocket in the Sun!')
    elif game.user_won[0] == game.rocket.target_planet.name and game.user_won[1]:
        # Win
        print(f"Your rocket matched {game.rocket.target_planet.name.capitalize()}'s speed and landed!")
    elif game.user_won[0] == game.rocket.target_planet.name and not game.user_won[1]:
        # Lose
        print(f"Your rocket didn't match {game.rocket.target_planet.name.capitalize()}'s speed and crashed!")
    elif game.user_won[0] != game.rocket.target_planet.name and game.user_won[1]:
        # Lose
        print(f'Your rocket went nowhere, landing back on {game.rocket.current_planet.name.capitalize()}!')
    elif game.user_won[0] != game.rocket.target_planet.name and not game.user_won[1]:
        # Lose
        print(f'Your rocket crashed back into {game.rocket.current_planet.name.capitalize()}!')
    if isinstance(game.rocket.current_planet, Planet):
        print(round(math.fabs(game.rocket.raw_velocity[0] - game.rocket.current_planet.velocity[0]), 2),
              round(math.fabs(game.rocket.raw_velocity[1] - game.rocket.current_planet.velocity[1]), 2))


# Use this if you need to print the velocity difference between the rocket and planet to the screen
def get_velocity_diff(game):
    if isinstance(game.rocket.current_planet, Planet):
        text = (f"X: {round(math.fabs(game.rocket.raw_velocity[0] - game.rocket.current_planet.velocity[0]), 2)}   "
                f"Y: {round(math.fabs(game.rocket.raw_velocity[1] - game.rocket.current_planet.velocity[1]), 2)}")
    else:
        text = "Obliterated by the Sun"
    return text
