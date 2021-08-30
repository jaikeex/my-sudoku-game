import unittest
from code.board import Board
from code.grid import Grid


class TestGridMethods(unittest.TestCase):
    def setUp(self) -> None:
        self.board_values_list = [[7, 8, 0, 4, 0, 0, 1, 2, 0],
                                  [6, 0, 0, 0, 7, 5, 0, 0, 9],
                                  [0, 0, 0, 6, 0, 1, 0, 7, 8],
                                  [0, 0, 7, 0, 4, 0, 2, 6, 0],
                                  [0, 0, 1, 0, 5, 0, 9, 3, 0],
                                  [9, 0, 4, 0, 6, 0, 0, 0, 5],
                                  [0, 7, 0, 3, 0, 0, 0, 1, 2],
                                  [1, 2, 0, 0, 0, 7, 4, 0, 0],
                                  [0, 4, 9, 2, 0, 6, 0, 0, 7]]
        self.board_values_list_solved = [[7, 8, 5, 4, 3, 9, 1, 2, 6],
                                         [6, 1, 2, 8, 7, 5, 3, 4, 9],
                                         [4, 9, 3, 6, 2, 1, 5, 7, 8],
                                         [8, 5, 7, 9, 4, 3, 2, 6, 1],
                                         [2, 6, 1, 7, 5, 8, 9, 3, 4],
                                         [9, 3, 4, 1, 6, 2, 7, 8, 5],
                                         [5, 7, 8, 3, 9, 4, 6, 1, 2],
                                         [1, 2, 6, 5, 8, 7, 4, 9, 3],
                                         [3, 4, 9, 2, 1, 6, 8, 5, 7]]

        self.board = Board(self.board_values_list)
        self.grid = Grid(self.board, (1, 1))

    def test_place_permanent_number(self):
        box = self.grid._find_box_by_coordinates((2, 4))
        box.pencil_numbers.append(2)
        self.assertTrue(self.grid.place_permanent_number((2, 4)))
        box.pencil_numbers.append(3)
        self.assertFalse(self.grid.place_permanent_number((2, 4)))

    def test_update_box_numbers(self):
        self.grid._update_model_from_list_of_values(self.board_values_list_solved)
        self.grid.update_box_numbers()
        self.assertEqual(self.grid._find_box_by_coordinates((5, 8)).number, 5)

    def test_select_box_by_coordinates(self):
        self.grid.select_box_by_coordinates((5, 8))
        self.assertTrue(self.grid._find_box_by_coordinates((5, 8)).is_selected)
        self.assertFalse(self.grid._find_box_by_coordinates((2, 4)).is_selected)

    def test_remove_useless_pencil_number(self):
        box_1 = self.grid.boxes[2]
        box_2 = self.grid.boxes[7]
        box_1.pencil_numbers.append(2)
        self.grid.remove_useless_pencil_number(box_2)
        self.assertEqual(box_1.pencil_numbers, [])

if __name__ == '__main__':
    unittest.main()

