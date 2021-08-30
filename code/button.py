import pygame

BLACK = (0, 0, 0)


class Button:
    """"""
    def __init__(self, position, size, text):
        self.button_text = text
        self.x, self.y = position
        self.width_in_pixels, self.height_in_pixels = size
        self.button_area = pygame.Rect(self.x, self.y,
                                       self.width_in_pixels,
                                       self.height_in_pixels)

        self.font = pygame.font.SysFont("calibri", 26)
        self.button_rendered_text = self.font.render(
            self.button_text, True, BLACK)


    def draw(self, game_window):
        game_window.blit(self.button_rendered_text, self.button_area)


    def clicked(self, game_window):
        pass













