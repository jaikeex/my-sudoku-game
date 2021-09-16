import unittest

from code.board import Board


class TestBoardMethods(unittest.TestCase):
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
        self.board_values_list_unsolvable = [[5, 1, 6, 8, 4, 9, 7, 3, 2],
                                             [3, 0, 7, 6, 0, 5, 0, 0, 0],
                                             [8, 0, 9, 7, 0, 0, 0, 6, 5],
                                             [1, 3, 5, 0, 6, 0, 9, 0, 7],
                                             [4, 7, 2, 5, 9, 1, 0, 0, 6],
                                             [9, 6, 8, 3, 7, 0, 0, 5, 0],
                                             [2, 5, 6, 1, 8, 6, 0, 7, 4],
                                             [6, 8, 4, 2, 0, 7, 5, 0, 0],
                                             [7, 9, 1, 0, 5, 0, 6, 0, 8]]
        self.board_empty_list = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0, 0]]
        self.triangle_indices = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4),
                                 (0, 5), (0, 6), (0, 7), (0, 8), (1, 1),
                                 (1, 2), (1, 3), (1, 4), (1, 5), (1, 6),
                                 (1, 7), (1, 8), (2, 2), (2, 3), (2, 4),
                                 (2, 5), (2, 6), (2, 7), (2, 8), (3, 3),
                                 (3, 4), (3, 5), (3, 6), (3, 7), (3, 8),
                                 (4, 4), (4, 5), (4, 6), (4, 7), (4, 8),
                                 (5, 5), (5, 6), (5, 7), (5, 8), (6, 6),
                                 (6, 7), (6, 8), (7, 7), (7, 8), (8, 8)]

        self.board = Board(self.board_values_list)
        self.new_board = Board(self.board_empty_list)

    def test_find_empty(self):
        self.assertEqual((0, 2), self.board._find_empty())

    def test_is_valid(self):
        self.assertTrue(self.board.is_valid_number(2, (2, 4)))
        self.assertTrue(self.board.is_valid_number(6, (7, 2)))
        self.assertFalse(self.board.is_valid_number(4, (4, 3)))

    def test_find_small_board_by_coordinates(self):
        self.assertEqual([[6, 7, 8], [0, 1, 2]],
                         self.board._find_small_board_by_coordinates((6, 2)))

    def test_solve(self):
        board_to_solve = Board(self.board_values_list)
        board_to_solve.solve()
        self.assertEqual(board_to_solve.model, self.board_values_list_solved)

    def test_is_solved(self):
        board_to_solve = Board(self.board_values_list)
        self.assertFalse(board_to_solve.is_solved())
        board_to_solve.model = self.board_values_list_solved
        self.assertTrue(board_to_solve.is_solved())

    def test_solve_empty_board_with_random_values(self):
        new_board = Board(self.board_empty_list)
        new_board._solve_empty_board_with_random_values()
        self.assertTrue(new_board.is_solved())

    def test_find_symmetrical_boxes(self):
        boxes = self.board._find_symmetrical_boxes()
        first_box = boxes[0]
        second_box = boxes[1]
        self.assertEqual(first_box[0], second_box[1])
        self.assertEqual(first_box[1], second_box[0])

    def test_top_right_triangle_indices(self):
        self.assertEqual(self.board._top_right_triangle_indices(),
                         self.triangle_indices)

    def test_total_number_of_empty_boxes(self):
        self.assertEqual(self.board._total_number_of_empty_boxes(), 43)

    def test_find_number_of_solutions(self):
        self.assertEqual(self.board._find_number_of_solutions(), 1)
        board_unsolvable = Board(self.board_values_list_unsolvable)
        self.assertEqual(board_unsolvable._find_number_of_solutions(), 0)

    def test_find_empty_by_distance_from_top_left(self):
        self.assertEqual(self.board._find_empty_by_distance_from_top_left(4),
                         (1, 1))

    def test_reset_board(self):
        self.board._reset_board()
        self.assertEqual(self.board.model, self.board_empty_list)


if __name__ == '__main__':
    unittest.main()


















