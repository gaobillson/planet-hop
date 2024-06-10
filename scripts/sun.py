import pygame


class Sun:
    def __init__(self, image, gravity, game):
        self.image = image
        self.gravity = gravity
        self.game = game
        self.x = game.screen.get_width() / 2 - image['img'].get_width() / 2
        self.y = game.screen.get_height() / 2 - image['img'].get_height() / 2
        self.rect = pygame.Rect(self.x, self.y, self.image['img'].get_width(), self.image['img'].get_height())

    def render(self):
        self.game.screen.blit(source=self.image['img'], dest=(self.x, self.y))
