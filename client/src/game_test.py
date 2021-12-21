import game
import unittest

class GameTest(unittest.TestCase):
    game_test = game.Game()

    def test_parse_game_field(self):
        test_field_dict = {
                        "status": "GAME_UPDATE",
                        "sessionID": "0",
                        "currentPlayer": "1",
                        "gameField": {"cell00": "2",
                                      "cell01": "2",
                                      "cell02": "2", 
                                      "cell10": "2",
                                      "cell11": "2",
                                      "cell12": "2",
                                      "cell20": "2",
                                      "cell21": "2",
                                      "cell22": "2"}
                    }
        test_game_field = [[2, 2, 2], [2, 2, 2], [2, 2, 2]]
        self.game_test.parse_game_field(test_field_dict["gameField"])
        self.assertEqual(self.game_test.game_field, test_game_field)

        test_field_dict = {
                        "status": "GAME_UPDATE",
                        "sessionID": "0",
                        "currentPlayer": "1",
                        "gameField": {"cell00": "2",
                                      "cell01": "1",
                                      "cell02": "2", 
                                      "cell10": "0",
                                      "cell11": "2",
                                      "cell12": "1",
                                      "cell20": "2",
                                      "cell21": "2",
                                      "cell22": "1"}
                    }
        test_game_field = [[2, 1, 2], [0, 2, 1], [2, 2, 1]]
        self.game_test.parse_game_field(test_field_dict["gameField"])
        self.assertEqual(self.game_test.game_field, test_game_field)

    def test_genenerate_mode_command(self):
        self.game_test.game_mode = 1
        self.assertEqual(self.game_test.genenerate_mode_command(), "<client><status>MODE</status><mode>1</mode></client>")

    def test_gen_restart_xml(self):
         self.assertEqual(self.game_test.gen_restart_xml(), "<client><status>RESTART</status></client>")

    def test_update(self):
        self.assertEqual(self.game_test.update(), None)

    def test_draw_menu(self):
        self.assertEqual(self.game_test.draw_menu(), None)

    def test_draw_game_grid(self):
        self.assertEqual(self.game_test.draw_game_grid(), None)

    def test_draw_game_field(self):
        self.game_test.game_field = [[2, 2, 2], [2, 2, 2], [2, 2, 2]]
        self.assertEqual(self.game_test.draw_game_field(), None)

    def test_draw_game_winner(self):
        self.game_test.game_winner = "X"
        self.assertEqual(self.game_test.draw_game_winner(), None)

        self.game_test.game_winner = "O"
        self.assertEqual(self.game_test.draw_game_winner(), None)

        self.game_test.game_winner = "DRAW"
        self.assertEqual(self.game_test.draw_game_winner(), None)
        
        
if __name__ == "__main__":
    unittest.main()