import unittest
from code.box import Box


class TestBoxMethods(unittest.TestCase):
    def test_initialize_pencil_number_boxes(self):
        box = Box((0, 0), (0, 0), 0)
        box.pencil_number_boxes = []
        box._initialize_pencil_number_boxes()
        self.assertEqual(len(box.pencil_number_boxes), 9)

    def test_remove_pencil_number(self):
        pass


if __name__ == '__main__':
    unittest.main()
