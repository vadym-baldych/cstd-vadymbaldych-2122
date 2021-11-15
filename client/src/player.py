import pygame

class Player:
    def generate_move_command(self, game):
        move_position = str(self.grid_x) + str(self.grid_y)
        move_command_xml = f"<client><status>MOVE</status><player>{game.current_player}</player><move>{move_position}</move></client>"
        return move_command_xml

    def update(self, game):
        self.mouse_position = pygame.mouse.get_pos()
        self.get_grid_position(game)

    def get_grid_position(self, game):
        self.grid_x = int(self.mouse_position[1] / game.DEFAULT_STEP)
        self.grid_y = int(self.mouse_position[0] / game.DEFAULT_STEP)
        if (self.grid_x > 2 or self.grid_y > 2):
            self.grid_x = -1
            self.grid_y = -1