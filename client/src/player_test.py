import player
import game
import unittest

class PlayerTest(unittest.TestCase):
    player_test = player.Player()
    game_test = game.Game()

    def test_generate_move_command(self):
        self.game_test.current_player = 1
        self.player_test.grid_x = 1
        self.player_test.grid_y = 2

        self.assertEqual(self.player_test.generate_move_command(self.game_test),
            "<client><status>MOVE</status><player>1</player><move>12</move></client>")

    def test_get_grid_position(self):
        self.player_test.mouse_position = (-1, -1)
        self.player_test.get_grid_position(self.game_test)
        self.assertEqual(self.player_test.grid_x, int(0))
        self.assertEqual(self.player_test.grid_y, int(0))

        self.player_test.mouse_position = (479, 479)
        self.player_test.get_grid_position(self.game_test)
        self.assertEqual(self.player_test.grid_x, int(2))
        self.assertEqual(self.player_test.grid_y, int(2))

        self.player_test.mouse_position = (480, 480)
        self.player_test.get_grid_position(self.game_test)
        self.assertEqual(self.player_test.grid_x, int(-1))
        self.assertEqual(self.player_test.grid_y, int(-1))

        self.player_test.mouse_position = (479, 480)
        self.player_test.get_grid_position(self.game_test)
        self.assertEqual(self.player_test.grid_x, int(-1))
        self.assertEqual(self.player_test.grid_y, int(-1))

        self.player_test.mouse_position = (480, 479)
        self.player_test.get_grid_position(self.game_test)
        self.assertEqual(self.player_test.grid_x, int(-1))
        self.assertEqual(self.player_test.grid_y, int(-1))

    def test_update(self):
        self.assertEqual(self.player_test.update(self.game_test), None)

if __name__ == "__main__":
    unittest.main()