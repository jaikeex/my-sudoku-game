import pygame
import time
from code.grid import Grid
from code.board import Board
from code.new_game_button import NewGameButton
from code.show_solution_button import ShowSolutionButton
from code.help_button import HelpButton

BOARD_SIZE = (540, 540)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 200, 0)


class GameWindow:
    """
    Manages the main interface of the game.
    """
    def __init__(self):
        self.board_size = BOARD_SIZE
        self.start_time = time.time()

        self.window = pygame.display.set_mode(size=(540, 660))
        pygame.display.set_caption("Sudoku game...")
        pygame.font.init()

        self.board = Board()
        self.board.generate_new_board(difficulty=0)
        self.grid = Grid(self.board, BOARD_SIZE)
        self.new_game_button = NewGameButton((10, 620), (180, 70), self.board)
        self.solve_button = ShowSolutionButton((380, 620), (180, 70))
        self.help_button = HelpButton((215, 620), (180, 70))

        self.window_elements_to_draw = [self.grid,
                                        self.new_game_button,
                                        self.solve_button,
                                        self.help_button]

        self.mistakes = 0
        self.key = None
        self.board_solved = False
        self.time_taken_to_solve = None
        self.running = False


    def run(self):
        """
        Starts the game.
        :return: None
        :rtype: None
        """
        self.running = True
        while self.running:
            for event in pygame.event.get():
                self._parse_event(event)

            if self.grid.selected_box is not None and self.key is not None:
                self._place_pencil_number_on_grid()

            self.key = None
            self._draw_window()
            pygame.display.update()


    def _parse_event(self, event):
        # Main crossroad for registered pygame events.
        if event.type == pygame.QUIT:
            self.running = False
        if event.type == pygame.KEYDOWN:
            self._key_pressed(event.key)
        if event.type == pygame.MOUSEBUTTONDOWN:
            self._mouse_clicked()


    def _key_pressed(self, key):
        # Controls the flow based on what key was pressed.
        if key == pygame.K_1 or key == pygame.K_KP_1:
            self.key = 1
        if key == pygame.K_2 or key == pygame.K_KP_2:
            self.key = 2
        if key == pygame.K_3 or key == pygame.K_KP_3:
            self.key = 3
        if key == pygame.K_4 or key == pygame.K_KP_4:
            self.key = 4
        if key == pygame.K_5 or key == pygame.K_KP_5:
            self.key = 5
        if key == pygame.K_6 or key == pygame.K_KP_6:
            self.key = 6
        if key == pygame.K_7 or key == pygame.K_KP_7:
            self.key = 7
        if key == pygame.K_8 or key == pygame.K_KP_8:
            self.key = 8
        if key == pygame.K_9 or key == pygame.K_KP_9:
            self.key = 9


        if key == pygame.K_RETURN or key == pygame.K_KP_ENTER:
            self._place_permanent_number_on_grid()

        if key == pygame.K_DELETE or key == pygame.K_BACKSPACE:
            box = self.grid.selected_box
            box.pencil_numbers.clear()


    def _mouse_clicked(self):
        mouse_position = pygame.mouse.get_pos()
        if self.new_game_button.difficulty_window.displayed:
            self.new_game_button.difficulty_window.difficulty_clicked(
                mouse_position, self)
        if self.new_game_button.button_area.collidepoint(mouse_position):
            self.new_game_button.clicked(self)
        if self.help_button.help_window.displayed:
            self.help_button.help_window.clicked_outside_help_window(
                mouse_position, self)
        if self.help_button.button_area.collidepoint(mouse_position):
            self.help_button.clicked(self)
        if self.solve_button.button_area.collidepoint(mouse_position):
            self.solve_button.clicked(self)
            self._game_won()
        self._select_box_on_mouse(mouse_position)


    def _place_pencil_number_on_grid(self):
        box = self.grid.selected_box
        if self.key not in box.pencil_numbers:
            box.pencil_numbers.append(self.key)
        else:
            box.pencil_numbers.remove(self.key)


    def _place_permanent_number_on_grid(self):
        box = self.grid.selected_box
        if len(box.pencil_numbers) == 1 and not \
                self.grid.place_permanent_number((box.row, box.column)):
            self.mistakes += 1

        if self.board.is_solved():
            self._game_won()


    def _game_won(self):
        self.board_solved = True
        self.time_taken_to_solve = int(time.time() - self.start_time)


    def _draw_window(self):
        self.window.fill(WHITE)
        self._draw_time()
        self._draw_mistakes()
        self._draw_buttons_and_popups()


    def _draw_buttons_and_popups(self):
        for element in self.window_elements_to_draw:
            element.draw(self.window)


    def _draw_mistakes(self):
        font = pygame.font.SysFont("calibri", 30)
        mistakes_text = font.render("Mistakes: ", True, BLACK)
        self.window.blit(mistakes_text, (10, 560))

        if self.mistakes <= 10:
            mistakes_count = font.render("X " * self.mistakes, True, RED)
            self.window.blit(mistakes_count, (150, 560))

        elif 10 < self.mistakes <= 20:
            mistakes_count_upper = font.render("X " * 10, True, RED)
            mistakes_count_lower = font.render("X " * (self.mistakes - 10), True, RED)
            self.window.blit(mistakes_count_upper, (150, 560))
            self.window.blit(mistakes_count_lower, (150, 590))

        elif self.mistakes > 20:
            mistakes_count_upper = font.render("X " * 10, True, RED)
            mistakes_count_lower = font.render("X " * 10, True, RED)
            self.window.blit(mistakes_count_upper, (150, 560))
            self.window.blit(mistakes_count_lower, (150, 590))


    def _draw_time(self):
        font = pygame.font.SysFont("calibri", 30)
        if not self.board_solved:
            time_played = int(time.time() - self.start_time)
            time_text = font.render(
                "Time: " + self._format_time(time_played), True, BLACK)
            self.window.blit(time_text, (540-160, 560))
        else:
            time_text = font.render(
                "Time: " + self._format_time(self.time_taken_to_solve), True, GREEN)
            self.window.blit(time_text, (540-160, 560))


    def start_new_game(self, difficulty):
        """
        Creates new board and resets the interface.
        :param difficulty: 0 - easy; 1 - medium; 2 - hard
        :type difficulty: int
        :return: None
        :rtype: None
        """
        self.board.generate_new_board(difficulty)
        self.board_solved = False
        self.grid.setup()
        self.grid.update_box_numbers()
        self._reset_interface()


    def _reset_interface(self):
        self._reset_timer()
        self._reset_mistakes()


    def _reset_mistakes(self):
        self.mistakes = 0


    def _reset_timer(self):
        self.time_taken_to_solve = None
        self.start_time = time.time()


    @staticmethod
    def _format_time(secs):
        sec = secs % 60
        minute = secs // 60
        time_str = time.strptime(f"{minute}:{sec}", "%M:%S")
        return time.strftime("%M:%S", time_str)


    def _select_box_on_mouse(self, position):
        row, column = map(lambda x: x // 60, position)
        if row < 9 and column < 9:
            self.grid.select_box_by_coordinates((column, row))
