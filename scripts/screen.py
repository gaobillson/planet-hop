import pygame


class Screen:
    def __init__(self, images: list[dict], hover_images, buffer, first_img_pos_y, game):
        self.images = images
        self.rects = {}
        for image in images:
            self.rects[image['path']] = image['img'].get_rect()
        self.hover_images = hover_images
        self.buffer = buffer
        self.game = game
        self.first_img_pos_y = first_img_pos_y
        self.next_pos = [self.game.screen.get_width() / 2 - self.images[0]['img'].get_width() / 2, first_img_pos_y]
        self.current_img_index = 0

    def render(self):
        self.next_pos[1] = self.first_img_pos_y

        for image, hover_image in zip(self.images, self.hover_images):
            self.rects[image['path']] = pygame.rect.Rect(self.next_pos[0],
                                                         self.next_pos[1],
                                                         image['img'].get_width(),
                                                         image['img'].get_height())
            if self.rects[image['path']].collidepoint(pygame.mouse.get_pos()):
                self.game.screen.blit(source=hover_image['img'], dest=self.next_pos)
            else:
                self.game.screen.blit(source=image['img'], dest=self.next_pos)
            self.next_pos[1] += image['img'].get_height() + self.buffer
            self.current_img_index += 1

    def current_hover(self):
        for image in self.images:
            if self.rects[image['path']].collidepoint(pygame.mouse.get_pos()):
                return image
