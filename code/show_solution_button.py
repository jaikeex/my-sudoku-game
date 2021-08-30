from code.button import Button

BLACK = (0, 0, 0)

class ShowSolutionButton(Button):
    def __init__(self, position, size):
        self.button_text = "Show solution"
        super().__init__(position, size, self.button_text)


    @staticmethod
    def clicked(game_window):
        game_window.board.solve()
        game_window.grid.update_box_numbers()
