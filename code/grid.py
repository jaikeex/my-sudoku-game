import pygame

from code.box import Box

BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
RED = (255, 0, 0)

class Grid:
    """
    Manages the grid part of the game gui.
    """
    def __init__(self, board, dims):
        self.width_in_pixels, self.height_in_pixels = dims
        self.board = board
        self.size = len(self.board.model)
        self.boxes = []
        self.selected_box = False
        self.setup()


    def setup(self):
        """Prepares the grid for playing, used after generating a board."""
        self._initialize_boxes()


    def _initialize_boxes(self):
        self.boxes.clear()
        box_width = self.width_in_pixels / 9
        box_height = self.height_in_pixels / 9
        for row in range(self.size):
            for column in range(self.size):
                box = Box((row, column),
                          (box_width, box_height),
                          self.board.model[row][column])
                self.boxes.append(box)


    def draw(self, game_window):
        """
        Draws the grid onto the main window.
        :param game_window: The main game window.
        :type game_window: pygame.Surface
        :return: None
        :rtype: None
        """
        self._draw_gridlines(game_window)
        self._draw_boxes(game_window)


    def _draw_gridlines(self, game_window):
        gap = self.width_in_pixels / self.size
        for i in range(self.size + 1):
            thickness = self._determine_gridline_thickness(i)
            pygame.draw.line(game_window, BLACK, (0, i * gap),
                             (self.width_in_pixels, i * gap), thickness)
            pygame.draw.line(game_window, BLACK, (i * gap, 0),
                             (i * gap, self.height_in_pixels), thickness)


    @staticmethod
    def _determine_gridline_thickness(gridline_number):
        if gridline_number % 3 == 0:
            return 3
        else:
            return 1


    def _draw_boxes(self, game_window):
        for box in self.boxes:
            box.draw(game_window)


    def is_board_solvable(self):
        """
        Checks if the active board has a solution.
        :return: None
        :rtype: None
        """
        return self.board.is_solvable()


    def place_permanent_number(self, coordinates):
        """

        :param coordinates:
        :type coordinates:
        :return:
        :rtype:
        """
        box = self._find_box_by_coordinates(coordinates)
        self._place_permanent_number_in_box(box)
        if self.board.is_valid_number(box.number, (box.row, box.column)):
            self.remove_useless_pencil_number(box)
            return True
        else:
            self._reset_permanent_number_in_box(box)
            return False


    def _place_permanent_number_in_box(self, box):
        box.place_permanent_number()
        self._update_model_from_list_of_boxes()


    def _reset_permanent_number_in_box(self, box):
        box.reset_permanent_number()
        self._update_model_from_list_of_boxes()


    def remove_useless_pencil_number(self, box):
        coordinates = box.row, box.column
        self._remove_pencil_number_in_row(box.number, box.row)
        self._remove_pencil_number_in_column(box.number, box.column)
        self._remove_pencil_number_in_small_box(box.number, coordinates)


    def _remove_pencil_number_in_row(self, number, row):
        for column in range(self.size):
            box = self._find_box_by_coordinates((row, column))
            box.remove_pencil_number(number)


    def _remove_pencil_number_in_column(self, number, column):
        for row in range(self.size):
            box = self._find_box_by_coordinates((row, column))
            box.remove_pencil_number(number)


    def _remove_pencil_number_in_small_box(self, number, coordinates):
        small_board_position = self.board._find_small_board_by_coordinates(coordinates)
        for row in small_board_position[0]:
            for column in small_board_position[1]:
                box = self._find_box_by_coordinates((row, column))
                box.remove_pencil_number(number)


    def update_box_numbers(self):
        for box in self.boxes:
            box.number = self.board.model[box.row][box.column]


    def select_box_by_coordinates(self, coordinates):
        if self.selected_box:
            previous_box = self.selected_box
            previous_box.is_selected = False

        box = self._find_box_by_coordinates(coordinates)
        self.selected_box = box
        box.is_selected = True


    def deselect_current_box(self):
        if self.selected_box:
            self.selected_box.is_selected = False
            self.selected_box = False


    def _find_box_by_coordinates(self, coordinates):
        row, column = coordinates
        for box in self.boxes:
            if box.row == row and box.column == column:
                return box
        return False


    def _update_model_from_list_of_boxes(self):
        for box in self.boxes:
            self.board.model[box.row][box.column] = box.number


    def _update_model_from_list_of_values(self, list_of_board_values):
        self.board.model = list_of_board_values
