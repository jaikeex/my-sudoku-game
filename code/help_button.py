import pygame

from code.button import Button

BLACK = (0, 0, 0)
LIGHT_GRAY = (200, 200, 200)


class HelpButton(Button):
    def __init__(self, position, size):
        self.button_text = "How to play"
        super().__init__(position, size, self.button_text)
        self.help_window = HelpWindow()


    def clicked(self, game_window):
        game_window.grid.deselect_current_box()
        sprites = pygame.sprite.Group(self.help_window)
        game_window.window_elements_to_draw.append(sprites)
        self.help_window.displayed = True
        pygame.display.update()


class HelpWindow(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.displayed = False
        self.image = pygame.Surface((300, 400))
        self.image.fill(LIGHT_GRAY)
        self.position = (270, 300)
        self.rect = self.image.get_rect(center=self.position)
        self.draw()


    def draw(self):
        font = pygame.font.SysFont("calibri", 18)
        help_text = [" - Use mouse to select a box",
                     "",
                     "-With a box selected, press 1-9",
                     " to draw a small hint number ",
                     "(you can have multiple hint ",
                     "numbers in a box) ",
                     "",
                     "-Press enter to place a permanent",
                     "number on the board,this only works ",
                     "when there is exactly one hint",
                     "number in that box",
                     "",
                     "-Continue until the puzzle is solved!"]
        help_text_positions = list(range(10, len(help_text) * 30 + 10, 30))

        for i in range(len(help_text)):
            help_text_renderd = font.render(help_text[i], True, BLACK)
            self.image.blit(help_text_renderd, (10, help_text_positions[i]))


    def clicked_outside_help_window(self, position, window):
        if not 170 < position[0] < 370 or not 200 < position[1] < 400:
            if self.displayed:
                window.window_elements_to_draw.pop()
                self.displayed = False











