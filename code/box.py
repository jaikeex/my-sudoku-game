import pygame

BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
RED = (255, 0, 0)
BLUE = (0, 0, 175)

class Box:
    def __init__(self, coordinates, dims, number):
        self.row, self.column = coordinates
        self.width_in_pixels, self.height_in_pixels = dims
        self.is_selected = False
        self.number = number

        self.color = None
        self.pencil_numbers = []
        self.pencil_number_boxes = []
        self.setup()


    def setup(self):
        self._initialize_pencil_number_boxes()
        self._set_color()


    def _set_color(self):
        if self.number:
            self.color = BLACK
        else:
            self.color = BLUE


    def _initialize_pencil_number_boxes(self):
        box_width = self.width_in_pixels / 3
        box_height = self.height_in_pixels / 3
        for row in range(3):
            for column in range(3):
                box = PencilNumberBox((row, column), (box_width, box_height))
                self.pencil_number_boxes.append(box)
        self._initialize_default_pencil_number_box_values()


    def _initialize_default_pencil_number_box_values(self):
        for box in self.pencil_number_boxes:
            box.number = self.pencil_number_boxes.index(box) + 1


    def draw(self, game_window):
        self._draw_numbers(game_window)
        if self.is_selected:
            self._hilight_selected(game_window)


    def _draw_numbers(self, game_window):
        if self.number:
            self._draw_permanent_number(game_window)
        if len(self.pencil_numbers) and not self.number:
            self._draw_pencil_numbers(game_window)


    def _draw_permanent_number(self, game_window):
        x_offset = 20
        y_offset = 10
        font = pygame.font.SysFont("calibri", 45)
        x = self.column * self.width_in_pixels + x_offset
        y = self.row * self.height_in_pixels + y_offset
        number_text = font.render(str(self.number), True, self.color)
        game_window.blit(number_text, (x, y))


    def _draw_pencil_numbers(self, game_window):
        font = pygame.font.SysFont("comicsansms", 18)
        x_offset = 5
        y_offset = -1.5
        for box in self.pencil_number_boxes:
            if box.number in self.pencil_numbers:
                x = self.column * self.width_in_pixels + \
                    box.column * box.width_in_pixels + x_offset
                y = self.row * self.height_in_pixels + \
                    box.row * box.height_in_pixels + y_offset
                pencil_text = font.render(str(box.number), True, GRAY)
                game_window.blit(pencil_text, (x, y))


    def _hilight_selected(self, game_window):
        box_borders = (self.column * self.width_in_pixels,
                       self.row * self.width_in_pixels,
                       self.width_in_pixels, self.width_in_pixels)
        pygame.draw.rect(game_window, RED, box_borders, 2)


    def place_permanent_number(self):
        if len(self.pencil_numbers) == 1:
            self.number = self.pencil_numbers[0]


    def reset_permanent_number(self):
        self.number = 0


    def remove_pencil_number(self, number):
        if number in self.pencil_numbers:
            self.pencil_numbers.remove(number)


class PencilNumberBox:
    def __init__(self, coordinates, dims):
        self.row, self.column = coordinates
        self.width_in_pixels, self.height_in_pixels = dims
        self.number = 0
