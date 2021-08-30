from random import shuffle
from random import choice
from copy import deepcopy
from collections import Counter

class Board:
    """Manages the board state at the base level, including creation
    of new puzzles."""
    def __init__(self, board=([0, 0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0, 0])):
        self._size = 9
        self.model = list(board)


    def solve(self):
        """
        Solves the board using backtracking algorithm.
        :return: True if the solution is found, False otherwise
        :rtype: bool
        """
        if self.is_solved():
            return True
        else:
            empty_box_coordinates = self._find_empty()
            row, column = empty_box_coordinates
            for i in range(1, 10):
                if self.is_valid_number(i, empty_box_coordinates):
                    self.model[row][column] = i

                    if self.solve():
                        return True

                self.model[row][column] = 0
        return False


    def is_solved(self):
        """
        Checks whether the board is solved or not.
        :return: True if solved, False otherwise
        :rtype: bool
        """
        if not self._find_empty():
            return True
        else:
            return False


    def is_solvable(self):
        """
        Checks whether the board has a valid solution.
        :return: True if the board is solvable, False otherwise
        :rtype: bool
        """
        self_copy = deepcopy(self)
        return self_copy.solve()


    def _find_empty(self):
        for row in range(self._size):
            for column in range(self._size):
                if not self.model[row][column]:
                    return row, column
        return False


    def is_valid_number(self, number, coordinates):
        """
        Checks whether a number is valid in a given box according to
        Sudoku rules.
        :param number: number to check
        :type number: int
        :param coordinates: position of the box
        :type coordinates: tuple
        :return: True if number is valid, False otherwise
        :rtype: bool
        """
        if self._is_valid_number_in_row(number, coordinates) and \
           self._is_valid_number_in_column(number, coordinates) and \
           self._is_valid_number_in_small_board(number, coordinates):
            return True
        return False


    def _is_valid_number_in_row(self, number, coordinates):
        row, column = coordinates
        for i in range(self._size):
            if self.model[row][i] == number and i != column:
                return False
        return True


    def _is_valid_number_in_column(self, number, coordinates):
        row, column = coordinates
        for i in range(self._size):
            if self.model[i][column] == number and i != row:
                return False
        return True


    def _is_valid_number_in_small_board(self, number, coordinates):
        row, column = coordinates
        small_board_position = self._find_small_board_by_coordinates(coordinates)
        for i in small_board_position[0]:
            for j in small_board_position[1]:
                if self.model[i][j] == number and (i, j) != (row, column):
                    return False
        return True


    @staticmethod
    def _find_small_board_by_coordinates(coordinates):
        # Returns sets of coordinates corresponding to a small box
        # where the argument box is found
        small_board_index_matrix = [[0, 1, 2],
                                    [3, 4, 5],
                                    [6, 7, 8]]
        small_board_position = []
        for coordinate in coordinates:
            for i in small_board_index_matrix:
                if coordinate in i:
                    small_board_position.append(i)
        return small_board_position


    def _solve_empty_board_with_random_values(self):
        # Solves the board. Intended to be used on an empty board
        # as part of a new puzzle creation process
        numbers = list(range(1, 10))
        shuffle(numbers)
        if self.is_solved():
            return True
        else:
            for i in numbers:
                row, column = self._find_empty()
                if self.is_valid_number(i, (row, column)):
                    self.model[row][column] = i

                    if self._solve_empty_board_with_random_values():
                        return True

                    self.model[row][column] = 0
        return False


    def _reset_board(self):
        self.model = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0]]


    def generate_new_board(self, difficulty=1):
        """
        Generates new puzzle for player to solve.
        :param difficulty: difficulty of the puzzle, either 0, 1 or 2
        :type difficulty: int
        :return: None
        :rtype: None
        """
        self._reset_board()
        self._solve_empty_board_with_random_values()
        self._remove_numbers_to_get_puzzle(difficulty)


    def _remove_numbers_to_get_puzzle(self, difficulty):
        # Removes random symmetrical boxes from the board
        # until the difficulty rating is achieved.
        # Checks the validity of the new board at each iteration.
        nr_of_boxes_to_remove = self._set_difficulty(difficulty)
        while self._total_number_of_empty_boxes() < nr_of_boxes_to_remove:
            boxes_to_remove = self._find_symmetrical_boxes()
            for box in boxes_to_remove:
                row, column = box
                value = self.model[row][column]
                self.model[row][column] = 0
                if self._find_number_of_solutions() != 1:
                    self.model[row][column] = value
                    break


    @staticmethod
    def _set_difficulty(difficulty):
        if difficulty == 0:
            return 34
        elif difficulty == 1:
            return 40
        elif difficulty == 2:
            return 46


    def _top_right_triangle_indices(self):
        i = 0
        triangle_indices = []
        for row in range(self._size):
            for column in range(i, self._size):
                triangle_indices.append((row, column))
            i += 1
        return triangle_indices


    def _find_symmetrical_boxes(self):
        boxes = []
        for i in range(1):
            row, column = choice(self._top_right_triangle_indices())
            box = (row, column)
            opposite_box = (column, row)
            boxes.append(box)
            boxes.append(opposite_box)
        return boxes


    def _total_number_of_empty_boxes(self):
        board_values_frequency_counter = Counter(self._flatten_model())
        total_empty_boxes = board_values_frequency_counter[0]
        return total_empty_boxes


    def _solve_for_number_of_solutions(self, starting_box_coordinates=None):
        # Solves the board. Intended to be used
        # as part of a new puzzle creation process
        if self.is_solved():
            return True
        else:
            if starting_box_coordinates is not None:
                empty_box_coordinates = starting_box_coordinates
            else:
                empty_box_coordinates = self._find_empty()
            row, column = empty_box_coordinates
            for i in range(1, 10):
                if self.is_valid_number(i, empty_box_coordinates):
                    self.model[row][column] = i

                    if self._solve_for_number_of_solutions():
                        return self.model

                    self.model[row][column] = 0
        return False


    def _find_empty_by_distance_from_top_left(self, distance):
        x = 0
        for row in range(self._size):
            for column in range(self._size):
                if self.model[row][column] == 0:
                    if x == distance:
                        return row, column
                    x += 1


    def _find_number_of_solutions(self):
        solutions = []
        total_empty_boxes = self._total_number_of_empty_boxes()
        for i in range(total_empty_boxes):
            board_copy = deepcopy(self)
            row, column = board_copy._find_empty_by_distance_from_top_left(i)
            solution = board_copy._solve_for_number_of_solutions((row, column))
            solutions.append(solution)
        number_of_solutions = self._count_unique_solutions(solutions)
        if number_of_solutions[0]:
            return len(number_of_solutions)
        else:
            return 0


    @staticmethod
    def _count_unique_solutions(solutions):
        unique_solutions = []
        for solution in solutions:
            if solution not in unique_solutions:
                unique_solutions.append(solution)
        return unique_solutions


    def _flatten_model(self):
        flattened_model = []
        for row in range(self._size):
            for column in range(self._size):
                flattened_model.append(self.model[row][column])
        return flattened_model
