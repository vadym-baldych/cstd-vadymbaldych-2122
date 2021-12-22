import pygame
import os

class Game:
    WINDOW_NAME = "Tic-Tac-Toe"
    WINDOW_BACKGROUND_COLOR = "WHITE"

    DEFAULT_STEP = 160
    WIDTH = DEFAULT_STEP * 3
    HEIGHT = DEFAULT_STEP * 4

    GAME_COLOR_BLACK = "BLACK"
    GAME_COLOR_RED = "RED"

    GAME_FONT_NAME = "Comic Sans MS"
    GAME_FONT_SIZE = 40

    X_SIZE = 3
    Y_SIZE = 3
    GRID_WIDTH = 4

    SYMBOL_E = 0
    SYMBOL_X = 1
    SYMBOL_O = 2

    SYMBOL_X_FILEPATH = "assets/asset_X.png"
    SYMBOL_O_FILEPATH= "assets/asset_O.png"

    STATISTICS_FILE = "statistics.txt"

    TIMEOUT_TIME = 1
    
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.game_font = pygame.font.SysFont(self.GAME_FONT_NAME, self.GAME_FONT_SIZE)
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))

        pygame.display.set_caption(self.WINDOW_NAME)

        self.image_x = pygame.image.load(self.SYMBOL_X_FILEPATH)
        self.image_o = pygame.image.load(self.SYMBOL_O_FILEPATH)

        self.game_mode = 0
        self.game_status = True
        self.current_player = None
        self.game_winner = None
        self.is_statistic_writed = False

        self.server_message_xml = ""
        self.server_message_dict = None
        self.last_send_message_time = 0

    def update(self):
        self.screen.fill(self.WINDOW_BACKGROUND_COLOR)

    def draw_menu(self):
        man_vs_man_text = self.game_font.render("Man VS Man", False, self.GAME_COLOR_BLACK)
        man_vs_ai_text = self.game_font.render("Man VS AI", False, self.GAME_COLOR_BLACK)

        self.man_vs_man_rect = self.screen.blit(man_vs_man_text, (self.DEFAULT_STEP*0.85, self.DEFAULT_STEP / 2))
        self.man_vs_ai_rect = self.screen.blit(man_vs_ai_text, (self.DEFAULT_STEP*0.85, self.DEFAULT_STEP + self.DEFAULT_STEP / 2))

    def create_statistics(self):
        if not os.path.exists(self.STATISTICS_FILE):
            with open(self.STATISTICS_FILE, "w") as f:
                f.write("X:0\n")
                f.write("O:0")

    def draw_statistics(self):
        self.create_statistics()
        with open(self.STATISTICS_FILE, "r") as f:
            file_lines = f.readlines()
            x_st, o_st = file_lines[0].strip(), file_lines[1].strip()
        statistics_text = self.game_font.render(x_st + "                " + o_st, False, self.GAME_COLOR_BLACK)
        self.statistics_rect = self.screen.blit(statistics_text, (self.DEFAULT_STEP*0.5, self.DEFAULT_STEP*3))

        self.is_statistic_writed = False

    def write_statistics(self):
        self.create_statistics()
        if self.is_statistic_writed == False:
            with open(self.STATISTICS_FILE, "r") as f:
                file_lines = f.readlines()
                x_st, o_st = file_lines[0].strip(), file_lines[1].strip()
                x_num, o_num = int(x_st.split(":")[1]), int(o_st.split(":")[1])

            with open(self.STATISTICS_FILE, "w") as f:
                if self.game_winner == "X":
                    x_num = x_num + 1
                elif self.game_winner == "O":
                    o_num = o_num + 1
                f.write(f"X:{x_num}\n")
                f.write(f"O:{o_num}")

            self.is_statistic_writed = True

    def parse_game_field(self, field_dict):
        self.game_field = []
        for x in range(0, self.X_SIZE):
            self.game_field.append([int(field_dict["cell" + str(x) + str(y)]) for y in range(0, self.Y_SIZE)])

    def draw_game_grid(self):
        pygame.draw.rect(self.screen, self.GAME_COLOR_BLACK, (0, 0, 3*self.DEFAULT_STEP, 3*self.DEFAULT_STEP), self.GRID_WIDTH)
        pygame.draw.line(self.screen, self.GAME_COLOR_BLACK, (self.DEFAULT_STEP, 0), (self.DEFAULT_STEP, 3*self.DEFAULT_STEP), self.GRID_WIDTH)
        pygame.draw.line(self.screen, self.GAME_COLOR_BLACK, (2*self.DEFAULT_STEP, 0), (2*self.DEFAULT_STEP, 3*self.DEFAULT_STEP), self.GRID_WIDTH)
        pygame.draw.line(self.screen, self.GAME_COLOR_BLACK, (0, self.DEFAULT_STEP), (3*self.DEFAULT_STEP, self.DEFAULT_STEP), self.GRID_WIDTH)
        pygame.draw.line(self.screen, self.GAME_COLOR_BLACK, (0, 2*self.DEFAULT_STEP), (3*self.DEFAULT_STEP, 2*self.DEFAULT_STEP), self.GRID_WIDTH)

    def draw_game_field(self):
        self.draw_game_grid()
        for x in range(0, self.X_SIZE):
            for y in range(0, self.Y_SIZE):
                if self.game_field[x][y] == self.SYMBOL_X:
                    self.screen.blit(self.image_x, (y*self.DEFAULT_STEP, x*self.DEFAULT_STEP))
                elif self.game_field[x][y] == self.SYMBOL_O:
                    self.screen.blit(self.image_o, (y*self.DEFAULT_STEP, x*self.DEFAULT_STEP))

        current_player_symbol = "X" if self.current_player == self.SYMBOL_X else "O"

        current_player_text = self.game_font.render(f"Turn: {current_player_symbol}", False, self.GAME_COLOR_BLACK)
        self.current_player_rect = self.screen.blit(current_player_text, (self.DEFAULT_STEP, 3 * self.DEFAULT_STEP))
    
    def draw_game_winner(self):
        if self.game_winner == "X":
            game_ended_status = "X WON"
        elif self.game_winner == "O":
            game_ended_status = "O WON"
        elif self.game_winner == "DRAW":
            game_ended_status = "DRAW"

        game_status_text = self.game_font.render(game_ended_status, False, self.GAME_COLOR_BLACK)
        self.game_status_rect = self.screen.blit(game_status_text, (self.DEFAULT_STEP, 3 * self.DEFAULT_STEP + self.DEFAULT_STEP / 3))

        restart_text = self.game_font.render("RESTART", False, self.GAME_COLOR_RED)
        self.restart_rect = self.screen.blit(restart_text, (self.DEFAULT_STEP, 3 * self.DEFAULT_STEP + self.DEFAULT_STEP / 1.5))

    def genenerate_mode_command(self):
        mode_command_xml = f"<client><status>MODE</status><mode>{self.game_mode}</mode></client>"
        return mode_command_xml

    def gen_restart_xml(self):
        return "<client><status>RESTART</status></client>"