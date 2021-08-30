import pygame
from code.button import Button

BLACK = (0, 0, 0)
LIGHT_GRAY = (200, 200, 200)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
RED = (255, 0, 0)


class NewGameButton(Button):
    def __init__(self, position, size, board):
        self.button_text = "Start new game"
        super().__init__(position, size, self.button_text)
        self.board = board
        self.difficulty_window = NewGameWindow(self.board)


    def clicked(self, game_window):
        game_window.grid.deselect_current_box()
        sprites = pygame.sprite.Group(self.difficulty_window)
        game_window.window_elements_to_draw.append(sprites)
        self.difficulty_window.displayed = True
        pygame.display.update()


class NewGameWindow(pygame.sprite.Sprite):
    def __init__(self, board):
        super().__init__()
        self.displayed = False
        self.board = board
        self.image = pygame.Surface((200, 250))
        self.image.fill(LIGHT_GRAY)
        self.position = (270, 300)

        self.rect = self.image.get_rect(center=self.position)
        self.select_easy_rect = pygame.Rect(30, 50, 70, 35)
        self.select_medium_rect = pygame.Rect(30, 85, 70, 35)
        self.select_hard_rect = pygame.Rect(30, 120, 70, 35)
        self.working_rect_upper = pygame.Rect(10, 180, 150, 35)
        self.working_rect_lower = pygame.Rect(10, 200, 150, 35)
        self.draw()


    def draw(self):
        font = pygame.font.SysFont("comicsansms", 18)
        text_select_difficulty = font.render("Select Difficulty:",
                                             True, BLACK)
        self.image.blit(text_select_difficulty, (10, 10))

        text_select_easy = font.render("Easy", True, BLACK)
        self.image.blit(text_select_easy, self.select_easy_rect)
        text_select_easy = font.render("Medium", True, BLACK)
        self.image.blit(text_select_easy, self.select_medium_rect)
        text_select_easy = font.render("Hard", True, BLACK)
        self.image.blit(text_select_easy, self.select_hard_rect)

        self.display_time_warning()


    def difficulty_clicked(self, position, window):
        position_inside_difficulty_window = \
            (position[0] - 150, position[1] - 175)
        if self.select_easy_rect.collidepoint(position_inside_difficulty_window):
            window.start_new_game(difficulty=0)
            self.clear_difficulty_window(window)
        if self.select_medium_rect.collidepoint(position_inside_difficulty_window):
            window.start_new_game(difficulty=1)
            self.clear_difficulty_window(window)
        if self.select_hard_rect.collidepoint(position_inside_difficulty_window):
            window.start_new_game(difficulty=2)
            self.clear_difficulty_window(window)
        if not 170 < position[0] < 370 or not 200 < position[1] < 400:
            self.clear_difficulty_window(window)


    def clear_difficulty_window(self, window):
        if self.displayed:
            window.window_elements_to_draw.pop()
            self.displayed = False


    def display_time_warning(self):
        font = pygame.font.SysFont("comicsansms", 15)
        working_text_part_one = font.render(
            "Creating medium and hard", True, BLACK)
        working_text_part_two = font.render(
            "puzzles may take a while", True, BLACK)
        self.image.blit(working_text_part_one, self.working_rect_upper)
        self.image.blit(working_text_part_two, self.working_rect_lower)
        pygame.display.update()
