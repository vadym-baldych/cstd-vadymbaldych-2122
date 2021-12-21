import connection
import unittest

class ConnectionTest(unittest.TestCase):
    def test_xml_to_dict(self):
        test_xml = "<server><status>GAME_MODE</status></server>"
        test_dict = {"status": "GAME_MODE"}
        self.assertEqual(dict(connection.xml_to_dict(test_xml)), test_dict)

        test_xml = "<server><status>GAME_UPDATE</status><sessionID>0</sessionID><currentPlayer>1</currentPlayer><gameField><cell00>2</cell00><cell01>2</cell01><cell02>2</cell02><cell10>2</cell10><cell11>2</cell11><cell12>2</cell12><cell20>2</cell20><cell21>2</cell21><cell22>2</cell22></gameField></server>"
        test_dict = {"status": "GAME_UPDATE", "sessionID": "0", "currentPlayer": "1", "gameField": {"cell00": "2", "cell01": "2", "cell02": "2", "cell10": "2", "cell11": "2", "cell12": "2", "cell20": "2", "cell21": "2", "cell22": "2"}}
        self.assertEqual(dict(connection.xml_to_dict(test_xml)), test_dict)

unittest.main()